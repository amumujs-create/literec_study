#!/usr/bin/env python3
"""발표용 개념 Figure — 학술/논문 스타일 (Matplotlib)."""

from __future__ import annotations

import math
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Polygon
from matplotlib.table import Table

from diagram_style import (
    C_BLUE,
    C_GRAY,
    C_GREEN,
    C_MUTED,
    C_NAVY,
    C_ORANGE,
    C_PURPLE,
    C_RED,
    C_SLATE,
    C_TEAL,
    EXTRAP_FILL,
    OUT,
    TRAIN_FILL,
    add_arrow,
    add_box,
    panel_label,
    save,
    setup_style,
    shade_regions,
    style_ax,
    suptitle,
    t,
)

# ── helpers ──────────────────────────────────────────────────────────

def _scatter_gaussian(ax, cx, cy, n, spread, seed, colors, scale=1.0):
    rng = np.random.default_rng(seed)
    xs = cx + rng.normal(0, spread, n) * scale
    ys = cy + rng.normal(0, spread * 0.85, n) * scale
    ax.scatter(xs, ys, c=colors, s=18, alpha=0.75, edgecolors="none", zorder=3)
    return xs, ys


# ── ACT 1: extrapolation foundations ─────────────────────────────────

def poly_extrapolation():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.90, bottom=0.12)

    def y_true(x):
        return 3.1 * (1.0 - np.exp(-x / 2.6))

    x_min, x_max, x_split = 0.0, 8.0, 5.0
    rng = np.random.default_rng(7)
    data_x = np.sort(rng.uniform(0.25, 4.9, 26))
    data_y = y_true(data_x) + rng.normal(0, 0.07, 26)
    coef = np.polyfit(data_x, data_y, 2)

    xs = np.linspace(x_min, x_max, 300)
    ys_true = y_true(xs)
    ys_fit = np.polyval(coef, xs)

    shade_regions(ax, x_split, (x_min, x_max), t("보간", "interp"), t("외삽", "extrap"))
    ax.scatter(data_x, data_y, c=C_BLUE, s=36, label=t("train 데이터", "train"), zorder=4)
    ax.plot(xs, ys_true, color=C_GRAY, linestyle="--", linewidth=1.5, label=t("실제 추세", "truth"), zorder=3)
    ax.plot(xs, ys_fit, color=C_RED, linewidth=2.0, label=t("2차 최소제곱 피팅", "quad fit"), zorder=3)

    xg = 6.8
    ax.annotate("", xy=(xg, ys_fit[np.argmin(np.abs(xs - xg))]), xytext=(xg, y_true(xg)),
                arrowprops=dict(arrowstyle="<->", color=C_RED, lw=1.2))
    ax.text(xg + 0.15, (y_true(xg) + np.polyval(coef, xg)) / 2, t("오차", "error"), fontsize=9, color=C_RED)

    style_ax(ax, xlabel=r"$x$", ylabel=r"$y$",
             title=t("2차 다항 회귀: train 구간 피팅 vs 외삽 발산", "Quadratic extrapolation failure"))
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.4, 3.9)
    ax.legend(loc="upper right", framealpha=1.0)
    ax.axvline(x_split, color="#555555", linewidth=0.8, linestyle=":", alpha=0.7)
    ax.text(x_split, -0.25, r"$x_{\mathrm{train}}=5$", ha="center", fontsize=9)
    save(fig, "toy_polynomial_extrapolation.png")


