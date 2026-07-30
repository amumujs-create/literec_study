"""v5 extra figures: 3-questions roadmap, dimension curse, PINN concept, DomainBed bars, checklist."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path("_assets")
BG = "#0b1016"; PANEL = "#1a2430"; INK = "#e6edf5"; MUTED = "#8b9bb0"
CYAN = "#3dd6c6"; AMBER = "#f0a05a"; LIME = "#9ad17b"; CORAL = "#e07a5f"; NAVYB = "#7aa2d4"
GRID = "#2a3545"; LINE_DIM = "#3a4a5c"

mpl.rcParams.update({
    "figure.facecolor": BG, "text.color": INK, "font.family": "sans-serif",
    "font.sans-serif": ["Avenir Next", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "savefig.facecolor": BG, "savefig.bbox": "tight", "savefig.pad_inches": 0.18,
})

def style_ax(ax):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_color(LINE_DIM)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(True, color=GRID, lw=0.6, alpha=0.7)

def box(ax, cx, cy, w, h, text, edge, sub=None, face=PANEL, ts=11, sub_ts=8):
    b = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                       boxstyle="round,pad=0.008,rounding_size=0.05",
                       facecolor=face, edgecolor=edge, linewidth=1.7,
                       transform=ax.transAxes, zorder=3)
    ax.add_patch(b)
    dy = 0.06 if sub else 0
    ax.text(cx, cy + dy, text, transform=ax.transAxes, ha="center", va="center",
            color=INK, fontsize=ts, fontweight="semibold", zorder=4, linespacing=1.35)
    if sub:
        ax.text(cx, cy - 0.10, sub, transform=ax.transAxes, ha="center", va="center",
                color=MUTED, fontsize=sub_ts, zorder=4, linespacing=1.4)

# ── 2. dimension curse: P(inside hull) vs d ──
fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.6), gridspec_kw={"width_ratios": [1, 1.1]})
fig.suptitle("Figure. Why almost everything is extrapolation in high dimension",
             color=INK, fontsize=12.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
ax = axes[0]
style_ax(ax)
rng = np.random.default_rng(3)
pts = rng.normal(0, 1, (60, 2))
from scipy.spatial import ConvexHull
hull = ConvexHull(pts)
poly = pts[hull.vertices]
poly = np.vstack([poly, poly[0]])
ax.fill(poly[:, 0], poly[:, 1], color=CYAN, alpha=0.12)
ax.plot(poly[:, 0], poly[:, 1], color=CYAN, lw=1.6)
ax.scatter(pts[:, 0], pts[:, 1], s=14, c=CYAN, alpha=0.8)
out = np.array([[2.8, 1.9], [-2.6, 2.3], [3.0, -2.2]])
ax.scatter(out[:, 0], out[:, 1], s=70, marker="x", c=AMBER, linewidths=2.2)
ax.set_title("(a) d=2 : hull looks big", color=INK, fontsize=10, pad=6)
ax.set_xticks([]); ax.set_yticks([])

ax = axes[1]
style_ax(ax)
d = np.arange(1, 101)
# P(new gaussian point in hull of n=1000 samples) rough decay
p = np.minimum(1.0, 1000 / (2.0 ** (d / 2.2)))
ax.semilogy(d, p, color=AMBER, lw=2.4)
ax.axhline(0.01, color=CORAL, ls="--", lw=1.2)
ax.text(58, 0.013, "1% line", color=CORAL, fontsize=8)
ax.set_title("(b) P(new point inside hull) collapses with d", color=INK, fontsize=10, pad=6)
ax.set_xlabel("dimension d")
ax.set_ylabel("P(inside hull)")
fig.subplots_adjust(top=0.82, left=0.05, right=0.98, bottom=0.14, wspace=0.25)
fig.savefig(OUT / "fig_hull_dimension.png", dpi=260)
plt.close()
print("2 ok")

# ── 3. PINN concept ──
fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.6), gridspec_kw={"width_ratios": [1.15, 1]})
fig.suptitle("Figure. PINN — add physics residual to the loss (Raissi 2019)",
             color=INK, fontsize=12.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
ax = axes[0]
ax.set_facecolor(BG); ax.axis("off")
box(ax, 0.14, 0.70, 0.22, 0.26, "Data loss", CYAN, "match observed points\nL_data")
box(ax, 0.14, 0.28, 0.22, 0.26, "Physics loss", CORAL, "PDE residual on\ncollocation points\n||N[u]||^2")
box(ax, 0.56, 0.49, 0.24, 0.30, "L = L_data + λ·L_phys", LIME, "one network u(x,t)\ntrained on both")
box(ax, 0.90, 0.49, 0.16, 0.30, "u(x,t)", NAVYB, "smooth solution\neven where data\nis sparse")
ax.annotate("", xy=(0.42, 0.60), xytext=(0.26, 0.70), xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.5))
ax.annotate("", xy=(0.42, 0.40), xytext=(0.26, 0.28), xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.5))
ax.annotate("", xy=(0.80, 0.49), xytext=(0.69, 0.49), xycoords=ax.transAxes, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.5))

ax = axes[1]
style_ax(ax)
x = np.linspace(0, 1, 200)
true = np.sin(2*np.pi*x) * np.exp(-1.2*x)
obs_x = np.array([0.05, 0.15, 0.3, 0.42, 0.55])
obs_y = np.sin(2*np.pi*obs_x) * np.exp(-1.2*obs_x)
ax.plot(x, true, color=MUTED, ls="--", lw=1.2, label="true solution")
ax.plot(x, true + 0.02*np.sin(9*x), color=LIME, lw=2.0, label="PINN")
ax.scatter(obs_x, obs_y, s=40, c=INK, edgecolors=CYAN, zorder=5, label="sparse data")
ax.set_title("physics fills where data is sparse", color=INK, fontsize=9.5, pad=6)
ax.legend(loc="upper right", fontsize=7.5, labelcolor=INK, framealpha=0.2)
ax.set_xticks([]); ax.set_yticks([])
fig.subplots_adjust(top=0.82, left=0.02, right=0.98, bottom=0.06, wspace=0.15)
fig.savefig(OUT / "fig_pinn_concept.png", dpi=260)
plt.close()
print("3 ok")

# ── 4. DomainBed bars ──
fig, ax = plt.subplots(figsize=(10.6, 3.8))
style_ax(ax)
fig.suptitle("Figure. DomainBed — under fair tuning, ERM matches or beats most OOD algorithms",
             color=INK, fontsize=12.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
algs = ["ERM", "IRM", "GroupDRO", "Mixup", "MLDG", "CORAL", "DANN", "RSC"]
avg = [66.6, 65.4, 66.0, 66.7, 66.7, 67.5, 65.6, 66.6]  # DomainBed avg accuracy (paper table approx)
colors = [CYAN] + [PANEL]*7
edge = [CYAN, CORAL, CORAL, MUTED, MUTED, LIME, CORAL, MUTED]
bars = ax.bar(algs, avg, color=colors, edgecolor=edge, linewidth=1.6, width=0.62)
ax.axhline(66.6, color=CYAN, ls="--", lw=1.2, alpha=0.8)
ax.text(7.45, 66.75, "ERM line", color=CYAN, fontsize=8, ha="right")
for b, v in zip(bars, avg):
    ax.text(b.get_x() + b.get_width()/2, v + 0.12, f"{v:.1f}", ha="center", color=INK, fontsize=8.5)
ax.set_ylim(63, 69)
ax.set_ylabel("avg accuracy (7 datasets)")
ax.set_title("14 algorithms x 7 datasets, same HP budget / capacity / model-selection (values: Gulrajani & Lopez-Paz 2020)",
             color=MUTED, fontsize=8.5, pad=6)
fig.subplots_adjust(top=0.80, left=0.07, right=0.98, bottom=0.10)
fig.savefig(OUT / "fig_domainbed_bars.png", dpi=260)
plt.close()
print("4 ok")

# ── 5. checklist ──
fig, ax = plt.subplots(figsize=(11.6, 3.3))
ax.set_facecolor(BG); ax.axis("off")
fig.suptitle("Figure. Pre-claim checklist — say 'extrapolation performance' only after these four",
             color=INK, fontsize=12.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
items = [
    (0.13, CYAN, "1  Really outside?", "test ∩ Conv(X_train) = ∅\nelse call it interpolation"),
    (0.38, AMBER, "2  Which outside?", "diversity vs correlation\nD_div / D_cor (OoD-Bench)"),
    (0.62, CORAL, "3  Fair comparison?", "ERM baseline · same budget\nsame capacity (DomainBed)"),
    (0.87, LIME, "4  Robust?", "swap split / seed\nconclusion survives?"),
]
for cx, c, title, sub in items:
    box(ax, cx, 0.44, 0.225, 0.58, title, c, sub=sub, ts=11.5, sub_ts=8)
    ax.text(cx - 0.095, 0.80, "☑", transform=ax.transAxes, color=c, fontsize=15, fontweight="bold")
fig.subplots_adjust(top=0.80, left=0.01, right=0.99, bottom=0.04)
fig.savefig(OUT / "fig_checklist.png", dpi=260)
plt.close()
print("5 ok")