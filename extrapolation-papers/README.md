# Extrapolation Papers

외삽(Extrapolation) 관련 논문 모음 — **50분 발표** 기반 문헌 정리

원본 레포: https://github.com/amumujs-create/literec_study

---

## 발표자료 (권장)

> **고정본: `외삽_50분_발표자료_v4.pptx`** (PDF 버튼). 그래프 수정본은 **`외삽_50분_발표자료_v8.pptx`** (S03·S10 훈련점 피팅).


| 파일 | 설명 |
|------|------|
| **`외삽_50분_발표자료_v8.pptx`** | **그래프 수정본** · S03 가정·S10 식별불가 곡선이 훈련점을 통과 |
| **`외삽_50분_발표자료_v4.pptx`** | **고정본** · PDF 버튼 46개 · `paper_pdfs/` 상대링크 |
| **`paper_pdfs/`** | **전체 PDF 39편 모음** (여기만 열어봐도 됨) |
| **`INDEX.md`** | 목록·분류 한눈에 |
| `열기.command` | 더블클릭 → PPT + paper_pdfs + INDEX 열기 |
| `외삽_완전정복_학습노트.pdf` | 복습 노트 |
| `_assets/paper_figs/` | 논문 Figure 크롭 |
| `01_`~`05_/` | 주제별 원본 |

### 50분 타임라인

| Part | 내용 | 시간 |
|------|------|------|
| 1 | 기초 이론 (Hull · Richardson · UQ) | 11분 |
| 2 | OOD (IRM · DomainBed · 시계열) | 11분 |
| 3 | 신경망 외삽 (Xu · EQL · NALU · Mono · PINN) | 14분 |
| 4 | N-CMAPSS APEX-Guard / strict_late | 10분 |
| 5 | 동향 · 필독 · 적용 | 4분 |
| — | Q&A | 별도 |

---

## 폴더 구조

```
extrapolation-papers/
├── 01_foundations/                  # 외삽의 고전적 통계 토대
├── 02_OOD_generalization/           # OOD (Out-of-Distribution) 일반화
├── 03_neural_network_extrapolation/ # 딥러닝/신경망 외삽 방법론
├── 04_battery_engineering/          # 배터리·공학 응용 (RUL 예측)
├── 05_uncertainty_quantification/   # 불확실성 정량화 + Bayesian 접근
└── _assets/                         # v3 발표용 그림
```

---

## 01. Foundations — 외삽 통계 이론 기초

| 파일명 | 저자 | 연도 | DOI/링크 |
|--------|------|------|----------|
| Pfister2024_Extrapolation-Aware_Nonparametric_Inference.pdf | Pfister & Bühlmann | 2024 | https://arxiv.org/abs/2402.09758 |
| Teckentrup2024_Probabilistic_Richardson_Extrapolation.pdf | Teckentrup et al. | 2024 | https://doi.org/10.1093/jrsssb/qkae098 |
| Bartley2019_Characterizing_Extrapolation_Multivariate.pdf | Bartley et al. | 2019 | https://arxiv.org/abs/1906.07036 |
| Muckley2023_Interpretable_Models_Extrapolation_SciML.pdf | Muckley et al. | 2023 | https://arxiv.org/abs/2212.10283 |
| Tsai2024_Trend_Extrapolation_Methods_Review.pdf | Tsai et al. | 2024 | https://arxiv.org/abs/2401.02549 |

---

## 02. OOD Generalization — 분포 이동 & 도메인 일반화

| 파일명 | 저자 | 연도 | DOI/링크 |
|--------|------|------|----------|
| Liu2023_OOD_Generalization_Survey.pdf | Liu et al. | 2023 | https://arxiv.org/abs/2108.13624 |
| Arjovsky2021_OOD_Generalization_in_ML.pdf | Arjovsky | 2021 | https://arxiv.org/abs/2103.02667 |
| Ye2022_OoD-Bench.pdf | Ye et al. | 2022 | https://arxiv.org/abs/2106.03721 |
| Ye2021_Theoretical_Framework_OOD.pdf | Ye et al. | 2021 | https://arxiv.org/abs/2106.04496 |
| Gulrajani2020_In_Search_of_Lost_Domain_Generalization.pdf | Gulrajani & Lopez-Paz | 2020 | https://arxiv.org/abs/2007.01434 |
| Nagarajan2024_Failure_Modes_OOD.pdf | Nagarajan et al. | 2024 | https://arxiv.org/abs/2010.15775 |
| Yu2024_Survey_Evaluation_OOD.pdf | Yu et al. | 2024 | https://arxiv.org/abs/2403.01874 |
| Wu2025_OOD_Time_Series_Survey.pdf | Wu et al. | 2025 | https://arxiv.org/abs/2503.13868 |
| Ahuja2022_Invariance_IB_OOD.pdf | Ahuja et al. | 2022 | https://arxiv.org/abs/2106.06607 |
| Yuan2022_OOD_Mechanics.pdf | Yuan et al. | 2022 | https://arxiv.org/abs/2206.14917 |
| Krueger2021_Risk_Extrapolation_REx.pdf | Krueger et al. | 2021 | https://arxiv.org/abs/2003.00688 |

---

