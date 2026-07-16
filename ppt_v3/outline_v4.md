# 외삽 50분 세미나 — v4 Outline (최종)

**작성일:** 2026-07-16  
**전략:** 제안안(산업 · Flip/Regime · MoE/Adapter/TTA) + v3 학술 골격(Hull · strict split · ReLU/PINN · N-CMAPSS) 하이브리드  
**분량:** 32장 / 50분

---

## 핵심 메시지

> 외삽은 피할 수 없다.  
> **엄밀한 측정(Hull · Extra R² · strict holdout)** + **구조(MoE · Adapter · 제약)** + **적응(TTA)** 으로 방어한다.

```
도입(8') → 현상(10') → 한계(5') → 해법(15') → 실전(10') → 마무리(2')
```

---

## 파일

| 항목 | 경로 |
|------|------|
| Outline (본 문서) | `ppt_v3/outline_v4.md` |
| PPT (v4) | `ppt_v3/외삽_50분_발표자료_v4.pptx` |
| 기존 PPT (v3) | `ppt_v3/외삽_50분_발표자료_v3.pptx` |
| Figure | `figures/` |
| 논문 (기존) | `extrapolation-papers/` |
| 논문 (추가) | `papers_to_add/` |

---

## Part 0 · 도입 (8분, Slide 1–5)

| # | 제목 | 핵심 한 줄 | Figure / 자산 | 논문 |
|---|------|-----------|-----------|------|
| 1 | 타이틀 | 외삽 완전 정복: 이론 → 현상 → 적응 → 실전 | — | — |
| 2 | 왜 지금 외삽인가 | 공정·센서·극한 조건은 **항상 train 범위를 벗어남** | 산업 실패 사례 1개 | — |
| 3 | 발표 로드맵 | 측정 → 현상 → 한계 → MoE/Adapter/TTA → Extra R² | `storyline_roadmap.png` | — |
| 4 | 보간 ≠ 외삽 | train hull **안=보간, 밖=외삽** | `pfister_extrapolation_fig2.png` | ★ Pfister & Bühlmann 2024 |
| 5 | Convex Hull + UQ | 고차원일수록 hull 밖 다수 · epistemic UQ 폭증 | `bonnasse_convex_hull_fig1.png`, `pfister_rmse_extrap_fig3.png` | ★ Bonnasse-Gahot 2022, Pfister 2024 |

**보조 인용:** Bartley et al. 2019 (다변량 CI 붕괴)

---

## Part 1 · OOD 물리/구조 현상 (10분, Slide 6–11)

| # | 제목 | 핵심 한 줄 | Figure | 논문 |
|---|------|-----------|--------|------|
| 6 | OOD란? | train과 다른 test 분포 = OOD | `ood_shift_diagram.png` | ★ Liu et al. 2023 |
| 7 | Covariate Shift vs Concept Drift | \(P(X)\) 변화 vs \(P(Y\|X)\) 변화 | `distribution_shift_types.png` | Liu 2023; (선택) Quinonero-Candela 2009 |
| 8 | ERM이 OOD에서 실패 | train 평균 최적 ≠ test 성공 | `ye_ood_failure_fig2.png` | ★ Ye et al. 2021, ★ Krueger et al. 2021 (REx) |
| 9 | Partial Correlation Flip | 정상 vs 극한에서 상관 **부호 역전** | 자체 다이어그램 | ★ Yuan et al. 2022, Schölkopf 2021 |
| 10 | Spurious correlation | 우연 상관 → regime 바뀌면 붕괴 | `irm_fig3_colored_mnist_setup.png` | ★ Arjovsky et al. 2019 (IRM) |
| 11 | Regime Shift | 비선형 상전이 → 오차 급증 | 시계열/phase 다이어그램 | Wu 2025 (OOD TS survey) |

---

## Part 2 · 왜 단순 모델로는 부족한가 (5분, Slide 12–14)

| # | 제목 | 핵심 한 줄 | Figure | 논문 |
|---|------|-----------|--------|------|
| 12 | ReLU MLP 외삽 실패 | hull 밖 → 조각별 **직선** | `xu_relu_extrapolation_fig1.png` | ★ Xu et al. 2021 |
| 13 | PINN도 외삽에서 깨짐 | 물리 넣어도 외삽 잔차 급증 | `fesser_pinn_failure_fig1.png` | ★ Fesser 2023, Raissi 2019 |
| 14 | 해법 예고 | **분할(MoE) · 잔차(Adapter) · 적응(TTA)** | 3박스 다이어그램 | — |

**필독 강등:** EQL, NALU, Monotonic NN → Slide 31

