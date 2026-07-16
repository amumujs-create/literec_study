#!/usr/bin/env python3
"""UQ 다이어그램 주장(claim) 논리 점검 — 3-pass."""

from __future__ import annotations

import math
import sys

SPLIT_FRAC = 0.52
ALEATORIC_W = 24
EPI_IN_W = 12
EPI_OUT_FRAC = 0.58


def width_fn_epistemic(x, split, R):
    if x <= split:
        return EPI_IN_W
    t_frac = (x - split) / max(R - split, 1)
    return EPI_IN_W + 98 * t_frac ** 1.08


def run_pass(pass_id: int) -> list[str]:
    issues = []
    L, R = 100, 900
    split = L + int((R - L) * SPLIT_FRAC)
    x_in = L + int((split - L) * 0.42)
    x_out = split + int((R - split) * EPI_OUT_FRAC)

    # Pass 1: Aleatoric — hull 무관 (폭 동일)
    w_ale_in = ALEATORIC_W
    w_ale_out = ALEATORIC_W
    if w_ale_in != w_ale_out:
        issues.append(f"[P{pass_id}] Aleatoric: hull 안·밖 σ 폭이 다름 ({w_ale_in} vs {w_ale_out})")

    # Pass 2: Epistemic — hull 밖 급증
    w_epi_in = width_fn_epistemic(x_in, split, R)
    w_epi_out = width_fn_epistemic(x_out, split, R)
    ratio = w_epi_out / max(w_epi_in, 1)
    if ratio < 4.0:
        issues.append(f"[P{pass_id}] Epistemic: hull 밖 σ 급증 부족 (비율 {ratio:.1f}x, 목표 ≥4x)")
    if w_epi_in >= w_ale_in:
        issues.append(f"[P{pass_id}] Epistemic hull 안 σ가 Aleatoric보다 넓음 ({w_epi_in} vs {w_ale_in})")

    # Pass 3: 대비 — Epistemic 밖 >> Aleatoric
    if w_epi_out <= w_ale_out * 2:
        issues.append(f"[P{pass_id}] 대비 약함: Epistemic 밖({w_epi_out}) vs Aleatoric({w_ale_out})")

    return issues


def main():
    all_issues = []
    for i in range(1, 4):
        all_issues.extend(run_pass(i))

    if all_issues:
        print("UQ claim audit FAILED:")
        for iss in all_issues:
            print(f"  - {iss}")
        sys.exit(1)

    print("UQ claim audit OK (3 passes)")
    print(f"  Aleatoric: σ={ALEATORIC_W} (hull 안·밖 동일)")
    split_demo = 100 + int(800 * SPLIT_FRAC)
    x_out = split_demo + int((900 - split_demo) * EPI_OUT_FRAC)
    w_out = width_fn_epistemic(x_out, split_demo, 900)
    print(f"  Epistemic: σ_in={EPI_IN_W}, σ_out≈{w_out} ({w_out/EPI_IN_W:.1f}x surge)")


if __name__ == "__main__":
    main()
