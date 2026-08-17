# Extrapolation Papers

외삽(Extrapolation) 관련 논문 모음 — **50분 발표** 기반 문헌 정리

원본 레포: https://github.com/amumujs-create/literec_study

---

## 발표자료 (권장)

> **통합본: `외삽_문헌조사_통합.pptx`** — v4 기초 + v5 심화 + v6 실전 + CA-CSS 사례 (125장). 한 파일로 읽기.

| 파일 | 설명 |
|------|------|
| **`외삽_문헌조사_통합.pptx`** | **권장** · 한글 섹션 구분 · v4+v5+v6+사례 |
| `외삽_50분_발표자료_v4.pptx` | 기초 문헌 (Hull · OOD · 신경망 외삽) |
| `외삽_50분_발표자료_v5_심화.pptx` | 가정 스펙트럼 · UQ · abstention |
| `외삽_50분_발표자료_v6.pptx` | 실전 가정 검증 · 체크리스트 |
| `외삽_50분_사례_CA-CSS_v4_부록.pptx` | N-CMAPSS / CA-CSS 사례 |
| **`paper_pdfs/`** | **전체 PDF 모음** (여기만 열어봐도 됨) |
| **`INDEX.md`** | 목록·분류 한눈에 |
| **`회귀_외삽_추가문헌.md`** | 01→05 순서 · **회귀** 쪽으로 이은 추가 18편 |
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
| King2006_Dangers_Extreme_Counterfactuals.pdf | King & Zeng | 2006 | https://gking.harvard.edu/files/counterft.pdf |
| Balestriero2021_Learning_High_Dimension_Extrapolation.pdf | Balestriero et al. | 2021 | https://arxiv.org/abs/2110.09485 |
| Shen2024_Engression_Distributional_Regression.pdf | Shen & Meinshausen | 2024 | https://arxiv.org/abs/2307.00835 |
| Dong2024_Progression_Extrapolation_Regression.pdf | Dong & Ma | 2024 | https://arxiv.org/abs/2410.23246 |

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
| Sugiyama2007_Direct_Importance_Estimation.pdf | Sugiyama et al. | 2007 | NeurIPS 2007 |
| Rothenhausler2021_Anchor_Regression.pdf | Rothenhäusler et al. | 2021 | https://arxiv.org/abs/1801.06229 |

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
| Sahoo2018_Learning_Equations_Extrapolation_Control.pdf | Sahoo, Lampert, Martius | 2018 | https://arxiv.org/abs/1806.07259 |
| Rahaman2019_Spectral_Bias_Neural_Networks.pdf | Rahaman et al. | 2019 | https://arxiv.org/abs/1806.08734 |
| Brunton2016_SINDy_Discovering_Governing_Equations.pdf | Brunton, Proctor, Kutz | 2016 | https://arxiv.org/abs/1509.03580 |
| Li2021_Fourier_Neural_Operator.pdf | Li et al. | 2021 | https://arxiv.org/abs/2010.08895 |

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
| Severson2019_Battery_Cycle_Life_Prediction.pdf | Severson et al. | 2019 | https://doi.org/10.1038/s41560-019-0356-8 |
| Attia2021_Statistical_Learning_Battery_Lifetime.pdf | Attia, Severson, Witmer | 2021 | https://arxiv.org/abs/2101.01885 |
| AriasChao2021_N-CMAPSS_Dataset.pdf | Arias Chao et al. | 2021 | https://doi.org/10.3390/data6010005 |

---

## 05. Uncertainty Quantification — 불확실성 정량화

| 파일명 | 저자 | 연도 | DOI/링크 |
|--------|------|------|----------|
| Ghahramani2013_Bayesian_Nonparametrics.pdf | Ghahramani | 2013 | https://doi.org/10.1098/rsta.2011.0553 |
| Wang2024_Extrapolation_Driven_PINN_Architecture.pdf | Wang et al. | 2024 | https://arxiv.org/abs/2406.12460 |
| Gal2016_Dropout_Bayesian_Approximation.pdf | Gal & Ghahramani | 2016 | https://arxiv.org/abs/1506.02142 |
| Lakshminarayanan2017_Deep_Ensembles.pdf | Lakshminarayanan et al. | 2017 | https://arxiv.org/abs/1612.01474 |
| Kendall2017_What_Uncertainties_Do_We_Need.pdf | Kendall & Gal | 2017 | https://arxiv.org/abs/1703.04977 |
| Kuleshov2018_Accurate_Uncertainties_Deep_Learning.pdf | Kuleshov et al. | 2018 | https://arxiv.org/abs/1807.00263 |
| Romano2019_Conformalized_Quantile_Regression.pdf | Romano, Patterson, Candès | 2019 | https://arxiv.org/abs/1905.03222 |

회귀 쪽으로 이은 이유·읽는 순서: [`회귀_외삽_추가문헌.md`](회귀_외삽_추가문헌.md)

---

*총 36편 + 회귀 추가 18편 | 추가 수집일: 2026-08-17*
