"""S25 — practical 4-step flow (natural Korean, no special glyphs)."""
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
})


def step(ax, cx, cy, w, h, title, lines, edge):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        facecolor=PANEL2, edgecolor=edge, linewidth=1.6,
        transform=ax.transAxes, zorder=2,
    ))
    ax.text(cx, cy + 0.038, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=9.5, fontweight="bold", color=INK)
    ax.text(cx, cy - 0.048, "\n".join(lines), transform=ax.transAxes, ha="center", va="center",
            fontsize=7.5, color=MUTED, linespacing=1.35)


def arrow(ax, x0, x1, y, color=MUTED):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8))


fig, ax = plt.subplots(figsize=(12.6, 2.55))
ax.set_facecolor(BG)
ax.axis("off")
ax.add_patch(FancyBboxPatch(
    (0.02, 0.08), 0.96, 0.84, boxstyle="round,pad=0.012,rounding_size=0.015",
    facecolor=PANEL, edgecolor=LINE_DIM, linewidth=1.0, transform=ax.transAxes,
))

Y = 0.58
steps = [
    (0.11, "1. 범위", ["학습 vs 현장", "밖 시험 미리 분리"], TEAL),
    (0.35, "2. 가정·방법", ["아는 만큼 선택", "EQL · CMNN · Physics · UQ"], TEAL),
    (0.59, "3. 성능 검증", ["밖에서 오차 비교", "MAPE · baseline · UQ"], CORAL),
    (0.83, "4. 배포", ["되면 현장 투입", "불안하면 예측 안 함"], LIME),
]
for cx, t, ls, c in steps:
    step(ax, cx, Y, 0.20, 0.30, t, ls, c)

for a, b in ((0.21, 0.25), (0.45, 0.49), (0.69, 0.73)):
    arrow(ax, a, b, Y, TEAL)

reminders = [
    (0.20, "학습만으론 가정을 고를 수 없음"),
    (0.50, "시험 데이터 없으면 숫자 판단 불가"),
    (0.80, "고위험: 틀린 답 > 답변 거부"),
]
for cx, txt in reminders:
    ax.text(cx, 0.18, txt, transform=ax.transAxes, ha="center", fontsize=8.2, color=AMBER)

fig.savefig(OUT / "fig_closing_practical.png", dpi=320, bbox_inches="tight", pad_inches=0.06)
plt.close()
print("fig_closing_practical ok")
