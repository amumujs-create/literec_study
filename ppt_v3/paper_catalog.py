#!/usr/bin/env python3
"""발표에 쓰는 핵심 논문 목록 — Figure 추출 + PDF 첨부용."""

from __future__ import annotations

# key figures to extract: fig_num -> output filename
# papers: relative to literec_study root
PAPERS: list[dict] = [
    {
        "id": "bartley2019",
        "short": "Bartley 2019",
        "title": "Characterizing Extrapolation in Multivariate Models",
        "act": "ACT 1",
        "why": "다변량 회귀에서 CI·외삽 구간이 깨지는 실제 사례",
        "pdf": "extrapolation-papers/01_foundations/Bartley2019_Characterizing_Extrapolation_Multivariate.pdf",
        "figs": {1: "bartley_chla_tp.png"},
    },
    {
        "id": "pfister2024",
        "short": "Pfister 2024",
        "title": "Extrapolation-Aware Nonparametric Inference",
        "act": "ACT 1",
        "why": "보간 vs 외삽 · extrapolation-aware CI의 이론적 근거",
        "pdf": "extrapolation-papers/01_foundations/Pfister2024_Extrapolation-Aware_Nonparametric_Inference.pdf",
        "figs": {2: "pfister_extrapolation_fig2.png", 3: "pfister_rmse_extrap_fig3.png"},
    },
    {
        "id": "bonnasse2022",
        "short": "Bonnasse-Gahot 2022",
        "title": "Interpolation, Extrapolation & Neural Networks",
        "act": "ACT 1",
        "why": "내재 공간 hull ≠ 신경 표현 공간 hull",
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Bonnasse-Gahot2022_Interpolation_Extrapolation_NN.pdf",
        "figs": {1: "bonnasse_convex_hull_fig1.png"},
    },
    {
        "id": "ye2021",
        "short": "Ye 2021",
        "title": "Theoretical Framework for OOD Generalization",
        "act": "ACT 2",
        "why": "OOD expansion · train 평균 최적 ≠ test 성공",
        "pdf": "extrapolation-papers/02_OOD_generalization/Ye2021_Theoretical_Framework_OOD.pdf",
        "figs": {1: "ye_ood_expansion_fig1.png", 2: "ye_ood_failure_fig2.png"},
    },
    {
        "id": "arjovsky2019",
        "short": "Arjovsky 2019",
        "title": "Invariant Risk Minimization (IRM)",
        "act": "ACT 3",
        "why": "환경 불변 표현 · SCM · Colored MNIST",
        "pdf": "papers_to_add/02_OOD/Arjovsky2019_Invariant_Risk_Minimization.pdf",
        "figs": {3: "irm_scm_fig3.png"},
    },
    {
        "id": "sagawa2020",
        "short": "Sagawa 2020",
        "title": "GroupDRO — Distributionally Robust Optimization",
        "act": "ACT 3",
        "why": "최악 그룹(worst-group) 보호 · Waterbirds/CelebA",
        "pdf": "papers_to_add/02_OOD/Sagawa2020_GroupDRO.pdf",
        "figs": {1: "sagawa_groupdro_fig1.png"},
    },
    {
        "id": "gulrajani2020",
        "short": "Gulrajani 2020",
        "title": "In Search of Lost Domain Generalization (DomainBed)",
        "act": "ACT 3",
        "why": "공정 비교 시 ERM ≥ 기존 OOD SOTA",
        "pdf": "extrapolation-papers/02_OOD_generalization/Gulrajani2020_In_Search_of_Lost_Domain_Generalization.pdf",
        "figs": {},  # Figure 캡션 형식 비표준 — PDF만 첨부
    },
    {
        "id": "xu2021",
        "short": "Xu 2021",
        "title": "How Neural Networks Extrapolate",
        "act": "ACT 4",
        "why": "ReLU MLP hull 밖 직선화 · GNN 구조 prior",
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Xu2021_How_Neural_Networks_Extrapolate.pdf",
        "figs": {1: "xu_relu_extrapolation_fig1.png", 2: "xu_gnn_arch_fig2.png"},
    },
    {
        "id": "martius2016",
        "short": "Martius 2016",
        "title": "EQL — Extrapolation & Learning Equations",
        "act": "ACT 4",
        "why": "연산 트리로 해석 가능한 수식 학습",
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Martius2016_Extrapolation_Learning_Equations_EQL.pdf",
        "figs": {1: "eql_architecture_fig1.png"},
    },
    {
        "id": "trask2018",
        "short": "Trask 2018",
        "title": "NALU — Neural Arithmetic Logic Units",
        "act": "ACT 4",
        "why": "±·×÷ 구조 내장 · 큰 수 외삽",
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Trask2018_Neural_Arithmetic_Logic_Units_NALU.pdf",
        "figs": {2: "nalu_architecture_fig2.png", 4: "trask_nalu_extrap_fig4.png"},
    },
    {
        "id": "runje2023",
        "short": "Runje 2023",
        "title": "Constrained Monotonic Neural Networks",
        "act": "ACT 4",
        "why": "단조 제약 Dense Unit · 외삽 안전성",
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Runje2023_Constrained_Monotonic_NN.pdf",
        "figs": {
            1: "runje_monotonic_fig1.png",
            3: "runje_monotonic_unit_fig3.png",
            4: "runje_monotonic_arch_fig4.png",
        },
    },
    {
        "id": "raissi2019",
        "short": "Raissi 2019",
        "title": "Physics-Informed Neural Networks (PINN)",
        "act": "ACT 4",
        "why": "L = L_data + λ·L_physics",
        "pdf": "papers_to_add/03_NN/Raissi2019_Physics_Informed_Neural_Networks.pdf",
        "figs": {1: "raissi_pinn_solution.png"},
    },
    {
        "id": "fesser2023",
        "short": "Fesser 2023",
        "title": "Extrapolation Failures of PINNs",
        "act": "ACT 4",
        "why": "PINN도 외삽 구간에서 실패 → UQ 필요",
        "pdf": "extrapolation-papers/03_neural_network_extrapolation/Fesser2023_Extrapolation_Failures_PINNs.pdf",
        "figs": {1: "fesser_pinn_failure_fig1.png"},
    },
]


def layout_jobs() -> list[dict]:
    """extract_figures_layout.py PAPER_JOBS 형식."""
    return [{"pdf": p["pdf"], "figs": p["figs"]} for p in PAPERS if p["figs"]]
