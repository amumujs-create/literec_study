#!/usr/bin/env python3
"""논문 Figure — 영문 캡션 제거 + 한글 설명 오버레이."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from diagram_style import load_font

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"

# crop_ratio: 상단만 유지(영문 캡션 잘림), title/sub: 하단 한글 배너
ANNOTATIONS: dict[str, dict] = {
    "bartley_chla_tp.png": {
        "crop": 0.84,
        "title": "Bartley 2019 Fig.1 — Chl a vs TP 회귀",
        "sub": "어두운 회색 = 외삽 구간 · 빨간 점선 = 95% 예측구간",
    },
    "pfister_extrapolation_fig2.png": {
        "crop": 0.92,
        "title": "Pfister 2024 Fig.2 — 선형 vs 비선형 외삽",
        "sub": "OLS/RF는 지원 밖에서 실패 · extrapolation-aware CI",
    },
    "pfister_rmse_extrap_fig3.png": {
        "crop": 0.90,
        "title": "Pfister 2024 Fig.3 — 외삽 구간 RMSE",
        "sub": "train 밖(D_out)에서 OLS 고정 · RF/SVR/MLP 개선",
    },
    "bonnasse_convex_hull_fig1.png": {
        "crop": 0.88,
        "title": "Bonnasse-Gahot 2022 Fig.1 — Convex Hull",
        "sub": "내재 공간 hull 안 ≠ 신경 표현 공간 hull 안",
    },
    "liu_ood_scm_fig1.png": {
        "crop": 0.88,
        "title": "Liu 2023 Fig.1 — IV vs Anchor Regression SCM",
        "sub": "OOD·인과: hidden confounder H 처리",
    },
    "ye_ood_expansion_fig1.png": {
        "crop": 0.90,
        "title": "Ye 2021 Fig.1 — OOD expansion function",
        "sub": "Office-Home · 가용 환경 vs 전체 환경",
    },
    "ye_ood_failure_fig2.png": {
        "crop": 0.95,
        "title": "Ye 2021 Fig.2 — OOD failure case",
        "sub": "train 평균 최적 ≠ test(다른 도메인) 성공",
    },
    "xu_relu_extrapolation_fig1.png": {
        "crop": 0.88,
        "title": "Xu 2021 Fig.1 — ReLU MLP 외삽 실패",
        "sub": "훈련 범위 밖 → 직선화 · 비선형 근사 불가",
    },
    "xu_activation_fig3.png": {
        "crop": 0.88,
        "title": "Xu 2021 Fig.3–4 — 활성화·분포별 외삽",
        "sub": "ReLU / Tanh / Sin · train 분포 = 외삽 가정",
    },
    "irm_fig3_colored_mnist_setup.png": {
        "crop": 0.90,
        "title": "Arjovsky 2019 Fig.3 — Colored MNIST SCM",
        "sub": "Z₁=인과 feature · Z₂=spurious(색)",
    },
    "irm_fig4_results_bars.png": {
        "crop": 0.88,
        "title": "Arjovsky 2019 Fig.4 — 인과 vs 비인과 weight",
        "sub": "IRM만 test(줄무늬)에서 non-causal 억제",
    },
    "domainbed_table1.png": {
        "crop": 0.92,
        "title": "Gulrajani 2020 Table 1 — DomainBed 결과",
        "sub": "공정 HP 탐색 시 ERM ≥ 기존 OOD SOTA",
    },
    "groupdro_spurious_examples.png": {
        "crop": 0.90,
        "title": "Sagawa 2020 Fig.1 — spurious correlation",
        "sub": "Waterbirds · CelebA · MultiNLI",
    },
    "eql_architecture_fig1.png": {
        "crop": 0.88,
        "title": "Martius 2016 Fig.1 — EQL 구조",
        "sub": "sin·cos·×·÷ 연산 트리 → 해석 가능 수식",
    },
    "nalu_architecture_fig2.png": {
        "crop": 0.88,
        "title": "Trask 2018 Fig.2 — NAC / NALU 구조",
        "sub": "NAC(±) + exp/log gate(×÷)",
    },
    "trask_nalu_extrap_fig4.png": {
        "crop": 0.88,
        "title": "Trask 2018 Fig.4 — NALU 외삽 성능",
        "sub": "train 2자리 → test 4자리 · NALU만 100%",
    },
    "runje_monotonic_fig1.png": {
        "crop": 0.88,
        "title": "Runje 2023 Fig.1 — 단조 NN 근사",
        "sub": "일반 ReLU vs Constrained Monotonic NN",
    },
    "fesser_pinn_failure_fig1.png": {
        "crop": 0.88,
        "title": "Fesser 2023 Fig.1 — PINN 외삽 실패",
        "sub": "보간 OK · 외삽 구간 오차·잔차 급증",
    },
    "raissi_pinn_solution.png": {
        "crop": 0.88,
        "title": "Raissi 2019 — PINN Burgers 해",
        "sub": "L = L_data + λ·L_physics",
    },
}


def annotate_one(path: Path, crop: float, title: str, sub: str):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    if crop < 1.0:
        img = img.crop((0, 0, w, int(h * crop)))

    banner = 72
    out = Image.new("RGB", (img.width, img.height + banner), "#ffffff")
    out.paste(img, (0, 0))
    d = ImageDraw.Draw(out)
    d.line([(0, img.height), (img.width, img.height)], fill="#cccccc", width=1)
    d.text((16, img.height + 8), title, fill="#1a1a1a", font=load_font(20, bold=True))
    d.text((16, img.height + 36), sub, fill="#666666", font=load_font(15))
    out.save(path, optimize=True)


def main():
    load_font()
    for name, cfg in ANNOTATIONS.items():
        path = FIG / name
        if not path.exists():
            print(f"SKIP {name}")
            continue
        annotate_one(path, cfg["crop"], cfg["title"], cfg["sub"])
        print(f"OK {name}")


if __name__ == "__main__":
    main()
