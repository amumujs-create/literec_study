"""Assumption definition — chart only (text lives on PPT cards)."""
from pathlib import Path

import matplotlib as mpl
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

mpl.rcParams.update(
    {
        "figure.facecolor": BG,
        "text.color": INK,
        "font.family": "sans-serif",
        "font.sans-serif": [
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

fig, ax = plt.subplots(figsize=(8.6, 3.55))
ax.set_facecolor(PANEL)
for sp in ax.spines.values():
    sp.set_color(LINE)
ax.tick_params(colors=MUTED, labelsize=7)
ax.grid(True, color=GRID, lw=0.5, alpha=0.7)

x = np.linspace(-1, 4.5, 300)
ax.axvspan(0, 2, color=SHADE, alpha=0.95)
ax.scatter([0.3, 0.7, 1.1, 1.5, 1.9], [0.3, 0.7, 1.1, 1.5, 1.9], s=32, c=CYAN, zorder=5, label="훈련점 (동일)")
ax.plot(x, x, color=CORAL, lw=2.0, label="가정 A: 선형")
ax.plot(x, np.exp(0.55 * x) - 1, color=LIME, lw=2.0, label="가정 B: 지수")
ax.plot(x, np.sin(1.2 * x) * 1.6 + 0.9 * x, color=AMBER, lw=1.8, label="가정 C: 진동+추세")
ax.set_ylim(-0.5, 5.2)
ax.set_xlim(-0.3, 4.5)
ax.set_title("같은 훈련점 — 가정만 바꾸면 밖이 전부 달라짐", color=INK, fontsize=10, pad=6)
ax.legend(loc="upper left", fontsize=7.5, labelcolor=INK, framealpha=0.25)
ax.text(1.0, 4.7, "훈련 범위", color=CYAN, fontsize=8, ha="center")
ax.text(3.3, 4.7, "외삽 영역", color=CORAL, fontsize=8, ha="center")

fig.subplots_adjust(top=0.92, left=0.08, right=0.98, bottom=0.12)
fig.savefig(OUT / "fig_assumption_defined.png", dpi=260)
plt.close()
print("assumption chart ok")
