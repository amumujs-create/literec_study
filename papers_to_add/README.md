# 추가 논문 (papers_to_add)

v3 발표자료 보강 (2026-07-13) + **v4 해법 논문** (2026-07-16).

## 01_foundations

| 파일 | 저자 | 연도 | 링크 | 용도 | 상태 |
|------|------|------|------|------|------|
| *(비어 있음)* | — | — | — | Quinonero-Candela 2009은 MIT Press 서적 → 공개 PDF 없음 | ❌ 수동/대체 |

## 02_OOD

| 파일 | 저자 | 연도 | 링크 | 용도 |
|------|------|------|------|------|
| Arjovsky2019_Invariant_Risk_Minimization.pdf | Arjovsky et al. | 2019 | https://arxiv.org/abs/1907.02893 | IRM, Colored MNIST |
| Sagawa2020_GroupDRO.pdf | Sagawa et al. | 2020 | https://arxiv.org/abs/1911.08731 | GroupDRO |
| Sun2016_CORAL_Correlation_Alignment.pdf | Sun & Saenko | 2016 | https://arxiv.org/abs/1607.01719 | CORAL |
| Scholkopf2021_Toward_Causal_Representation_Learning.pdf | Schölkopf et al. | 2021 | https://arxiv.org/abs/2104.11123 | 인과 ML |
| Ganin2016_Domain_Adversarial_Training.pdf | Ganin et al. | 2016 | https://arxiv.org/abs/1505.07818 | DANN |
| BenDavid2010_Domain_Adaptation_Theory.pdf | Ben-David et al. | 2010 | https://arxiv.org/abs/0902.3430 | DA 이론 |
| **Krueger2021_Risk_Extrapolation_REx.pdf** | Krueger et al. | 2021 | https://arxiv.org/abs/2003.00688 | **REx · ERM OOD 실패** (v4 신규) |

## 03_NN

| 파일 | 저자 | 연도 | 링크 | 용도 |
|------|------|------|------|------|
| Raissi2019_Physics_Informed_Neural_Networks.pdf | Raissi et al. | 2019 | https://arxiv.org/abs/1711.10566 | PINN |
| Lu2021_Learning_Nonlinear_Operators_DeepONet.pdf | Lu et al. | 2021 | https://arxiv.org/abs/1910.03193 | DeepONet |
| **Shazeer2017_Sparsely_Gated_MoE.pdf** | Shazeer et al. | 2017 | https://arxiv.org/abs/1701.06538 | **MoE** (v4 신규) |
| **Wang2021_Tent_Test_Time_Adaptation.pdf** | Wang et al. | 2021 | https://arxiv.org/abs/2006.10726 | **Tent / TTA** (v4 신규) |
| **Rebuffi2017_Residual_Adapters.pdf** | Rebuffi et al. | 2017 | https://arxiv.org/abs/1705.08045 | **Residual Adapters** (v4 신규) |

## 06_benchmarks

| 파일 | 저자 | 연도 | 링크 | 용도 |
|------|------|------|------|------|
| Koh2021_WILDS_Benchmark.pdf | Koh et al. | 2021 | https://arxiv.org/abs/2012.07421 | WILDS |
| Hollmann2022_TabPFN.pdf | Hollmann et al. | 2022 | https://arxiv.org/abs/2207.01848 | TabPFN baseline |

## 다운로드 실패 (수동 보완 / 대체 인용)

| 논문 | 이유 | 발표 시 대체 |
|------|------|-------------|
| Quinonero-Candela et al. 2009 *Dataset Shift in ML* | MIT Press 서적, 공개 PDF 없음 | Liu et al. 2023 OOD Survey |
| Shimodaira 2000 Covariate Shift (JMLR) | jmlr.org 403 | Liu / Ye 2021 |
| Haley & Soloway 1992 (IEEE IJCNN) | IEEE paywall | Xu et al. 2021 |

---

## 07_rul_extrapolation (2026-08-17 조사)

일반 외삽 카드(01–06)와 별개. **RUL에서 밖이 네 갈래**라는 분류용.  
본문: `ca-css-ncmapss/docs/RUL_EXTRAPOLATION_SURVEY.md` · 목록: [`../extrapolation-papers/06_rul_extrapolation/README.md`](../extrapolation-papers/06_rul_extrapolation/README.md)

| 파일 | 저자 | 연도 | 링크 | 유형 | 상태 |
|------|------|------|------|------|------|
| Costa2023_DA_Operation_Profile_RUL.pdf | Costa et al. | 2023 | https://doi.org/10.1016/j.ress.2023.109718 | A 운용위상 DA | ❌ 수집 대기 |
| Severson2019_Battery_Cycle_Life_Early.pdf | Severson et al. | 2019 | https://doi.org/10.1038/s41560-019-0356-8 | B 조기예측 원전 | ❌ 수집 대기 |
| EviAdapt2025_Evidential_DA_Incomplete_RUL.pdf | EviAdapt | 2025 | https://doi.org/10.1109/tim.2025.3551977 | A+B 불완전열화 | ❌ 수집 대기 (실험은 함) |
| CruiseBench2026_NCMAPSS_Cruise_Benchmark.pdf | CruiseBench | 2026 | https://arxiv.org/abs/2607.19380 | D 인접 벤치 | ❌ 수집 대기 |
| TurbofanDA2025_Review.pdf | — | 2025 | https://arxiv.org/abs/2510.03604 | A 서베이 | ❌ 수집 대기 |
| CURA2025_SourceFree_RUL.pdf | CURA | 2025 | MSSP / github.com/keyplay/CURA | A source-free | ❌ 수집 대기 |
| Chen2025_DTL_Machinery_RUL_Review.pdf | Chen et al. | 2025 | https://doi.org/10.1088/1361-6501/ad8940 | A 리뷰 | ❌ 수집 대기 |
| BatteryGPT2025_Early_Degradation.pdf | BatteryGPT | 2025 | https://doi.org/10.1038/s41467-025-66819-0 | B | ❌ 수집 대기 |
| PhyResBiLSTM2025.pdf | PhyRes-BiLSTM | 2025 | https://doi.org/10.1109/ieeeconf65522.2025.11137054 | C 단조 PINN | ❌ 수집 대기 |
| PHME_ConstraintGuided_RUL.pdf | PHME | — | https://papers.phmsociety.org/index.php/phme/article/download/4897/2946 | C CGGD | ❌ 수집 대기 |

관련 outline: [`../ppt_v3/outline_v4.md`](../ppt_v3/outline_v4.md)
