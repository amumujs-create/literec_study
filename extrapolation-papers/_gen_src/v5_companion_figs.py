"""Companion example figures: fill empty slide space with concrete examples."""
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path("_assets")
BG="#0b1016"; PANEL="#1a2430"; INK="#e6edf5"; MUTED="#8b9bb0"
CYAN="#3dd6c6"; AMBER="#f0a05a"; LIME="#9ad17b"; CORAL="#e07a5f"; NAVYB="#7aa2d4"
GRID="#2a3545"; LINE_DIM="#3a4a5c"; SHADE="#12324a"

mpl.rcParams.update({
    "figure.facecolor": BG, "text.color": INK, "font.family": "sans-serif",
    "font.sans-serif": ["Avenir Next", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "savefig.facecolor": BG, "savefig.bbox": "tight", "savefig.pad_inches": 0.15,
})

def style_ax(ax, grid=True):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values(): sp.set_color(LINE_DIM)
    ax.tick_params(colors=MUTED, labelsize=8)
    if grid: ax.grid(True, color=GRID, lw=0.6, alpha=0.7)

def shade_train(ax, lo, hi, label="train region"):
    ax.axvspan(lo, hi, color=SHADE, alpha=0.9, zorder=0)
    ax.text((lo+hi)/2, 0.97, label, transform=ax.get_xaxis_transform(),
            ha="center", va="top", color=CYAN, fontsize=8)

# ── A. Xu concrete example: MLP on sin -> tangent line outside ──
rng = np.random.default_rng(0)
x = np.linspace(-6, 6, 400)
true = np.sin(x)
# fake "MLP prediction": sin inside [-2,2], tangent continuation outside
pred = np.where(x < -2, np.sin(-2) + np.cos(-2)*(x+2),
       np.where(x > 2, np.sin(2) + np.cos(2)*(x-2), np.sin(x)))
fig, ax = plt.subplots(figsize=(9.2, 3.4))
style_ax(ax)
fig.suptitle("Example. MLP trained on y=sin(x), x in [-2, 2] — outside it draws the tangent line",
             color=INK, fontsize=11.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
shade_train(ax, -2, 2)
ax.plot(x, true, ls="--", color=MUTED, lw=1.4, label="true  y = sin(x)")
ax.plot(x, pred, color=CORAL, lw=2.4, label="MLP prediction")
xt = rng.uniform(-2, 2, 28)
ax.scatter(xt, np.sin(xt) + rng.normal(0, .03, 28), s=16, c=CYAN, zorder=5, label="train data")
ax.annotate("inside: perfect fit", xy=(0, 0.4), xytext=(-0.9, 1.55),
            color=CYAN, fontsize=9, arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.2))
ax.annotate("outside: straight line,\nnever curves back", xy=(4.4, np.sin(2)+np.cos(2)*2.4), xytext=(3.0, -1.7),
            color=CORAL, fontsize=9, arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.2))
ax.set_ylim(-2.2, 2.2); ax.legend(loc="upper left", fontsize=8, labelcolor=INK, framealpha=0.2)
fig.subplots_adjust(top=0.86, left=0.05, right=0.99, bottom=0.10)
fig.savefig(OUT / "fig_xu_sin_tangent.png", dpi=260); plt.close(); print("A ok")