## 03. Neural Network Extrapolation — 신경망 외삽 방법론

| 파일명 | 저자 | 연도 | DOI/링크 |
|--------|------|------|----------|
| Xu2021_How_Neural_Networks_Extrapolate.pdf | Xu et al. | 2021 | https://arxiv.org/abs/2009.11848 |
| Bonnasse-Gahot2022_Interpolation_Extrapolation_NN.pdf | Bonnasse-Gahot | 2022 | https://arxiv.org/abs/2207.08648 |
| Bay2024_ML_vs_DL_Generalization.pdf | Bay & Yearick | 2024 | https://arxiv.org/abs/2403.01621 |
| Martius2016_Extrapolation_Learning_Equations_EQL.pdf | Martius & Lampert | 2016 | https://arxiv.org/abs/1610.02995 |
| Trask2018_Neural_Arithmetic_Logic_Units_NALU.pdf | Trask et al. | 2018 | https://arxiv.org/abs/1808.00508 |
| Netanyahu2023_Learning_to_Extrapolate_Transductive.pdf | Netanyahu et al. | 2023 | https://arxiv.org/abs/2304.14329 |
| Webb2023_Representations_Supporting_Extrapolation.pdf | Webb et al. | 2023 | https://arxiv.org/abs/2007.05059 |
| Decugis2024_Extrapolation_Power_Implicit_Models.pdf | Decugis et al. | 2024 | https://arxiv.org/abs/2407.14430 |
| Runje2023_Constrained_Monotonic_NN.pdf | Runje & Shankaranarayana | 2023 | https://arxiv.org/abs/2205.11775 |
| Liu2022_Certified_Monotonic_NN.pdf | Liu et al. | 2022 | https://arxiv.org/abs/2011.10219 |
| Fesser2023_Extrapolation_Failures_PINNs.pdf | Fesser et al. | 2023 | https://arxiv.org/abs/2306.09478 |
| Zhu2022_Reliable_Extrapolation_DeepONet.pdf | Zhu et al. | 2022 | https://arxiv.org/abs/2212.06347 |
| Hay2024_Function_Extrapolation_Manifolds.pdf | Hay & Sharon | 2024 | https://arxiv.org/abs/2405.10563 |
| Shazeer2017_Sparsely_Gated_MoE.pdf | Shazeer et al. | 2017 | https://arxiv.org/abs/1701.06538 |
| Wang2021_Tent_Test_Time_Adaptation.pdf | Wang et al. | 2021 | https://arxiv.org/abs/2006.10726 |
| Rebuffi2017_Residual_Adapters.pdf | Rebuffi et al. | 2017 | https://arxiv.org/abs/1705.08045 |

---

## 04. Battery Engineering — 배터리 수명 외삽 응용

| 파일명 | 저자 | 연도 | DOI/링크 |
|--------|------|------|----------|
| Li2023_Predicting_Battery_Lifetime_Varying_Conditions.pdf | Li et al. | 2023 | https://arxiv.org/abs/2307.08382 |
| Xue2025_Survival_Analysis_Battery_RUL.pdf | Xue et al. | 2025 | https://arxiv.org/abs/2503.13558 |
| Fernandez2021_Review_Online_Battery_RUL.pdf | Fernandez et al. | 2021 | https://doi.org/10.3389/fmech.2021.719718 |
| Aykol2021_Physics_ML_Battery_Lifetime.pdf | Aykol et al. | 2021 | https://doi.org/10.1149/1945-7111/ABEC55 |
| Magrini2024_Review_Degradation_RUL_LiIon.pdf | Magrini et al. | 2024 | https://doi.org/10.3390/s24113382 |
| Laufer2022_ML_Lifetime_Prediction_LiIon.pdf | Laufer et al. | 2022 | https://doi.org/10.1002/advs.202200630 |

---

## 05. Uncertainty Quantification — 불확실성 정량화

| 파일명 | 저자 | 연도 | DOI/링크 |
|--------|------|------|----------|
| Ghahramani2013_Bayesian_Nonparametrics.pdf | Ghahramani | 2013 | https://doi.org/10.1098/rsta.2011.0553 |
| Wang2024_Extrapolation_Driven_PINN_Architecture.pdf | Wang et al. | 2024 | https://arxiv.org/abs/2406.12460 |

---

*총 40편+ | 수집일: 2026-07-02 · v4 추가: 2026-07-16*

---

## 발표자료

| 파일 | 설명 |
|------|------|
| `../ppt_v3/외삽_50분_발표자료_v3.pptx` | v3 (37장) — Hull→OOD→알고리즘→N-CMAPSS |
| `../ppt_v3/build_ppt_v3.py` | v3 PPT 재생성 스크립트 |
| `../ppt_v3/outline_v3.md` | v3 outline |
| **`../ppt_v3/outline_v4.md`** | **v4 최종 outline** (MoE+Adapter+TTA 하이브리드) |

## 추가 논문

- **2026-07-13** `../papers_to_add/` — IRM, GroupDRO, PINN, DeepONet, WILDS, TabPFN 등
- **2026-07-16** MoE (Shazeer), Tent (Wang), Residual Adapters (Rebuffi), REx (Krueger)
