"""S22 — extrapolation · Physics-ML (Feature / Physics loss). Publication-quality layout."""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

OUT = Path("_assets")
BG = "#0b1016"
PANEL = "#141c26"
PANEL2 = "#1a2430"
INK = "#e6edf5"
MUTED = "#8b9bb0"
CYAN = "#3dd6c6"
AMBER = "#f0a05a"
LIME = "#9ad17b"
CORAL = "#e07a5f"
NAVY = "#7aa2d4"
GRID = "#2a3545"
LINE_DIM = "#3a4a5c"

mpl.rcParams.update({
    "figure.facecolor": BG,
    "text.color": INK,
    "font.family": "sans-serif",
    "font.sans-serif": ["Apple SD Gothic Neo", "Avenir Next", "Helvetica Neue", "Arial", "DejaVu Sans"],
    "axes.titlesize": 10.5,
    "axes.labelsize": 9.5,
    "legend.fontsize": 8.5,
    "savefig.facecolor": BG,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.12,
})


def style_ax(ax, grid=True):
    ax.set_facecolor(PANEL2)
    for sp in ax.spines.values():
        sp.set_color(LINE_DIM)
        sp.set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=8.5, length=3, width=0.8)
    if grid:
        ax.grid(True, color=GRID, lw=0.55, alpha=0.65)
    ax.set_axisbelow(True)


def panel_bg(ax, color=PANEL):
    ax.add_patch(FancyBboxPatch(
        (0, 0), 1, 1, boxstyle="round,pad=0.012,rounding_size=0.015",
        facecolor=color, edgecolor=LINE_DIM, linewidth=1.0,
        transform=ax.transAxes, zorder=-1, clip_on=False,
    ))


def flow_box(ax, cx, cy, w, h, title, edge, fs=8.5):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.006,rounding_size=0.025",
        facecolor=PANEL2, edgecolor=edge, linewidth=1.4,
        transform=ax.transAxes, zorder=2,
    ))
    ax.text(cx, cy, title, transform=ax.transAxes,
            ha="center", va="center", fontsize=fs, fontweight="semibold", color=INK, zorder=3)


def arrow(ax, x0, y0, x1, y1, color=MUTED, lw=1.4):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=2, shrinkB=2))


rng = np.random.default_rng(11)

fig = plt.figure(figsize=(12.4, 7.0))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.08], hspace=0.38, wspace=0.20)

# ── (a) Extrapolation failure ─────────────────────────────────────────────
ax0 = fig.add_subplot(gs[0, :])
style_ax(ax0)
panel_bg(ax0, PANEL)

dod_all = np.linspace(5, 100, 400)
truth = 8 + 55 * np.exp(-dod_all / 32)
dod_tr = rng.uniform(48, 92, 48)
life_tr = 8 + 55 * np.exp(-dod_tr / 32) + rng.normal(0, 0.7, 48)
coef = np.polyfit(dod_tr, life_tr, 1)
ai_line = np.polyval(coef, dod_all)

dod_te = np.array([14, 20, 26])
life_te = 8 + 55 * np.exp(-dod_te / 32) + rng.normal(0, 0.8, 3)
ai_te = np.polyval(coef, dod_te)

BOUND = 45
ax0.axvspan(BOUND, 100, color=NAVY, alpha=0.08)
ax0.axvspan(5, BOUND, color=CORAL, alpha=0.04)
ax0.axvline(BOUND, color=CORAL, ls=(0, (5, 4)), lw=1.4, alpha=0.9)

ax0.plot(dod_all, truth, color=LIME, lw=2.6, label="Ground truth", zorder=3)
ax0.plot(dod_all, ai_line, color=AMBER, lw=2.4, ls=(0, (6, 3)), label="ML fit (linear extrap.)", zorder=3)
ax0.scatter(dod_tr, life_tr, s=22, c=NAVY, alpha=0.75, edgecolors="none", zorder=4, label="Train (DoD 48–92%)")
ax0.scatter(dod_te, life_te, s=85, c=LIME, marker="s", edgecolors=INK, lw=0.6, zorder=5, label="Test actual (DoD ~20%)")
ax0.scatter(dod_te, ai_te, s=85, c=AMBER, marker="X", linewidths=2.0, zorder=5, label="Test ML prediction")