def convex_hull():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.72, top=0.90, bottom=0.12)

    rng = np.random.default_rng(2)
    hull_pts = np.array([[1.0, 1.2], [2.2, 3.5], [3.8, 3.8], [5.2, 3.0], [4.8, 1.5], [3.0, 1.8], [1.8, 1.4]])
    poly = Polygon(hull_pts, closed=True, facecolor="#dbeafe", edgecolor=C_BLUE, linewidth=1.5, alpha=0.5, zorder=1)
    ax.add_patch(poly)

    for _ in range(50):
        base = hull_pts[rng.integers(len(hull_pts))]
        pt = base + rng.normal(0, 0.35, 2)
        ax.scatter(*pt, c=C_BLUE, s=20, alpha=0.6, zorder=2)

    ax.scatter(hull_pts[:, 0], hull_pts[:, 1], c=C_BLUE, s=60, edgecolors="white", linewidths=0.8, zorder=4)
    ax.scatter([3.4], [2.0], c=C_GREEN, s=120, marker="+", linewidths=2.5, label=t("hull 안 (보간)", "in hull"), zorder=5)
    ax.scatter([6.2], [3.8], c=C_RED, s=120, marker="x", linewidths=2.5, label=t("hull 밖 (외삽)", "out hull"), zorder=5)

    style_ax(ax, xlabel=r"$x_1$", ylabel=r"$x_2$", title=t("2D 특징 공간의 Convex Hull", "Convex hull"))
    ax.set_xlim(0.5, 7.0)
    ax.set_ylim(0.8, 4.5)
    ax.legend(loc="upper right")
    ax.text(0.72, 0.55, t("hull 안: 보간\nhull 밖: 추가 가정 필요", "interp vs extrap"),
            transform=fig.transFigure, fontsize=10, va="center",
            bbox=dict(boxstyle="square,pad=0.4", facecolor="white", edgecolor="#cccccc", linewidth=0.8))
    save(fig, "toy_convex_hull_2d.png")


def uq_aleatoric_epistemic():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.88, bottom=0.12, wspace=0.30)

    def draw_panel(ax, epistemic: bool, label: str, title: str):
        x = np.linspace(0, 10, 200)
        y_mid = 2.0 + 0.8 * np.sin(x * 0.7)
        split = 5.2
        if epistemic:
            sigma = np.where(x <= split, 0.15, 0.15 + 0.9 * ((x - split) / (10 - split)) ** 1.1)
        else:
            sigma = np.full_like(x, 0.35)

        shade_regions(ax, split, (0, 10), t("hull 안", "in hull"), t("hull 밖", "out hull"))
        ax.fill_between(x, y_mid - sigma, y_mid + sigma, color=C_RED if epistemic else C_BLUE, alpha=0.2, zorder=2)
        ax.plot(x, y_mid, color=C_SLATE, linewidth=1.5, zorder=3)

        rng = np.random.default_rng(11 if epistemic else 12)
        if epistemic:
            xd = rng.uniform(0.3, split - 0.3, 40)
        else:
            xd = rng.uniform(0.3, 9.7, 50)
        ax.scatter(xd, y_mid[np.searchsorted(x, xd)] + rng.normal(0, 0.2, len(xd)),
                   c=C_RED if epistemic else C_BLUE, s=16, alpha=0.7, zorder=4)

        style_ax(ax, xlabel=r"$x$", ylabel=r"$\hat{y}$", title=title)
        panel_label(ax, label)
        ax.set_xlim(0, 10)

    draw_panel(axes[0], False, "(a)", t("우연적 불확실성 (Aleatoric)", "Aleatoric"))
    draw_panel(axes[1], True, "(b)", t("인식적 불확실성 (Epistemic)", "Epistemic"))
    suptitle(fig, t("불확실성 분해", "Uncertainty decomposition"),
             t("우연적: σ 고정 · 인식적: hull 밖에서 σ 급증", ""))
    save(fig, "uq_aleatoric_epistemic.png")


# ── ACT 2: OOD ───────────────────────────────────────────────────────

def ood_shift_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.88, bottom=0.14)

    boundary = lambda x, y: y > 0.52 * x + 0.3
    rng = np.random.default_rng(42)
    tr_x, tr_y = rng.normal(1.8, 0.7, 75), rng.normal(1.5, 0.6, 75)
    te_x, te_y = rng.normal(4.5, 0.7, 75), rng.normal(3.8, 0.6, 75)

    c_tr = [C_BLUE if boundary(x, y) else C_ORANGE for x, y in zip(tr_x, tr_y)]
    c_te = [C_BLUE if boundary(x, y) else C_ORANGE for x, y in zip(te_x, te_y)]

    ax.scatter(tr_x, tr_y, c=c_tr, s=22, alpha=0.7, label=t("train", "train"), zorder=3)
    ax.scatter(te_x, te_y, c=c_te, s=22, alpha=0.7, marker="^", label=t("test (OOD)", "test"), zorder=3)
    ax.plot([0, 6], [0.3, 3.42], color=C_GREEN, linewidth=1.5, linestyle="--", label=r"$P(Y|X)$ 동일")

    for cx, cy, lab in [(1.8, 1.5, r"$P_{\mathrm{train}}(X)$"), (4.5, 3.8, r"$P_{\mathrm{test}}(X)$")]:
        ax.add_patch(Ellipse((cx, cy), 2.2, 1.8, fill=False, edgecolor=C_GRAY, linewidth=1.0, linestyle=":"))

    style_ax(ax, xlabel=r"$X$", ylabel=r"$Y$", title=t("Covariate shift: $P(X)$ 변화, $P(Y|X)$ 유지", ""))
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.5, 5.5)
    ax.legend(loc="lower right", fontsize=9)
    save(fig, "ood_shift_diagram.png")


