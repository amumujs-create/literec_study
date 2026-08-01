"""Assumption definition — chart only (text lives on PPT cards).

Train [0, 2]: one indistinguishable fit — data alone cannot pick an assumption.
Extrap x > 2: each assumption continues differently (not "three models all fitted").
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

OUT = Path("_assets")
BG = "#0b1016"
PANEL = "#1a2430"
INK = "#e6edf5"
MUTED = "#8b9bb0"
CYAN = "#3dd6c6"
LIME = "#9ad17b"
CORAL = "#e07a5f"
AMBER = "#f0a05a"
GRID = "#2a3545"
LINE = "#3a4a5c"
SHADE = "#12324a"
X_TRAIN_HI = 2.0

# Linux/Windows/macOS — pick first available CJK font (avoid □□□ tofu)
_KO_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "C:/Windows/Fonts/malgun.ttf",
]


def _setup_korean_font() -> str:
    for path in _KO_FONT_CANDIDATES:
        if not Path(path).exists():
            continue
        fm.fontManager.addfont(path)
        name = fm.FontProperties(fname=path).get_name()
        mpl.rcParams["font.family"] = name
        mpl.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
        return name
    mpl.rcParams["font.family"] = "DejaVu Sans"
    return "DejaVu Sans"


_setup_korean_font()
mpl.rcParams.update(
    {
        "figure.facecolor": BG,
        "text.color": INK,
        "axes.unicode_minus": False,
        "savefig.facecolor": BG,
        "savefig.edgecolor": BG,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.14,
    }
)

# Training points
x_pts = np.array([0.0, 0.3, 0.7, 1.1, 1.5, 1.9, 2.0])
y_pts = np.array([0.0, 0.3, 0.7, 1.1, 1.5, 1.9, 2.0])

x = np.linspace(-0.3, 4.5, 400)
mask_in = x <= X_TRAIN_HI
x_out = x[x >= X_TRAIN_HI]

# Shared fit inside train hull
y_shared = np.interp(x, x_pts, y_pts)
y_at_boundary = 2.0

y_linear_ex = y_at_boundary + 1.0 * (x_out - X_TRAIN_HI)
y_exp_ex = y_at_boundary + 2.2 * (np.exp(0.55 * (x_out - X_TRAIN_HI)) - 1.0)
y_wave_ex = y_at_boundary + 0.85 * (x_out - X_TRAIN_HI) + 1.4 * np.sin(1.15 * (x_out - X_TRAIN_HI))

fig, ax = plt.subplots(figsize=(8.6, 3.55))
ax.set_facecolor(PANEL)
for sp in ax.spines.values():
    sp.set_color(LINE)
ax.tick_params(colors=MUTED, labelsize=7)
ax.grid(True, color=GRID, lw=0.5, alpha=0.7)

ax.axvspan(0, X_TRAIN_HI, color=SHADE, alpha=0.95)
ax.axvline(X_TRAIN_HI, color=CYAN, ls="--", lw=0.9, alpha=0.55)
ax.scatter(x_pts[1:-1], y_pts[1:-1], s=36, c=CYAN, zorder=6, label="훈련점 (동일)")

# Train: single fit — "which assumption?" is not identifiable from data alone
ax.plot(x[mask_in], y_shared[mask_in], color=INK, lw=2.4, alpha=0.55, zorder=4,
        label="훈련 적합 (가정 구분 불가)")

# Extrap only: three different priors / continuations from x = 2
ax.plot(x_out, y_linear_ex, color=CORAL, lw=2.0, ls="-", label="가정 A: 선형 (x>2)")
ax.plot(x_out, y_exp_ex, color=LIME, lw=2.0, ls="-", label="가정 B: 지수 (x>2)")
ax.plot(x_out, y_wave_ex, color=AMBER, lw=1.8, ls="-", label="가정 C: 진동+추세 (x>2)")

ax.set_ylim(-0.5, 5.2)
ax.set_xlim(-0.3, 4.5)
ax.set_title("같은 훈련 데이터 — 밖(x>2)으로 나가면 가정마다 예측이 갈린다",
             color=INK, fontsize=10, pad=6)
ax.legend(loc="upper left", fontsize=7.2, labelcolor=INK, framealpha=0.25)
ax.text(1.0, 4.7, "훈련 범위", color=CYAN, fontsize=8, ha="center")
ax.text(3.3, 4.7, "외삽 영역", color=CORAL, fontsize=8, ha="center")
ax.text(X_TRAIN_HI, -0.35, "x = 2", color=CYAN, fontsize=7, ha="center")
ax.annotate(
    "여러 가정이\n훈련점을 설명 가능",
    xy=(1.0, 1.0), xytext=(0.35, 2.35),
    fontsize=7, color=MUTED, ha="left",
    arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8),
)

fig.subplots_adjust(top=0.92, left=0.08, right=0.98, bottom=0.12)
fig.savefig(OUT / "fig_assumption_defined.png", dpi=260)
plt.close()
print("assumption chart ok")
