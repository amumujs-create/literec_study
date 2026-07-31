"""Assumption definition — chart only (text lives on PPT cards).

Curves share the same training points (exact pass-through). Inside the
training range they stay on / very near those points; outside they diverge
by assumption family (linear / exponential-like / oscillation+trend).
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("_assets")
BG = "#0b1016"
PANEL = "#1a2430"
INK = "#e6edf5"
MUTED = "#8b9bb0"
CYAN = "#3dd6c6"
LIME = "#9ad17b"
CORAL = "#e07a5f"
AMBER = "#f0a05a"
GRID = "#2a3545"
LINE = "#3a4a5c"
SHADE = "#12324a"

for _font in (
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
):
    if Path(_font).exists():
        try:
            fm.fontManager.addfont(_font)
        except (ValueError, OSError):
            pass

mpl.rcParams.update(
    {
        "figure.facecolor": BG,
        "text.color": INK,
        "font.family": "sans-serif",
        "font.sans-serif": [
            "NanumGothic",
            "Noto Sans CJK KR",
            "Apple SD Gothic Neo",
            "AppleGothic",
            "Malgun Gothic",
            "Avenir Next",
            "Helvetica Neue",
            "Arial",
            "DejaVu Sans",
        ],
        "savefig.facecolor": BG,
        "savefig.edgecolor": BG,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.14,
    }
)

x_pts = np.array([0.3, 0.7, 1.1, 1.5, 1.9])
y_pts = x_pts.copy()
x = np.linspace(-1, 4.5, 400)
x_b = 2.0  # training / extrapolation boundary


def _vanishing(x_grid: np.ndarray) -> np.ndarray:
    """Zero at every training x — keeps exact pass-through at ●."""
    v = np.ones_like(x_grid, dtype=float)
    for xi in x_pts:
        v = v * (x_grid - xi)
    scale = abs(np.prod(2.2 - x_pts))
    return v / scale


def _out(x_grid: np.ndarray) -> np.ndarray:
    return np.maximum(0.0, x_grid - x_b) ** 2


def _curve_b(xg: np.ndarray) -> np.ndarray:
    return xg + 0.03 * _vanishing(xg) + 0.42 * _out(xg) * np.exp(
        0.35 * np.maximum(0.0, xg - x_b)
    )


def _curve_c(xg: np.ndarray) -> np.ndarray:
    return (
        xg
        + 0.03 * _vanishing(xg) * np.sin(2.4 * xg)
        + 0.55 * _out(xg) * np.sin(2.6 * (xg - x_b))
    )


# A: linear — through all training points
y_a = x.copy()
# B: exponential-like tail (exact at ●; mild between-point path + strong outside rise)
y_b = _curve_b(x)
# C: oscillation + trend (exact at ●; wiggle grows outside)
y_c = _curve_c(x)

# Sanity: training-point residuals must be ~0
assert np.max(np.abs(y_pts - y_pts)) < 1e-12
assert np.max(np.abs(_curve_b(x_pts) - y_pts)) < 1e-9
assert np.max(np.abs(_curve_c(x_pts) - y_pts)) < 1e-9

fig, ax = plt.subplots(figsize=(8.6, 3.55))
ax.set_facecolor(PANEL)
for sp in ax.spines.values():
    sp.set_color(LINE)
ax.tick_params(colors=MUTED, labelsize=7)
ax.grid(True, color=GRID, lw=0.5, alpha=0.7)

ax.axvspan(0, x_b, color=SHADE, alpha=0.95)
ax.plot(x, y_a, color=CORAL, lw=2.0, label="가정 A: 선형", zorder=3)
ax.plot(x, y_b, color=LIME, lw=2.0, label="가정 B: 지수", zorder=3)
ax.plot(x, y_c, color=AMBER, lw=1.8, label="가정 C: 진동+추세", zorder=3)
ax.scatter(x_pts, y_pts, s=32, c=CYAN, zorder=5, label="훈련점 (동일)")
ax.set_ylim(-0.5, 5.2)
ax.set_xlim(-0.3, 4.5)
ax.set_title("같은 훈련점 — 가정만 바꾸면 밖이 전부 달라짐", color=INK, fontsize=10, pad=6)
ax.legend(loc="upper left", fontsize=7.5, labelcolor=INK, framealpha=0.25)
ax.text(1.0, 4.7, "훈련 범위", color=CYAN, fontsize=8, ha="center")
ax.text(3.3, 4.7, "외삽 영역", color=CORAL, fontsize=8, ha="center")

fig.subplots_adjust(top=0.92, left=0.08, right=0.98, bottom=0.12)
fig.savefig(OUT / "fig_assumption_defined.png", dpi=260)
plt.close()
print("assumption chart ok (train-fit exact at ●)")
