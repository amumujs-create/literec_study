#!/usr/bin/env python3
"""v4용 개념 다이어그램 (PIL only — numpy/matplotlib 의존 없음)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FIG = Path(__file__).resolve().parent.parent / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def _font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/nanum/NanumBarunGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _rounded(draw, box, fill, outline, width=3, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _center_text(draw, box, text, font, fill="#0f172a"):
    x0, y0, x1, y1 = box
    lines = text.split("\n")
    # estimate line height
    ascent = font.size + 4
    total_h = ascent * len(lines)
    y = y0 + (y1 - y0 - total_h) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = x0 + (x1 - x0 - w) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += ascent


def _arrow(draw, x0, y, x1, fill="#334155"):
    draw.line([(x0, y), (x1 - 10, y)], fill=fill, width=4)
    draw.polygon([(x1, y), (x1 - 14, y - 7), (x1 - 14, y + 7)], fill=fill)


def pipeline():
    w, h = 1600, 420
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    font = _font(28, bold=True)
    font_s = _font(20)
    boxes = [
        (40, 120, 260, 280, "입력 x", "#f1f5f9"),
        (320, 120, 620, 280, "Gating\n(regime)", "#dbeafe"),
        (680, 120, 1080, 280, "Expert + Adapter", "#ccfbf1"),
        (1140, 120, 1340, 280, "예측 ŷ", "#fef3c7"),
        (1400, 120, 1560, 280, "TTA\n(선택)", "#fce7f3"),
    ]
    for x0, y0, x1, y1, t, c in boxes:
        _rounded(d, (x0, y0, x1, y1), c, "#0e7490")
        _center_text(d, (x0, y0, x1, y1), t, font)
    for i in range(len(boxes) - 1):
        _arrow(d, boxes[i][2] + 4, 200, boxes[i + 1][0] - 4)
    _center_text(d, (0, 320, w, 400),
                 "제안 결합 구조 · MoE(Shazeer) · Adapter(Rebuffi) · TTA(Tent) — 개별 모듈만 논문 근거",
                 font_s, fill="#64748b")
    img.save(FIG / "v4_combine_pipeline.png")


def solution_preview():
    w, h = 1400, 360
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    font = _font(32, bold=True)
    font_s = _font(20)
    items = [
        (60, "MoE\n분할", "#dbeafe"),
        (500, "Adapter\n잔차 보정", "#ccfbf1"),
        (940, "TTA\n테스트시 적응", "#fce7f3"),
    ]
    for x, t, c in items:
        _rounded(d, (x, 60, x + 380, 250), c, "#0e7490")
        _center_text(d, (x, 60, x + 380, 250), t, font)
    _center_text(d, (0, 280, w, 350),
                 "Part 3 예고 — 각 방법은 논문 Figure·인용으로만 소개",
                 font_s, fill="#64748b")
    img.save(FIG / "v4_solution_preview.png")


def correlation_flip():
    """개념도: regime에 따라 상관 부호가 바뀔 수 있음 (Yuan/IRM 메시지)."""
    w, h = 1400, 520
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    font = _font(26, bold=True)
    font_s = _font(18)
    # left panel: positive
    _rounded(d, (40, 60, 660, 460), "#f8fafc", "#0e7490")
    _center_text(d, (40, 70, 660, 120), "Regime A (정상 운전)", font, "#0f172a")
    # scatter-ish positive
    pts_a = [(120, 380), (180, 340), (240, 300), (300, 250), (360, 210), (420, 160), (500, 120)]
    for x, y in pts_a:
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill="#0284c7")
    d.line([(110, 400), (520, 100)], fill="#0369a1", width=5)
    _center_text(d, (40, 410, 660, 450), "부분상관 ≈ +  (같은 방향)", font_s, "#0369a1")
    # right panel: negative
    _rounded(d, (740, 60, 1360, 460), "#fff7ed", "#c2410c")
    _center_text(d, (740, 70, 1360, 120), "Regime B (극한/고부하)", font, "#0f172a")
    pts_b = [(820, 140), (880, 180), (940, 230), (1000, 280), (1060, 320), (1120, 360), (1200, 400)]
    for x, y in pts_b:
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill="#ea580c")
    d.line([(810, 120), (1220, 410)], fill="#c2410c", width=5)
    _center_text(d, (740, 410, 1360, 450), "부분상관 ≈ −  (부호 역전 가능)", font_s, "#c2410c")
    _center_text(
        d, (0, 470, w, 510),
        "개념도 — 환경/메커니즘이 바뀌면 상관 구조가 흔들릴 수 있음 (Yuan 2022 · IRM/spurious)",
        font_s, "#64748b",
    )
    img.save(FIG / "v4_correlation_flip.png")


def regime_shift():
    w, h = 1400, 420
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    font = _font(24, bold=True)
    font_s = _font(18)
    # timeline bars
    phases = [
        (60, "Regime 1\n저부하", "#dbeafe"),
        (400, "전이 구간\n비선형", "#fef3c7"),
        (740, "Regime 2\n고부하", "#fecaca"),
        (1080, "미관측\n외삽", "#e2e8f0"),
    ]
    for x, t, c in phases:
        _rounded(d, (x, 80, x + 280, 260), c, "#334155")
        _center_text(d, (x, 80, x + 280, 260), t, font)
    for i in range(3):
        x0 = phases[i][0] + 280
        x1 = phases[i + 1][0]
        _arrow(d, x0 + 4, 170, x1 - 4)
    _center_text(
        d, (0, 300, w, 400),
        "시계열·공정: 국소 regime이 바뀌면 통계·역학이 달라짐 → 단일 전역 ERM이 취약\n"
        "(개념: Yuan mechanism shift · Wu OOD Time Series survey)",
        font_s, "#64748b",
    )
    img.save(FIG / "v4_regime_shift.png")


def eval_philosophy():
    w, h = 1500, 400
    img = Image.new("RGB", (w, h), "#ffffff")
    d = ImageDraw.Draw(img)
    font = _font(26, bold=True)
    font_s = _font(18)
    boxes = [
        (40, 70, 360, 280, "1. Holdout 축\n고부하·late·unit", "#dbeafe"),
        (400, 70, 720, 280, "2. Hull 밖만\nExtra R²", "#ccfbf1"),
        (760, 70, 1080, 280, "3. ERM baseline\n동일 HP", "#fef3c7"),
        (1120, 70, 1460, 280, "4. Ablation\n모듈 기여", "#fce7f3"),
    ]
    for x0, y0, x1, y1, t, c in boxes:
        _rounded(d, (x0, y0, x1, y1), c, "#0e7490")
        _center_text(d, (x0, y0, x1, y1), t, font)
    _center_text(
        d, (0, 310, w, 380),
        "평가 철학 — Pfister(hull) · Ye(OOD) · DomainBed(ERM) 정신을 운영 지표로 번역",
        font_s, "#64748b",
    )
    img.save(FIG / "v4_eval_philosophy.png")


if __name__ == "__main__":
    pipeline()
    solution_preview()
    correlation_flip()
    regime_shift()
    eval_philosophy()
    for name in [
        "v4_combine_pipeline.png",
        "v4_solution_preview.png",
        "v4_correlation_flip.png",
        "v4_regime_shift.png",
        "v4_eval_philosophy.png",
    ]:
        print("OK", FIG / name)
