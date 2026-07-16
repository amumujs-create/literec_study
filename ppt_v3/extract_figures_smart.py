#!/usr/bin/env python3
"""논문 PDF Figure 자동 추출 — caption 기반 + 시각 영역 bbox (PyMuPDF only).

scientific-figure-extractor 방식을 참고해, Figure N 캡션 위의 시각 영역을
자동으로 찾아 잘라냅니다. ML 모델 불필요.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"

DEFAULT_DPI = 250
DEFAULT_PADDING = 12
CROSS_COLUMN_TOL = 50
FULL_WIDTH_RATIO = 0.45
TEXT_LABEL_MARGIN = 60

CAPTION_RE = re.compile(
    r"^\s*(Figure|Fig\.?|Table|Extended\s+Data\s+Fig(?:ure|\.)?)\s*(\d+)",
    re.IGNORECASE,
)

# pdf_rel, wanted figure numbers, output name map {fig_num: filename}
PAPER_JOBS = [
    {
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Runje2023_Constrained_Monotonic_NN.pdf",
        "figs": {1: "runje_monotonic_fig1.png", 3: "runje_monotonic_unit_fig3.png", 4: "runje_monotonic_arch_fig4.png"},
    },
    {
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Martius2016_Extrapolation_Learning_Equations_EQL.pdf",
        "figs": {1: "eql_architecture_fig1.png"},
    },
    {
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Trask2018_Neural_Arithmetic_Logic_Units_NALU.pdf",
        "figs": {2: "nalu_architecture_fig2.png"},
    },
    {
        "pdf": "papers_to_add/02_OOD/Arjovsky2019_Invariant_Risk_Minimization.pdf",
        "figs": {3: "irm_scm_fig3.png"},
    },
    {
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Xu2021_How_Neural_Networks_Extrapolate.pdf",
        "figs": {2: "xu_gnn_arch_fig2.png"},
    },
]


@dataclass
class Caption:
    page: int
    number: int
    label: str
    bbox: tuple[float, float, float, float]
    text: str
    kind: str


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
            bx0, _, bx1, _ = b["bbox"]
            if (bx1 - bx0) < 20:
                continue
            raw = m.group(1).strip().lower()
            kind = "table" if "table" in raw else "figure"
            num = int(m.group(2))
            out.append(
                Caption(
                    page=pi + 1,
                    number=num,
                    label=f"Figure {num}",
                    bbox=tuple(b["bbox"]),
                    text=" ".join("".join(s["text"] for s in line["spans"]) for line in b["lines"])[:500],
                    kind=kind,
                )
            )
    return out


def get_column(bbox, page_width: float) -> str:
    x0, _, x1, _ = bbox
    mid = page_width / 2
    if x1 < mid + CROSS_COLUMN_TOL and x0 < mid:
        return "left"
    if x0 > mid - CROSS_COLUMN_TOL and x1 > mid:
        return "right"
    return "full"


def in_column(bbox, column: str, page_width: float) -> bool:
    x0, _, x1, _ = bbox
    mid = page_width / 2
    if column == "left":
        return x1 <= mid + CROSS_COLUMN_TOL
    if column == "right":
        return x0 >= mid - CROSS_COLUMN_TOL
    return True


def _combine(boxes, page: fitz.Page, padding: float) -> tuple[float, float, float, float]:
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    pw, ph = page.rect.width, page.rect.height
    return (
        max(0, x0 - padding),
        max(0, y0 - padding),
        min(pw, x1 + padding),
        min(ph, y1 + padding),
    )


def find_figure_region(page: fitz.Page, caption: Caption, prev_y: float, padding: float):
    pw = page.rect.width
    _, cy0, _, _ = caption.bbox
    column = get_column(caption.bbox, pw)

    visuals: list[tuple[float, float, float, float]] = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") == 1:
            visuals.append(tuple(b["bbox"]))
    for d in page.get_drawings():
        r = d.get("rect")
        if r and r.width > 2 and r.height > 2:
            visuals.append((r.x0, r.y0, r.x1, r.y1))

    all_candidates = []
    for bb in visuals:
        _, by0, _, by1 = bb
        if by0 > cy0 + 5:
            continue
        if by1 < prev_y - 5:
            continue
        all_candidates.append(bb)

    if not all_candidates:
        return None

    combined_x0 = min(b[0] for b in all_candidates)
    combined_x1 = max(b[2] for b in all_candidates)
    effective_column = "full" if (combined_x1 - combined_x0) > pw * FULL_WIDTH_RATIO else column

    candidates = [bb for bb in all_candidates if in_column(bb, effective_column, pw)] or all_candidates

    vx0 = min(b[0] for b in candidates)
    vy0 = min(b[1] for b in candidates)
    vx1 = max(b[2] for b in candidates)
    vy1 = max(b[3] for b in candidates)

    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        bb = tuple(b["bbox"])
        if bb == caption.bbox:
            continue
        bx0, by0, bx1, by1 = bb
        if by0 > cy0 + 5 or by1 < prev_y - 5:
            continue
        if (bx1 - bx0) > pw * 0.35:
            continue
        if (
            bx1 > vx0 - TEXT_LABEL_MARGIN
            and bx0 < vx1 + TEXT_LABEL_MARGIN
            and by1 > vy0 - TEXT_LABEL_MARGIN
            and by0 < vy1 + TEXT_LABEL_MARGIN
        ):
            candidates.append(bb)

    return _combine(candidates, page, padding)


def _fallback_region(page: fitz.Page, caption: Caption, prev_y: float, padding: float):
    pw, ph = page.rect.width, page.rect.height
    cy0 = caption.bbox[1]
    col = get_column(caption.bbox, pw)
    if col == "left":
        x0, x1 = 0.0, pw / 2
    elif col == "right":
        x0, x1 = pw / 2, pw
    else:
        x0, x1 = 0.0, pw
    clip = fitz.Rect(x0, max(0, prev_y), x1, cy0)
    if clip.height < 10:
        return None
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), clip=clip, alpha=False)
    samples = pix.samples
    n = pix.width * pix.height
    if n == 0:
        return None
    white = sum(1 for i in range(0, len(samples), 3) if samples[i] > 240 and samples[i + 1] > 240 and samples[i + 2] > 240)
    if white / n > 0.97:
        return None
    return (
        max(0, x0 - padding),
        max(0, clip.y0 - padding),
        min(pw, x1 + padding),
        min(ph, cy0 - 2),
    )


def prev_boundary_y(caption: Caption, page_caps: list[Caption]) -> float:
    prev_y = 0.0
    col = None
    for other in page_caps:
        if other.page != caption.page:
            continue
        if other is caption:
            col = get_column(caption.bbox, 0)  # placeholder
            break
    page_width = 0
    col = get_column(caption.bbox, 612)  # default; overwritten below
    for other in page_caps:
        if other.page != caption.page or other is caption:
            continue
        if get_column(other.bbox, 612) != get_column(caption.bbox, 612):
            continue
        if other.bbox[3] < caption.bbox[1] and other.bbox[3] > prev_y:
            prev_y = other.bbox[3]
    return prev_y


def extract_one(doc: fitz.Document, caption: Caption, page_caps: list[Caption], dpi: int, padding: float):
    page = doc[caption.page - 1]
    prev_y = 0.0
    col = get_column(caption.bbox, page.rect.width)
    for other in page_caps:
        if other.page != caption.page or other is caption:
            continue
        if get_column(other.bbox, page.rect.width) != col:
            continue
        if other.bbox[3] < caption.bbox[1] and other.bbox[3] > prev_y:
            prev_y = other.bbox[3]

    region = find_figure_region(page, caption, prev_y, padding)
    render_page = page

    if region is None and caption.page < len(doc):
        next_page = doc[caption.page]
        next_caps = [c for c in page_caps if c.page == caption.page + 1]
        boundary_y = min(c.bbox[1] for c in next_caps) if next_caps else next_page.rect.height
        syn = Caption(caption.page + 1, caption.number, caption.label, (0, boundary_y, next_page.rect.width, boundary_y), caption.text, caption.kind)
        region = find_figure_region(next_page, syn, 0, padding)
        if region is not None:
            render_page = next_page

    if region is None:
        region = _fallback_region(page, caption, prev_y, padding)

    if region is None:
        return None

    # 페이지 헤더·캡션 본문 제외
    _, cy0, _, _ = caption.bbox
    x0, y0, x1, y1 = region
    region = (x0, max(y0, 62), x1, min(y1, cy0 - 4))
    if region[3] - region[1] < 20:
        return None

    clip = fitz.Rect(*region)
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = render_page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    return pix, region


def run_jobs(dpi: int = DEFAULT_DPI, padding: float = DEFAULT_PADDING, jobs=None):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    meta = []
    jobs = jobs or PAPER_JOBS

    for job in jobs:
        pdf = ROOT / job["pdf"]
        if not pdf.exists():
            print(f"SKIP missing {pdf}")
            continue
        doc = fitz.open(pdf)
        caps = find_captions(doc)
        by_page: dict[int, list[Caption]] = {}
        for c in caps:
            by_page.setdefault(c.page, []).append(c)

        for fig_num, out_name in job["figs"].items():
            cap = next((c for c in caps if c.kind == "figure" and c.number == fig_num), None)
            if cap is None:
                print(f"SKIP {out_name}: Figure {fig_num} caption not found in {pdf.name}")
                continue
            result = extract_one(doc, cap, caps, dpi, padding)
            if result is None:
                print(f"SKIP {out_name}: no visual region for Figure {fig_num}")
                continue
            pix, region = result
            out = FIG_DIR / out_name
            pix.save(str(out))
            meta.append({"pdf": str(job["pdf"]), "figure": fig_num, "output": out_name, "bbox": [round(v, 1) for v in region], "caption": cap.text[:120]})
            print(f"OK {out_name} Figure {fig_num} bbox=({region[0]:.0f},{region[1]:.0f},{region[2]:.0f},{region[3]:.0f})")
        doc.close()

    (FIG_DIR / "smart_extract.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(meta)} figures -> {FIG_DIR}")


def main():
    p = argparse.ArgumentParser(description="Caption-anchored figure extraction for paper PDFs")
    p.add_argument("--dpi", type=int, default=DEFAULT_DPI)
    p.add_argument("--padding", type=float, default=DEFAULT_PADDING)
    p.add_argument("--pdf", help="single PDF path (optional)")
    p.add_argument("--fig", type=int, action="append", dest="figs", help="figure number(s)")
    p.add_argument("--out-dir", default=str(FIG_DIR))
    args = p.parse_args()

    if args.pdf:
        pdf = Path(args.pdf)
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        doc = fitz.open(pdf)
        caps = find_captions(doc)
        wanted = set(args.figs) if args.figs else {c.number for c in caps if c.kind == "figure"}
        for cap in caps:
            if cap.kind != "figure" or cap.number not in wanted:
                continue
            result = extract_one(doc, cap, caps, args.dpi, args.padding)
            if not result:
                print(f"SKIP Figure {cap.number}")
                continue
            pix, region = result
            out = out_dir / f"p{cap.page:03d}_Figure_{cap.number}.png"
            pix.save(str(out))
            print(f"OK Figure {cap.number} -> {out.name} bbox={[round(v) for v in region]}")
        doc.close()
        return

    run_jobs(dpi=args.dpi, padding=args.padding)


if __name__ == "__main__":
    main()
