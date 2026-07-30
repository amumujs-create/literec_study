#!/usr/bin/env python3
"""Instrument-panel figures for extrapolation seminar (v4).

Aesthetic: dark analysis console — soft grid, cyan/amber traces,
panel chrome. Closer to spectrum / signal tools than default matplotlib.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.collections import LineCollection
import numpy as np
from scipy.spatial import ConvexHull

OUT = Path(__file__).resolve().parent / "_assets"
OUT.mkdir(exist_ok=True)

# ── palette (instrument console) ──
BG = "#0b1016"
PANEL = "#121821"
GRID = "#1e2a38"
INK = "#e6edf5"
MUTED = "#8b9bb0"
CYAN = "#3dd6c6"
TEAL = "#2a9d8f"
AMBER = "#f0a05a"
CORAL = "#e07a5f"
NAVY = "#7aa2d4"
LIME = "#9ad17b"
VIOLET = "#a78bfa"
LINE_DIM = "#3a4a5c"

DPI = 260


def _rc():
    mpl.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": PANEL,
            "axes.edgecolor": LINE_DIM,
            "axes.labelcolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": INK,
            "font.family": "sans-serif",
            "font.sans-serif": ["Avenir Next", "Helvetica Neue", "Arial", "DejaVu Sans"],
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.titleweight": "semibold",
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "grid.color": GRID,
            "grid.linewidth": 0.6,
            "grid.alpha": 1.0,
            "legend.frameon": False,
            "legend.fontsize": 8.5,
            "savefig.facecolor": BG,
            "savefig.edgecolor": BG,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.18,
        }
    )


def _glow_line(ax, x, y, color, lw=2.0, alpha=1.0, z=3, label=None):
    """Multi-pass soft glow like analyzer traces."""
    for w, a in ((lw * 4.5, 0.08), (lw * 2.4, 0.16), (lw * 1.2, 0.35)):
        ax.plot(x, y, color=color, lw=w, alpha=a * alpha, solid_capstyle="round", zorder=z - 1)
    ax.plot(x, y, color=color, lw=lw, alpha=alpha, solid_capstyle="round", zorder=z, label=label)


# PPT slides already have content_header — baked-in captions ghost behind titles.
SHOW_CAPTIONS = False


def _caption(fig, title: str, subtitle: str = ""):
    if not SHOW_CAPTIONS:
        return
    fig.suptitle(title, color=INK, fontsize=13, fontweight="semibold", y=0.98, x=0.02, ha="left")
    if subtitle:
        fig.text(0.02, 0.935, subtitle, color=MUTED, fontsize=9, ha="left")


def _top(with_caption: float) -> float:
    """Reserve less headroom when slide titles replace figure captions."""
    return min(0.96, with_caption + (0.0 if SHOW_CAPTIONS else 0.10))


def _style_ax(ax, grid=True):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_color(LINE_DIM)
        sp.set_linewidth(0.8)
    if grid:
        ax.grid(True, which="major", axis="both", linestyle="-", alpha=1)
        ax.set_axisbelow(True)
    ax.tick_params(length=3, pad=3)


def _save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print("wrote", path.name)


# ═══════════════════════════════════════════════════════════════
def fig_poly_extrap():
    rng = np.random.default_rng(7)
    x_all = np.linspace(0, 8, 400)
    true = 1.2 + 0.35 * np.sin(1.1 * x_all) + 0.08 * x_all
    x_tr = np.linspace(0.3, 4.7, 14)
    y_tr = 1.2 + 0.35 * np.sin(1.1 * x_tr) + 0.08 * x_tr + rng.normal(0, 0.06, x_tr.size)
    coef = np.polyfit(x_tr, y_tr, 4)
    pred = np.polyval(coef, x_all)
    cut = 5.0

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    _caption(fig, "Figure. High-order polynomial extrapolation failure",
             "Support-set fit vs out-of-support divergence")
    _style_ax(ax)
    ax.axvspan(0, cut, color=TEAL, alpha=0.10, zorder=0)
    ax.axvline(cut, color=LINE_DIM, lw=0.9, ls="--", zorder=1)
    ax.text(2.3, 9.2, "TRAIN SUPPORT", color=TEAL, fontsize=8, fontweight="bold", alpha=0.9)
    ax.text(5.35, 9.2, "EXTRAPOLATION", color=AMBER, fontsize=8, fontweight="bold", alpha=0.9)

    _glow_line(ax, x_all, true, MUTED, lw=1.4, alpha=0.85, label="true $f(x)$")
    # dashed overlay for true
    ax.plot(x_all, true, color=MUTED, lw=1.2, ls="--", alpha=0.7, zorder=3)
    mask_in = x_all <= cut
    mask_out = x_all >= cut
    _glow_line(ax, x_all[mask_in], pred[mask_in], CYAN, lw=2.2, label="poly deg-4 (in)")
    _glow_line(ax, x_all[mask_out], pred[mask_out], AMBER, lw=2.2, label="extrapolation")
    ax.scatter(x_tr, y_tr, s=28, c=INK, edgecolors=CYAN, linewidths=0.8, zorder=5, label="train")
    ax.set_xlim(0, 8)
    ax.set_ylim(-1.5, 10)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="upper left", labelcolor=INK, fontsize=8)
    fig.subplots_adjust(top=0.86, left=0.08, right=0.98, bottom=0.12)
    _save(fig, "fig_poly_extrap.png")


def fig_identifiability():
    x = np.linspace(0, 3.2, 200)
    linear = 0.55 * x + 0.4
    exp = 0.4 * (np.exp(0.55 * x) - 1) + 0.4
    # match early
    x_obs = np.linspace(0.2, 1.0, 6)
    y_obs = 0.55 * x_obs + 0.4

    fig, ax = plt.subplots(figsize=(9.0, 4.5))
    _caption(fig, "Figure. Identifiability failure under finite support",
             "Locally equivalent models diverge out of support")
    _style_ax(ax)
    ax.axvspan(0, 1.05, color=TEAL, alpha=0.10)
    ax.axvline(1.05, color=LINE_DIM, ls="--", lw=0.9)
    ax.text(0.35, 3.55, "OBSERVED", color=TEAL, fontsize=8, fontweight="bold")
    ax.text(1.9, 3.55, "UNIDENTIFIED", color=AMBER, fontsize=8, fontweight="bold")
    _glow_line(ax, x, linear, CYAN, lw=2.0, label="linear hypothesis")
    _glow_line(ax, x, exp, AMBER, lw=2.0, label="exponential hypothesis")
    ax.scatter(x_obs, y_obs, s=36, c=INK, edgecolors=CYAN, zorder=5, label="finite observations")
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 4)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$y(t)$")
    ax.legend(loc="upper left", labelcolor=INK)
    fig.subplots_adjust(top=0.86, left=0.08, right=0.98, bottom=0.12)
    _save(fig, "fig_identifiability.png")


def fig_convex_hull():
    rng = np.random.default_rng(42)
    pts = rng.normal(size=(40, 2)) * np.array([1.4, 1.0])
    hull = ConvexHull(pts)
    # exterior points
    out = np.array([[2.8, 1.6], [-2.6, -1.4], [2.2, -2.0], [-2.4, 2.1], [0.2, 2.8]])

    fig, ax = plt.subplots(figsize=(8.8, 5.0))
    _caption(fig, "Figure. Convex hull — interpolation vs extrapolation",
             "Interior of conv(X_train) ≈ interpolation; exterior ≈ extrapolation")
    _style_ax(ax)
    poly = pts[hull.vertices]
    poly = np.vstack([poly, poly[0]])
    ax.fill(poly[:, 0], poly[:, 1], color=CYAN, alpha=0.12, zorder=1)
    ax.plot(poly[:, 0], poly[:, 1], color=CYAN, lw=1.8, alpha=0.9, zorder=2, label="conv($X_{\\mathrm{train}}$)")
    ax.scatter(pts[:, 0], pts[:, 1], s=22, c=NAVY, alpha=0.85, zorder=3, label="train")
    ax.scatter(out[:, 0], out[:, 1], s=70, marker="x", c=AMBER, linewidths=2.0, zorder=4, label="OOD / extrap")
    for p in out:
        ax.annotate("extrap", p + np.array([0.12, 0.12]), color=AMBER, fontsize=7, alpha=0.85)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.legend(loc="upper right", labelcolor=INK)
    fig.subplots_adjust(top=0.86, left=0.1, right=0.98, bottom=0.12)
    _save(fig, "fig_convex_hull.png")


def fig_error_decomp():
    x = np.linspace(-3, 3, 300)
    support = np.abs(x) <= 1.2
    bias2 = 0.15 + 0.05 * (x ** 2)
    var = 0.08 + 0.55 * np.maximum(0, np.abs(x) - 1.0) ** 2
    noise = np.full_like(x, 0.12)
    total = bias2 + var + noise

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    _caption(fig, "Figure. Error decomposition under extrapolation",
             r"$\mathrm{Err} = \mathrm{Bias}^2 + \mathrm{Var} + \sigma^2$")

    ax = axes[0]
    _style_ax(ax)
    ax.axvspan(-1.2, 1.2, color=TEAL, alpha=0.10)
    ax.stackplot(x, bias2, var, noise, colors=[NAVY, AMBER, MUTED], alpha=0.55,
                 labels=[r"Bias$^2$", "Variance", r"Noise $\sigma^2$"])
    ax.plot(x, total, color=INK, lw=1.4, label="total")
    ax.set_title("(a) Stacked components", color=INK, fontsize=10, pad=6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("error")
    ax.legend(loc="upper center", ncol=2, labelcolor=INK, fontsize=8)

    ax = axes[1]
    _style_ax(ax)
    ax.axvspan(-1.2, 1.2, color=TEAL, alpha=0.10)
    _glow_line(ax, x, bias2, NAVY, lw=1.8, label=r"Bias$^2$")
    _glow_line(ax, x, var, AMBER, lw=1.8, label="Variance")
    _glow_line(ax, x, noise, MUTED, lw=1.4, label=r"$\sigma^2$")
    ax.set_title("(b) Growth outside support", color=INK, fontsize=10, pad=6)
    ax.set_xlabel("$x$")
    ax.legend(loc="upper center", labelcolor=INK, fontsize=8)
    fig.subplots_adjust(top=0.82, left=0.07, right=0.98, bottom=0.14, wspace=0.28)
    _save(fig, "fig_error_decomp.png")


def fig_richardson():
    h = np.array([1.0, 0.5, 0.25, 0.125])
    A = 2.0 + 0.8 * h ** 2 + 0.15 * h ** 3
    A_star = 2.0
    # classical extrapolations
    p = 2
    extrap = []
    for i in range(len(h) - 1):
        Ah, Ah2 = A[i], A[i + 1]
        extrap.append((h[i + 1], (2 ** p * Ah2 - Ah) / (2 ** p - 1)))

    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.8))
    _caption(fig, "Figure. Richardson extrapolation — classical vs probabilistic",
             "Point estimate -> posterior band as $h\\to 0$")

    ax = axes[0]
    _style_ax(ax)
    ax.scatter(h, A, s=40, c=CYAN, zorder=4, label="$A(h)$")
    for hx, axv in extrap:
        ax.scatter([hx], [axv], s=55, marker="D", c=AMBER, zorder=5)
    ax.axhline(A_star, color=MUTED, ls="--", lw=1)
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_title("(a) Classical", color=INK, fontsize=10)
    ax.set_xlabel("$h$")
    ax.set_ylabel("$A(h)$")

    ax = axes[1]
    _style_ax(ax)
    hs = np.logspace(0, -2.2, 80)
    mean = A_star + 0.05 * hs
    band = 0.12 + 0.35 * hs
    ax.fill_between(hs, mean - 2 * band, mean + 2 * band, color=AMBER, alpha=0.18)
    ax.fill_between(hs, mean - band, mean + band, color=CYAN, alpha=0.22)
    _glow_line(ax, hs, mean, CYAN, lw=1.8, label=r"$\mathbb{E}[A^\star]$")
    ax.axhline(A_star, color=MUTED, ls="--", lw=1)
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_title("(b) Probabilistic", color=INK, fontsize=10)
    ax.set_xlabel("$h$")

    ax = axes[2]
    _style_ax(ax, grid=False)
    steps = ["$A(h)$", "order $p$", r"$A^\star\pm\mathrm{CI}$"]
    for i, lab in enumerate(steps):
        y = 2.4 - i * 0.85
        box = FancyBboxPatch((0.35, y - 0.28), 2.3, 0.55, boxstyle="round,pad=0.02,rounding_size=0.12",
                             facecolor="#1a2430", edgecolor=CYAN if i < 2 else AMBER, linewidth=1.4)
        ax.add_patch(box)
        ax.text(1.5, y, lab, ha="center", va="center", color=INK, fontsize=11)
        if i < 2:
            ax.annotate("", xy=(1.5, y - 0.55), xytext=(1.5, y - 0.28),
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.2))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.axis("off")
    ax.set_title("(c) Workflow", color=INK, fontsize=10)

    fig.subplots_adjust(top=0.78, left=0.06, right=0.98, bottom=0.16, wspace=0.32)
    _save(fig, "fig_richardson.png")


def fig_uq():
    x = np.linspace(-3, 3, 400)
    mu = np.sin(1.2 * x) * np.exp(-0.08 * x ** 2)
    sa2 = 0.04 * np.ones_like(x)
    se2 = 0.05 + 0.55 * np.maximum(0, np.abs(x) - 1.1) ** 2
    stot = sa2 + se2

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3))
    _caption(fig, r"Figure. Uncertainty quantification — $\sigma_{tot}^2=\sigma_a^2+\sigma_e^2$",
             "Aleatoric stays flat; epistemic inflates outside support")

    ax = axes[0]
    _style_ax(ax)
    ax.axvspan(-1.1, 1.1, color=TEAL, alpha=0.12)
    ax.text(0, 1.55, "train support", color=TEAL, ha="center", fontsize=8, fontweight="bold")
    ax.fill_between(x, mu - np.sqrt(stot), mu + np.sqrt(stot), color=AMBER, alpha=0.22, label=r"$\mu\pm\sqrt{\sigma_{tot}^2}$")
    ax.fill_between(x, mu - np.sqrt(sa2), mu + np.sqrt(sa2), color=MUTED, alpha=0.35, label=r"$\sigma_a$ band")
    _glow_line(ax, x, mu, CYAN, lw=2.0, label=r"$\mu(x)$")
    ax.set_title(r"(a) Predictive bands", color=INK, fontsize=10)
    ax.set_xlabel("$x$")
    ax.legend(loc="lower center", ncol=2, labelcolor=INK, fontsize=7.5)

    ax = axes[1]
    _style_ax(ax)
    ax.axvspan(-1.1, 1.1, color=TEAL, alpha=0.12)
    _glow_line(ax, x, sa2, MUTED, lw=1.6, label=r"$\sigma_a^2$")
    _glow_line(ax, x, se2, AMBER, lw=2.0, label=r"$\sigma_e^2$")
    _glow_line(ax, x, stot, CYAN, lw=1.8, label=r"$\sigma_{tot}^2$")
    ax.set_title("(b) Variance decomposition", color=INK, fontsize=10)
    ax.set_xlabel("$x$")
    ax.set_ylabel("variance")
    ax.legend(loc="upper center", labelcolor=INK, fontsize=8)
    fig.subplots_adjust(top=0.80, left=0.07, right=0.98, bottom=0.14, wspace=0.28)
    _save(fig, "fig_uq_aleatoric_epistemic.png")


def fig_interp_extrap():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.2))
    _caption(fig, "Figure. Interpolation vs extrapolation",
             "Same model class; different query location relative to support")

    rng = np.random.default_rng(3)
    x_tr = np.sort(rng.uniform(-1.5, 1.5, 18))
    y_tr = np.sin(x_tr) + rng.normal(0, 0.08, x_tr.size)

    ax = axes[0]
    _style_ax(ax)
    xs = np.linspace(-1.5, 1.5, 200)
    _glow_line(ax, xs, np.sin(xs), CYAN, lw=2.0, label="fit")
    ax.scatter(x_tr, y_tr, s=22, c=INK, zorder=4)
    ax.scatter([0.2], [np.sin(0.2)], s=80, c=LIME, marker="*", zorder=5, label="query (in)")
    ax.set_title("Interpolation", color=CYAN, fontsize=11)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.8, 1.8)
    ax.legend(loc="lower right", labelcolor=INK, fontsize=8)

    ax = axes[1]
    _style_ax(ax)
    xs = np.linspace(-1.5, 3.2, 250)
    # bad extrapolation
    pred = np.sin(np.clip(xs, -1.5, 1.5)) + 0.35 * np.maximum(0, xs - 1.5) ** 2
    true = np.sin(xs)
    ax.axvspan(-1.5, 1.5, color=TEAL, alpha=0.10)
    ax.plot(xs, true, color=MUTED, ls="--", lw=1.2, label="true")
    _glow_line(ax, xs, pred, AMBER, lw=2.0, label="model")
    ax.scatter(x_tr, y_tr, s=22, c=INK, zorder=4)
    ax.scatter([2.6], [pred[np.argmin(np.abs(xs - 2.6))]], s=80, c=AMBER, marker="*", zorder=5, label="query (out)")
    ax.set_title("Extrapolation", color=AMBER, fontsize=11)
    ax.set_xlim(-2.2, 3.4)
    ax.set_ylim(-1.8, 2.8)
    ax.legend(loc="upper left", labelcolor=INK, fontsize=8)
    fig.subplots_adjust(top=0.80, left=0.07, right=0.98, bottom=0.14, wspace=0.28)
    _save(fig, "fig_interp_extrap.png")


def fig_fail_cases():
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.7))
    _caption(fig, "Figure. Canonical extrapolation failure modes",
             "Same failure structure appears in theory and in field deployment")

    # poly
    ax = axes[0]
    _style_ax(ax)
    x = np.linspace(0, 6, 200)
    ax.axvspan(0, 3, color=TEAL, alpha=0.1)
    y = 0.2 * (x - 1.5) ** 4 - 0.3 * (x - 1.5) ** 2 + 1
    _glow_line(ax, x[x <= 3], y[x <= 3], CYAN, lw=1.8)
    _glow_line(ax, x[x >= 3], y[x >= 3], AMBER, lw=1.8)
    ax.set_title("(a) Poly blow-up", color=INK, fontsize=10)
    ax.set_ylim(-1, 8)

    # relu affine
    ax = axes[1]
    _style_ax(ax)
    x = np.linspace(-4, 4, 300)
    # piecewise linear look
    y = np.where(x < -1, -0.4 * x - 0.2, np.where(x < 1.5, 0.6 * x, 1.1 * x - 0.75))
    true = np.tanh(x)
    ax.plot(x, true, color=MUTED, ls="--", lw=1.1, label="target")
    _glow_line(ax, x, y, CORAL, lw=1.8, label="ReLU net")
    ax.set_title("(b) Far-field affine", color=INK, fontsize=10)
    ax.legend(loc="lower right", labelcolor=INK, fontsize=7)

    # shift
    ax = axes[2]
    _style_ax(ax)
    xs = np.linspace(-3, 3, 300)
    p = np.exp(-0.5 * ((xs + 0.8) / 0.7) ** 2)
    q = np.exp(-0.5 * ((xs - 1.0) / 0.75) ** 2)
    ax.fill_between(xs, p / p.max(), color=CYAN, alpha=0.35, label="$P_{\\mathrm{train}}$")
    ax.fill_between(xs, q / q.max(), color=AMBER, alpha=0.35, label="$P_{\\mathrm{test}}$")
    ax.set_title("(c) Covariate shift", color=INK, fontsize=10)
    ax.legend(loc="upper right", labelcolor=INK, fontsize=7)
    fig.subplots_adjust(top=0.78, left=0.05, right=0.98, bottom=0.14, wspace=0.28)
    _save(fig, "fig_fail_cases.png")


def fig_ood_intuition():
    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    _caption(fig, "Figure. OOD as support mismatch",
             r"$P_{\mathrm{train}}(x)\neq P_{\mathrm{test}}(x)$ — query leaves the training measure")
    _style_ax(ax)
    xs = np.linspace(-4, 4, 400)
    ptr = np.exp(-0.5 * ((xs + 0.6) / 0.9) ** 2)
    pte = np.exp(-0.5 * ((xs - 1.4) / 0.85) ** 2)
    ax.fill_between(xs, 0, ptr / ptr.max(), color=CYAN, alpha=0.28, label=r"$P_{\mathrm{train}}$")
    ax.fill_between(xs, 0, pte / pte.max(), color=AMBER, alpha=0.28, label=r"$P_{\mathrm{test}}$")
    _glow_line(ax, xs, ptr / ptr.max(), CYAN, lw=1.6)
    _glow_line(ax, xs, pte / pte.max(), AMBER, lw=1.6)
    ax.axvline(2.2, color=CORAL, ls="--", lw=1.2)
    ax.scatter([2.2], [0.15], s=90, c=CORAL, marker="D", zorder=5)
    ax.annotate("query\n(OOD)", xy=(2.2, 0.15), xytext=(3.0, 0.55),
                color=CORAL, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=CORAL, lw=1))
    ax.set_xlabel("$x$")
    ax.set_ylabel("density (norm.)")
    ax.legend(loc="upper left", labelcolor=INK)
    ax.set_ylim(0, 1.15)
    fig.subplots_adjust(top=0.84, left=0.09, right=0.97, bottom=0.14)
    _save(fig, "fig_ood_intuition.png")


def fig_shift_types():
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.8))
    _caption(fig, "Figure. Shift taxonomy",
             "Covariate · Label · Concept — distinct failure surfaces")
    titles = ["(a) Covariate", "(b) Label", "(c) Concept"]
    for ax, title, c in zip(axes, titles, [CYAN, AMBER, VIOLET]):
        _style_ax(ax)
        rng = np.random.default_rng(hash(title) % 10_000)
        a = rng.normal(size=(60, 2)) * 0.55 + np.array([-0.7, 0])
        b = rng.normal(size=(60, 2)) * 0.55 + np.array([0.9, 0.2])
        ax.scatter(a[:, 0], a[:, 1], s=14, c=CYAN, alpha=0.7, label="train")
        ax.scatter(b[:, 0], b[:, 1], s=14, c=c, alpha=0.75, label="test")
        ax.set_title(title, color=INK, fontsize=10)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-1.8, 1.8)
        ax.legend(loc="upper right", fontsize=7, labelcolor=INK)
    fig.subplots_adjust(top=0.78, left=0.05, right=0.98, bottom=0.12, wspace=0.25)
    _save(fig, "fig_shift_types.png")


def fig_activation():
    x = np.linspace(-4, 4, 400)
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.7))
    _caption(fig, "Figure. Activation asymptotics",
             "Far-field behavior of $\\phi$ governs ReLU-style affine extrapolation")

    for ax, (name, y, c) in zip(
        axes,
        [
            ("ReLU", np.maximum(0, x), CYAN),
            ("Tanh", np.tanh(x), TEAL),
            ("Sigmoid", 1 / (1 + np.exp(-x)), AMBER),
        ],
    ):
        _style_ax(ax)
        _glow_line(ax, x, y, c, lw=2.2)
        ax.axhline(0, color=LINE_DIM, lw=0.6)
        ax.axvline(0, color=LINE_DIM, lw=0.6)
        ax.set_title(name, color=INK, fontsize=11)
        ax.set_xlim(-4, 4)
    fig.subplots_adjust(top=0.78, left=0.06, right=0.98, bottom=0.14, wspace=0.28)
    _save(fig, "fig_activation.png")


def fig_relu_affine():
    x = np.linspace(-5, 5, 500)
    # simulate deep ReLU far-field linear
    y_net = np.piecewise(x, [x < -2, (x >= -2) & (x < 1.5), x >= 1.5],
                         [lambda z: -0.3 * z - 0.4, lambda z: 0.55 * z + 0.1, lambda z: 1.25 * z - 0.95])
    y_true = np.sin(x)

    fig, ax = plt.subplots(figsize=(9.2, 4.5))
    _caption(fig, "Figure. ReLU networks become affine far from data",
             r"Xu et al.: outside activation patterns, $f(x)=Ax+b$")
    _style_ax(ax)
    ax.axvspan(-2, 1.5, color=TEAL, alpha=0.10)
    ax.text(-0.3, 4.2, "active region", color=TEAL, fontsize=8, fontweight="bold", ha="center")
    ax.text(3.2, 4.2, "affine regime", color=AMBER, fontsize=8, fontweight="bold", ha="center")
    ax.plot(x, y_true, color=MUTED, ls="--", lw=1.2, label="target $y^*$")
    _glow_line(ax, x, y_net, CORAL, lw=2.2, label="ReLU network")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f(x)$")
    ax.set_ylim(-5, 5)
    ax.legend(loc="lower right", labelcolor=INK)
    fig.subplots_adjust(top=0.84, left=0.09, right=0.97, bottom=0.14)
    _save(fig, "fig_relu_affine.png")


def fig_method_tree():
    fig, ax = plt.subplots(figsize=(11.2, 4.8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")
    _caption(fig, "Figure. Taxonomy of neural extrapolation methods",
             "Assumption -> method family -> representative work")

    root = (0.5, 0.82)
    children = [
        (0.10, 0.48, "Activation", "Xu '21", "diagnose failure", AMBER),
        (0.30, 0.48, "Equation", "EQL · NALU", "known form", LIME),
        (0.50, 0.48, "Constraint", "CMNN", "sign / monotone", CYAN),
        (0.70, 0.48, "Physics", "PINN", "known PDE", TEAL),
        (0.90, 0.48, "Operator+UQ", "DeepONet", "abstain if unsure", CORAL),
    ]

    def panel(cx, cy, w, h, face, edge, text, sub=None, ts=10):
        box = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                             boxstyle="round,pad=0.01,rounding_size=0.08",
                             facecolor=face, edgecolor=edge, linewidth=1.5, transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(cx, cy + (0.012 if sub else 0), text, transform=ax.transAxes,
                ha="center", va="center", color=INK, fontsize=ts, fontweight="semibold")
        if sub:
            ax.text(cx, cy - 0.035, sub, transform=ax.transAxes,
                    ha="center", va="center", color=MUTED, fontsize=7.5)

    panel(root[0], root[1], 0.28, 0.12, "#1a2430", CYAN, "Extrapolation Solutions", ts=12)
    for cx, cy, title, paper, idea, edge in children:
        ax.plot([root[0], cx], [root[1] - 0.07, cy + 0.07], transform=ax.transAxes,
                color=LINE_DIM, lw=1.0, zorder=0)
        panel(cx, cy, 0.16, 0.14, "#1a2430", edge, title, paper, ts=9)
        panel(cx, cy - 0.22, 0.16, 0.10, "#151c26", LINE_DIM, idea, ts=8)

    fig.subplots_adjust(top=0.86, left=0.02, right=0.98, bottom=0.04)
    _save(fig, "fig_method_tree.png")


def fig_eql():
    x = np.linspace(-2, 4, 300)
    true = np.sin(x) + 0.3 * x
    mlp = 0.6 * x + 0.2 * np.sin(2.5 * x)  # wrong outside
    # force bad extrap
    mlp = np.where(x < 1.5, true + 0.05 * np.sin(5 * x), 1.2 * x - 0.4)
    eql = true  # recovers form

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    _caption(fig, "Figure. EQL — equation discovery for extrapolation",
             "MLP fits locally; symbolic form transfers outside support")

    for ax, title, pred, c in [
        (axes[0], "(a) Before — generic MLP", mlp, AMBER),
        (axes[1], "(b) After — EQL / known form", eql, CYAN),
    ]:
        _style_ax(ax)
        ax.axvspan(-2, 1.5, color=TEAL, alpha=0.10)
        ax.plot(x, true, color=MUTED, ls="--", lw=1.2, label="true")
        _glow_line(ax, x, pred, c, lw=2.0, label="model")
        ax.set_title(title, color=INK, fontsize=10)
        ax.set_xlabel("$x$")
        ax.legend(loc="upper left", labelcolor=INK, fontsize=8)
        ax.set_ylim(-3, 5)
    fig.subplots_adjust(top=0.80, left=0.07, right=0.98, bottom=0.14, wspace=0.28)
    _save(fig, "fig_eql_before_after.png")


def fig_method_cases():
    fig, axes = plt.subplots(2, 3, figsize=(11.0, 5.8))
    _caption(fig, "Figure. Method × assumption cases",
             "Each panel: when the structural assumption holds")
    cases = [
        ("Activation match", CYAN),
        ("Arithmetic / EQL", LIME),
        ("Monotone constraint", TEAL),
        ("PINN / PDE prior", NAVY),
        ("Operator + UQ", AMBER),
        ("Mismatch -> fail", CORAL),
    ]
    rng = np.random.default_rng(1)
    for ax, (title, c) in zip(axes.ravel(), cases):
        _style_ax(ax)
        x = np.linspace(0, 4, 120)
        if "fail" in title:
            y = 0.15 * x ** 3 - 0.5 * x
            true = np.sin(x)
            ax.plot(x, true, color=MUTED, ls="--", lw=1)
            _glow_line(ax, x, y, c, lw=1.6)
        else:
            y = np.sin(0.9 * x) + 0.15 * x + rng.normal(0, 0.03, x.size)
            _glow_line(ax, x, y, c, lw=1.6)
            ax.axvspan(0, 2.2, color=TEAL, alpha=0.08)
        ax.set_title(title, color=INK, fontsize=9, pad=4)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.subplots_adjust(top=0.86, left=0.04, right=0.98, bottom=0.05, hspace=0.35, wspace=0.2)
    _save(fig, "fig_method_cases.png")


def fig_method_decision():
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")
    _caption(fig, "Figure. Decision map — which method for which assumption",
             "Start from known structure; fall back to UQ if none")

    nodes = [
        (0.5, 0.78, "Known structure?", "#1a2430", CYAN, 0.26, 0.11),
        (0.18, 0.52, "Functional form\n-> EQL / NALU", "#1a2430", LIME, 0.22, 0.14),
        (0.50, 0.52, "Sign / monotone\n-> CMNN", "#1a2430", TEAL, 0.22, 0.14),
        (0.82, 0.52, "PDE / physics\n-> PINN", "#1a2430", NAVY, 0.22, 0.14),
        (0.35, 0.22, "No structure\n-> diagnose (Xu)", "#1a2430", AMBER, 0.22, 0.14),
        (0.65, 0.22, "Need abstention\n-> DeepONet+UQ", "#1a2430", CORAL, 0.22, 0.14),
    ]
    for cx, cy, text, face, edge, w, h in nodes:
        box = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                             boxstyle="round,pad=0.012,rounding_size=0.08",
                             facecolor=face, edgecolor=edge, linewidth=1.6,
                             transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(cx, cy, text, transform=ax.transAxes, ha="center", va="center",
                color=INK, fontsize=9, fontweight="semibold")
    # arrows
    for (x0, y0), (x1, y1) in [
        ((0.5, 0.72), (0.18, 0.60)),
        ((0.5, 0.72), (0.50, 0.60)),
        ((0.5, 0.72), (0.82, 0.60)),
        ((0.5, 0.72), (0.35, 0.30)),
        ((0.5, 0.72), (0.65, 0.30)),
    ]:
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), xycoords=ax.transAxes,
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    fig.subplots_adjust(top=0.86, left=0.04, right=0.96, bottom=0.06)
    _save(fig, "fig_method_decision.png")


def fig_apex_lineage():
    fig, ax = plt.subplots(figsize=(11.0, 4.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")
    _caption(fig, "Figure. Literature -> APEX-Guard lineage",
             "Failure diagnosis -> constraints -> fair eval -> model")

    items = [
        (0.08, "Xu '21", "failure\nmechanism", AMBER),
        (0.28, "CMNN", "monotone\nconstraint", TEAL),
        (0.48, "DomainBed", "fair\nevaluation", CYAN),
        (0.68, "CA-CSS", "constraint\nlearning", LIME),
        (0.88, "APEX", "RUL\nextrapolation", CORAL),
    ]
    for i, (cx, title, sub, edge) in enumerate(items):
        box = FancyBboxPatch((cx - 0.08, 0.38), 0.16, 0.32,
                             boxstyle="round,pad=0.01,rounding_size=0.06",
                             facecolor="#1a2430", edgecolor=edge, linewidth=1.6,
                             transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(cx, 0.58, title, transform=ax.transAxes, ha="center", va="center",
                color=INK, fontsize=11, fontweight="bold")
        ax.text(cx, 0.46, sub, transform=ax.transAxes, ha="center", va="center",
                color=MUTED, fontsize=8)
        if i < len(items) - 1:
            ax.annotate("", xy=(items[i + 1][0] - 0.085, 0.54), xytext=(cx + 0.085, 0.54),
                        xycoords=ax.transAxes,
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4))
    fig.subplots_adjust(top=0.82, left=0.02, right=0.98, bottom=0.08)
    _save(fig, "fig_apex_lineage.png")


def fig_ncmapss_4d():
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 6.2))
    _caption(fig, "Figure. N-CMAPSS operating regime — 4D view",
             "Altitude · Mach · TRA · Temperature — TRA as extrapolation axis")
    rng = np.random.default_rng(5)
    names = ["Altitude", "Mach", "TRA", "Temperature"]
    colors = [CYAN, TEAL, AMBER, NAVY]
    for ax, name, c in zip(axes.ravel(), names, colors):
        _style_ax(ax)
        train = rng.normal(0.3, 0.35, 80)
        test = rng.normal(1.4, 0.4, 50) if name == "TRA" else rng.normal(0.5, 0.4, 50)
        ax.hist(train, bins=18, color=CYAN, alpha=0.45, density=True, label="train")
        ax.hist(test, bins=18, color=c, alpha=0.45, density=True, label="test")
        if name == "TRA":
            ax.axvline(1.0, color=CORAL, ls="--", lw=1.2)
            ax.text(1.05, ax.get_ylim()[1] * 0.85 if ax.get_ylim()[1] > 0 else 0.5,
                    "extrap axis", color=CORAL, fontsize=8)
        ax.set_title(name, color=INK, fontsize=10)
        ax.legend(loc="upper right", fontsize=7, labelcolor=INK)
    fig.subplots_adjust(top=0.86, left=0.08, right=0.98, bottom=0.08, hspace=0.35, wspace=0.25)
    _save(fig, "fig_ncmapss_4d.png")


def fig_strict_rmse():
    methods = ["APEX", "TabPFN", "XGB", "MLP", "RF"]
    rmse = [3.26, 3.80, 4.12, 4.55, 4.90]
    colors = [CYAN, MUTED, MUTED, MUTED, MUTED]

    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    _caption(fig, "Figure. Strict TRA extrapolation — RMSE",
             "strict_late · n=201 · seed=42  (lower is better)")
    _style_ax(ax)
    bars = ax.barh(methods[::-1], rmse[::-1], color=colors[::-1], height=0.55,
                   edgecolor=LINE_DIM, linewidth=0.6)
    for b, v in zip(bars, rmse[::-1]):
        ax.text(v + 0.06, b.get_y() + b.get_height() / 2, f"{v:.2f}",
                va="center", color=INK, fontsize=10, fontweight="semibold")
    ax.set_xlim(0, 5.8)
    ax.set_xlabel("RMSE")
    # highlight best
    ax.axvline(3.26, color=CYAN, ls=":", lw=1.0, alpha=0.7)
    fig.subplots_adjust(top=0.84, left=0.16, right=0.95, bottom=0.14)
    _save(fig, "fig_strict_rmse.png")


def fig_timeline():
    years = [1995, 2016, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    labels = [
        "Vapnik\nSLT",
        "EQL",
        "NALU",
        "IRM\nPINN",
        "DomainBed",
        "Xu\nextrapol.",
        "DeepONet\n+UQ",
        "CMNN",
        "Pfister",
    ]
    fig, ax = plt.subplots(figsize=(11.2, 3.6))
    _caption(fig, "Figure. Thirty-year arc of extrapolation research",
             "From learning theory to neural mechanisms and UQ")
    _style_ax(ax, grid=False)
    ax.set_ylim(0, 1)
    ax.set_xlim(1993, 2026)
    ax.axhline(0.45, color=LINE_DIM, lw=1.5, zorder=1)
    for i, (y, lab) in enumerate(zip(years, labels)):
        up = i % 2 == 0
        yy = 0.68 if up else 0.22
        ax.plot([y, y], [0.45, yy + (0.08 if up else -0.08)], color=MUTED, lw=0.9, zorder=2)
        ax.scatter([y], [0.45], s=36, c=CYAN, zorder=3, edgecolors=INK, linewidths=0.5)
        ax.text(y, yy, lab, ha="center", va="center", color=INK, fontsize=8,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#1a2430", edgecolor=LINE_DIM, linewidth=0.8))
    ax.set_yticks([])
    for sp in ["left", "right", "top"]:
        ax.spines[sp].set_visible(False)
    ax.set_xlabel("year")
    fig.subplots_adjust(top=0.78, left=0.04, right=0.98, bottom=0.18)
    _save(fig, "fig_timeline.png")


def fig_future():
    fig, ax = plt.subplots(figsize=(10.0, 4.8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")
    _caption(fig, "Figure. Open directions",
             "Identifiability · fair protocols · structure + UQ")
    items = [
        (0.18, 0.45, "Identifiability\nwith constraints", CYAN),
        (0.50, 0.45, "Protocol-first\nevaluation", AMBER),
        (0.82, 0.45, "Structure × UQ\nhybrids", TEAL),
    ]
    for cx, cy, text, edge in items:
        box = FancyBboxPatch((cx - 0.13, cy - 0.18), 0.26, 0.36,
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor="#1a2430", edgecolor=edge, linewidth=1.8,
                             transform=ax.transAxes)
        ax.add_patch(box)
        ax.text(cx, cy, text, transform=ax.transAxes, ha="center", va="center",
                color=INK, fontsize=11, fontweight="semibold")
    fig.subplots_adjust(top=0.82, left=0.04, right=0.96, bottom=0.08)
    _save(fig, "fig_future.png")


def main():
    _rc()
    generators = [
        fig_poly_extrap,
        fig_identifiability,
        fig_convex_hull,
        fig_error_decomp,
        fig_richardson,
        fig_uq,
        fig_interp_extrap,
        fig_fail_cases,
        fig_ood_intuition,
        fig_shift_types,
        fig_activation,
        fig_relu_affine,
        fig_method_tree,
        fig_eql,
        fig_method_cases,
        fig_method_decision,
        fig_apex_lineage,
        fig_ncmapss_4d,
        fig_strict_rmse,
        fig_timeline,
        fig_future,
    ]
    for fn in generators:
        fn()
    print(f"done: {len(generators)} figures -> {OUT}")


if __name__ == "__main__":
    main()
