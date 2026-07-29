"""S25 — verification flow: assumption -> extrap test -> compare to actual."""
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


def box(ax, cx, cy, w, h, title, sub, edge, fs=10):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        facecolor=PANEL2, edgecolor=edge, linewidth=1.6,
        transform=ax.transAxes, zorder=2,
    ))
    ax.text(cx, cy + 0.018, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=fs, fontweight="bold", color=INK)
    if sub:
        ax.text(cx, cy - 0.045, sub, transform=ax.transAxes, ha="center", va="center",
                fontsize=8.2, color=MUTED)


def arrow(ax, x0, y0, x1, y1, color=MUTED):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8))


fig, ax = plt.subplots(figsize=(12.4, 3.8))
ax.set_facecolor(BG)
ax.axis("off")
panel_bg = FancyBboxPatch(
    (0.02, 0.08), 0.96, 0.84, boxstyle="round,pad=0.012,rounding_size=0.015",
    facecolor=PANEL, edgecolor=LINE_DIM, linewidth=1.0, transform=ax.transAxes,
)
ax.add_patch(panel_bg)

ax.text(0.5, 0.94, "뭐가 맞나? — train만으론 모름 · **밖 구간 시험(actual)** 으로 판정",
        transform=ax.transAxes, ha="center", fontsize=12, fontweight="bold", color=INK)

# row 1 flow
Y1 = 0.68
box(ax, 0.12, Y1, 0.18, 0.18, "1. 가정·방법", "지식→EQL/CMNN/\nPhysics-ML/UQ", TEAL)
box(ax, 0.35, Y1, 0.18, 0.18, "2. 학습", "train hull **안**만", TEAL)
box(ax, 0.58, Y1, 0.18, 0.18, "3. 밖 시험", "hull **밖** 입력\n+ **actual y**", CORAL)
box(ax, 0.81, Y1, 0.18, 0.18, "4. 비교", "MAPE/RMSE\nbaseline 대비", LIME)
for a, b in ((0.21, 0.26), (0.44, 0.49), (0.67, 0.72)):
    arrow(ax, a, Y1, b, Y1, TEAL)

# row 2 pitfalls
Y2 = 0.32
ax.text(0.04, Y2 + 0.12, "함정", transform=ax.transAxes, fontsize=9, color=CORAL, fontweight="bold")
pitfalls = [
    (0.20, "test가 hull **안** → 보간 점수 착각"),
    (0.50, "train RMSE 좋아도 밖 **터짐** (Fesser)"),
    (0.80, "밖인데 **과신** — UQ/기권 확인"),
]
for cx, txt in pitfalls:
    ax.add_patch(FancyBboxPatch(
        (cx - 0.14, Y2 - 0.10), 0.28, 0.16, boxstyle="round,pad=0.008",
        facecolor=PANEL2, edgecolor=CORAL, linewidth=1.0, transform=ax.transAxes,
    ))
    ax.text(cx, Y2, txt, transform=ax.transAxes, ha="center", va="center", fontsize=8.3, color=INK)

ax.text(0.5, 0.06, "가정 선택 = 사전 지식 + **밖 시험** + baseline + UQ  (Li: 고DoD train → 저DoD test)",
        transform=ax.transAxes, ha="center", fontsize=9, color=AMBER, style="italic")

fig.savefig(OUT / "fig_verification_guide.png", dpi=320)
plt.close()
print("fig_verification_guide ok")