# single clear gap annotation
xd = 20
yt, ya = 8 + 55 * np.exp(-xd / 32), np.polyval(coef, xd)
ax0.annotate("", xy=(xd + 1.5, ya), xytext=(xd + 1.5, yt),
             arrowprops=dict(arrowstyle="<->", color=CORAL, lw=2.0))
ax0.text(xd + 5, (yt + ya) / 2, f"Δ ≈ {yt - ya:.0f} wk", fontsize=9, color=CORAL, fontweight="bold", va="center")

ax0.text(0.03, 0.94, "In-distribution", transform=ax0.transAxes, fontsize=9, color=NAVY, fontweight="bold", va="top")
ax0.text(0.97, 0.94, "OOD / extrapolation", transform=ax0.transAxes, fontsize=9, color=CORAL,
         fontweight="bold", ha="right", va="top")

ax0.set_xlim(5, 100)
ax0.set_ylim(0, 50)
ax0.set_xlabel("DoD [%]  —  depth of discharge (방전 깊이 · 사용 강도)")
ax0.set_ylabel("Predicted lifetime [weeks]")
ax0.set_title("(a)  Extrapolation failure  ·  train high-DoD, test low-DoD  (Li et al., 2023)", pad=10, fontweight="semibold")
leg = ax0.legend(loc="center right", framealpha=0.92, facecolor=PANEL, edgecolor=LINE_DIM, labelcolor=INK)

# ── (b) Feature path ──────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[1, 0])
ax1.set_facecolor(BG)
ax1.axis("off")
panel_bg(ax1)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)

ax1.text(0.03, 0.97, "(b)  Physics-ML · Feature (입력에 물리)", transform=ax1.transAxes,
         fontsize=10.5, fontweight="semibold", color=LIME, va="top")
ax1.text(0.03, 0.90, "Li 2023  ·  충방전 곡선에서 열화 peak를 입력으로", transform=ax1.transAxes,
         fontsize=8.3, color=MUTED, va="top")

FLOW_Y = 0.78
flow_box(ax1, 0.12, FLOW_Y, 0.13, 0.09, "Q(V)", CYAN, fs=8.2)
flow_box(ax1, 0.31, FLOW_Y, 0.13, 0.09, "dQ/dV", LIME, fs=8.2)
flow_box(ax1, 0.50, FLOW_Y, 0.13, 0.09, "회귀", NAVY, fs=8.2)
flow_box(ax1, 0.69, FLOW_Y, 0.13, 0.09, "수명", AMBER, fs=8.2)
for a, b in ((0.185, 0.245), (0.375, 0.435), (0.565, 0.625)):
    arrow(ax1, a, FLOW_Y, b, FLOW_Y, LIME, 1.2)
ax1.text(0.5, 0.70, "충방전 곡선 → 미분 peak → ML 입력  (loss 아님)", transform=ax1.transAxes,
         ha="center", va="center", fontsize=7.8, color=MUTED)

ax1_l = ax1.inset_axes([0.05, 0.06, 0.42, 0.58])
ax1_r = ax1.inset_axes([0.53, 0.06, 0.42, 0.58])
for sub in (ax1_l, ax1_r):
    style_ax(sub)
cyc = np.linspace(0, 15, 60)
ax1_l.plot(cyc, 100 - 0.31 * cyc, color=NAVY, lw=2.2, label="30주")
ax1_l.plot(cyc, 100 - 0.29 * cyc, color=LIME, lw=2.2, ls=(0, (5, 3)), label="60주")
ax1_l.set_xlim(0, 15)
ax1_l.set_ylim(94.9, 100.1)
ax1_l.set_title("용량 — 수명별로 겹침", fontsize=8.5, color=AMBER, pad=5)
ax1_l.set_xlabel("초기 15% 사이클", fontsize=7.5, color=MUTED)
ax1_l.set_ylabel("용량 [%]", fontsize=7.5, color=MUTED)
ax1_l.legend(fontsize=7, loc="lower left", framealpha=0.85, facecolor=PANEL2)

