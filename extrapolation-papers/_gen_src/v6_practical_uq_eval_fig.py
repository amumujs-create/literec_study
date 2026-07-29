"""S27 — practical extrap evaluation + UQ deployment."""
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


def box(ax, cx, cy, w, h, title, sub, edge, fs=9.2):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.03",
        facecolor=PANEL2, edgecolor=edge, linewidth=1.5,
        transform=ax.transAxes, zorder=2,
    ))
    ax.text(cx, cy + 0.020, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=fs, fontweight="bold", color=INK)
    if sub:
        ax.text(cx, cy - 0.040, sub, transform=ax.transAxes, ha="center", va="center",
                fontsize=7.6, color=MUTED, linespacing=1.22)


def arrow(ax, x0, y0, x1, y1, color=MUTED):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6))


fig, ax = plt.subplots(figsize=(12.6, 4.0))
ax.set_facecolor(BG)
ax.axis("off")
ax.add_patch(FancyBboxPatch(
    (0.02, 0.05), 0.96, 0.90, boxstyle="round,pad=0.012,rounding_size=0.015",
    facecolor=PANEL, edgecolor=LINE_DIM, linewidth=1.0, transform=ax.transAxes,
))

ax.text(0.5, 0.93, "실무 외삽 평가 — **밖 MAPE** + **UQ** 같이 보고 배포 규칙 정하기",
        transform=ax.transAxes, ha="center", fontsize=11.5, fontweight="bold", color=INK)

# pipeline
Y = 0.74
pipe = [
    (0.10, "① 분리", "train / **밖 시험**\n(학습 전)", TEAL),
    (0.30, "② 학습+UQ", "점수+불확실\n(앙상블 등)", TEAL),
    (0.50, "③ 밖 평가", "**MAPE** + σ↑?\n(과신 검사)", CORAL),
    (0.70, "④ 임계", "σ_low / σ_high\n정하기", AMBER),
    (0.90, "⑤ 배포", "경고·기권\n코드 박기", LIME),
]
for i, (cx, t, s, c) in enumerate(pipe):
    box(ax, cx, Y, 0.16, 0.16, t, s, c)
    if i < len(pipe) - 1:
        arrow(ax, cx + 0.085, Y, pipe[i + 1][0] - 0.085, Y, c)

# deployment rules
ax.text(0.04, 0.52, "배포 규칙", transform=ax.transAxes, fontsize=8.5, color=LIME, fontweight="bold")
rules = [
    (0.18, "σ < T_low", "정상 출력", TEAL),
    (0.42, "T_low ≤ σ < T_high", "숫자 + **불확실↑** (UQ)", AMBER),
    (0.66, "σ ≥ T_high", "**예측 안 함** (기권)", CORAL),
    (0.88, "범위 밖 입력", "무조건 경고/기권", CORAL),
]
for cx, cond, act, c in rules:
    ax.add_patch(FancyBboxPatch(
        (cx - 0.11, 0.38), 0.22, 0.11, boxstyle="round,pad=0.006",
        facecolor=PANEL2, edgecolor=c, linewidth=0.9, transform=ax.transAxes,
    ))
    ax.text(cx, 0.445, cond, transform=ax.transAxes, ha="center", fontsize=7.3, color=INK, fontweight="bold")
    ax.text(cx, 0.405, act, transform=ax.transAxes, ha="center", fontsize=7.2, color=MUTED)

# checklist
ax.text(0.04, 0.30, "체크 5", transform=ax.transAxes, fontsize=8.5, color=TEAL, fontweight="bold")
checks = [
    "운영 범위표 (train vs 현장)",
    "밖 시험 **학습 전** 분리",
    "밖 **MAPE** (train 점수 X)",
    "baseline **튜닝·데이터 동일**",
    "밖에서 **σ↑** · 틀릴 때 σ 큼",
]
for i, txt in enumerate(checks):
    col = i % 3
    row = i // 3
    cx = 0.20 + col * 0.28
    cy = 0.22 - row * 0.07
    ax.text(cx, cy, f"· {txt}", transform=ax.transAxes, ha="center", fontsize=7.4, color=MUTED)

ax.text(0.5, 0.06,
        "actual 없음 → MAPE 못 냄 · **UQ+기권**만 · pilot 로그 쌓이면 ③ 재평가 · 고위험: **틀린 숫자 > 기권**",
        transform=ax.transAxes, ha="center", fontsize=8.0, color=AMBER, style="italic")

fig.savefig(OUT / "fig_practical_uq_eval.png", dpi=320)
plt.close()
print("fig_practical_uq_eval ok")
