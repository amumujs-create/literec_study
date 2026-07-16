#!/usr/bin/env python3
"""PP-DocLayoutV2(Paddle) 레이아웃 인식으로 논문 Figure 추출.

회사망에서 HuggingFace/ModelScope가 막혀 figcrop(MinerU) 대신
Baidu CDN에서 받은 PP-DocLayoutV2를 사용합니다.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import fitz
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"
MODEL_DIR = Path(__file__).resolve().parent / "models" / "PP-DocLayoutV2_infer"
VENV_PYTHON = Path(__file__).resolve().parent / ".venv-figcrop" / "bin" / "python"

DETECT_DPI = 150
RENDER_DPI = 300
PAD_PT = 8
VISUAL_LABELS = {"image", "chart", "table", "figure"}

CAPTION_RE = re.compile(
    r"^\s*(Figure|Fig\.?)\s*(\d+)",
    re.IGNORECASE,
)

import sys

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from paper_catalog import layout_jobs

PAPER_JOBS = layout_jobs()


@dataclass
class Caption:
    page: int  # 0-indexed
    number: int
    bbox: tuple[float, float, float, float]
    text: str


def find_captions(doc: fitz.Document) -> list[Caption]:
    out: list[Caption] = []
    for pi, page in enumerate(doc):
        for b in page.get_text("dict")["blocks"]:
            if b.get("type") != 0 or not b.get("lines"):
                continue
            first = "".join(s["text"] for s in b["lines"][0]["spans"]).strip()
            m = CAPTION_RE.match(first)
            if not m:
                continue
            if (b["bbox"][2] - b["bbox"][0]) < 20:
                continue
            full = " ".join("".join(s["text"] for s in line["spans"]) for line in b["lines"])[:400]
            out.append(Caption(pi, int(m.group(2)), tuple(b["bbox"]), full))
    return out


def _load_model():
    from paddlex import create_model

    if not MODEL_DIR.exists():
        raise FileNotFoundError(
            f"PP-DocLayoutV2 not found at {MODEL_DIR}. "
            "Download with: curl -k -L -o models/PP-DocLayoutV2_infer.tar "
            "'https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-DocLayoutV2_infer.tar'"
        )
    return create_model(model_name="PP-DocLayoutV2", model_dir=str(MODEL_DIR))


def detect_boxes(model, page: fitz.Page) -> list[dict]:
    """Return boxes in PDF point coordinates: {label, score, x0,y0,x1,y1}."""
    scale = DETECT_DPI / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    tmp = Path("/tmp") / f"_layout_{id(page)}.png"
    pix.save(str(tmp))
    try:
        result = list(model.predict(str(tmp), batch_size=1))[0]
        boxes = result["boxes"]
    finally:
        tmp.unlink(missing_ok=True)

    out = []
    for b in boxes:
        x0, y0, x1, y1 = b["coordinate"]
        out.append(
            {
                "label": b["label"],
                "score": float(b["score"]),
                "x0": x0 / scale,
                "y0": y0 / scale,
                "x1": x1 / scale,
                "y1": y1 / scale,
            }
        )
    return out


def region_for_caption(boxes: list[dict], caption: Caption, page: fitz.Page) -> tuple[float, float, float, float] | None:
    """Union visual regions above caption, same page; prefer nearest figure_title match."""
    cy0 = caption.bbox[1]
    visuals = [
        b
        for b in boxes
        if b["label"] in VISUAL_LABELS and b["score"] >= 0.5 and b["y1"] <= cy0 + 5
    ]
    if not visuals:
        # fallback: any visual above caption with looser labels
        visuals = [
            b
            for b in boxes
            if b["label"] in VISUAL_LABELS | {"display_formula"} and b["y1"] <= cy0 + 5 and b["y0"] < cy0
        ]
        visuals = [b for b in visuals if b["label"] in VISUAL_LABELS]

    if not visuals:
        return None

    # If multiple figures on page, keep those whose bottom is closest above this caption
    # (and above previous content gap). Prefer boxes whose y1 is within 120pt of caption.
    near = [b for b in visuals if (cy0 - b["y1"]) < 120]
    if near:
        visuals = near

    # Group overlapping / nearby panels into one figure (multi-panel)
    # Take all visuals whose vertical band overlaps the tallest near-caption cluster
    visuals.sort(key=lambda b: b["y1"], reverse=True)
    # start from closest-to-caption visuals
    cluster = [visuals[0]]
    for b in visuals[1:]:
        # same horizontal band (multi-panel side by side) or stacked with small gap
        if abs(b["y1"] - cluster[0]["y1"]) < 40 or abs(b["y0"] - cluster[0]["y0"]) < 40:
            cluster.append(b)
        elif b["y1"] > cluster[0]["y0"] - 30:
            cluster.append(b)

    x0 = min(b["x0"] for b in cluster) - PAD_PT
    y0 = min(b["y0"] for b in cluster) - PAD_PT
    x1 = max(b["x1"] for b in cluster) + PAD_PT
    y1 = max(b["y1"] for b in cluster) + PAD_PT

    # include nearby (a)(b)(c) titles just below panels but above main caption
    for b in boxes:
        if b["label"] != "figure_title":
            continue
        if b["y0"] >= cy0 - 2:
            continue
        if b["y0"] < y1 - 5:
            continue
        # horizontally overlapping figure band
        if b["x1"] < x0 - 20 or b["x0"] > x1 + 20:
            continue
        y1 = max(y1, b["y1"] + 2)

    pw, ph = page.rect.width, page.rect.height
    return (
        max(0, x0),
        max(0, y0),
        min(pw, x1),
        min(ph, min(y1, cy0 - 2)),
    )


def render_region(page: fitz.Page, region, out_path: Path, dpi: int = RENDER_DPI):
    clip = fitz.Rect(*region)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    pix.save(str(out_path))


def run_jobs(jobs=None, dpi: int = RENDER_DPI):
    from paddlex import create_model

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    model = create_model(model_name="PP-DocLayoutV2", model_dir=str(MODEL_DIR))
    meta = []
    jobs = jobs or PAPER_JOBS
    page_cache: dict[tuple[str, int], list[dict]] = {}

    for job in jobs:
        pdf = ROOT / job["pdf"]
        if not pdf.exists():
            print(f"SKIP missing {pdf}")
            continue
        doc = fitz.open(pdf)
        caps = find_captions(doc)
        for fig_num, out_name in job["figs"].items():
            cap = next((c for c in caps if c.number == fig_num), None)
            if cap is None:
                print(f"SKIP {out_name}: Figure {fig_num} not found")
                continue
            key = (str(pdf), cap.page)
            if key not in page_cache:
                page_cache[key] = detect_boxes(model, doc[cap.page])
            boxes = page_cache[key]
            region = region_for_caption(boxes, cap, doc[cap.page])
            if region is None:
                print(f"SKIP {out_name}: no visual region for Figure {fig_num}")
                continue
            out = FIG_DIR / out_name
            render_region(doc[cap.page], region, out, dpi=dpi)
            meta.append(
                {
                    "pdf": job["pdf"],
                    "figure": fig_num,
                    "output": out_name,
                    "bbox": [round(v, 1) for v in region],
                    "engine": "PP-DocLayoutV2",
                }
            )
            print(f"OK {out_name} Fig.{fig_num} bbox=({region[0]:.0f},{region[1]:.0f},{region[2]:.0f},{region[3]:.0f})")
        doc.close()

    (FIG_DIR / "layout_extract.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(meta)} figures → {FIG_DIR} (PP-DocLayoutV2)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dpi", type=int, default=RENDER_DPI)
    args = p.parse_args()
    run_jobs(dpi=args.dpi)


if __name__ == "__main__":
    main()