def distribution_shift_types():
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.88, bottom=0.08, wspace=0.28, hspace=0.38)
    rng = np.random.default_rng(0)

    # (a) covariate
    ax = axes[0, 0]
    for cx, cy, col, mk in [(1.5, 2.0, C_BLUE, "o"), (4.0, 3.5, C_ORANGE, "^")]:
        xs, ys = rng.normal(cx, 0.6, 40), rng.normal(cy, 0.5, 40)
        ax.scatter(xs, ys, c=col, s=16, alpha=0.7, marker=mk)
    ax.plot([0, 5.5], [0.5, 3.5], "k--", lw=1.0, alpha=0.5)
    style_ax(ax, title=t("① Covariate shift", ""))
    panel_label(ax, "(a)")
    ax.set_xlim(0, 5.5); ax.set_ylim(0, 5)

    # (b) label
    ax = axes[0, 1]
    for ratio, off in [(0.75, 0), (0.35, 3)]:
        n0, n1 = int(40 * ratio), 40 - int(40 * ratio)
        ax.scatter(rng.uniform(0, 2.5, n0) + off, rng.uniform(0, 4, n0), c=C_BLUE, s=16, alpha=0.7)
        ax.scatter(rng.uniform(0, 2.5, n1) + off, rng.uniform(0, 4, n1), c=C_ORANGE, s=16, alpha=0.7)
    ax.axvline(2.75, color=C_GRAY, lw=0.8, ls=":")
    ax.text(1.3, 4.3, "train", ha="center", fontsize=9)
    ax.text(4.0, 4.3, "test", ha="center", fontsize=9)
    style_ax(ax, title=t("② Label shift", ""))
    panel_label(ax, "(b)")

    # (c) concept
    ax = axes[1, 0]
    xs, ys = rng.uniform(0, 5, 50), rng.uniform(0, 5, 50)
    colors = [C_BLUE if x < 2.0 + y * 0.3 else C_ORANGE for x, y in zip(xs, ys)]
    ax.scatter(xs, ys, c=colors, s=16, alpha=0.7)
    ax.plot([0, 5], [0.5, 2.0], color=C_GREEN, lw=1.5, label="train rule")
    ax.plot([0, 5], [5, 0], color=C_RED, lw=1.5, label="test rule")
    style_ax(ax, title=t("③ Concept shift", ""))
    panel_label(ax, "(c)")
    ax.legend(fontsize=8)

    # (d) domain
    ax = axes[1, 1]
    ax.hist(rng.normal(1.5, 0.4, 200), bins=20, range=(0, 6), alpha=0.6, color=C_PURPLE, label="lab")
    ax.hist(rng.normal(3.5, 0.6, 200), bins=20, range=(0, 6), alpha=0.6, color=C_ORANGE, label="field")
    style_ax(ax, title=t("④ Domain shift", ""))
    panel_label(ax, "(d)")
    ax.legend(fontsize=8)

    suptitle(fig, t("분포 이동 4유형", "Distribution shift types"),
             t("외삽과 가장 직접 연결: ① Covariate shift", ""))
    save(fig, "distribution_shift_types.png")


def erm_vs_ood_objective():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.85, bottom=0.15, wspace=0.30)

    risks = [0.25, 0.30, 0.85]
    names = [t("공장 A", "A"), t("공장 B", "B"), t("공장 C", "C")]
    x = np.arange(3)
    width = 0.55

    ax = axes[0]
    bars = ax.bar(x, risks, width, color=[C_BLUE, C_BLUE, C_GRAY], edgecolor="#333333", linewidth=0.6)
    ax.axhline(np.mean(risks[:2]), color=C_GREEN, linewidth=1.2, linestyle="--",
               label=t("ERM 목표: train 평균", "ERM avg"))
    style_ax(ax, ylabel=t("위험 (오차)", "Risk"), title=t("ERM: train 평균 최소화", "ERM"))
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylim(0, 1.0)
    panel_label(ax, "(a)")
    ax.legend(fontsize=9)

    ax = axes[1]
    colors = [C_BLUE, C_BLUE, C_RED]
    ax.bar(x, risks, width, color=colors, edgecolor="#333333", linewidth=0.6)
    ax.annotate(t("최악 환경", "worst"), xy=(2, 0.85), xytext=(1.5, 0.95),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.0), fontsize=9, color=C_RED)
    style_ax(ax, ylabel=t("위험 (오차)", "Risk"), title=t("OOD: 최악 환경(공장 C) 최소화", "OOD"))
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylim(0, 1.0)
    panel_label(ax, "(b)")

    suptitle(fig, t("ERM vs OOD 목표", ""))
    save(fig, "erm_vs_ood_objective.png")