# ── B. regenerate fig_relu_affine: 2 panels, no overlapping caption ──
fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.5))
fig.suptitle("Figure. Why the output becomes a straight line — neurons freeze, layers turn linear",
             color=INK, fontsize=11.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
ax = axes[0]; style_ax(ax)
xx = np.linspace(-6, 6, 500)
kinks = [-1.5, -0.4, 0.7, 1.8]
for i, k in enumerate(kinks):
    ax.plot(xx, np.maximum(0, xx - k)*0.5 + i*0.9, color=[CYAN, LIME, NAVYB, AMBER][i], lw=1.6)
    ax.axvline(k, color=GRID, lw=0.8, ls=":")
shade_train(ax, -2, 2)
ax.text(4.0, 0.35, "right of the last kink:\nevery neuron fixed ON/OFF", color=INK, fontsize=8.5)
ax.set_title("(a) each ReLU neuron bends only once (kink)", color=INK, fontsize=9.5, pad=5)
ax.set_yticks([])
ax = axes[1]; style_ax(ax)
y = np.where(xx < -2, -0.9 - 0.55*(xx+2), np.where(xx > 2, 0.9 + 0.8*(xx-2), np.sin(xx*1.3)*0.9))
shade_train(ax, -2, 2)
ax.plot(xx, y, color=CORAL, lw=2.4, label="network output")
ax.plot(xx, np.sin(xx*1.3)*0.9, ls="--", color=MUTED, lw=1.2, label="target")
ax.annotate("f(x) = A·x + b\n(affine regime)", xy=(4.6, 0.9+0.8*2.6), xytext=(2.8, -1.9),
            color=CORAL, fontsize=9, arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.2))
ax.text(0, -2.35, "all bends live near the data", color=CYAN, fontsize=8.5, ha="center")
ax.set_ylim(-2.6, 3.4)
ax.set_title("(b) far from data: sum of frozen lines = one line", color=INK, fontsize=9.5, pad=5)
ax.legend(loc="upper left", fontsize=8, labelcolor=INK, framealpha=0.2)
fig.subplots_adjust(top=0.84, left=0.03, right=0.99, bottom=0.08, wspace=0.12)
fig.savefig(OUT / "fig_relu_affine.png", dpi=260); plt.close(); print("B ok")