---

## Part 3 · 해법 딥다이브 (15분, Slide 15–22) ← 핵심

| # | 제목 | 핵심 한 줄 | 내용 | 논문 |
|---|------|-----------|------|------|
| 15 | 결합 아키텍처 | Gating → Expert/Adapter → (선택) TTA | **파이프라인 다이어그램 필수** | — |
| 16 | MoE 원리 | Regime별 Expert + Gating | Sparse MoE layer | ★ Shazeer et al. 2017 |
| 17 | MoE 함정 | Gating OOD 오분류 시 위험 | expert collapse / load balance | Shazeer 2017 |
| 18 | Residual Adapter | Base freeze · **잔차만** 학습 | 파라미터 효율 | ★ Rebuffi et al. 2017 |
| 19 | Adapter × Regime | 새 regime = 작은 adapter | MoE expert와 연결 | Rebuffi 2017 |
| 20 | TTA (Tent) | Test-time **entropy 최소화** | Unlabeled stream | ★ Wang et al. 2021 (Tent) |
| 21 | TTA 한계 | Latency · forgetting · noisy stream | on/off 규칙 | Tent |
| 22 | 왜 셋이 필요한가 | MoE=분할, Adapter=보정, TTA=적응 | 역할 분담 표 | DomainBed (ERM baseline) |

### 결합 구조

```
입력 x
  → Gating Network (regime 추정)
  → Expert_i + Residual Adapter_i
  → 예측 ŷ
  → (고엔트로피/OOD 시) Tent-style TTA로 소수 파라미터 업데이트
```

| 방법 | 푸는 문제 | 실패 모드 |
|------|-----------|-----------|
| MoE | 단일 모델 전 regime 과적합 | gating 오분류 |
| Adapter | full fine-tune 불안정·고비용 | regime 라벨 애매 |
| TTA | 배포 후 분포 이동 | latency, drift |

**비교 원칙:** 항상 **ERM baseline** 포함 (Gulrajani & Lopez-Paz 2020 DomainBed)

---

## Part 4 · 실험·검증 (10분, Slide 23–28)

| # | 제목 | 핵심 한 줄 | 내용 | 논문 |
|---|------|-----------|------|------|
| 23 | 평가 철학 | random split = 보간 평가일 수 있음 | Hull 밖 / holdout 축 명시 | Ye 2021, Pfister 2024 |
| 24 | Extra R² | **순수 외삽 구간** \(R^2\) | 전체 \(R^2\)와 대비 | — |
| 25 | 데이터셋 A | Naval Propulsion / CCPP | holdout 축 필수 | UCI 벤치마크 |
| 26 | 데이터셋 B | N-CMAPSS TRA holdout · strict_late | v3 ACT5 재사용 | N-CMAPSS, TabPFN |
| 27 | 결과 | MoE+Adapter+TTA vs ERM | Extra R² + Flip 구간 | — |
| 28 | 실전 교훈 | strict split 없으면 승리는 환상 | APEX-Guard L1–L3 | — |

### 실험 체크리스트

1. Holdout 축 명시 (고온/고부하/late cycle/미관측 unit)
2. Train hull 밖 test만 Extra R²에 포함
3. Baseline: ERM (동일 HP·모델 크기)
4. Ablation: MoE / Adapter / TTA / Full
5. Flip·Regime 구간 별도 리포트

---

## Part 5 · 결론 (2분, Slide 29–32)

| # | 제목 | 내용 |
|---|------|------|
| 29 | Key Takeaways | ① Hull ② Flip/Regime ③ MoE·Adapter·TTA ④ Extra R² |
| 30 | 한계·Future | TTA latency · gating OOD · adapter 라벨 · 인과 결합 |
| 31 | 필독 논문 Top 8 | 아래 필수 8편 |
| 32 | Q&A | — |

---

## 필수 논문 8편 (슬라이드에 명시)

| # | 논문 | 역할 | 경로 | 상태 |
|---|------|------|------|------|
| 1 | Pfister & Bühlmann 2024 | Hull·외삽 정의 | `extrapolation-papers/01_foundations/` | ✅ |
| 2 | Xu et al. 2021 | NN 외삽 한계 | `.../03_neural_network_extrapolation/` | ✅ |
| 3 | Ye et al. 2021 | OOD framework / ERM 실패 | `.../02_OOD_generalization/` | ✅ |
| 4 | Arjovsky et al. 2019 IRM | spurious / 상관 역전 | `papers_to_add/02_OOD/` | ✅ |
| 5 | Shazeer et al. 2017 MoE | 분할 정복 | `papers_to_add/03_NN/` + extrapolation-papers | ✅ **신규** |
| 6 | Wang et al. 2021 Tent | TTA | 동일 | ✅ **신규** |
| 7 | Rebuffi et al. 2017 Adapters | 잔차 어댑터 | 동일 | ✅ **신규** |
| 8 | Gulrajani & Lopez-Paz 2020 | ERM baseline 공정 비교 | `.../02_OOD_generalization/` | ✅ |

