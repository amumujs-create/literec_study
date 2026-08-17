# 06. RUL Extrapolation — 잔존수명에서 외삽이 네 갈래인 이유

일반 외삽(01–05)과 배터리 리뷰(04)만으로는 RUL 논문을 분류할 수 없다.  
**조사 본문:** 연구 레포 `ca-css-ncmapss/docs/RUL_EXTRAPOLATION_SURVEY.md` (2026-08-17).

---

## 네 유형

| 유형 | 밖 | 대표 | 우리 |
|------|----|------|------|
| **A. 도메인 이동** | FD / 비행급 / 하중 라벨 | Costa 2023, EviAdapt, CURA | 옆줄 (재현 실패) |
| **B. 시간축 조기예측** | 초반 → EOL | Severson 2019, BatteryGPT | 배터리 실험은 여기. 본편 아님 |
| **C. 물리 제약** | 반사실 방향·단조 | PINN, CMNN, PhyRes, CGGD | H1 / TRA 공동 지표 |
| **D. typed 기하** | hull · TRA quantile · unit×regime | Pfister, Bartley + **우리 Hard** | **본편** |

**본편 인사이트:** `데이터 → TabPFN → RUL` vs `데이터 + 구조 prior → 모델 → RUL`.  
hard(범위가 갈라진 시험)에서 foundation 사전학습만으로는 부족하고, 문제에 맞는 구조 prior가 추가 이득. 평균보다 최악 시드. C-MAPSS SOTA로 확장 금지.

---

## 추가 수집 대상 (아직 PDF 없음)

| 우선 | 파일명 제안 | 링크 | 유형 |
|------|-------------|------|------|
| ★★★ | Costa2023_DA_Operation_Profile_RUL.pdf | https://doi.org/10.1016/j.ress.2023.109718 | A |
| ★★★ | Severson2019_Battery_Cycle_Life_Early.pdf | https://doi.org/10.1038/s41560-019-0356-8 | B |
| ★★★ | EviAdapt2025_Evidential_DA_Incomplete_RUL.pdf | https://doi.org/10.1109/tim.2025.3551977 | A+B |
| ★★ | CruiseBench2026_NCMAPSS_Cruise_Benchmark.pdf | https://arxiv.org/abs/2607.19380 | D 인접 |
| ★★ | TurbofanDA2025_Review.pdf | https://arxiv.org/abs/2510.03604 | A |
| ★★ | CURA2025_SourceFree_RUL.pdf | https://github.com/keyplay/CURA | A |
| ★ | Chen2025_DTL_Machinery_RUL_Review.pdf | https://doi.org/10.1088/1361-6501/ad8940 | A |
| ★ | BatteryGPT2025_Early_Degradation.pdf | https://doi.org/10.1038/s41467-025-66819-0 | B |
| ★ | PhyResBiLSTM2025.pdf | https://doi.org/10.1109/ieeeconf65522.2025.11137054 | C |
| ★ | PHME_ConstraintGuided_RUL.pdf | https://papers.phmsociety.org/index.php/phme/article/download/4897/2946 | C |

04_battery에 이미 있는 Aykol / Laufer / Magrini / Fernandez / Li / Xue는 **다시 받지 말 것.**