v = np.linspace(3.2, 3.9, 240)
ax1_r.plot(v, 1.0 * np.exp(-((v - 3.38) ** 2) / 0.003), color=NAVY, lw=2.2, label="30주")
ax1_r.plot(v, 0.42 * np.exp(-((v - 3.38) ** 2) / 0.003), color=LIME, lw=2.2, ls=(0, (5, 3)), label="60주")
ax1_r.set_title("dQ/dV peak — 수명별로 구분", fontsize=8.5, color=LIME, pad=5)
ax1_r.set_xlabel("전압 [V]", fontsize=7.5, color=MUTED)
ax1_r.legend(fontsize=7, loc="upper right", framealpha=0.85, facecolor=PANEL2)

# ── (c) Physics loss path ─────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 1])
ax2.set_facecolor(BG)
ax2.axis("off")
panel_bg(ax2)
ax2.text(0.03, 0.96, "(c)  Physics-ML · Physics loss", transform=ax2.transAxes,
         fontsize=10.5, fontweight="semibold", color=CORAL, va="top")
ax2.text(0.03, 0.88, "방향만 → CMNN (②)  ·  법칙 형태 → loss (③)  ·  Aykol B1", transform=ax2.transAxes,
         fontsize=8.3, color=MUTED, va="top")

flow_box(ax2, 0.12, 0.72, 0.12, 0.10, "입력", CYAN, fs=8.2)
flow_box(ax2, 0.30, 0.72, 0.12, 0.10, "NN", NAVY, fs=8.2)
flow_box(ax2, 0.48, 0.72, 0.12, 0.10, "수명", AMBER, fs=8.2)
arrow(ax2, 0.18, 0.72, 0.24, 0.72)
arrow(ax2, 0.36, 0.72, 0.42, 0.72)

ax2.add_patch(FancyBboxPatch((0.62, 0.66), 0.34, 0.14, boxstyle="round,pad=0.008",
                             facecolor="#1e1418", edgecolor=CORAL, linewidth=1.5, transform=ax2.transAxes))
ax2.text(0.79, 0.735, r"$L = L_{\mathrm{data}} + \lambda\, L_{\mathrm{physics}}$", transform=ax2.transAxes,
         ha="center", fontsize=9.5, color=CORAL, fontweight="bold")
ax2.text(0.79, 0.685, "penalize constraint violation", transform=ax2.transAxes,
         ha="center", fontsize=7.5, color=MUTED)

constraints = [
    ("Arrhenius", "온도 T 올리면 열화 가속  (~ exp(-E_a/kT))", "온도-열화 관계 위반 -> penalty", CORAL, 0.50),
    ("열역학", "효율 eta <= 1  (에너지 보존)", "eta > 1 예측 -> penalty", NAVY, 0.28),
]
for tag, law, viol, col, y in constraints:
    ax2.add_patch(FancyBboxPatch((0.04, y - 0.11), 0.92, 0.17, boxstyle="round,pad=0.006",
                                 facecolor=PANEL2, edgecolor=col, linewidth=1.1, transform=ax2.transAxes))
    ax2.text(0.07, y + 0.01, tag, transform=ax2.transAxes, fontsize=8.2, fontweight="bold", color=col, va="center")
    ax2.text(0.24, y + 0.015, law, transform=ax2.transAxes, fontsize=8.0, color=INK, va="center")
    ax2.text(0.24, y - 0.055, viol, transform=ax2.transAxes, fontsize=7.6, color=MUTED, va="center")

ax2.text(0.5, 0.04, "Law shape holds OOD — not a substitute for CMNN when only direction is known",
         transform=ax2.transAxes, ha="center", fontsize=7.8, color=CORAL, style="italic")

fig.savefig(OUT / "fig_physics_loss_example.png", dpi=320)
plt.close()
print("fig_physics_loss_example ok")