def erm_baseline_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    ax.axis("off")
    fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)

    ax.text(0.5, 0.95, "ERM = Empirical Risk Minimization", ha="center", fontsize=14, fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.88, r"$\min_\theta \frac{1}{N}\sum_{i=1}^{N} \ell(y_i, f_\theta(x_i))$",
            ha="center", fontsize=13, transform=ax.transAxes)

    rows = [
        [t("항목", ""), t("ERM", ""), t("Baseline 요구", "")],
        [t("정의", ""), t("train N개 샘플 평균 손실 최소화", ""), t("모든 OOD 논문의 비교 기준선", "")],
        [t("함정", ""), t("spurious feature 암기 → OOD 급락", ""), t("ERM 결과 반드시 표에 포함", "")],
        [t("공정 비교", ""), t("기본 SGD/Adam 학습", ""), t("HP·모델 크기·탐색 횟수 동일", "")],
    ]
    table = ax.table(cellText=rows[1:], colLabels=rows[0], loc="center",
                     cellLoc="left", bbox=[0.02, 0.25, 0.96, 0.55])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)
    for (row, col), cell in table.get_celld().items():
        cell.set_linewidth(0.6)
        if row == 0:
            cell.set_facecolor("#f0f0f0")
            cell.set_text_props(fontweight="bold")

    ax.text(0.5, 0.12, t("DomainBed (Gulrajani 2020): 공정 비교 시 ERM ≥ IRM인 경우 다수 → baseline 생략 불가",
                          ""), ha="center", fontsize=10, color=C_MUTED, transform=ax.transAxes)
    save(fig, "erm_baseline_diagram.png")


# ── ACT 3: OOD algorithms ───────────────────────────────────────────

def irm_colored_mnist_diagram():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.06, right=0.96, top=0.82, bottom=0.18, wspace=0.35)

    for ax, env, digits, colors, label in [
        (axes[0], "train", [("7", C_GREEN), ("3", C_RED)], t("초록→1, 빨강→0", ""), "(a)"),
        (axes[1], "test", [("7", C_RED), ("3", C_GREEN)], t("색 반전 (OOD)", ""), "(b)"),
    ]:
        ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
        panel_label(ax, label)
        ax.set_title(f"{env}: {t('Colored MNIST', '')}", fontsize=11)
        for i, (dig, col) in enumerate(digits):
            rect = plt.Rectangle((1.5 + i * 4, 2), 2, 2, facecolor=col, edgecolor="#333333", linewidth=0.8, alpha=0.7)
            ax.add_patch(rect)
            ax.text(2.5 + i * 4, 3.0, dig, ha="center", va="center", fontsize=20, fontweight="bold", color="white")

    fig.text(0.5, 0.06, t("ERM: 색 힌트 학습 → test 실패  |  IRM: 숫자 모양(불변 feature) 학습",
                            ""), ha="center", fontsize=10)
    suptitle(fig, "IRM — Colored MNIST")
    save(fig, "irm_colored_mnist_diagram.png")


def irm_results_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.10, right=0.96, top=0.88, bottom=0.18)

    x = np.arange(2)
    width = 0.35
    erm = [87, 25]; irm = [73, 71]
    labels = [t("Train", ""), t("Test (OOD)", "")]

    ax.bar(x - width / 2, erm, width, label="ERM", color=C_BLUE, edgecolor="#333333", linewidth=0.6)
    ax.bar(x + width / 2, irm, width, label="IRM", color=C_GREEN, edgecolor="#333333", linewidth=0.6)
    for i, (e, r) in enumerate(zip(erm, irm)):
        ax.text(i - width / 2, e + 2, f"{e}%", ha="center", fontsize=9)
        ax.text(i + width / 2, r + 2, f"{r}%", ha="center", fontsize=9)

    style_ax(ax, ylabel=t("정확도 (%)", "Accuracy (%)"),
             title=t("Colored MNIST: ERM vs IRM", ""))
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylim(0, 100)
    ax.legend()
    save(fig, "irm_results_diagram.png")


