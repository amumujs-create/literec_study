#!/usr/bin/env python3
"""PPT에 쓰이는 모든 Figure 존재·크기 점검."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
BUILD = Path(__file__).resolve().parent / "build_ppt_v3.py"

REQUIRED = sorted(set(re.findall(r'fig\("([^"]+)"\)', BUILD.read_text())))


def main():
    lines = ["# Figure 점검 리포트\n", f"경로: `{FIG}`\n\n", "| Figure | 상태 | 크기 | 해상도 |\n", "|--------|------|------|--------|\n"]
    ok = 0
    for name in REQUIRED:
        p = FIG / name
        if not p.exists():
            lines.append(f"| {name} | **없음** | - | - |\n")
            continue
        im = Image.open(p)
        w, h = im.size
        kb = p.stat().st_size // 1024
        flag = "OK" if w >= 800 and kb >= 20 else "주의"
        if flag == "OK":
            ok += 1
        lines.append(f"| {name} | {flag} | {kb}KB | {w}×{h} |\n")
    lines.append(f"\n**{ok}/{len(REQUIRED)}** Figure 정상\n")
    out = Path(__file__).resolve().parent / "figure_audit.md"
    out.write_text("".join(lines), encoding="utf-8")
    print("".join(lines))
    print(f"saved -> {out}")


if __name__ == "__main__":
    main()
