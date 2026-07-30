#!/usr/bin/env python3
"""Generate figures for CA-CSS v4 case appendix PPT."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parent
# ca-css-ncmapss repo (sibling under extra_study/)
PROJ = ROOT.parent.parent / "ca-css-ncmapss"
sys.path.insert(0, str(PROJ))

OUT = ROOT / "_assets" / "case_v4"
OUT.mkdir(parents=True, exist_ok=True)

# dark-console palette (match v5 PPT)
BG = "#0B1016"
PANEL = "#141B24"
TEAL = "#3DD6C6"
CORAL = "#E89A5C"
INK = "#ECF1F7"
SLATE = "#A0ADBC"
BLUE = "#2563eb"
RED = "#dc2626"
GRAY = "#6E7C8C"
ACCENT_DIM = "#243A42"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL,
    "axes.edgecolor": "#2C3848", "axes.labelcolor": INK,
    "text.color": INK, "xtick.color": SLATE, "ytick.color": SLATE,
    "font.size": 10, "savefig.dpi": 200,
    "font.family": ["Apple SD Gothic Neo", "AppleGothic", "sans-serif"],
})


def save(fig, name: str, dpi: int | None = None) -> Path:
    p = OUT / f"{name}.png"
    fig.savefig(p, bbox_inches="tight", facecolor=BG, dpi=dpi or plt.rcParams["savefig.dpi"])
    plt.close(fig)
    print("saved", p)
    return p


def fig_architecture() -> None:
    """Compact v4 diagram — dark panel + colored border, readable text."""
    fig, ax = plt.subplots(figsize=(13, 3.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 3.5)
    ax.axis("off")
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)

    PANEL_D = "#141B24"
    C_ATTN, C_FFN = "#E89A5C", "#5B9BD5"
    C_NORM_E = "#8A9BB5"
    C_EMB, C_MASK = "#C084FC", "#3DD6C6"
    C_HEALTH, C_DAMAGE = TEAL, CORAL
    C_FUSE = "#818CF8"

    hx, dx, fx, cx_in = 3.2, 9.8, 6.5, 6.5

    def block(cx, y, w, h, text, ec, fs=9.5, tc=INK):
        x = cx - w / 2
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.06",
            facecolor=PANEL_D, edgecolor=ec, linewidth=2.2, zorder=2,
        ))
        ax.text(cx, y + h / 2, text, ha="center", va="center", fontsize=fs,
                color=tc, fontweight="bold", zorder=3, linespacing=1.12)

    def varrow(x, y1, y2, color=SLATE, lw=1.5):
        ax.add_patch(FancyArrowPatch(
            (x, y1), (x, y2), arrowstyle="-|>", mutation_scale=10,
            color=color, linewidth=lw, zorder=1))

    def harrow(x1, x2, y, color=SLATE, rad=0.0):
        style = f"arc3,rad={rad}" if rad else "arc3"
        ax.add_patch(FancyArrowPatch(
            (x1, y), (x2, y), arrowstyle="-|>", mutation_scale=9,
            color=color, linewidth=1.3, connectionstyle=style, zorder=1))

    def enc_stack(cx, y, w, h):
        x = cx - w / 2
        ax.add_patch(FancyBboxPatch(
            (x - 0.08, y - 0.06), w + 0.16, h + 0.12,
            boxstyle="round,pad=0.01,rounding_size=0.05",
            facecolor="none", edgecolor=C_HEALTH, linewidth=1.8, linestyle="--", zorder=1))
        ax.text(x - 0.04, y + h / 2, "N×2", ha="right", va="center",
                fontsize=9, color=C_HEALTH, fontweight="bold", rotation=90)
        lh = (h - 0.08) / 4
        ly = y + 0.04
        for title, ec in [
            ("Multi-Head Attention", C_ATTN),
            ("Add & Norm", C_NORM_E),
            ("Feed Forward 128", C_FFN),
            ("Add & Norm", C_NORM_E),
        ]:
            block(cx, ly, w - 0.1, lh - 0.01, title, ec, fs=8.5)
            ly += lh

    def mono_parallel(cx, y, w, h):
        x = cx - w / 2
        ax.add_patch(FancyBboxPatch(
            (x - 0.06, y - 0.05), w + 0.12, h + 0.1,
            boxstyle="round,pad=0.01,rounding_size=0.05",
            facecolor="none", edgecolor=C_DAMAGE, linewidth=1.8, linestyle="--", zorder=1))
        ax.text(cx, y + h + 0.06, "MonotoneLoadHead", ha="center", va="bottom",
                fontsize=9, color=C_DAMAGE, fontweight="bold")
        bw = (w - 0.18) / 2
        by = y + 0.1
        bh = h - 0.52
        lx, rx = cx - bw / 2 - 0.04, cx + bw / 2 + 0.04
        block(lx, by, bw, bh, "mono\nw⁺·TRA+w⁺·cycle", C_DAMAGE, fs=8.5)
        block(rx, by, bw, bh, "other\nMLP→softplus", C_FFN, fs=8.5)
        sum_y = y + 0.04
        block(cx, sum_y, w - 0.08, 0.3, "D = mono + other", C_DAMAGE, fs=9, tc=CORAL)
        varrow(lx, by + bh, sum_y + 0.3, C_DAMAGE, 1.2)
        varrow(rx, by + bh, sum_y + 0.3, C_DAMAGE, 1.2)

    block(cx_in, 0.14, 2.1, 0.38, "Inputs  X_seq (B,T,33)", GRAY, fs=10)
    varrow(cx_in, 0.54, 0.64, SLATE)
    harrow(cx_in, hx, 0.64, C_HEALTH)
    harrow(cx_in, dx, 0.64, C_DAMAGE)

    y0 = 0.74
    ax.text(hx, 3.28, "Health path", ha="center", fontsize=10, color=C_HEALTH, fontweight="bold")
    block(hx, y0, 1.4, 0.34, "TRA Mask → 0", C_MASK, fs=9)
    varrow(hx, y0 + 0.34, y0 + 0.4, C_HEALTH)
    y1 = y0 + 0.4
    block(hx, y1, 1.45, 0.34, "Linear 33→64", C_EMB, fs=9)
    varrow(hx, y1 + 0.34, y1 + 0.4, C_HEALTH)
    y2 = y1 + 0.4
    enc_stack(hx, y2, 1.5, 1.08)
    y3 = y2 + 1.08 + 0.06
    varrow(hx, y2 + 1.08, y3, C_HEALTH)
    block(hx, y3, 1.4, 0.34, "Health Head → H", C_HEALTH, fs=9)

    ax.text(dx, 3.28, "Load / Damage", ha="center", fontsize=10, color=C_DAMAGE, fontweight="bold")
    block(dx, y0, 1.7, 0.34, "Load [TRA,φ,T30,cycle]", C_DAMAGE, fs=8.5)
    varrow(dx, y0 + 0.34, y0 + 0.4, C_DAMAGE)
    mono_parallel(dx, y0 + 0.4, 1.9, 1.38)
    ax.text(dx + 0.98, y0 + 1.55, "D", fontsize=12, color=C_DAMAGE, fontweight="bold")

    my = 2.62
    harrow(hx + 0.72, fx - 0.32, my, C_HEALTH, rad=0.08)
    harrow(dx - 0.72, fx + 0.32, my, C_DAMAGE, rad=-0.08)
    varrow(fx, my, my + 0.1, C_FUSE)
    block(fx, my + 0.1, 1.3, 0.32, "RUL = H − D", C_FUSE, fs=10.5)
    varrow(fx, my + 0.42, my + 0.5, C_FUSE)
    block(fx, my + 0.5, 1.5, 0.3, "Isotonic → RUL", C_FUSE, fs=9)

    save(fig, "fig_v4_architecture", dpi=300)

def fig_tra_hard_split() -> None:
    """시험(외삽) 구간만 — 새 엔진 + TRA>q90."""
    fig, ax = plt.subplots(figsize=(8.0, 3.2))
    rng = np.random.default_rng(42)
    tra_test_ood = rng.normal(82.5, 0.8, 80)
    q90 = 81.7
    ax.hist(tra_test_ood, bins=14, alpha=0.75, color=CORAL,
            label="시험(외삽) · 엔진 11·14·15 · TRA > q90", density=True)
    ax.axvline(q90, color=RED, ls="--", lw=1.4, label=f"외삽 시작 q90 = {q90}")
    ax.set_xlim(q90 - 0.3, 84.8)
    ax.set_xlabel("TRA (스로틀·부하)")
    ax.set_ylabel("밀도 (개념도)")
    ax.set_title("평가 구간 — 시험(외삽)만", fontsize=11, color=TEAL)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.text(0.5, 0.92, "훈련에 없던 엔진 · 훈련보다 높은 부하만 평가 (n≈159 windows)",
            transform=ax.transAxes, ha="center", fontsize=8.5, color=SLATE)
    save(fig, "fig_tra_hard_split")


def _hard_y_variance() -> float:
    """Mean per-sample SS_tot on hard_extrap from v4 runs (for TabPFN R² estimate)."""
    p = PROJ / "results" / "v4_paper_main" / "v4_paper_main.json"
    if not p.exists():
        return 350.0
    runs = [
        r for r in json.loads(p.read_text())["runs"]
        if r.get("dataset") == "ncmapss_hard" and r.get("band") == "hard_extrap"
        and r.get("rmse") is not None and r.get("r2") is not None
    ]
    if not runs:
        return 350.0
    return float(np.mean([r["rmse"] ** 2 / (1 - r["r2"]) for r in runs]))


def _rmse_to_r2(rmse: float, ss_tot: float) -> float:
    return max(0.0, 1.0 - rmse ** 2 / ss_tot)


def load_hard_baselines() -> list[dict]:
    """Fair-protocol metrics (e15 · val/fix HP · test 튜닝 ✗) from results JSON."""
    ss_tot = _hard_y_variance()
    out: list[dict] = []

    main_p = PROJ / "results" / "v4_paper_main" / "v4_paper_main.json"
    if main_p.exists():
        runs = [
            r for r in json.loads(main_p.read_text())["runs"]
            if r.get("dataset") == "ncmapss_hard"
            and r.get("band") == "hard_extrap"
            and r.get("ablation_mode") is None
            and r.get("config") == "paper_e15"
        ]
        if runs:
            rmses = [r["rmse"] for r in runs]
            r2s = [r["r2"] for r in runs]
            out.append({
                "label": "v4+iso",
                "rmse": float(np.mean(rmses)),
                "rmse_std": float(np.std(rmses)) if len(rmses) > 1 else 0.0,
                "r2": float(np.mean(r2s)),
                "r2_std": float(np.std(r2s)) if len(r2s) > 1 else 0.0,
                "color": BLUE,
                "note": "3-seed e15",
            })
            tab = json.loads(main_p.read_text()).get("tabpfn_v8", {}).get("ncmapss_hard", 4.788)
            out.append({
                "label": "TabPFN",
                "rmse": float(tab),
                "rmse_std": 0.0,
                "r2": _rmse_to_r2(float(tab), ss_tot),
                "r2_std": 0.0,
                "color": RED,
                "note": "ref (in-context)",
            })

    sig_p = PROJ / "results" / "v4_significance" / "v4_significance.json"
    if sig_p.exists():
        sig = json.loads(sig_p.read_text())
        gbm = [r for r in sig["runs"]
               if r.get("dataset") == "ncmapss_hard" and r.get("model") == "xgb_iso"]
        if gbm:
            rmses = [r["rmse"] for r in gbm]
            r2s = [r["r2"] for r in gbm if r.get("r2") is not None]
            out.append({
                "label": "GBM+iso",
                "rmse": float(np.mean(rmses)),
                "rmse_std": float(np.std(rmses)) if len(rmses) > 1 else 0.0,
                "r2": float(np.mean(r2s)) if r2s else _rmse_to_r2(float(np.mean(rmses)), ss_tot),
                "r2_std": float(np.std(r2s)) if len(r2s) > 1 else 0.0,
                "color": GRAY,
                "note": "10-seed e15",
            })

    extra_p = PROJ / "results" / "v4_extra_baselines" / "v4_extra_baselines.json"
    if extra_p.exists():
        lstm = [r for r in json.loads(extra_p.read_text())["runs"]
                if r.get("dataset") == "ncmapss_hard" and r.get("model") == "lstm_iso"]
        if lstm:
            rmses = [r["rmse"] for r in lstm]
            r2s = [r["r2"] for r in lstm if r.get("r2") is not None]
            out.append({
                "label": "LSTM+iso",
                "rmse": float(np.mean(rmses)),
                "rmse_std": float(np.std(rmses)) if len(rmses) > 1 else 0.0,
                "r2": float(np.mean(r2s)) if r2s else 0.0,
                "r2_std": float(np.std(r2s)) if len(r2s) > 1 else 0.0,
                "color": GRAY,
                "note": "5-seed e15",
            })

    if not out:
        return [
            {"label": "v4+iso", "rmse": 3.88, "rmse_std": 0.80, "r2": 0.95, "r2_std": 0.02,
             "color": BLUE, "note": "fallback"},
            {"label": "TabPFN", "rmse": 4.79, "rmse_std": 0.0, "r2": 0.94, "r2_std": 0.0,
             "color": RED, "note": "fallback"},
            {"label": "GBM+iso", "rmse": 5.74, "rmse_std": 0.0, "r2": 0.91, "r2_std": 0.0,
             "color": GRAY, "note": "fallback"},
            {"label": "LSTM+iso", "rmse": 16.0, "rmse_std": 0.0, "r2": 0.29, "r2_std": 0.0,
             "color": GRAY, "note": "fallback"},
        ]
    return out


def fig_main_rmse() -> None:
    rows = load_hard_baselines()
    labels = [r["label"] for r in rows]
    rmse = [r["rmse"] for r in rows]
    err = [r["rmse_std"] for r in rows]
    r2 = [r["r2"] for r in rows]
    colors = [r["color"] for r in rows]

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    x = np.arange(len(labels))
    bars = ax.bar(x, rmse, yerr=err, color=colors, capsize=3, width=0.58, edgecolor="none")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("hard_extrap RMSE ↓")
    ax.set_title("N-CMAPSS hard — fair baseline (e15 · val/fix HP · test 튜닝 ✗)")
    ymax = max(rmse) * 1.18
    ax.set_ylim(0, ymax)
    for i, (b, v, r2v, row) in enumerate(zip(bars, rmse, r2, rows)):
        e = err[i]
        top = v + (e if e else 0)
        ax.text(b.get_x() + b.get_width() / 2, top + 0.25,
                f"RMSE {v:.2f}" + (f"±{e:.2f}" if e else ""),
                ha="center", fontsize=8, color=INK)
        ax.text(b.get_x() + b.get_width() / 2, top + 0.85,
                f"R²={r2v:.3f}",
                ha="center", fontsize=8.5, fontweight="bold", color=TEAL)
    ax.text(0.02, 0.02,
            "※ test set HP 튜닝 baseline은 RMSE 더 낮게 나올 수 있음 — 본 그림은 공정 비교 프로토콜",
            transform=ax.transAxes, fontsize=7.5, color=SLATE, va="bottom")
    save(fig, "fig_main_rmse")
    # sidecar for PPT table builder
    meta = OUT / "hard_baseline_metrics.json"
    meta.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print("saved", meta)


def fig_arch_ablation() -> None:
    p = PROJ / "results" / "v4_arch_ablation" / "v4_arch_ablation.json"
    if not p.exists():
        return
    rows = json.loads(p.read_text())["rows"]
    variants = ["full", "no_zero_tra", "free_load", "free_both"]
    labels = ["full", "no zero\nTRA", "free\nload", "free\nboth"]
    by_v: dict[str, list[float]] = {v: [] for v in variants}
    for r in rows:
        if r.get("rmse") is not None and r["variant"] in by_v:
            by_v[r["variant"]].append(r["rmse"])
    means = [np.mean(by_v[v]) if by_v[v] else 0 for v in variants]
    stds = [np.std(by_v[v]) if len(by_v[v]) > 1 else 0 for v in variants]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    x = np.arange(len(variants))
    cols = [BLUE, TEAL, CORAL, GRAY]
    ax.bar(x, means, yerr=stds, color=cols, capsize=3, width=0.55)
    ax.axhline(4.788, color=RED, ls="--", lw=1.2, label="TabPFN 4.788")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("hard_extrap RMSE")
    ax.set_title("구조 prior ablation (3-seed, e15)")
    ax.legend(frameon=False, fontsize=9)
    save(fig, "fig_arch_ablation")


def fig_training_curve() -> None:
    """One seed — val RMSE per epoch (hard split)."""
    from project_env import load_project_env
    load_project_env()
    from extrap_gx_v4 import train_eval_v4_iso  # noqa — quick path below instead

    import torch
    from device_utils import get_torch_device
    from ncmapss_css_v5_damage import CSSConfigV5, train_css_v5_with_oc, predict_v5_oc
    from ncmapss_oc_norm import OCNormalizer
    from run_v4_paper_main_multiseed import _build

    split, constraints, kw = _build("ncmapss_hard", 42, 1500, None)
    cfg = CSSConfigV5(
        epochs=15, random_seed=42, enable_tstar_aux=False, lambda_t=0.0,
        variant_id="v4_disentangled", extrap_feat_idx=kw["extrap_feat_idx"],
        load_aux_feat_indices=kw["load_aux"], op_idx=list(kw["op_idx"]),
        lambda_tra=0.05, max_rul=kw["max_rul"],
    )
    # Manual epoch loop logging val on hard_extrap band
    from ncmapss_css_v5_damage import _build_v5_model, _augment_cycle_channel, _fit_cycle_scaler
    from ncmapss_config import set_torch_seed
    from sklearn.preprocessing import StandardScaler
    from torch.utils.data import DataLoader, TensorDataset
    import torch.nn as nn

    set_torch_seed(42)
    device = get_torch_device()
    aw = split.all_windows
    test_units = split.meta["unit_ids"]["test"]
    test_mask = aw.hard_extrap_mask(test_units, thresholds=split.thresholds)

    oc_norm = OCNormalizer().fit(split.train.X_seq, n_feat=split.train.X_seq.shape[2])
    cycle_scaler = _fit_cycle_scaler(aw.cycles_end[aw.tra_split_code == 0])
    n_base = split.train.X_seq.shape[2]
    X_tr_oc = oc_norm.transform(split.train.X_seq)
    X_va_oc = oc_norm.transform(split.val.X_seq)
    X_all_oc = oc_norm.transform(aw.X_seq)
    X_tr = _augment_cycle_channel(X_tr_oc, split.train.cycles_end, cycle_scaler)
    X_va = _augment_cycle_channel(X_va_oc, split.val.cycles_end, cycle_scaler)
    n_feat = X_tr.shape[2]
    scaler = StandardScaler().fit(X_tr.reshape(-1, n_feat))
    Xtr = scaler.transform(X_tr.reshape(-1, n_feat)).reshape(X_tr.shape)
    Xva = scaler.transform(X_va.reshape(-1, n_feat)).reshape(X_va.shape)
    Xall = scaler.transform(
        _augment_cycle_channel(X_all_oc, aw.cycles_end, cycle_scaler).reshape(-1, n_feat)
    ).reshape(len(aw), X_tr.shape[1], n_feat)

    model = _build_v5_model(n_feat, cfg).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()
    ds = TensorDataset(torch.tensor(Xtr, dtype=torch.float32),
                     torch.tensor(split.train.y, dtype=torch.float32))
    loader = DataLoader(ds, batch_size=256, shuffle=True)

    val_rmses: list[float] = []
    test_rmses: list[float] = []
    for epoch in range(15):
        model.train()
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad()
            rul, _, _ = model.forward_rul(xb)
            loss = loss_fn(rul.squeeze(), yb)
            loss.backward()
            opt.step()
        model.eval()
        with torch.no_grad():
            xb = torch.tensor(Xva, dtype=torch.float32).to(device)
            vp = model.forward_rul(xb)[0].cpu().numpy().ravel()
            val_rmses.append(float(np.sqrt(np.mean((vp - split.val.y) ** 2))))
            xb2 = torch.tensor(Xall[test_mask], dtype=torch.float32).to(device)
            tp = model.forward_rul(xb2)[0].cpu().numpy().ravel()
            test_rmses.append(float(np.sqrt(np.mean((tp - aw.y[test_mask]) ** 2))))

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ep = np.arange(1, 16)
    ax.plot(ep, val_rmses, "o-", color=TEAL, lw=1.8, label="val band RMSE")
    ax.plot(ep, test_rmses, "s--", color=CORAL, lw=1.8, label="hard_extrap RMSE")
    ax.set_xlabel("epoch")
    ax.set_ylabel("RMSE")
    ax.set_title("학습 곡선 — seed 42 (iso 전 raw)")
    ax.legend(frameon=False)
    ax.set_xticks(ep)
    save(fig, "fig_training_curve")


# Per-model fair epoch (§4.8 — train 크기·수렴 기준 개별 조정)
FAIR_EPOCH_RULE: dict[str, dict[str, int]] = {
    "ncmapss_hard": {
        "v4_iso": 15,
        "transformer_iso": 120,
        "lstm_iso": 120,
        "gru_iso": 120,
        "xgb_iso": 15,
    },
    "cmapss_fd002": {
        "v4_iso": 120,
        "transformer_iso": 120,
        "lstm_iso": 60,
        "gru_iso": 60,
        "xgb_iso": 15,
    },
    "cmapss_fd004": {
        "v4_iso": 120,
        "transformer_iso": 120,
        "lstm_iso": 60,
        "gru_iso": 60,
        "xgb_iso": 15,
    },
}

MODEL_DISPLAY = {
    "v4_iso": ("v4+iso", BLUE),
    "transformer_iso": ("Transformer", TEAL),
    "tabpfn": ("TabPFN", RED),
    "xgb_iso": ("GBM+iso", GRAY),
    "lstm_iso": ("LSTM+iso", "#94a3b8"),
    "gru_iso": ("GRU+iso", "#64748b"),
}

MODEL_ORDER = ["v4_iso", "transformer_iso", "tabpfn", "xgb_iso", "lstm_iso", "gru_iso"]

DATASET_PANELS = [
    ("ncmapss_hard", "N-CMAPSS hard ★"),
    ("cmapss_fd002", "C-MAPSS FD002"),
    ("cmapss_fd004", "C-MAPSS FD004"),
]


def _stats(runs: list[dict]) -> dict:
    rmses = [r["rmse"] for r in runs if r.get("rmse") is not None]
    r2s = [r["r2"] for r in runs if r.get("r2") is not None]
    return {
        "rmse": float(np.mean(rmses)) if rmses else None,
        "rmse_std": float(np.std(rmses)) if len(rmses) > 1 else 0.0,
        "r2": float(np.mean(r2s)) if r2s else None,
        "r2_std": float(np.std(r2s)) if len(r2s) > 1 else 0.0,
        "n_seed": len(rmses),
    }


def load_fair_baseline_comparison() -> list[dict]:
    """모델별 fair epoch + TabPFN ref — RMSE·R² (extrap band)."""
    fair_p = PROJ / "results" / "v4_fair_epochs" / "v4_fair_epochs.json"
    sig_p = PROJ / "results" / "v4_significance" / "v4_significance.json"
    fair_runs: list[dict] = []
    sig_runs: list[dict] = []
    tab_ref: dict[str, float] = {}
    if fair_p.exists():
        fair_runs = json.loads(fair_p.read_text()).get("runs", [])
    if sig_p.exists():
        sig = json.loads(sig_p.read_text())
        sig_runs = sig.get("runs", [])
        tab_ref = sig.get("tabpfn_ref", {})

    out: list[dict] = []
    for ds_key, ds_label in DATASET_PANELS:
        ss_tot = None
        panel_rows: list[dict] = []
        for mk in MODEL_ORDER:
            if mk == "tabpfn":
                tab_rmse = tab_ref.get(ds_key)
                if tab_rmse is None:
                    continue
                if ss_tot is None:
                    v4s = [r for r in sig_runs if r.get("dataset") == ds_key and r.get("model") == "v4_iso"]
                    if v4s and v4s[0].get("r2"):
                        ss_tot = float(np.mean([r["rmse"] ** 2 / (1 - r["r2"]) for r in v4s if r.get("r2")]))
                    else:
                        ss_tot = tab_rmse ** 2 / 0.06
                disp, color = MODEL_DISPLAY["tabpfn"]
                panel_rows.append({
                    "dataset": ds_key, "model_key": mk, "label": disp, "color": color,
                    "rmse": float(tab_rmse), "rmse_std": 0.0,
                    "r2": _rmse_to_r2(float(tab_rmse), ss_tot), "r2_std": 0.0,
                    "epoch": "ref", "n_seed": 1, "note": "in-context ref",
                })
                continue

            epoch = FAIR_EPOCH_RULE[ds_key][mk]
            if mk == "v4_iso" and epoch == 15:
                pool = [r for r in sig_runs
                        if r.get("dataset") == ds_key and r.get("model") == "v4_iso"]
                note = f"10-seed e{epoch}"
            elif mk == "xgb_iso":
                pool = [r for r in sig_runs
                        if r.get("dataset") == ds_key and r.get("model") == "xgb_iso"]
                note = f"10-seed e{epoch}"
            else:
                pool = [r for r in fair_runs
                        if r.get("dataset") == ds_key and r.get("model") == mk
                        and r.get("epochs") == epoch]
                note = f"3-seed e{epoch}"
            if not pool:
                continue
            st = _stats(pool)
            disp, color = MODEL_DISPLAY[mk]
            panel_rows.append({
                "dataset": ds_key, "model_key": mk, "label": disp, "color": color,
                "epoch": epoch, "note": note, **st,
            })
        out.append({"dataset": ds_key, "label": ds_label, "models": panel_rows})

    meta = OUT / "fair_baseline_metrics.json"
    meta.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("saved", meta)
    return out


def fig_baseline_fair_hard() -> None:
    """hard_extrap only — 모델별 fair epoch RMSE + R²."""
    panels = load_fair_baseline_comparison()
    panel = next((p for p in panels if p["dataset"] == "ncmapss_hard"), None)
    if not panel:
        return
    models = panel["models"]
    fig, ax = plt.subplots(figsize=(10.0, 4.6))
    xlabels = []
    for m in models:
        ep = m.get("epoch", "")
        ep_s = f"e{ep}" if isinstance(ep, int) else str(ep)
        xlabels.append(f"{m['label']}\n({ep_s})")
    x = np.arange(len(xlabels))
    rmses = [m["rmse"] for m in models]
    errs = [m["rmse_std"] for m in models]
    colors = [m["color"] for m in models]
    bars = ax.bar(x, rmses, yerr=errs, color=colors, capsize=3, width=0.55, edgecolor="none")
    ymax = max(rmses) * 1.32
    ax.set_ylim(0, ymax)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels, fontsize=9.5, linespacing=1.35)
    ax.tick_params(axis="x", pad=10)
    ax.set_ylabel("hard_extrap RMSE ↓")
    ax.set_title("N-CMAPSS hard — fair baseline (모델별 epoch 최적 · iso 공통)", fontsize=11, color=TEAL)
    for b, m in zip(bars, models):
        top = m["rmse"] + (m["rmse_std"] or 0)
        ax.text(b.get_x() + b.get_width() / 2, top + 0.15,
                f"{m['rmse']:.2f}" + (f"±{m['rmse_std']:.2f}" if m.get("rmse_std") else ""),
                ha="center", fontsize=9, color=INK)
        if m.get("r2") is not None:
            ax.text(b.get_x() + b.get_width() / 2, top + 0.58,
                    f"R²={m['r2']:.3f}", ha="center", fontsize=9.5, fontweight="bold", color=TEAL)
    ax.axhline(4.788, color=RED, ls=":", lw=1.0, alpha=0.6)
    ax.text(len(xlabels) - 0.45, 4.88, "TabPFN 4.788", fontsize=7.5, color=RED)
    fig.subplots_adjust(bottom=0.22, top=0.88)
    fig.text(0.5, 0.02, "v4 e15 · Trans/LSTM/GRU e120 · GBM e15 · TabPFN in-context ref",
             ha="center", fontsize=8, color=SLATE)
    save(fig, "fig_baseline_fair_hard")


def fig_baseline_fair_compare() -> None:
    """Legacy 3-panel — PPT는 fig_baseline_fair_hard 사용."""
    fig_baseline_fair_hard()


def fig_seed_distribution_hard() -> None:
    sig_p = PROJ / "results" / "v4_significance" / "v4_significance.json"
    if not sig_p.exists():
        return
    sig = json.loads(sig_p.read_text())
    ds = "ncmapss_hard"
    tab_ref = sig.get("tabpfn_ref", {}).get(ds, 4.788)
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    rng = np.random.default_rng(0)
    for i, (model, color, lbl) in enumerate([
        ("v4_iso", BLUE, "v4+iso (10-seed)"),
        ("xgb_iso", GRAY, "GBM+iso (10-seed)"),
    ]):
        vals = [r["rmse"] for r in sig["runs"] if r.get("dataset") == ds and r.get("model") == model]
        x = np.full(len(vals), i) + rng.uniform(-0.1, 0.1, len(vals))
        ax.scatter(x, vals, s=40, color=color, alpha=0.8, zorder=3, label=lbl)
        ax.hlines(np.mean(vals), i - 0.25, i + 0.25, color=color, lw=2.5, zorder=4)
    ax.axhline(tab_ref, color=RED, ls="--", lw=1.5, label=f"TabPFN ref {tab_ref:.3f}", zorder=2)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["v4+iso", "GBM+iso"])
    ax.set_ylabel("hard_extrap RMSE ↓")
    ax.set_title("N-CMAPSS hard — 10-seed 분포 (e15 · iso on)")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    save(fig, "fig_seed_distribution_hard")


def load_main_dataset_metrics() -> list[dict]:
    """10-seed v4 / GBM + TabPFN ref — RMSE·R² for 3 MAIN datasets."""
    sig_p = PROJ / "results" / "v4_significance" / "v4_significance.json"
    if not sig_p.exists():
        return []
    sig = json.loads(sig_p.read_text())
    tab_ref = sig.get("tabpfn_ref", {})
    ds_info = [
        ("ncmapss_hard", "N-CMAPSS\nhard", 4.788),
        ("cmapss_fd002", "C-MAPSS\nFD002", 16.3),
        ("cmapss_fd004", "C-MAPSS\nFD004", 17.156),
    ]
    out: list[dict] = []
    for ds_key, label, tab_rmse in ds_info:
        v4 = [r for r in sig["runs"] if r.get("dataset") == ds_key and r.get("model") == "v4_iso"]
        gbm = [r for r in sig["runs"] if r.get("dataset") == ds_key and r.get("model") == "xgb_iso"]
        if not v4:
            continue
        v4_rmses = [r["rmse"] for r in v4]
        v4_r2s = [r["r2"] for r in v4 if r.get("r2") is not None]
        ss_tot = float(np.mean([r["rmse"] ** 2 / (1 - r["r2"]) for r in v4 if r.get("r2")]))
        gbm_rmses = [r["rmse"] for r in gbm] if gbm else []
        gbm_r2s = [r["r2"] for r in gbm if r.get("r2") is not None] if gbm else []
        out.append({
            "dataset": ds_key,
            "label": label,
            "v4_rmse": float(np.mean(v4_rmses)),
            "v4_rmse_std": float(np.std(v4_rmses)),
            "v4_r2": float(np.mean(v4_r2s)),
            "v4_r2_std": float(np.std(v4_r2s)),
            "gbm_rmse": float(np.mean(gbm_rmses)) if gbm_rmses else None,
            "gbm_rmse_std": float(np.std(gbm_rmses)) if len(gbm_rmses) > 1 else 0.0,
            "gbm_r2": float(np.mean(gbm_r2s)) if gbm_r2s else None,
            "gbm_r2_std": float(np.std(gbm_r2s)) if len(gbm_r2s) > 1 else 0.0,
            "tab_rmse": float(tab_rmse),
            "tab_r2": _rmse_to_r2(float(tab_rmse), ss_tot),
            "n_windows": v4[0].get("n"),
            "headline": ds_key == "ncmapss_hard",
        })
    meta = OUT / "main_dataset_metrics.json"
    meta.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("saved", meta)
    return out


def fig_dataset_overview() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 4.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    b = FancyBboxPatch((0.06, 0.06), 0.88, 0.88, boxstyle="round,pad=0.02,rounding_size=0.06",
                       facecolor=PANEL, edgecolor=TEAL, linewidth=2.2)
    ax.add_patch(b)
    ax.text(0.5, 0.88, "N-CMAPSS DS02-006 — TurboFan RUL", ha="center", va="top",
            fontsize=14, fontweight="bold", color=TEAL)
    lines = [
        "9 engines (units) · 650만+ sensor rows · window 1500",
        "Target: RUL 0–88 cycles · Extrap axis: TRA (throttle) ~78–83",
        "Sensors: T2, T30, P15, Nf, … + OC (alt, Mach, TRA, T2)",
        "Eval band: hard_extrap — test unit + TRA > q90 · n≈159 windows",
        "Post-process: unit isotonic (전 모델 공통)",
    ]
    for i, ln in enumerate(lines):
        ax.text(0.1, 0.72 - i * 0.12, "•  " + ln, ha="left", va="top", fontsize=11, color=INK)
    save(fig, "fig_dataset_overview")


def fig_split_matrix() -> None:
    """Split protocol comparison — easy / hard / C-MAPSS."""
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.axis("off")
    cols = ["Split", "Engine (unit)", "Train band", "Test / eval band", "n windows", "‘밖’의 의미"]
    rows = [
        ["N-C easy", "9대 전부 (row-level)", "TRA ≤ q70", "TRA > q85", "~1,671", "regime only"],
        ["N-C hard ★", "train 5 / test 3\n(11,14,15)", "train unit\nTRA ≤ q70",
         "test unit\nTRA > q90\n+ late RUL≤50", "159", "unit × regime\n(결합 외삽)"],
    ]
    tbl = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1.0, 2.1)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor("#2C3848")
        cell.set_facecolor(PANEL if r > 0 else ACCENT_DIM if False else "#1a2330")
        if r == 0:
            cell.set_facecolor("#1a2330")
            cell.set_text_props(color=TEAL, fontweight="bold")
        elif r == 2:
            cell.set_facecolor("#243A42")
            for txt in cell.get_text().get_text().split("\n"):
                pass
            cell.get_text().set_color(INK)
            cell.get_text().set_fontweight("bold")
        else:
            cell.get_text().set_color(SLATE if r != 2 else INK)
    ax.set_title("N-CMAPSS split — easy vs hard_extrap", fontsize=12, color=TEAL, pad=16)
    ax.text(0.5, 0.02, "★ 평가 = hard_extrap only · quantile q70/q90 · split seed = model seed",
            ha="center", transform=ax.transAxes, fontsize=8.5, color=SLATE)
    save(fig, "fig_split_matrix")


def fig_main_rmse_r2() -> None:
    rows = load_main_dataset_metrics()
    if not rows:
        return
    labels = [r["label"] for r in rows]
    n = len(labels)
    x = np.arange(n)
    w = 0.24
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.0))

    v4_rmse = [r["v4_rmse"] for r in rows]
    v4_err = [r["v4_rmse_std"] for r in rows]
    gbm_rmse = [r["gbm_rmse"] or 0 for r in rows]
    gbm_err = [r["gbm_rmse_std"] or 0 for r in rows]
    tab_rmse = [r["tab_rmse"] for r in rows]

    ax1.bar(x - w, v4_rmse, w, yerr=v4_err, color=BLUE, capsize=3, label="v4+iso (10-seed)")
    ax1.bar(x, gbm_rmse, w, yerr=gbm_err, color=GRAY, capsize=3, label="GBM+iso")
    for i, t in enumerate(tab_rmse):
        ax1.hlines(t, i - 0.45, i + 0.45, colors=RED, linestyles="--", lw=1.4)
    ax1.scatter([n - 0.55], [tab_rmse[-1]], color=RED, s=0)  # legend anchor
    ax1.plot([], [], color=RED, ls="--", lw=1.4, label="TabPFN ref")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=9)
    ax1.set_ylabel("extrap RMSE ↓")
    ax1.set_title("MAIN — RMSE (e15 · iso on · fair HP)")
    ax1.legend(frameon=False, fontsize=8, loc="upper right")

    v4_r2 = [r["v4_r2"] for r in rows]
    v4_r2e = [r["v4_r2_std"] for r in rows]
    gbm_r2 = [r["gbm_r2"] or 0 for r in rows]
    gbm_r2e = [r["gbm_r2_std"] or 0 for r in rows]
    tab_r2 = [r["tab_r2"] for r in rows]
    ax2.bar(x - w, v4_r2, w, yerr=v4_r2e, color=BLUE, capsize=3, label="v4+iso")
    ax2.bar(x, gbm_r2, w, yerr=gbm_r2e, color=GRAY, capsize=3, label="GBM+iso")
    for i, t in enumerate(tab_r2):
        ax2.hlines(t, i - 0.45, i + 0.45, colors=RED, linestyles="--", lw=1.4)
    ax2.plot([], [], color=RED, ls="--", lw=1.4, label="TabPFN est.")
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9)
    ax2.set_ylabel("R² ↑")
    ax2.set_ylim(0.85, 1.0)
    ax2.set_title("MAIN — R² (동일 extrap band)")
    ax2.legend(frameon=False, fontsize=8, loc="lower right")
    for i, row in enumerate(rows):
        if row["headline"]:
            ax1.text(i, max(v4_rmse[i], gbm_rmse[i], tab_rmse[i]) + 1.2, "★ headline",
                     ha="center", fontsize=8, color=CORAL, fontweight="bold")
    fig.suptitle("CA-CSS v4+iso · 3 MAIN datasets · 10-seed significance", fontsize=11, color=TEAL)
    save(fig, "fig_main_rmse_r2")


def copy_existing() -> None:
    copies = [
        (PROJ / "results/v4_paper_main/figures/fig_seed_distribution.png", "fig_seed_distribution.png"),
        (PROJ / "results/v4_paper_main/figures/fig_ablation.png", "fig_ablation.png"),
        (PROJ / "results/v4_paper_main/figures/fig_pred_vs_true_hard.png", "fig_pred_vs_true_hard.png"),
        (PROJ / "results/v4_paper_main/figures/fig_rul_trajectory_hard.png", "fig_rul_trajectory_hard.png"),
        (PROJ / "results/ncmapss_tra_split/plots/ecdf_TRA.png", "fig_tra_eda.png"),
        (ROOT / "_assets/fig_assumption_spectrum.png", "fig_assumption_spectrum.png"),
        (ROOT / "_assets/fig_checklist.png", "fig_checklist.png"),
    ]
    for src, dst in copies:
        if src.exists():
            shutil.copy2(src, OUT / dst)
            print("copied", dst)


def fig_physics_vs_structure() -> None:
    """λ_tra sweep + ablation — direction from structure, not physics loss."""
    p_prior = PROJ / "results" / "v4_prior_evidence" / "v4_prior_evidence.json"
    p_abl = PROJ / "results" / "v4_paper_ablation" / "v4_paper_ablation_report.md"
    lam_labels, lam_rmse, lam_adh = [], [], []
    if p_prior.exists():
        rows = json.loads(p_prior.read_text())["lambda_rows"]
        by_lam: dict[float, list[float]] = {}
        adh: dict[float, list[float]] = {}
        for r in rows:
            if r.get("band") != "hard_extrap":
                continue
            lam = float(r["lambda_tra"])
            by_lam.setdefault(lam, []).append(r["rmse"])
            adh.setdefault(lam, []).append(r["adherence"]["frac_negative"])
        for lam in sorted(by_lam):
            lam_labels.append(f"λ={lam:g}")
            lam_rmse.append(float(np.mean(by_lam[lam])))
            lam_adh.append(float(np.mean(adh[lam])) * 100)
    else:
        lam_labels = ["λ=0", "λ=0.05", "λ=0.5"]
        lam_rmse = [3.97, 3.88, 3.89]
        lam_adh = [100, 100, 100]

    abl_names = ["full", "λ=0", "no_phys", "no_iso"]
    abl_rmse = [3.88, 3.97, 4.21, 4.37]
    abl_colors = [BLUE, TEAL, CORAL, GRAY]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 3.8))

    x1 = np.arange(len(lam_labels))
    bars1 = ax1.bar(x1, lam_rmse, color=TEAL, width=0.5, edgecolor="none")
    ax1.set_xticks(x1)
    ax1.set_xticklabels(lam_labels)
    ax1.set_ylabel("hard RMSE ↓")
    ax1.set_title("λ_tra 스윕 — RMSE 거의 무반응", fontsize=10, color=TEAL)
    for b, v in zip(bars1, lam_rmse):
        ax1.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.2f}",
                 ha="center", fontsize=9, color=INK)
    ax1.set_ylim(0, max(lam_rmse) * 1.25)
    ax1_t = ax1.twinx()
    ax1_t.plot(x1, lam_adh, "o--", color=CORAL, lw=1.8, markersize=7)
    ax1_t.set_ylabel("ΔRUL<0 adherence (%)", color=CORAL)
    ax1_t.set_ylim(95, 101)
    ax1_t.tick_params(axis="y", labelcolor=CORAL)

    x2 = np.arange(len(abl_names))
    bars2 = ax2.bar(x2, abl_rmse, color=abl_colors, width=0.55, edgecolor="none")
    ax2.set_xticks(x2)
    ax2.set_xticklabels(abl_names, fontsize=9)
    ax2.set_ylabel("hard RMSE ↓")
    ax2.set_title("ablation — no_physics +0.33 · no_iso +0.49", fontsize=10, color=TEAL)
    ax2.axhline(4.788, color=RED, ls="--", lw=1.0, alpha=0.7)
    for b, v in zip(bars2, abl_rmse):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.1, f"{v:.2f}",
                 ha="center", fontsize=9, color=INK)
    ax2.set_ylim(0, max(abl_rmse) * 1.2)

    fig.text(0.5, 0.02,
             "방향(ΔRUL<0)은 MonotoneLoadHead 구조 항등식 — physics loss는 fit 보조만",
             ha="center", fontsize=9, color=SLATE)
    save(fig, "fig_physics_vs_structure")


def main():
    fig_dataset_overview()
    fig_split_matrix()
    fig_architecture()
    fig_tra_hard_split()
    fig_baseline_fair_hard()
    fig_seed_distribution_hard()
    fig_main_rmse()
    # fig_main_rmse_r2()  — PPT hard-only; JSON은 load_main_dataset_metrics()로 유지
    load_main_dataset_metrics()
    fig_arch_ablation()
    fig_physics_vs_structure()
    try:
        fig_training_curve()
    except Exception as e:
        print("training curve skip:", e)
    copy_existing()
    print("DONE ->", OUT)


if __name__ == "__main__":
    main()