def groupdro_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.10, right=0.96, top=0.88, bottom=0.18)

    groups = [t("물새+물", ""), t("물새+땅", ""), t("육새+물", ""), t("육새+땅", "")]
    acc = [95, 20, 60, 90]
    colors = [C_BLUE, C_RED, C_TEAL, C_GREEN]
    x = np.arange(4)

    bars = ax.bar(x, acc, 0.6, color=colors, edgecolor="#333333", linewidth=0.6)
    bars[1].set_edgecolor(C_RED)
    bars[1].set_linewidth(2.0)
    ax.annotate(t("worst group $g^*$", ""), xy=(1, 20), xytext=(1.8, 45),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=1.0), fontsize=9, color=C_RED)

    style_ax(ax, ylabel=t("정확도 (%)", ""), title=t("GroupDRO: worst-group accuracy", ""))
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=9)
    ax.set_ylim(0, 100)
    ax.axhline(np.mean(acc), color=C_GRAY, linestyle="--", linewidth=1.0, label="ERM (mean)")
    ax.legend(fontsize=9)
    save(fig, "groupdro_diagram.png")


def domainbed_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.10, right=0.96, top=0.88, bottom=0.22)

    datasets = ["Rotated\nMNIST", "PACS", "VLCS", "Office-\nHome"]
    erm = [98.0, 85.7, 77.4, 67.5]
    ood = [97.2, 84.5, 75.9, 65.5]
    x = np.arange(4)
    width = 0.35

    ax.bar(x - width / 2, erm, width, label="ERM", color=C_BLUE, edgecolor="#333333", linewidth=0.6)
    ax.bar(x + width / 2, ood, width, label="OOD SOTA", color=C_ORANGE, edgecolor="#333333", linewidth=0.6)

    style_ax(ax, ylabel=t("OOD test accuracy (%)", ""), title="DomainBed (Gulrajani et al., 2020)")
    ax.set_xticks(x); ax.set_xticklabels(datasets, fontsize=9)
    ax.set_ylim(60, 100)
    ax.legend()
    save(fig, "domainbed_diagram.png")


# ── ACT 4: NN extrapolation ───────────────────────────────────────────

def _relu_mlp_curve(t):
    if t <= 0.55:
        return 0.35 + 0.55 * math.sin(2.2 * math.pi * t) + 0.15 * t
    y_end = 0.35 + 0.55 * math.sin(2.2 * math.pi * 0.55) + 0.15 * 0.55
    return y_end + 0.08 * (t - 0.55)


def relu_mlp_extrapolation_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.88, bottom=0.14)

    ts = np.linspace(0, 1, 200)
    y_true = 0.35 + 0.55 * np.sin(2.2 * np.pi * ts) + 0.15 * ts
    y_mlp = np.array([_relu_mlp_curve(t) for t in ts])

    shade_regions(ax, 0.55, (0, 1), t("train", ""), t("extrapolation", ""))
    ax.plot(ts, y_true, color=C_GRAY, linestyle="--", linewidth=1.5, label=t("비선형 타깃", "target"))
    ax.plot(ts[ts <= 0.55], y_mlp[ts <= 0.55], color=C_BLUE, linewidth=2.0, label="ReLU MLP (train)")
    ax.plot(ts[ts >= 0.55], y_mlp[ts >= 0.55], color=C_RED, linewidth=2.0, label=t("ReLU MLP (extrap → affine)", ""))

    rng = np.random.default_rng(3)
    td = rng.uniform(0.05, 0.52, 28)
    ax.scatter(td, 0.35 + 0.55 * np.sin(2.2 * np.pi * td) + 0.15 * td + rng.normal(0, 0.03, 28),
               c=C_BLUE, s=20, alpha=0.7, zorder=4)

    style_ax(ax, xlabel=r"$x$", ylabel=r"$f(x)$", title=t("ReLU MLP 외삽 실패 (Xu et al., 2021)", ""))
    ax.legend(fontsize=9)
    save(fig, "relu_mlp_extrapolation_diagram.png")


