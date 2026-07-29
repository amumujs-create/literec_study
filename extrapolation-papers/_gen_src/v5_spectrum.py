"""v5 figures: assumption spectrum map + summary chain."""
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path("_assets")
BG = "#0b1016"; PANEL = "#1a2430"; INK = "#e6edf5"; MUTED = "#8b9bb0"
CYAN = "#3dd6c6"; AMBER = "#f0a05a"; LIME = "#9ad17b"; CORAL = "#e07a5f"; NAVYB = "#7aa2d4"

mpl.rcParams.update({
    "figure.facecolor": BG, "text.color": INK, "font.family": "sans-serif",
    "font.sans-serif": ["Avenir Next", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "savefig.facecolor": BG, "savefig.bbox": "tight", "savefig.pad_inches": 0.18,
})

def box(ax, cx, cy, w, h, text, edge, sub=None, face=PANEL, ts=10.5, sub_ts=7.6):
    b = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                       boxstyle="round,pad=0.008,rounding_size=0.05",
                       facecolor=face, edgecolor=edge, linewidth=1.6,
                       transform=ax.transAxes, zorder=3)
    ax.add_patch(b)
    dy = 0.05 if sub else 0
    ax.text(cx, cy + dy, text, transform=ax.transAxes, ha="center", va="center",
            color=INK, fontsize=ts, fontweight="semibold", zorder=4, linespacing=1.3)
    if sub:
        ax.text(cx, cy - 0.09, sub, transform=ax.transAxes, ha="center", va="center",
                color=MUTED, fontsize=sub_ts, zorder=4, linespacing=1.35)

# ── 1. assumption spectrum (Act 2 map) ──
fig, ax = plt.subplots(figsize=(12.0, 4.4))
ax.set_facecolor(BG); ax.axis("off")
fig.suptitle("Figure. The assumption spectrum — what you buy, and what it costs",
             color=INK, fontsize=13, fontweight="semibold", y=0.98, x=0.02, ha="left")
fig.text(0.02, 0.90, "Stronger assumption = better extrapolation when right, worse failure when wrong",
         color=MUTED, fontsize=9)

# gradient spectrum bar
import numpy as np
grad = np.linspace(0, 1, 400).reshape(1, -1)
ax.imshow(grad, extent=[0.04, 0.96, 0.60, 0.66], transform=ax.transAxes,
          aspect="auto", cmap=mpl.colors.LinearSegmentedColormap.from_list("s", [CORAL, AMBER, CYAN]),
          alpha=0.85, zorder=1)
ax.text(0.04, 0.71, "STRONG assumption", transform=ax.transAxes, color=CORAL, fontsize=10, fontweight="bold")
ax.text(0.96, 0.71, "NO assumption", transform=ax.transAxes, color=CYAN, fontsize=10, fontweight="bold", ha="right")

stations = [
    (0.13, CORAL, "1  Function family\nknown", "EQL / NALU\nbuy: global closed form\ncost: gate instability,\ncatastrophic if wrong"),
    (0.38, AMBER, "2  Direction only\nknown", "Monotonic (CMNN)\nbuy: no sign reversal\ncost: needs right\nreparameterization"),
    (0.62, LIME, "3  Governing eq.\nknown", "PINN\nbuy: physics guidance\ncost: residual != guarantee\n(needs validation)"),
    (0.87, CYAN, "4  Nothing\nknown", "UQ + abstain (DeepONet)\nbuy: honest silence\ncost: no prediction\nin far region"),
]
for cx, c, title, sub in stations:
    ax.plot([cx], [0.63], marker="v", color=c, markersize=10, transform=ax.transAxes, zorder=5)
    box(ax, cx, 0.30, 0.215, 0.42, title, c, sub=sub, ts=10)

fig.subplots_adjust(top=0.84, left=0.02, right=0.98, bottom=0.02)
fig.savefig(OUT / "fig_assumption_spectrum.png", dpi=260)
plt.close()
print("wrote fig_assumption_spectrum.png")

