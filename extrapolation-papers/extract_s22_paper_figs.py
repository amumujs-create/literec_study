#!/usr/bin/env python3
"""Extract/crop paper figures for S22 (physics loss vs PINN)."""
from __future__ import annotations

import io
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "paper_pdfs"
OUT = ROOT / "_assets" / "paper_figs"


def render_clip(pdf_name: str, page: int, out_name: str, clip: tuple[float, float, float, float], zoom: float = 2.2) -> None:
    doc = fitz.open(PDF / pdf_name)
    pg = doc[page - 1]
    r = pg.rect
    c = fitz.Rect(
        r.x0 + r.width * clip[0],
        r.y0 + r.height * clip[1],
        r.x0 + r.width * clip[2],
        r.y0 + r.height * clip[3],
    )
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=c)
    pix.save(str(OUT / out_name))
    print("clip", out_name, pix.width, pix.height)


def extract_embedded(pdf_name: str, page: int, out_name: str) -> None:
    doc = fitz.open(PDF / pdf_name)
    imgs = doc[page - 1].get_images(full=True)
    if not imgs:
        raise RuntimeError(f"no image on {pdf_name} p{page}")
    base = doc.extract_image(imgs[0][0])
    im = Image.open(io.BytesIO(base["image"]))
    im.save(OUT / out_name)
    print("embed", out_name, im.size)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    extract_embedded("Aykol2021_Physics_ML_Battery_Lifetime.pdf", 3, "aykol_fig1_integration_map.png")
    render_clip(
        "Li2023_Predicting_Battery_Lifetime_Varying_Conditions.pdf",
        8,
        "li2023_fig4_ab_extrap.png",
        (0.04, 0.06, 0.72, 0.55),
        2.3,
    )
    render_clip(
        "Muckley2023_Interpretable_Models_Extrapolation_SciML.pdf",
        9,
        "muckley_fig4_interp_extrap.png",
        (0.06, 0.06, 0.94, 0.46),
        2.4,
    )
    render_clip(
        "Raissi2019_Physics_Informed_Neural_Networks.pdf",
        8,
        "raissi_fig1_burgers.png",
        (0.06, 0.08, 0.94, 0.72),
        2.2,
    )
    orig = OUT / "fesser_fig1_pinn_extrap_orig.png"
    if orig.exists():
        Image.open(orig).save(OUT / "fesser_fig1_pinn_extrap.png")
        print("copy fesser from orig")
    print("done →", OUT)


if __name__ == "__main__":
    main()