def activation_extrapolation_diagram():
    fig, axes = plt.subplots(1, 3, figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.06, right=0.97, top=0.85, bottom=0.14, wspace=0.32)

    fns = [
        ("ReLU", lambda t: max(0, t - 0.3) * 0.9 + 0.2),
        ("Tanh", lambda t: 0.5 + 0.45 * math.tanh(3 * (t - 0.5))),
        ("Sin", lambda t: 0.5 + 0.35 * math.sin(4 * math.pi * t)),
    ]
    ts = np.linspace(0, 1, 100)
    for ax, (name, fn), lab in zip(axes, fns, ["(a)", "(b)", "(c)"]):
        ys = [fn(t) for t in ts]
        shade_regions(ax, 0.55, (0, 1))
        ax.plot(ts, ys, color=C_SLATE, linewidth=2.0)
        style_ax(ax, xlabel=r"$x$", ylabel=r"$f(x)$", title=name)
        panel_label(ax, lab)

    suptitle(fig, t("활성화 함수 = 암묵적 extrapolation prior", "Activation = extrap prior"),
             "Xu et al. (2021)")
    save(fig, "activation_extrapolation_diagram.png")


def eql_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.05)

    ax.set_title("EQL — Equation Learner (Martius & Lampert, 2016)", fontsize=12, pad=12)
    nodes = {
        "x1": (1, 5), "x2": (1, 3.5), "x3": (1, 2),
        "sin": (3.5, 5.5), "mul": (3.5, 3), "add": (6, 4.2), "y": (9, 4.2),
    }
    for name, (x, y) in nodes.items():
        fc = C_GREEN if name == "y" else (C_TEAL if name in ("sin", "mul", "add") else C_BLUE)
        add_box(ax, (x - 0.5, y - 0.35), 1.0, 0.7, name, fc=fc, ec="#333333", fontsize=10)

    edges = [("x1", "sin"), ("x2", "mul"), ("x3", "mul"), ("sin", "add"), ("mul", "add"), ("add", "y")]
    for a, b in edges:
        x1, y1 = nodes[a]; x2, y2 = nodes[b]
        add_arrow(ax, (x1 + 0.5, y1), (x2 - 0.5, y2))

    ax.text(6, 0.8, r"$y = \sin(x_1) + x_2 \cdot x_3$  —  해석 가능한 수식 구조", ha="center", fontsize=11)
    save(fig, "eql_diagram.png")


def nalu_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.10, right=0.96, top=0.88, bottom=0.18)
    x = np.arange(2)
    w = 0.3
    ax.bar(x - w, [95, 35], w, label="MLP", color=C_RED, edgecolor="#333333", linewidth=0.6)
    ax.bar(x + w, [98, 92], w, label="NALU", color=C_GREEN, edgecolor="#333333", linewidth=0.6)
    style_ax(ax, ylabel=t("정확도 (%)", ""), title=t("NALU vs MLP — counting $a+b$ (Trask et al., 2018)", ""))
    ax.set_xticks(x)
    ax.set_xticklabels([t("train (1–10)", ""), t("extrap (11–50)", "")])
    ax.set_ylim(0, 105)
    ax.legend()
    save(fig, "nalu_diagram.png")


def pinn_overview_diagram():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.82, bottom=0.18, wspace=0.30)

    ax = axes[0]
    rng = np.random.default_rng(9)
    xd = rng.uniform(0, 5, 20)
    yd = 0.3 + 0.4 * np.sin(xd * 0.8) + rng.normal(0, 0.05, 20)
    xs = np.linspace(0, 5, 100)
    ax.scatter(xd, yd, c=C_BLUE, s=25, label=r"$L_{\mathrm{data}}$", zorder=3)
    ax.plot(xs, 0.3 + 0.4 * np.sin(xs * 0.8), color=C_GREEN, linewidth=1.5)
    style_ax(ax, xlabel=r"$x$", ylabel=r"$u$", title=r"$L_{\mathrm{data}}$: data fit")
    panel_label(ax, "(a)")

    ax = axes[1]
    ax.text(0.5, 0.6, r"$\mathcal{L}_{\mathrm{physics}} = \left\|\frac{\partial u}{\partial t} + \mathcal{N}[u]\right\|^2$",
            ha="center", va="center", fontsize=14, transform=ax.transAxes)
    ax.text(0.5, 0.35, t("PDE residual at collocation points", ""), ha="center", fontsize=10, color=C_MUTED, transform=ax.transAxes)
    ax.axis("off")
    panel_label(ax, "(b)")
    ax.set_title(r"$L_{\mathrm{physics}}$: PDE constraint", fontsize=11)

    fig.text(0.5, 0.06, r"$L_{\mathrm{total}} = L_{\mathrm{data}} + \lambda \cdot L_{\mathrm{physics}}$  (Raissi et al., 2019)",
             ha="center", fontsize=12)
    suptitle(fig, "PINN — Physics-Informed Neural Network")
    save(fig, "pinn_overview_diagram.png")


