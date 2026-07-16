"""Matplotlib 논문/학술 Figure 스타일 — 발표 슬라이드용 (1920×1080)."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, Rectangle
from PIL import ImageFont

W, H = 12.8, 7.2  # inches @ dpi=150 → 1920×1080
DPI = 150

OUT = Path(__file__).resolve().parent.parent / "figures"
FONT_DIR = Path(__file__).resolve().parent / "fonts"

# Colorblind-friendly (matplotlib tab10 계열)
C_BLUE = "#1f77b4"
C_ORANGE = "#ff7f0e"
C_GREEN = "#2ca02c"
C_RED = "#d62728"
C_PURPLE = "#9467bd"
C_TEAL = "#17becf"
C_GRAY = "#7f7f7f"
C_SLATE = "#333333"
C_MUTED = "#666666"
C_NAVY = "#1a1a1a"

TRAIN_FILL = "#e8f4fc"
EXTRAP_FILL = "#fdf0e6"
_TRAIN_FILL = TRAIN_FILL
_EXTRAP_FILL = EXTRAP_FILL


def _register_korean_font() -> str:
    candidates = [
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        Path(__file__).resolve().parent / "fonts" / "NanumGothic.ttf",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            font_manager.fontManager.addfont(str(p))
            return font_manager.FontProperties(fname=str(p)).get_name()
    return "DejaVu Sans"


_FONT = _register_korean_font()
_STYLE_READY = False


def setup_style():
    global _STYLE_READY
    if _STYLE_READY:
        return
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [_FONT, "DejaVu Sans", "Arial"],
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#333333",
        "axes.labelcolor": "#333333",
        "axes.titleweight": "normal",
        "axes.unicode_minus": False,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "legend.frameon": True,
        "legend.framealpha": 1.0,
        "legend.edgecolor": "#cccccc",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": DPI,
        "grid.alpha": 0.35,
        "grid.linewidth": 0.5,
        "grid.color": "#cccccc",
        "lines.linewidth": 1.8,
        "lines.markersize": 5,
        "mathtext.fontset": "dejavusans",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    _STYLE_READY = True


def new_figure(nrows: int = 1, ncols: int = 1, **kwargs):
    setup_style()
    fig, axes = plt.subplots(nrows, ncols, figsize=(W, H), dpi=DPI, **kwargs)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.92, bottom=0.08, wspace=0.28, hspace=0.32)
    return fig, axes


def save(fig, name: str):
    setup_style()
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return path


def style_ax(ax, xlabel: str = "", ylabel: str = "", title: str = ""):
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, pad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=4, width=0.8)


def panel_label(ax, label: str, x: float = -0.10, y: float = 1.04):
    ax.text(x, y, label, transform=ax.transAxes, fontsize=12, fontweight="bold", va="top", ha="left")


def shade_regions(ax, x_split, xlim, train_label: str = "interpolation", extrap_label: str = "extrapolation"):
    ax.axvspan(xlim[0], x_split, color=_TRAIN_FILL, alpha=0.6, zorder=0)
    ax.axvspan(x_split, xlim[1], color=_EXTRAP_FILL, alpha=0.6, zorder=0)
    ax.axvline(x_split, color="#555555", linewidth=0.9, linestyle="--", zorder=1)
    ymax = ax.get_ylim()[1]
    ax.text((xlim[0] + x_split) / 2, ymax, train_label, ha="center", va="bottom", fontsize=9, color=C_MUTED)
    ax.text((x_split + xlim[1]) / 2, ymax, extrap_label, ha="center", va="bottom", fontsize=9, color=C_MUTED)


def add_box(ax, xy, w, h, text: str, fc: str = "white", ec: str = "#333333", fontsize: int = 10):
    rect = Rectangle(xy, w, h, linewidth=0.8, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(rect)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center", fontsize=fontsize, zorder=3)


def add_arrow(ax, p1, p2, color: str = "#333333"):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle="-|>", mutation_scale=12, linewidth=1.0, color=color, zorder=4,
        shrinkA=0, shrinkB=0,
    ))


def suptitle(fig, title: str, subtitle: str = ""):
    fig.suptitle(title, fontsize=14, fontweight="bold", y=0.98)
    if subtitle:
        fig.text(0.5, 0.935, subtitle, ha="center", fontsize=10, color=C_MUTED)


def t(ko: str, en: str = "") -> str:
    return ko


# annotate_figures.py 호환 — PIL 한글 폰트
_PIL_FONT: dict = {}


def load_font(size: int = 20, bold: bool = False):
    key = (size, bold)
    if key in _PIL_FONT:
        return _PIL_FONT[key]
    names = ("NanumBarunGothicBold.ttf", "NanumBarunGothic.ttf") if bold else ("NanumBarunGothic.ttf",)
    paths = [FONT_DIR / n for n in names] + [Path(f"/usr/share/fonts/truetype/nanum/{n}") for n in names]
    for path in paths:
        if path.exists():
            try:
                f = ImageFont.truetype(str(path), size)
                _PIL_FONT[key] = f
                return f
            except OSError:
                pass
    return ImageFont.load_default()
