#!/usr/bin/env python3
"""논문 PDF에서 모델 구조(architecture) 다이어그램만 추출 — 캡션·본문 제외."""

from __future__ import annotations

from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# pdf_rel, page(1-indexed), caption_y, output_name, pad, extra_rects, min_y
# caption_y: "Figure N:" 캡션 시작 y — 이 위까지만 포함
# extra_rects: drawing/image로 잡히지 않는 텍스트(수식 등) bbox를 수동 보정
# min_y: 페이지 헤더 등 상단 잡음 제외
ARCH_JOBS = [
    (
        "extrapolation-papers/03_neural_network_extrapolation/Martius2016_Extrapolation_Learning_Equations_EQL.pdf",
        3,
        178,
        "eql_architecture_fig1.png",
        6,
        None,
        0,
    ),
    (
        "extrapolation-papers/03_neural_network_extrapolation/Trask2018_Neural_Arithmetic_Logic_Units_NALU.pdf",
        3,
        228,
        "nalu_architecture_fig2.png",
        4,
        (105, 74, 515, 202),
        0,
    ),
    (
        "extrapolation-papers/03_neural_network_extrapolation/Runje2023_Constrained_Monotonic_NN.pdf",
        5,
        256,
        "runje_monotonic_unit_fig3.png",
        6,
        (65, 78, 545, 252),
        75,
    ),
    (
        "extrapolation-papers/03_neural_network_extrapolation/Runje2023_Constrained_Monotonic_NN.pdf",
        6,
        206,
        "runje_monotonic_arch_fig4.png",
        6,
        None,
        55,
    ),
    (
        "papers_to_add/02_OOD/Arjovsky2019_Invariant_Risk_Minimization.pdf",
        15,
        284,
        "irm_scm_fig3.png",
        6,
        (125, 205, 475, 278),
        0,
    ),
    (
        "extrapolation-papers/03_neural_network_extrapolation/Xu2021_How_Neural_Networks_Extrapolate.pdf",
        2,
        322,
        "xu_gnn_arch_fig2.png",
        6,
        (108, 212, 505, 302),
        210,
    ),
]


def _union_rects(rects: list[fitz.Rect]) -> fitz.Rect | None:
    if not rects:
        return None
    x0 = min(r.x0 for r in rects)
    y0 = min(r.y0 for r in rects)
    x1 = max(r.x1 for r in rects)
    y1 = max(r.y1 for r in rects)
    return fitz.Rect(x0, y0, x1, y1)


def auto_clip(page: fitz.Page, caption_y: float, pad: float, extra=None, min_y: float = 0) -> tuple[float, float, float, float]:
    rects: list[fitz.Rect] = []

    for path in page.get_drawings():
        r = path["rect"]
        if r.y1 < caption_y - 2 and r.y1 > min_y:
            rects.append(r)

    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            if r.y1 < caption_y - 2 and r.y1 > min_y:
                rects.append(r)

    if extra and len(extra) == 4:
        # extra만으로 clip 고정 (auto union 대신)
        return tuple(extra)

    merged = _union_rects(rects)
    if merged is None:
        raise ValueError("no drawable content found above caption")

    return (
        merged.x0 - pad,
        max(merged.y0 - pad, min_y),
        merged.x1 + pad,
        min(merged.y1 + pad, caption_y - 4),
    )


def render_clip(pdf_path: Path, page_num: int, clip, out_path: Path, zoom: float = 3.5):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    mat = fitz.Matrix(zoom, zoom)
    rect = fitz.Rect(*clip)
    pix = page.get_pixmap(matrix=mat, clip=rect, alpha=False)
    pix.save(str(out_path))
    doc.close()


def main():
    ok, skip = 0, 0
    for rel, page, caption_y, name, pad, extra, min_y in ARCH_JOBS:
        pdf = ROOT / rel
        out = FIG_DIR / name
        if not pdf.exists():
            print(f"SKIP missing: {pdf}")
            skip += 1
            continue
        doc = fitz.open(pdf)
        clip = auto_clip(doc[page - 1], caption_y, pad, extra, min_y)
        doc.close()
        render_clip(pdf, page, clip, out)
        print(f"OK {out.name} clip=({clip[0]:.0f},{clip[1]:.0f},{clip[2]:.0f},{clip[3]:.0f})")
        ok += 1
    print(f"\n{ok} architecture figures → {FIG_DIR}")


if __name__ == "__main__":
    main()