def pinn_failure_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.88, bottom=0.14)

    ts = np.linspace(0, 1, 200)
    y_true = 0.4 + 0.5 * np.exp(-ts) * np.cos(4 * ts)
    y_pinn = np.where(ts <= 0.5, y_true,
                      0.4 + 0.5 * np.exp(-0.5) * np.cos(2) + 0.6 * (ts - 0.5))

    shade_regions(ax, 0.5, (0, 1), t("train", ""), t("extrapolation", ""))
    ax.plot(ts, y_true, color=C_GRAY, linestyle="--", linewidth=1.5, label=t("ground truth", ""))
    ax.plot(ts[ts <= 0.5], y_pinn[ts <= 0.5], color=C_BLUE, linewidth=2.0, label="PINN (train)")
    ax.plot(ts[ts >= 0.5], y_pinn[ts >= 0.5], color=C_RED, linewidth=2.0, label=t("PINN (extrap)", ""))

    style_ax(ax, xlabel=r"$t$", ylabel=r"$u(t)$", title=t("PINN 외삽 실패 (Fesser et al., 2023)", ""))
    ax.legend(fontsize=9)
    save(fig, "pinn_failure_diagram.png")


def monotonic_nn_diagram():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.08, right=0.96, top=0.88, bottom=0.14)

    ts = np.linspace(0, 1, 80)
    y_mono = 0.15 + ts ** 0.82 * 0.75
    y_mlp = ts * 0.55 + 0.12 * np.sin(ts * 14)

    shade_regions(ax, 0.55, (0, 1))
    ax.plot(ts, y_mono, color=C_GREEN, linewidth=2.0, label=t("Monotonic NN", ""))
    ax.plot(ts, y_mlp, color=C_RED, linewidth=1.5, linestyle="--", label=t("일반 MLP", ""))

    rng = np.random.default_rng(4)
    td = rng.uniform(0.05, 0.52, 22)
    ax.scatter(td, 0.15 + td ** 0.82 * 0.75 + rng.normal(0, 0.02, 22), c=C_BLUE, s=20, alpha=0.7)

    style_ax(ax, xlabel=t("SOC", ""), ylabel=t("OCV", ""), title=t("Monotonic NN: SOC↑ → OCV↑", ""))
    ax.legend(fontsize=9)
    save(fig, "monotonic_nn_diagram.png")


# ── ACT 5: N-CMAPSS ──────────────────────────────────────────────────

def ncmapss_extrapolation():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.06, right=0.96, top=0.88, bottom=0.20)
    ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")

    add_box(ax, (0.5, 1.2), 3.5, 1.2, t("훈련\n(저 TRA)", ""), fc=TRAIN_FILL)
    add_box(ax, (5.0, 1.2), 4.0, 1.2, t("테스트 holdout\n(고 TRA)", ""), fc=EXTRAP_FILL)
    add_arrow(ax, (4.0, 1.8), (5.0, 1.8))

    ax.text(5, 0.5, t("① TRA shift  ② unit holdout  ③ strict_late", ""), ha="center", fontsize=10)
    ax.set_title(t("N-CMAPSS 외삽 실험 설계", "N-CMAPSS extrapolation"), fontsize=12, pad=10)
    save(fig, "ncmapss_extrapolation.png")


def apex_guard_pipeline():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    ax.set_xlim(0, 12); ax.set_ylim(0, 4); ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.10)

    layers = [
        ("L1", "strict_late", t("순수 외삽 측정", "")),
        ("L2", "CA-CSS", "TRA(−), mono"),
        ("L3", "isotonic", t("unit별 회귀", "")),
    ]
    for i, (tag, name, desc) in enumerate(layers):
        x = 0.5 + i * 3.8
        add_box(ax, (x, 1.5), 3.0, 1.5, f"{tag}\n{name}\n{desc}", fontsize=9)
        if i < 2:
            add_arrow(ax, (x + 3.0, 2.25), (x + 3.8, 2.25))

    ax.set_title("APEX-Guard Pipeline", fontsize=12, pad=10)
    ax.text(6, 0.5, t("이중 인코더: Health(TRA=0) + Load(TRA, cycle)", ""), ha="center", fontsize=10)
    save(fig, "apex_guard_pipeline.png")


