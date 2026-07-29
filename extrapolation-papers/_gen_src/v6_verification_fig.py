#!/usr/bin/env python3
"""S25 검증 장 — 이해하기 쉬운 흐름도 (주장 → 함정 → 확인 4)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "_assets"
OUT.mkdir(exist_ok=True)

BG = "#0b1016"
PANEL = "#141b24"
LINE = "#2c3848"
INK = "#ecf1f7"
MUTED = "#8b9cb3"
TEAL = "#3dd6c6"
CORAL = "#e89a5c"
AMBER = "#f0a05a"
SOFT = "#b8c4d0"


def _box(ax, xy, wh, text, sub="", fc=PANEL, ec=TEAL, title_color=TEAL, fs=11):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        facecolor=fc, edgecolor=ec, linewidth=1.4,
        transform=ax.transAxes,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h - 0.045, text, transform=ax.transAxes,
            ha="center", va="top", color=title_color, fontsize=fs, fontweight="bold")
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.02, sub, transform=ax.transAxes,
                ha="center", va="center", color=SOFT, fontsize=9, linespacing=1.35)


def _arrow(ax, p0, p1, color=TEAL):
    arr = FancyArrowPatch(
        p0, p1, transform=ax.transAxes,
        arrowstyle="-|>", mutation_scale=14, lw=1.6, color=color,
        connectionstyle="arc3,rad=0",
    )
    ax.add_patch(arr)


def _mini_hull(ax, left=0.08, bottom=0.12, size=0.22):
    """작은 hull 안/밖 스케치."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    pts = np.array([[0.15, 0.2], [0.55, 0.15], [0.7, 0.55], [0.25, 0.65]])
    hull = Polygon(pts, closed=True, facecolor=TEAL, alpha=0.18, edgecolor=TEAL, lw=1.2)
    ax.add_patch(hull)
    ax.scatter([0.35, 0.45, 0.5, 0.3], [0.35, 0.45, 0.3, 0.5], s=28, c=TEAL, zorder=3)
    ax.scatter([0.88, 0.92], [0.75, 0.25], s=55, c=CORAL, marker="*", zorder=4)
    ax.text(0.42, 0.08, "훈련 hull", ha="center", color=MUTED, fontsize=7)
    ax.text(0.9, 0.82, "test\n(밖)", ha="center", color=CORAL, fontsize=7)


def main() -> None:
    plt.rcParams.update({
        "figure.facecolor": BG,
        "font.family": "Apple SD Gothic Neo",
        "font.sans-serif": ["Apple SD Gothic Neo", "Arial Unicode MS", "Malgun Gothic", "sans-serif"],
    })

    fig = plt.figure(figsize=(12.8, 4.2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.axis("off")

    # ── 1. 주장 ──
    _box(ax, (0.04, 0.82), (0.92, 0.12),
         "주장  ·  \"훈련 범위 밖에서도 예측이 된다\"",
         sub="가정(EQL·CMNN·Physics·UQ)을 넣었다 — 그럼 끝?",
         fc="#152030", ec=TEAL, fs=12)
    _arrow(ax, (0.5, 0.80), (0.5, 0.74))

    # ── 2. 함정 3 ──
    ax.text(0.04, 0.715, "왜 속을까?  (함정 3)", color=AMBER, fontsize=11, fontweight="bold")
    traps = [
        (0.04, "① 시험이 사실 안",
         "test가 hull 안인데\n\"외삽 성능\"이라 부름\n→ 보간 점수"),
        (0.355, "② 밖인데도 과신",
         "범위 밖인데도\n확신·분산 그대로\n→ 자신 있게 틀림"),
        (0.67, "③ train 지표 착시",
         "train RMSE·PDE 잔차 OK\n밖(시간·DoD)에서는\n터질 수 있음 (Fesser)"),
    ]
    for x0, title, sub in traps:
        _box(ax, (x0, 0.48), (0.29, 0.22), title, sub=sub, fc=PANEL, ec=AMBER, title_color=AMBER, fs=10.5)

    _arrow(ax, (0.5, 0.46), (0.5, 0.40))

    # ── 3. 확인 4 ──
    ax.text(0.04, 0.375, "그래서 이렇게 확인  (체크 4)", color=TEAL, fontsize=11, fontweight="bold")
    checks = [
        ("① hull", "test가 Conv(X_train)\n밖인가?\nmin–max 금지"),
        ("② holdout", "입력·y·시간\n범위 밖으로\n별도 시험"),
        ("③ baseline", "선형·RF vs NN\n같은 튜닝\n예산"),
        ("④ UQ·기권", "밖에서 띠↑\n또는 예측 안 함\n시드·분할"),
    ]
    xs = [0.04, 0.27, 0.50, 0.73]
    for x0, (title, sub) in zip(xs, checks):
        _box(ax, (x0, 0.06), (0.22, 0.28), title, sub=sub, fc=PANEL, ec=TEAL, fs=10.5)
        if title.startswith("①"):
            inset = fig.add_axes([0.055, 0.09, 0.09, 0.14])
            _mini_hull(inset)

    for i in range(3):
        _arrow(ax, (xs[i] + 0.22, 0.20), (xs[i + 1], 0.20), color=MUTED)

    ax.text(0.5, 0.01,
            "회귀 extrap = hull 밖 holdout · 공정 baseline · UQ 동작   "
            "(IRM·DomainBed = 분류 DG → 오늘 범위 밖)",
            ha="center", color=MUTED, fontsize=8.5, transform=ax.transAxes)

    fig.savefig(OUT / "fig_verification_guide.png", dpi=260, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
    plt.close()
    print("wrote", OUT / "fig_verification_guide.png")


if __name__ == "__main__":
    main()