# ── C. activation match example: ReLU fails on sin, cos-activation succeeds ──
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.2))
fig.suptitle("Example. Same target y=sin(x) — only the matching activation keeps extrapolating",
             color=INK, fontsize=11.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
for ax, ok in zip(axes, [False, True]):
    style_ax(ax); shade_train(ax, -2, 2)
    ax.plot(x, true, ls="--", color=MUTED, lw=1.2, label="true sin(x)")
    if ok:
        ax.plot(x, np.sin(x)+0.03*np.sin(7*x)*np.clip(np.abs(x)-2,0,None), color=LIME, lw=2.2, label="cos-activation net")
        ax.set_title("(b) activation = cos  ->  follows the wave", color=LIME, fontsize=9.5, pad=5)
    else:
        ax.plot(x, pred, color=CORAL, lw=2.2, label="ReLU net")
        ax.set_title("(a) activation = ReLU  ->  straight line", color=CORAL, fontsize=9.5, pad=5)
    ax.set_ylim(-2.0, 2.0); ax.legend(loc="upper left", fontsize=7.5, labelcolor=INK, framealpha=0.2)
fig.subplots_adjust(top=0.84, left=0.04, right=0.99, bottom=0.08, wspace=0.12)
fig.savefig(OUT / "fig_activation_match.png", dpi=260); plt.close(); print("C ok")

# ── D. EQL example: learned formula extends forever ──
fig, ax = plt.subplots(figsize=(9.2, 3.0))
style_ax(ax)
fig.suptitle("Example. EQL learns the formula itself — 'y = sin(1.01x)' is valid everywhere",
             color=INK, fontsize=11.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
shade_train(ax, -2, 2)
ax.plot(x, true, ls="--", color=MUTED, lw=1.4, label="true sin(x)")
ax.plot(x, np.sin(1.01*x), color=LIME, lw=2.2, label="EQL:  y = sin(1.01x)")
ax.plot(x, pred, color=CORAL, lw=1.6, alpha=0.85, label="MLP: straight line")
ax.annotate("formula keeps working\nfar outside", xy=(5.0, np.sin(5.05)), xytext=(3.2, 1.55),
            color=LIME, fontsize=9, arrowprops=dict(arrowstyle="->", color=LIME, lw=1.2))
ax.set_ylim(-2.2, 2.2); ax.legend(loc="lower left", fontsize=8, labelcolor=INK, framealpha=0.2)
fig.subplots_adjust(top=0.84, left=0.05, right=0.99, bottom=0.10)
fig.savefig(OUT / "fig_eql_example.png", dpi=260); plt.close(); print("D ok")

# ── E. NALU example: error vs test number range ──
fig, ax = plt.subplots(figsize=(9.2, 3.0))
style_ax(ax)
fig.suptitle("Example. Learn a+b on numbers 0–10, test on bigger numbers",
             color=INK, fontsize=11.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
ranges = ["0–10\n(train)", "0–100", "0–1,000", "0–10,000"]
mlp_err = [0.1, 18, 240, 3100]
nalu_err = [0.1, 0.3, 0.9, 2.5]
xpos = np.arange(4)
ax.bar(xpos-0.18, mlp_err, 0.34, color=PANEL, edgecolor=CORAL, linewidth=1.6, label="MLP")
ax.bar(xpos+0.18, nalu_err, 0.34, color=PANEL, edgecolor=LIME, linewidth=1.6, label="NALU")
ax.set_yscale("log"); ax.set_xticks(xpos); ax.set_xticklabels(ranges, fontsize=8.5)
ax.set_ylabel("prediction error (log)")
for xp, v in zip(xpos, mlp_err): ax.text(xp-0.18, v*1.25, f"{v:g}", ha="center", color=CORAL, fontsize=8)
for xp, v in zip(xpos, nalu_err): ax.text(xp+0.18, v*1.25, f"{v:g}", ha="center", color=LIME, fontsize=8)
ax.legend(fontsize=8.5, labelcolor=INK, framealpha=0.2)
ax.set_title("MLP error explodes off the trained range — NALU stays flat (schematic, cf. Trask 2018 Fig.3)",
             color=MUTED, fontsize=8.5, pad=5)
fig.subplots_adjust(top=0.80, left=0.06, right=0.99, bottom=0.12)
fig.savefig(OUT / "fig_nalu_example.png", dpi=260); plt.close(); print("E ok")

# ── F. PINN time extrapolation: residual low, error explodes ──
fig, ax = plt.subplots(figsize=(9.2, 3.2))
style_ax(ax)
fig.suptitle("Example. Train on t in [0, T/2] — training residual stays low, yet future error explodes",
             color=INK, fontsize=11.5, fontweight="semibold", y=0.99, x=0.02, ha="left")
t = np.linspace(0, 1, 300)
err = np.where(t <= 0.5, 0.02 + 0.01*np.sin(9*t), 0.02*np.exp(9.5*(t-0.5)))
res = 0.015 + 0.008*np.sin(13*t)
ax.axvspan(0, 0.5, color=SHADE, alpha=0.9, zorder=0)
ax.text(0.25, 0.93, "train  t in [0, T/2]", transform=ax.get_xaxis_transform(), ha="center", color=CYAN, fontsize=8.5)
ax.semilogy(t, err, color=CORAL, lw=2.4, label="L2 solution error")
ax.semilogy(t, res, color=CYAN, lw=1.8, ls="--", label="PDE residual (what PINN optimizes)")
ax.axvline(0.5, color=AMBER, lw=1.2, ls=":")
ax.annotate("residual still low —\nmodel looks 'healthy'", xy=(0.72, 0.02), xytext=(0.52, 0.0035),
            color=CYAN, fontsize=8.5, arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.1))
ax.annotate("true error x100", xy=(0.86, 0.6), xytext=(0.6, 1.6),
            color=CORAL, fontsize=9, arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.2))
ax.set_xlabel("time t / T"); ax.set_ylim(1e-3, 5)
ax.legend(loc="upper left", fontsize=8, labelcolor=INK, framealpha=0.2)
fig.subplots_adjust(top=0.84, left=0.06, right=0.99, bottom=0.14)
fig.savefig(OUT / "fig_pinn_time_extrap.png", dpi=260); plt.close(); print("F ok")