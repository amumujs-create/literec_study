"""OoD-Bench diversity vs correlation shift figure."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path("_assets")
BG = "#0b1016"; PANEL = "#1a2430"; INK = "#e6edf5"; MUTED = "#8b9bb0"
CYAN = "#3dd6c6"; AMBER = "#f0a05a"; LIME = "#9ad17b"; CORAL = "#e07a5f"; NAVYB = "#7aa2d4"

mpl.rcParams.update({
    "figure.facecolor": BG, "text.color": INK, "font.family": "sans-serif",
    "font.sans-serif": ["Avenir Next", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "savefig.facecolor": BG, "savefig.bbox": "tight", "savefig.pad_inches": 0.18,
})

def style_ax(ax):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_color("#3a4a5c")
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(True, color="#2a3545", lw=0.6, alpha=0.7)

fig, axes = plt.subplots(1, 3, figsize=(11.8, 4.2), gridspec_kw={"width_ratios": [1.05, 1.05, 1.15]})
fig.suptitle("Figure. OoD-Bench (Ye et al., CVPR 2022) — two shift types before choosing a method",
             color=INK, fontsize=12.5, fontweight="semibold", y=0.98, x=0.02, ha="left")
fig.text(0.02, 0.90, "Same 'OOD' label hides different failure modes — quantify D_div and D_cor first",
         color=MUTED, fontsize=9)

# (a) Diversity shift
ax = axes[0]
style_ax(ax)
xs = np.linspace(-3, 3, 300)
ptr = np.exp(-0.5*((xs+0.8)/0.55)**2)
qtr = np.exp(-0.5*((xs-1.1)/0.55)**2)
ax.fill_between(xs, 0, ptr/ptr.max()*0.9, color=CYAN, alpha=0.35, label="train p(z)")
ax.fill_between(xs, 0, qtr/qtr.max()*0.9, color=AMBER, alpha=0.35, label="test q(z)")
ax.axvspan(-3, -0.2, color=CYAN, alpha=0.08)
ax.axvspan(0.4, 3, color=AMBER, alpha=0.08)
ax.text(-1.8, 0.72, "novel region\n(not in train)", color=CYAN, fontsize=8, ha="center")
ax.set_title("(a) Diversity shift", color=INK, fontsize=10, pad=6)
ax.set_xlabel("latent feature z")
ax.set_yticks([])
ax.legend(loc="upper right", fontsize=7, labelcolor=INK, framealpha=0.2)

# (b) Correlation shift
ax = axes[1]
style_ax(ax)
z = np.linspace(-2.5, 2.5, 200)
# same support, different P(Y|z)
ax.fill_between(z, 0, np.exp(-0.5*(z/1.1)**2)/np.exp(-0.5*(z/1.1)**2).max()*0.85, color=MUTED, alpha=0.25, label="shared support")
for c, off, lab in [(CYAN, -0.35, "p(y|z) train"), (AMBER, 0.35, "q(y|z) test")]:
    y = 0.55 + 0.35*np.tanh(1.2*z + off)
    ax.plot(z, y, color=c, lw=2.2, label=lab)
ax.text(0, 0.15, "spurious cue\nsame z, new rule", color=CORAL, fontsize=8, ha="center")
ax.set_ylim(0, 1.05)
ax.set_title("(b) Correlation shift", color=INK, fontsize=10, pad=6)
ax.set_xlabel("latent feature z (shared)")
ax.set_yticks([])
ax.legend(loc="upper left", fontsize=7, labelcolor=INK, framealpha=0.2)

# (c) dataset map (approx from paper Fig.3)
ax = axes[2]
style_ax(ax)
pts = {
    "ColoredMNIST": (0.82, 0.18, CORAL),
    "CelebA": (0.75, 0.28, CORAL),
    "PACS": (0.35, 0.78, CYAN),
    "Camelyon": (0.55, 0.72, CYAN),
    "DomainNet": (0.48, 0.62, CYAN),
    "ImageNet-V2": (0.22, 0.22, MUTED),
    "NICO": (0.58, 0.45, NAVYB),
}
for name, (x, y, c) in pts.items():
    ax.scatter([x], [y], s=55 if c!=MUTED else 40, c=c, edgecolors=INK, linewidths=0.6, zorder=3)
    ax.text(x+0.03, y+0.03, name, color=INK if c!=MUTED else MUTED, fontsize=7)
ax.set_xlim(0.05, 1.0)
ax.set_ylim(0.05, 1.0)
ax.set_xlabel("Correlation shift  (D_cor)")
ax.set_ylabel("Diversity shift  (D_div)")
ax.set_title("(c) Dataset shift profile (approx.)", color=INK, fontsize=10, pad=6)
ax.text(0.12, 0.88, "Diversity-dominated", color=CYAN, fontsize=7.5)
ax.text(0.62, 0.12, "Correlation-dominated", color=CORAL, fontsize=7.5)

fig.subplots_adjust(top=0.82, left=0.04, right=0.98, bottom=0.10, wspace=0.28)
fig.savefig(OUT / "fig_ood_bench_shifts.png", dpi=260)
plt.close()
print("wrote fig_ood_bench_shifts.png")