def ncmapss_results_chart():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    fig.subplots_adjust(left=0.10, right=0.96, top=0.88, bottom=0.18)

    models = ["APEX-Guard", "TabPFN", "Transformer", "TCN"]
    rmse = [3.26, 3.80, 7.31, 14.09]
    colors = [C_GREEN, C_BLUE, C_ORANGE, C_RED]
    x = np.arange(4)

    ax.bar(x, rmse, 0.55, color=colors, edgecolor="#333333", linewidth=0.6)
    for i, r in enumerate(rmse):
        ax.text(i, r + 0.3, f"{r}", ha="center", fontsize=9)

    style_ax(ax, ylabel="RMSE", title=t("strict_late 결과 (n=201, 고 TRA OOD)", ""))
    ax.set_xticks(x); ax.set_xticklabels(models, fontsize=9)
    save(fig, "ncmapss_results_chart.png")


# ── misc ─────────────────────────────────────────────────────────────

def storyline_roadmap():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.02)

    steps = [
        ("1", t("외삽이란?", ""), t("보간 · Hull · UQ", "")),
        ("2", t("OOD란?", ""), t("분포 이동 · 환경", "")),
        ("3", t("OOD 알고리즘", ""), "ERM · IRM · GroupDRO"),
        ("4", t("NN 외삽", ""), t("ReLU · 구조 제약", "")),
        ("5", "N-CMAPSS", "APEX-Guard"),
    ]
    for i, (num, title, desc) in enumerate(steps):
        y = 6.0 - i * 1.2
        add_box(ax, (0.5, y - 0.4), 0.6, 0.8, num, fc="#f0f0f0", fontsize=11)
        add_box(ax, (1.3, y - 0.4), 8.0, 0.8, f"{title}  —  {desc}", fc="white", fontsize=10)
        if i < 4:
            ax.plot([0.8, 0.8], [y - 0.5, y - 0.8], color=C_GRAY, linewidth=0.8)

    ax.set_title(t("발표 스토리라인", "Talk roadmap"), fontsize=12, pad=8)
    save(fig, "storyline_roadmap.png")


def further_reading_visual():
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150)
    ax.axis("off")
    fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)

    papers = [
        ["중요도", "논문", "주제"],
        ["★★★", "Xu 2021", t("신경망 외삽", "")],
        ["★★★", "Gulrajani 2020", "DomainBed"],
        ["★★★", "Liu 2023", "OOD 서베이"],
        ["★★☆", "Arjovsky 2019", "IRM"],
        ["★★☆", "Pfister 2024", t("외삽 bounds", "")],
        ["★★☆", "Fesser 2023", t("PINN 실패", "")],
    ]
    table = ax.table(cellText=papers[1:], colLabels=papers[0], loc="center",
                     cellLoc="left", bbox=[0.05, 0.15, 0.9, 0.75])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.6)
    for (row, col), cell in table.get_celld().items():
        cell.set_linewidth(0.6)
        if row == 0:
            cell.set_facecolor("#f0f0f0")
            cell.set_text_props(fontweight="bold")

    ax.set_title(t("필독 논문", "Must-read papers"), fontsize=12, pad=20)
    save(fig, "further_reading_visual.png")


def main():
    setup_style()
    fns = [
        distribution_shift_types, poly_extrapolation, convex_hull, ood_shift_diagram,
        storyline_roadmap, uq_aleatoric_epistemic, erm_vs_ood_objective, erm_baseline_diagram,
        irm_colored_mnist_diagram, irm_results_diagram, groupdro_diagram, domainbed_diagram,
        relu_mlp_extrapolation_diagram, activation_extrapolation_diagram, eql_diagram, nalu_diagram,
        monotonic_nn_diagram, pinn_overview_diagram, pinn_failure_diagram,
        ncmapss_extrapolation, apex_guard_pipeline, further_reading_visual,
        ncmapss_results_chart,
    ]
    for fn in fns:
        fn()
        print(f"  ✓ {fn.__name__}")
    print(f"\nSaved {len(fns)} figures → {OUT}")


if __name__ == "__main__":
    main()
