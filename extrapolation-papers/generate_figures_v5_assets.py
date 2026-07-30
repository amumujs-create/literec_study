#!/usr/bin/env python3
"""Regenerate _assets for v5 PPT — no baked-in Figure. captions."""
from __future__ import annotations

import os
import re
from pathlib import Path

import generate_figures_v4 as g4

ROOT = Path(__file__).resolve().parent
GEN = ROOT / "_gen_src"


def strip_and_run(path: Path) -> None:
    code = path.read_text(encoding="utf-8")
    code = re.sub(r"\nfig\.suptitle\([\s\S]*?\)\n", "\n", code)
    code = re.sub(r"\nfig\.text\(0\.02, 0\.9[\d]+,[\s\S]*?\)\n", "\n", code)

    def bump(m: re.Match[str]) -> str:
        return f"top={min(0.96, float(m.group(1)) + 0.10)}"

    code = re.sub(r"top=([0-9.]+)", bump, code)
    glo = {"__name__": "__main__", "Path": Path}
    exec(compile(code, str(path), "exec"), glo, glo)  # noqa: S102


def main() -> None:
    os.chdir(ROOT)
    g4._rc()  # dark console theme — required before v4 figure functions
    print("v4 figures…")
    for fn in (
        g4.fig_interp_extrap,
        g4.fig_convex_hull,
        g4.fig_poly_extrap,
        g4.fig_identifiability,
        g4.fig_error_decomp,
        g4.fig_relu_affine,
        g4.fig_uq,
        g4.fig_method_cases,
        g4.fig_method_decision,
        g4.fig_fail_cases,
    ):
        fn()

    # Remove roadmap / unused blocks before strip+run
    extra = (GEN / "v5_extra_figs.py").read_text(encoding="utf-8")
    extra = re.sub(r"# ── 1\. three questions[\s\S]*?print\(\"1 ok\"\)\n\n", "", extra)
    (GEN / "v5_extra_figs.py").write_text(extra, encoding="utf-8")

    spectrum = (GEN / "v5_spectrum.py").read_text(encoding="utf-8")
    spectrum = re.sub(r"# ── 2\. summary chain[\s\S]*", "", spectrum)
    (GEN / "v5_spectrum.py").write_text(spectrum, encoding="utf-8")

    print("v5 figures…")
    for name in (
        "v5_extra_figs.py",
        "v5_companion_figs.py",
        "v5_assumption_figs.py",
        "v5_spectrum.py",
        "v5_ood_figs.py",
        "v5_ood_vs_extrap_fig.py",
        "v5_physics_loss_fig.py",
        "v6_method_cases_fig.py",
        "v6_verification_guide_fig.py",
        "v6_closing_practical_fig.py",
    ):
        strip_and_run(GEN / name)
    print("done")


if __name__ == "__main__":
    main()