### 보조 인용

| 논문 | 역할 | 상태 |
|------|------|------|
| Bonnasse-Gahot 2022 | Hull 시각 | ✅ |
| Bartley 2019 | 다변량 CI | ✅ |
| Fesser 2023 | PINN 외삽 실패 | ✅ |
| Krueger 2021 REx | Risk extrapolation | ✅ **신규** |
| Yuan 2022 OOD Mechanics | mechanism shift | ✅ |
| Schölkopf 2021 | 인과 표현 | ✅ |
| Liu 2023 OOD Survey | 정의·분류 | ✅ |
| Raissi 2019 PINN | 물리 제약 | ✅ |
| Wu 2025 OOD Time Series | regime/시계열 | ✅ |

### 확보 실패 / 수동 필요

| 논문 | 이유 | 대안 |
|------|------|------|
| Quinonero-Candela 2009 *Dataset Shift* | MIT Press 서적 (공개 PDF 없음) | Liu 2023 survey로 대체 인용 |
| Shimodaira 2000 Covariate Shift | JMLR 403 | Liu/Ye로 대체 |
| Haley & Soloway 1992 | IEEE paywall | Xu 2021로 대체 (동일 메시지) |

---

## v3 → v4 리매핑

| v3 | 처리 | v4 |
|----|------|-----|
| ACT1 Hull·UQ | 살림(축약) | Part 0 |
| ACT2 OOD·Ye | 살림 | Part 1 |
| ACT3 IRM·GroupDRO·DomainBed | 대폭 축약 | Flip용 IRM 1장 + DomainBed 1문장 |
| ACT4 ReLU·PINN | 살림 2–3장 | Part 2 |
| ACT4 EQL·NALU·Monotonic | 필독 강등 | Slide 31 |
| ACT5 N-CMAPSS | 살림 | Part 4 |
| (신규) Flip·Regime | 신규 | Part 1 |
| (신규) MoE·Adapter·TTA | 신규 핵심 | Part 3 |

---

## 시간 스크립트

| 분 | 내용 |
|----|------|
| 0–2 | 타이틀·산업 동기 |
| 2–8 | Hull·보간/외삽·UQ |
| 8–18 | Shift · ERM 실패 · Flip · Regime · IRM |
| 18–23 | ReLU·PINN 한계 |
| 23–38 | MoE → Adapter → TTA → 결합 |
| 38–48 | Extra R² · 데이터 · 결과 |
| 48–50 | Takeaways · Q&A |

---

## 실행 체크리스트

**콘텐츠**
- [ ] Flip 예시 1개 확정 (수치·산점도)
- [ ] 결합 아키텍처 다이어그램 1장
- [ ] Extra R² 수식·구간 정의
- [ ] Holdout 프로토콜 (Naval/CCPP 및/또는 N-CMAPSS)
- [ ] Ablation 표

**논문**
- [x] MoE, Tent, Adapter, REx 다운로드
- [ ] Quinonero-Candela / Shimodaira (선택·수동)

**Figure 재사용**
- [ ] Pfister, Bonnasse, Xu, Fesser, Ye, IRM, APEX/N-CMAPSS

---

## 신규 다운로드 파일 (2026-07-16)

```
papers_to_add/03_NN/Shazeer2017_Sparsely_Gated_MoE.pdf          # arXiv:1701.06538
papers_to_add/03_NN/Wang2021_Tent_Test_Time_Adaptation.pdf      # arXiv:2006.10726
papers_to_add/03_NN/Rebuffi2017_Residual_Adapters.pdf            # arXiv:1705.08045
papers_to_add/02_OOD/Krueger2021_Risk_Extrapolation_REx.pdf      # arXiv:2003.00688

# 동일 파일 복사본
extrapolation-papers/03_neural_network_extrapolation/Shazeer2017_Sparsely_Gated_MoE.pdf
extrapolation-papers/03_neural_network_extrapolation/Wang2021_Tent_Test_Time_Adaptation.pdf
extrapolation-papers/03_neural_network_extrapolation/Rebuffi2017_Residual_Adapters.pdf
extrapolation-papers/02_OOD_generalization/Krueger2021_Risk_Extrapolation_REx.pdf
```
