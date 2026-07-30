"""S26 — practical: choose assumption/method & respond."""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path("_assets")
BG = "#0b1016"
PANEL = "#1a2430"
PANEL2 = "#141c26"
INK = "#e6edf5"
MUTED = "#8b9bb0"
TEAL = "#3dd6c6"
CORAL = "#e07a5f"
AMBER = "#f0a05a"
LIME = "#9ad17b"
LINE_DIM = "#3a4a5c"

mpl.rcParams.update({
    "figure.facecolor": BG,
    "text.color": INK,
    "font.family": "sans-serif",
    "font.sans-serif": ["Apple SD Gothic Neo", "Avenir Next", "Helvetica Neue", "Arial"],
    "savefig.facecolor": BG,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.10,
})


def box(ax, cx, cy, w, h, title, sub, edge, fs=9.5):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        facecolor=PANEL2, edgecolor=edge, linewidth=1.5,
        transform=ax.transAxes, zorder=2,
    ))
    ax.text(cx, cy + 0.022, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=fs, fontweight="bold", color=INK)
    if sub:
        ax.text(cx, cy - 0.038, sub, transform=ax.transAxes, ha="center", va="center",
                fontsize=7.8, color=MUTED, linespacing=1.25)


def arrow(ax, x0, y0, x1, y1, color=MUTED):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6))


fig, ax = plt.subplots(figsize=(12.6, 4.2))
ax.set_facecolor(BG)
ax.axis("off")
ax.add_patch(FancyBboxPatch(
    (0.02, 0.06), 0.96, 0.88, boxstyle="round,pad=0.012,rounding_size=0.015",
    facecolor=PANEL, edgecolor=LINE_DIM, linewidth=1.0, transform=ax.transAxes,
))

ax.text(0.5, 0.93, "가정·방법 여러 개 → 밖 예측 다름 → **이 순서**로 고르고 대응",
        transform=ax.transAxes, ha="center", fontsize=11.5, fontweight="bold", color=INK)

# row 1 — workflow
Y = 0.72
steps = [
    (0.11, "1. 범위 확인", "운영 범위표\n(train vs 현장)", TEAL),
    (0.32, "2. 후보 가정", "지식→방법\n(EQL/CMNN/Physics/UQ)", TEAL),
    (0.53, "3. 각각 학습", "같은 train\n**밖 시험 분리**", TEAL),
    (0.74, "4. □ MAPE", "actual y로\n**판정**", CORAL),
    (0.92, "5. 대응", "표·기권·재학습", LIME),
]
for i, (cx, t, s, c) in enumerate(steps):
    box(ax, cx, Y, 0.17, 0.17, t, s, c)
    if i < len(steps) - 1:
        nx = steps[i + 1][0]
        arrow(ax, cx + 0.09, Y, nx - 0.09, Y, c)

# row 2 — knowledge → method
ax.text(0.04, 0.48, "지식→후보", transform=ax.transAxes, fontsize=8.5, color=TEAL, fontweight="bold")
mapping = [
    (0.14, "함수·식 알음", "EQL / NALU"),
    (0.36, "방향만 알음", "CMNN"),
    (0.58, "법칙·물리 알음", "Physics-ML"),
    (0.80, "모름", "UQ + 기권"),
]
for cx, k, m in mapping:
    ax.add_patch(FancyBboxPatch(
        (cx - 0.10, 0.36), 0.20, 0.10, boxstyle="round,pad=0.006",
        facecolor=PANEL2, edgecolor=TEAL, linewidth=0.9, transform=ax.transAxes,
    ))
    ax.text(cx, 0.415, k, transform=ax.transAxes, ha="center", fontsize=7.6, color=INK, fontweight="bold")
    ax.text(cx, 0.375, m, transform=ax.transAxes, ha="center", fontsize=7.4, color=AMBER)

# row 3 — decision matrix
ax.text(0.04, 0.28, "판정→대응", transform=ax.transAxes, fontsize=8.5, color=CORAL, fontweight="bold")
rows = [
    ("밖 MAPE OK", "UQ OK", "해당 범위 **배포**", LIME),
    ("밖 MAPE OK", "UQ NG(과신)", "**UQ·기권** 강화 후 재시험", AMBER),
    ("밖 MAPE NG", "UQ OK(경보)", "**기권** — 밖은 숫자 X", CORAL),
    ("밖 MAPE NG", "UQ NG", "**배포 금지** · 가정·데이터 재검토", CORAL),
]
for i, (a, b, act, c) in enumerate(rows):
    y = 0.22 - i * 0.045
    ax.text(0.12, y, a, transform=ax.transAxes, ha="center", fontsize=7.2, color=MUTED)
    ax.text(0.28, y, b, transform=ax.transAxes, ha="center", fontsize=7.2, color=MUTED)
    ax.add_patch(FancyBboxPatch(
        (0.38, y - 0.018), 0.56, 0.032, boxstyle="round,pad=0.004",
        facecolor=PANEL2, edgecolor=c, linewidth=0.8, transform=ax.transAxes,
    ))
    ax.text(0.66, y, act, transform=ax.transAxes, ha="center", fontsize=7.5, color=INK)

ax.text(0.5, 0.04,
        "□ actual 없으면 MAPE 판정 불가 → **UQ+기권**으로 위험 구간 차단 · pilot 후 재평가",
        transform=ax.transAxes, ha="center", fontsize=8.2, color=AMBER, style="italic")

fig.savefig(OUT / "fig_practical_assumption_flow.png", dpi=320)
plt.close()
print("fig_practical_assumption_flow ok")
