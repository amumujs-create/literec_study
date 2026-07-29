"""OOD vs extrapolation — side-by-side comparison figure for S05."""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from scipy.spatial import ConvexHull

OUT = Path("_assets")
BG = "#0b1016"
PANEL = "#1a2430"
INK = "#e6edf5"
MUTED = "#8b9bb0"
CYAN = "#3dd6c6"
AMBER = "#f0a05a"
CORAL = "#e07a5f"
VIOLET = "#a78bfa"
GRID = "#2a3545"
LINE_DIM = "#3a4a5c"

mpl.rcParams.update({
    "figure.facecolor": BG,
    "text.color": INK,
    "font.family": "sans-serif",
    "font.sans-serif": ["Avenir Next", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "savefig.facecolor": BG,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.16,
})


def style_ax(ax):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_color(LINE_DIM)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.7)


fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.35), gridspec_kw={"width_ratios": [1.05, 1.05]})
fig.suptitle(
    "OOD vs Extrapolation — different questions",
    color=INK, fontsize=12.5, fontweight="semibold", y=0.98, x=0.02, ha="left",
)
fig.text(
    0.02, 0.90,
    "Left: distribution shift (OOD umbrella)   ·   Right: input outside convex hull (today's focus)",
    color=MUTED, fontsize=8.5,
)

# (a) OOD — covariate / support shift
ax = axes[0]
style_ax(ax)
xs = np.linspace(-4, 4, 400)
ptr = np.exp(-0.5 * ((xs + 0.6) / 0.75) ** 2)
qtr = np.exp(-0.5 * ((xs - 1.4) / 0.80) ** 2)
ax.fill_between(xs, 0, ptr / ptr.max() * 0.92, color=CYAN, alpha=0.32, label=r"$P_{\mathrm{train}}$")
ax.fill_between(xs, 0, qtr / qtr.max() * 0.92, color=AMBER, alpha=0.32, label=r"$P_{\mathrm{test}}$")
ax.axvline(2.35, color=AMBER, ls="--", lw=1.1, alpha=0.75)
ax.scatter([2.35], [0.22], s=90, c=AMBER, marker="D", zorder=5, edgecolors=INK, linewidths=0.6)
ax.annotate(
    "query\n(OOD)", xy=(2.35, 0.22), xytext=(2.85, 0.55),
    color=AMBER, fontsize=8, ha="left",
    arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.0),
)
ax.text(-2.6, 0.78, "train support", color=CYAN, fontsize=8, ha="center")
ax.text(0.6, 0.78, "overlap", color=MUTED, fontsize=7.5, ha="center")
ax.text(3.2, 0.78, "novel region", color=AMBER, fontsize=8, ha="center")
ax.set_title("(a) OOD — train ≠ test distribution", color=INK, fontsize=10, pad=6)
ax.set_xlabel("feature $x$")
ax.set_ylabel("density (norm.)")
ax.set_xlim(-4, 4)
ax.set_ylim(0, 1.02)
ax.legend(loc="upper left", fontsize=7.5, labelcolor=INK, framealpha=0.15)

# (b) Extrapolation — convex hull geometry
ax = axes[1]
style_ax(ax)
rng = np.random.default_rng(7)
pts = rng.normal(size=(42, 2)) * np.array([1.35, 1.05])
hull = ConvexHull(pts)
poly = pts[hull.vertices]
poly = np.vstack([poly, poly[0]])
ax.fill(poly[:, 0], poly[:, 1], color=CYAN, alpha=0.14, zorder=1)
ax.plot(poly[:, 0], poly[:, 1], color=CYAN, lw=1.8, alpha=0.95, zorder=2, label="conv($X_{\\mathrm{train}}$)")

# train cloud
ax.scatter(pts[:, 0], pts[:, 1], s=20, c=CYAN, alpha=0.75, zorder=3, label="train")

# extrap query — outside hull
extrap = np.array([2.75, 1.55])
ax.scatter([extrap[0]], [extrap[1]], s=95, c=AMBER, marker="*", zorder=6, edgecolors=INK, linewidths=0.5)
ax.annotate(
    "extrap\n(outside hull)", xy=extrap, xytext=(1.55, 2.35),
    color=AMBER, fontsize=8, ha="center",
    arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.0),
)

# concept shift — inside hull but OOD (different rule)
concept = np.array([0.15, -0.35])
ax.scatter([concept[0]], [concept[1]], s=75, c=VIOLET, marker="s", zorder=6, edgecolors=INK, linewidths=0.5)
ax.annotate(
    "concept shift\n(OOD, inside hull)", xy=concept, xytext=(-2.1, -1.85),
    color=VIOLET, fontsize=7.5, ha="center",
    arrowprops=dict(arrowstyle="->", color=VIOLET, lw=1.0),
)

ax.set_aspect("equal", adjustable="datalim")
ax.set_title("(b) Extrapolation — input outside hull", color=INK, fontsize=10, pad=6)
ax.set_xlabel("$x_1$")
ax.set_ylabel("$x_2$")
ax.legend(loc="upper right", fontsize=7.5, labelcolor=INK, framealpha=0.15)

# Venn hint between panels (fig coords)
venn = FancyBboxPatch(
    (0.46, 0.06), 0.08, 0.14,
    boxstyle="round,pad=0.01,rounding_size=0.02",
    transform=fig.transFigure, facecolor=PANEL, edgecolor=LINE_DIM, linewidth=0.8, zorder=10,
)
fig.patches.append(venn)
fig.text(0.50, 0.16, "extrap\noften\nsubset of\nOOD", ha="center", va="center", color=MUTED, fontsize=6.5, zorder=11)

fig.subplots_adjust(top=0.82, left=0.06, right=0.98, bottom=0.12, wspace=0.22)
fig.savefig(OUT / "fig_ood_vs_extrap.png", dpi=260)
plt.close()
print("wrote fig_ood_vs_extrap.png")
