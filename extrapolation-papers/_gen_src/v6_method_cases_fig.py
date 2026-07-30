"""S24 — wide slide chart: same train, different extrap + test actual."""
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
TEAL = "#2a9d8f"
AMBER = "#f0a05a"
CORAL = "#e07a5f"
NAVY = "#7aa2d4"
LIME = "#9ad17b"
GRID = "#2a3545"
LINE_DIM = "#3a4a5c"
TRAIN_END = 2.2

mpl.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": PANEL,
    "text.color": INK,
    "font.family": "sans-serif",
    "font.sans-serif": ["Apple SD Gothic Neo", "Avenir Next", "Helvetica Neue", "Arial"],
    "savefig.facecolor": BG,
})

rng = np.random.default_rng(7)
x = np.linspace(0, 4.0, 400)
x_tr = np.linspace(0.35, 2.05, 12)
true = np.sin(1.15 * x) + 0.28 * x
y_tr = np.sin(1.15 * x_tr) + 0.28 * x_tr + rng.normal(0, 0.05, x_tr.size)

x_te = np.array([2.55, 2.95, 3.35, 3.75])
y_te = np.sin(1.15 * x_te) + 0.28 * x_te

coef = np.polyfit(x_tr, y_tr, 1)
curves = [
    ("MLP", np.polyval(coef, x), CYAN),
    ("EQL", np.sin(1.15 * x) + 0.28 * x, LIME),
    ("CMNN", 0.55 * np.power(np.maximum(x, 0), 1.45) + 0.35, TEAL),
    ("Physics-ML", 2.6 * (1.0 - np.exp(-1.05 * x)), NAVY),
]

# wide cinematic — matches slide ~12.6 × 2.7 in
fig, ax = plt.subplots(figsize=(12.6, 2.72))
fig.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.18)

for sp in ax.spines.values():
    sp.set_color(LINE_DIM)
ax.grid(True, color=GRID, lw=0.5, alpha=0.55)
ax.tick_params(colors=MUTED, labelsize=8.5)

ax.axvspan(0, TRAIN_END, color=TEAL, alpha=0.07)
ax.axvspan(TRAIN_END, 4.0, color=CORAL, alpha=0.05)
ax.axvline(TRAIN_END, color=CORAL, ls=(0, (5, 4)), lw=1.4)

ax.plot(x, true, color=MUTED, lw=1.8, ls=(0, (6, 4)), zorder=2)
ax.scatter(x_tr, y_tr, s=42, c=INK, edgecolors=TEAL, lw=0.8, zorder=6)
ax.scatter(x_te, y_te, s=78, c=LIME, marker="s", edgecolors=INK, lw=0.7, zorder=7)

for _name, y, col in curves:
    ax.plot(x, y, color=col, lw=2.2, zorder=4)

mlp_te = np.polyval(coef, x_te)
eql_te = np.sin(1.15 * x_te) + 0.28 * x_te
mlp_mape = np.mean(np.abs(mlp_te - y_te) / np.abs(y_te)) * 100
eql_mape = np.mean(np.abs(eql_te - y_te) / np.abs(y_te)) * 100

ax.set_xlim(0, 4)
ax.set_ylim(-0.35, 3.55)
ax.set_xlabel("입력 x", fontsize=9, color=MUTED, labelpad=2)
ax.set_ylabel("y", fontsize=9, color=MUTED, labelpad=2)

# zone labels — hull boundary
ax.text(TRAIN_END * 0.42, 3.38, "train (hull 안)", color=TEAL, fontsize=8.5, fontweight="bold", ha="center")
ax.text(TRAIN_END + (4 - TRAIN_END) * 0.42, 3.38, "hull 밖 · 시험", color=CORAL, fontsize=8.5, fontweight="bold", ha="center")
ax.text(TRAIN_END, -0.22, "hull\n경계", color=CORAL, fontsize=7.5, fontweight="bold", ha="center", va="top")

# MAPE — upper-left, no arrow through plot
ax.text(
    0.02, 0.97,
    f"밖 MAPE  MLP {mlp_mape:.0f}%  ·  EQL {eql_mape:.0f}%",
    transform=ax.transAxes, fontsize=8.5, color=INK, va="top", ha="left",
    bbox=dict(boxstyle="round,pad=0.28", facecolor=PANEL, edgecolor=AMBER, alpha=0.95),
)

# legend — single row top center
handles = [
    plt.Line2D([0], [0], color=MUTED, lw=1.8, ls=(0, (6, 4)), label="target"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=INK, markeredgecolor=TEAL,
               markersize=6, lw=0, label="train ●"),
    plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=LIME, markeredgecolor=INK,
               markersize=7, lw=0, label="밖 시험"),
]
for name, y, col in curves:
    handles.append(plt.Line2D([0], [0], color=col, lw=2.2, label=name))
ax.legend(
    handles=handles, loc="upper center", bbox_to_anchor=(0.52, 1.01),
    ncol=7, fontsize=7.5, framealpha=0.92, facecolor=PANEL, edgecolor=LINE_DIM,
    columnspacing=0.9, handletextpad=0.35,
)

fig.savefig(OUT / "fig_method_cases.png", dpi=320, bbox_inches="tight", pad_inches=0.06)
plt.close()
print("fig_method_cases ok")
