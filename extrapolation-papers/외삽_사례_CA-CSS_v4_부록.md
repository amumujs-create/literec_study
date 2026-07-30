# 외삽 50분 발표 — **사례 부록** · CA-CSS v4 (N-CMAPSS)

**본편 PPT:** `외삽_50분_발표자료_v5_심화.pptx` (S33 **뒤**에 붙일 별도 장)  
**관통 문장 (본편 echo):** 밖을 지탱하는 것은 데이터가 **아니라 가정**이다 — **우리 사례에서 그 가정을 구조에 넣고, S30 체크 4항으로 검증했다.**

> 본편 PPT에는 **넣지 않음**. 이 문서를 보고 슬라이드 10~12장을 별도 deck으로 만든다.

---

## 이 부록 읽는 법

| 구분 | 보면 되는 곳 |
|------|-------------|
| **발표 중** | 각 장 **슬라이드** → **⓪ 흐름** → **② 대본** |
| **슬라이드 제작** | **③ 장표 핵심 (카드)** + 표·수치 |
| **논문/리포트** | `results/v4_paper_main/PAPER_WEAKNESSES_AND_RESULTS.md` |

---

## 목차·시간 (부록 ~12분)

| 부 | 장 | 시간 | 내용 |
|----|-----|------|------|
| 연결 | A01 | 1분 | 본편 S33 → 사례 브릿지 |
| **1. 문제 정의** | A02–A04 | 2.5분 | RUL + **결합 외삽** 정의 |
| **2. 가정** | A05–A07 | 3분 | counterfactual prior + **구조 보장** |
| **3. 실험** | A08–A09 | 2분 | 프로토콜·baseline·ablation |
| **4. 결과** | A10–A11 | 2.5분 | RMSE·구조 ablation·일관성 |
| **5. 검증** | A12–A13 | 2.5분 | S30 체크 4항 + **정직 서술** |
| 마무리 | A14 | 0.5분 | 한 줄 takeaway |

---

## 본편 연결 맵

| 본편 장 | 부록에서의 대응 |
|---------|----------------|
| S10 · 훈련 범위 | A03 — TRA q70/q90 밴드, hard = **밖** |
| S15 · 대응법 지도 | A05 — 방법②(방향) + ③(물리-informed) **하이브리드** |
| S20 · CMNN | A06 — **구조에 단조·방향 내장** (loss 아님) |
| S27 · 검증 동기 | A12 — 라벨에 없는 관계 → **별도 검증 필수** |
| S30 · 체크 4항 | A12–A13 — 4항 **전부** 적용 사례 |

---

# Part 1 · 문제 정의

## A01 · 브릿지 — 본편에서 우리 사례로 {#a01}

**슬라이드 A01/N14**

### ⓪ 발표 흐름

**역할:** S33 Q&A 직후 — “이론을 **우리 데이터**에 적용하면?”

**앞에서:** 본편 결론 — *가정 + 검증*.

**다음으로:** **무엇을 예측하고, 어디를 ‘밖’이라 부르는지** (A02).

### ② 발표 대본

```text
[45초]
대본: 본편 33장은 ‘외삽’의 정의·실패·대응·검증 프레임이었습니다. 
이제 같은 프레임으로 **실제 사례** 하나를 끝까지 밀어 보겠습니다.
항공 엔진 **남은 수명(RUL)** 예측, N-CMAPSS, TabPFN급 baseline 대비.
순서는 본편과 같습니다 — 문제 정의, 가정, 실험, 결과, 검증.
관통 문장은 그대로입니다: 밖은 데이터가 아니라 **가정**으로 버티고, 
그 가정이 맞는지는 **체크 4항**으로 확인합니다.
```

### ③ 장표 핵심

- **과제:** Turbofan RUL — CA-CSS v4 + isotonic
- **Headline 데이터셋:** N-CMAPSS **hard** (결합 외삽)
- **비교:** TabPFN v8 · GBM · LSTM/GRU/Transformer
- **5단:** 문제 → 가정 → 실험 → 결과 → 검증

**하단 takeaway:** 본편 이론의 **실전 적용 예** — 슬라이드 deck 분리

---

## A02 · 무엇을 예측하는가 — RUL과 좌표 {#a02}

**슬라이드 A02/N14**

### ⓪ 발표 흐름

**역할:** 예측 대상·입력 좌표 고정.

**다음으로:** “**어디가 밖**인가” — A03.

### ② 발표 대본

```text
[1분]
대본: 예측 대상은 **Remaining Useful Life**, 남은 사이클 수입니다.
입력은 멀티센서 시계열 — 온도, 압력, 회전수, 그리고 **TRA(스로틀·부하)**.
본편 S05–S06에서 말한 ‘좌표’가 여기서 TRA 축입니다.
RUL 라벨 자체는 **EOL − 현재 cycle**로 정의됩니다.
중요한 한 줄 — **같은 시점에서 TRA를 올려도 라벨 RUL은 안 바뀝니다.**
per-sample로는 ∂RUL/∂TRA = 0입니다. 
이게 뒤에서 ‘물리 가정’ 서술할 때 꼭 필요합니다.
```

### ③ 장표 핵심

| 항목 | 내용 |
|------|------|
| Target | RUL (cycles), cap 88 (N-CMAPSS) |
| Driver | **TRA** — 외삽 축 (regime shift) |
| Context | 20+ 센서 + OC(운용조건) |
| 라벨 성질 | cycle 기반 — **순간 TRA와 무관** |

**하단 takeaway:** 외삽 문제 = **TRA 축** 밖 — 라벨은 cycle만 본다

---

## A03 · 어디가 ‘밖’인가 — hard split {#a03}

**슬라이드 A03/N14**

### ⓪ 발표 흐름

**역할:** S30 ① “진짜 밖인가?” — **프로토콜 정의**.

**다음으로:** 가정 파트 (A05).

### ② 발표 대본

```text
[1.5분]
대본: ‘밖’을 두 겹으로 겹칩니다 — 본편 S28의 diversity + correlation shift가 동시에 옵니다.
첫째, **unit holdout**: 훈련에 없던 엔진(unit)에서 테스트.
둘째, **regime holdout**: 그 test unit 안에서도 TRA > q90 구간만 평가.
이걸 **hard_extrap** 밴드라 부릅니다. n≈159 windows — 작아서 seed 민감합니다.
쉬운 비교 — **easy**: 같은 데이터셋에서 TRA > q85만 밖 (unit은 섞임).
표준 C-MAPSS FD002/004는 TRA quantile **extrap_test** 한 축.
핵심 주장은 **hard**에만 걸립니다: 
“축 하나만 밖”이 아니라 **엔진도 새 + 부하도 높음** — 결합 일반화.
```

### ③ 장표 핵심

| split | train | test (평가 밴드) | “밖”의 의미 |
|-------|-------|------------------|-------------|
| **hard** | train unit, TRA≤q70 | **test unit**, TRA>q90 | unit × regime |
| easy | TRA≤q70 | TRA>q85 (unit 혼합) | regime only |
| FD002/004 | op quantile train | extrap_test (op 밖) | 단일 축 |

**그림 제안:** TRA 축에 q70 / q90 표시 + test unit만 q90 오른쪽 강조

**하단 takeaway:** hard = **S30 ① 통과** — test ∩ train support = ∅ (unit·regime)

---

## A04 · 왜 어려운가 — baseline도 여기서 깨짐 {#a04}

**슬라이드 A04/N14** *(선택 — 시간 없으면 A03에 합침)*

### ② 발표 대본

```text
[45초]
대본: 이 밴드에서 TabPFN v8 ref RMSE 4.79, GBM+iso 5.74, LSTM/GRU는 16 전후로 붕괴.
충분히 학습한 Transformer도 4.8~5.0에서 정체 — v4(3.88)와 격차.
즉 “아무 NN”이 아니라 **프로토콜이 난이도를 만든다**는 뜻입니다.
```

### ③ 장표 핵심 (hard_extrap · **fair protocol**)

> **fair** = e15 · val/fix HP · **test set 튜닝 ✗**  
> 실험 때 test HP 튜닝 baseline은 RMSE 더 낮게 나올 수 있음 — **본 장 수치와 다름** (공정 비교 아님)

| model | RMSE↓ | R²↑ | proto |
|-------|------:|----:|-------|
| **v4+iso** | **3.88±0.80** | **0.950** | 3-seed e15 |
| TabPFN v8 | 4.79 | ≈0.94 | in-context ref |
| GBM+iso | 5.74±0.49 | 0.908 | 10-seed e15 |
| LSTM+iso | 16.0±1.4 | **0.292** | 5-seed e15 |

**해석:** RMSE 격차 크지만 — v4·GBM·TabPFN은 **R² 0.91~0.97** (여전히 차이 있음). LSTM은 R²≈0.29로 **설명력도 붕괴**.

---

# Part 2 · 가정

## A05 · 가정 스펙트럼 — 우리가 넣은 것 {#a05}

**슬라이드 A05/N14**

### ⓪ 발표 흐름

**역할:** S15 지도 위에 **우리 핀** 박기.

**다음으로:** 구조 설계 (A06).

### ② 발표 대본

```text
[1.5분]
대본: 본편 S15 가로축 — 사전 지식 강도. 우리는 **② 방향 + ③ 물리-informed** 사이.
수식(EQL)까지는 모릅니다. 대신 세 가지를 넣습니다.
(1) **시간 방향** — 같은 unit에서 cycle↑면 RUL↓ (단조, H1).
(2) **부하 방향** — 지속 고부하 → 열화 가속 (counterfactual prior).
(3) **구조 분해** — RUL = health − damage, health는 TRA-blind.
④ 무가정(UQ)은 안 씁니다 — 대신 isotonic **후처리**로 (1)을 강제.
중요: (2)는 **데이터 라벨에 없는 관계**입니다. 
unit마다 궤적 하나 — “TRA 올리면 RUL 바로 ↓”는 라벨로 검증 불가.
**외부 도메인 지식**을 inductive bias로 주입하는 케이스입니다.
```

### ③ 장표 핵심 (카드)

*① 시간 단조 (약–중)*
- 가정: cycle↑ → RUL↓
- 구현: **unit isotonic** 후처리
- 근거: RUL 정의와 일치

*② 부하→열화 (counterfactual)*
- 가정: TRA↑ → damage↑ → RUL↓ (지속 부하)
- ⚠️ per-sample 라벨: **∂RUL/∂TRA = 0**
- unit-level 상관 r≈0 (n=9) — **데이터로는 미검증**

*③ 구조 분해 (중–강)*
- RUL = health − damage
- health 경로: TRA **zero**
- damage: MonotoneLoadHead

**하단 takeaway:** **지식 우선** — 라벨에 없어도 도메인 prior + 구조

---

## A06 · 핵심 설계 — 구조가 방향을 보장 (CMNN echo) {#a06}

**슬라이드 A06/N14**

### ⓪ 발표 흐름

**역할:** S20 “구조 불변량” — **우리 버전**.

**다음으로:** λ_tra loss 역할 재정의 (A07).

### ② 발표 대본

```text
[1.5분] ★ 부록 핵심 장.
대본: v4_disentangled forward를 보면 — health encoder는 TRA 채널을 0으로 지웁니다.
damage head는 softplus 가중치 times TRA plus cycle.
RUL = health minus damage이니 **∂RUL/∂TRA ≤ −softplus(w) < 0** — 항등식입니다.
본편 S20 CMNN과 같은 철학: **손실로 유도가 아니라 구조상 위반 불가.**
λ_tra Jacobian loss는 v4에서 사실상 **중복** — 이미 만족해서 gradient 0.
실험: λ를 0, 0.05, 0.5로 바꿔도 adherence 100%·RMSE 무반응.
진짜 레버는 **MonotoneLoadHead vs free MLP** ablation입니다.
```

### ③ 장표 핵심

**식 (슬라이드):**
\[
\text{RUL} = \underbrace{h(\mathbf{x}_{\setminus \text{TRA}})}_{\text{health, TRA-blind}} - \underbrace{d(\text{TRA}, \text{cycle}, \ldots)}_{\text{MonotoneLoadHead}}
\]

**구조 ablation (3-seed, hard RMSE):**

| variant | mono head | RMSE mean±std | worst seed | ΔRUL<0 |
|---------|:---------:|--------------:|-----------:|-------:|
| **full** | ✓ | **3.88±0.65** | **4.77** | **100%** |
| free_load | ✗ | 4.24±1.37 | 6.11 | 0% |
| free_both | ✗ | 3.94±1.47 | 6.00 | 12% |

**하단 takeaway:** **S20 echo** — prior는 **아키텍처**에, loss는 보조

---

## A07 · 정직한 한계 — 라벨·데이터가 말해주지 않는 것 {#a07}

**슬라이드 A07/N14**

### ② 발표 대본

```text
[1분]
대본: Q&A 방어용 장입니다. 
“TRA 올리면 RUL 내려가게 학습” — 데이터 fact가 아닙니다.
GBM은 TRA 섭동에 ΔRUL **+9** (양의 반응). Transformer는 **무감응**.
우리 모델만 모델-입력 공간에서 ΔRUL<0 100% — **설계한 대로**입니다.
unit 평균 TRA vs 총수명 상관 **r≈0, n.s.** — prior는 논문·매뉴얼에서 온 **외부 지식**.
그래서 “물리 법칙 준수”라고 쓰면 안 되고,
**counterfactual inductive bias + OOD RMSE로만 효용 증명**합니다.
```

### ③ 장표 핵심

| 주장 | 가능? | 근거 |
|------|:-----:|------|
| hard RMSE ↓ | ✓ | 10-seed, p=0.00017 vs TabPFN |
| 구조 prior OOD 유지 | ✓ | model-input ΔRUL<0 100% |
| “데이터가 TRA↓RUL↓ 증명” | ✗ | ∂RUL/∂TRA=0, r≈0 |
| “loss가 방향 만듦” | ✗ | λ 스윕 무반응, arch ablation |

**하단 takeaway:** 가정은 **밖에서 온 prior** — 검증은 **성능·구조**로

---

# Part 3 · 실험

## A08 · 실험 설계 — 프로토콜·공정성 {#a08}

**슬라이드 A08/N14**

### ② 발표 대본

```text
[1.5분]
대본: S30 체크 ③ 공정 비교를 맞춥니다.
데이터: MAIN은 ncmapss hard + C-MAPSS FD002/004.
window 1500, split seed = model seed, **동일 isotonic** 후처리.
Baseline: TabPFN v8(ref 고정), GBM snapshot+OC, LSTM/GRU/Transformer e15→e120 스윕.
v4: e15( hard 조기 수렴), C-MAPSS는 e120 **수렴까지** 별표.
평가: hard_extrap RMSE primary, NASA PHM08 score 보조.
multiseed 3/10, ablation 9 variant, 구조 ablation 4 variant.
```

### ③ 장표 핵심

| 항목 | 설정 |
|------|------|
| Primary metric | hard_extrap RMSE ↓ |
| Seeds | 42–44 (main), 42–51 (significance) |
| Epochs | hard e15 · C-MAPSS e120 fair |
| Post-process | unit isotonic (전 모델) |
| TabPFN | in-context ref 4.788 (per-seed OOM 한계 명시) |

**Ablation 목록:** full · no_iso · no_physics · λ_tra=0 · revin · data_only · **arch 4종**

---

## A09 · 실험 지도 — 무엇을 무엇 때문에 {#a09}

**슬라이드 A09/N14**

### ③ 장표 핵심 (표)

| 실험 | 질문 | 스크립트 |
|------|------|----------|
| MAIN multiseed | baseline 대비 승? | `run_v4_paper_main_multiseed.py` |
| 9-variant ablation | iso·physics 기여? | `run_v4_paper_ablation.py` |
| 10-seed + t-test | 우연이 아닌가? | `run_v4_significance.py` |
| LSTM/GRU/Trans | seq 붕괴? | `run_v4_extra_baselines.py` |
| fair epoch | underfit 제거? | `run_v4_fair_epochs.py` |
| physics v2 | 일관성·TRA 반응? | `run_v4_physics_v2.py` |
| arch ablation | 구조 prior 인과? | `run_v4_arch_ablation.py` |

---

# Part 4 · 결과

## A10 · MAIN — hard에서만 명확 우위 {#a10}

**슬라이드 A10/N14**

### ② 발표 대본

```text
[1.5분]
대본: 결과를 솔직히 나눕니다.
**Headline — ncmapss hard:** v4 3.88±0.80 (3-seed), 10-seed 3.43±0.77.
TabPFN 4.79 — p=0.00017. GBM 5.74 — paired p≈3e-6.
NASA score 0.29 vs GBM 0.69.
**C-MAPSS:** e15는 둘 다 underfit. e120 수렴 후 v4≈Transformer (Δ<0.2, std 내).
TabPFN 16/17은 약한 baseline — C-MAPSS headline에 쓰지 않습니다.
스토리: 표준 축 외삽은 수렴하면 여러 모델 OK → **결합 hard만 v4 유일**.
```

### ③ 장표 핵심

**Table 1 — MAIN (extrap RMSE)**

| Dataset | v4 | TabPFN | GBM | 비고 |
|---------|---:|-------:|----:|------|
| **ncmapss hard** | **3.43±0.77** (10s) | 4.79 | 5.74 | **headline** |
| FD002 | 4.15±0.18 (e120) | 16.30 | 14.25 | ≈ Trans 4.07 |
| FD004 | 3.89±0.23 (e120) | 17.16 | 13.18 | ≈ Trans 3.75 |

**Ablation (hard):** no_iso **+0.49** · no_physics +0.33 · revin **+5.0**

---

## A11 · 구조·일관성 — prior가 무엇을 했나 {#a11}

**슬라이드 A11/N14**

### ② 발표 대본

```text
[1.5분]
대본: 성능만이 아닙니다 — 가정이 **어떻게** 작동했는지.
구조 ablation: mono head 빼면 adherence 0%, worst seed 6.1 — seed42 TabPFN 패배.
full만 **전 seed TabPFN 승** — prior 효용은 **평균이 아니라 분산·worst 방어**.
H1 temporal consistency (iso 전 raw): OOD 13% vs GBM/Trans 30%.
TRA: 모델-입력 공간 ΔRUL<0 100% (설계). 물리 공간 +6 — OC confound, 각주.
```

### ③ 장표 핵심

| 지표 | v4 full | GBM | Transformer |
|------|--------:|----:|------------:|
| H1 violation (OOD, raw) | **13%** | 31% | 31% |
| frac ΔRUL<0 (model-input) | **100%** | ~17% | ~0% |
| RMSE std (3-seed) | **0.65** | — | 1.37 (free_load) |

**하단 takeaway:** prior = **구조** → worst-seed·방향·일관성

---

# Part 5 · 검증

## A12 · S30 체크 4항 — 우리가 통과한 것 {#a12}

**슬라이드 A12/N14**

### ② 발표 대본

```text
[1.5분]
대본: 본편 S30 네 가지를 그대로 적습니다.
① 진짜 밖? — hard는 test unit + TRA>q90. id_regime(unit 고정·TRA≤q70)과 대비.
② 어떤 밖? — D_div(unit) + D_cor(regime) **동시**. OoD-Bench 언어로 ‘둘 다’.
③ 공정? — 동일 split/window/iso, baseline epoch 스윕, TabPFN ref 한계 footnote.
④ 튼튼? — 10-seed, t-test, 9 ablation, 4 arch variant, extreme split e120.
네 개 중 하나라도 빠지면 “hard SOTA” 주장 불가 — 우리는 ①②를 가장 엄격히 잡았습니다.
```

### ③ 장표 핵심 (체크리스트)

| # | S30 질문 | 우리 답 |
|---|----------|---------|
| ① | test ∩ train support = ∅? | ✓ unit holdout + q90 |
| ② | D_div / D_cor? | ✓ **둘 다** (hard) |
| ③ | 공정 비교? | ✓ iso·epoch fair · 5 baselines |
| ④ | seed/가정 약화? | ✓ 10-seed · arch ablation |

---

## A13 · 검증 함정 — 우리가 **안** 주장하는 것 {#a13}

**슬라이드 A13/N14**

### ② 발표 대본

```text
[1.5분]
대본: S27 함정 3개를 우리에게 적용합니다.
함정1 — easy band RMSE 4.1은 ‘외삽’이 아니라 regime-only; headline에 쓰지 않음.
함정2 — 구 physics violation 97%는 Transformer **무반응** 오분류; v2 지표로 교체.
함정3 — λ_tra·PDE 잔차 좋다고 물리 증명 아님; **구조 항등식 + RMSE**만.
FD002 no_physics 더 좋음 — constraint gate 재검토 필요, 정직히 씀.
TabPFN per-seed paired는 MPS OOM — ref 1-sample t-test 한계 footnote.
```

### ③ 장표 핵심

**Claim / No-claim 표**

| ✓ Claim | ✗ No-claim |
|---------|-----------|
| hard extrap RMSE ↓ 유의 | “TRA↑ ⇒ RUL↓ 데이터 법칙” |
| 구조 prior → OOD 방향 100% | “λ_tra loss가 방향 생성” |
| full만 worst-seed TabPFN 승 | “모든 split·epoch SOTA” |
| C-MAPSS ≈ Transformer @ e120 | “C-MAPSS에서 TabPFN-beating headline” |

---

## A14 · 마무리 — 한 문장 {#a14}

**슬라이드 A14/N14**

### ② 발표 대본

```text
[30초]
대본: 정리합니다.
N-CMAPSS hard — unit×regime 결합 외삽.
가정 — counterfactual 부하 prior를 **MonotoneLoadHead 구조**에 내장.
검증 — S30 네 항 + 10-seed + 구조 ablation.
본편과 같은 결론, 데이터로 증명된 버전:
밖은 **가정(구조)** 으로 버티고, 그 가정이 **RMSE·worst-seed**에서만 payoff.
질문 받겠습니다.
```

### ③ 장표 핵심

**한 장 요약 (5 bullet)**
1. **문제:** RUL @ hard (unit×TRA 밖)
2. **가정:** health−damage + mono TRA (**구조**, not label)
3. **실험:** 7 suites · fair epoch · 5 baselines
4. **결과:** hard **3.43** vs TabPFN **4.79** (p=0.00017)
5. **검증:** S30 4/4 · 정직 no-claim 4건

**하단 (본편 echo):** *“외삽 되나?” → “내 가정을 구조에 넣었고, 밖에서 검증했나?”*

---

## Q&A 암기 (부록용 5 bullets)

- **왜 TRA prior?** 라벨엔 없음 — **도메인 counterfactual** + OOD RMSE payoff
- **loss vs 구조?** v4는 **MonotoneLoadHead** — λ_tra redundant
- **easy vs hard?** easy=regime only · **hard=headline** (결합 shift)
- **C-MAPSS?** e120 **≈ Transformer** — hard만 차별화
- **physics 97% violation?** **폐기** — 무반응≠위반 (v2)

---

## 슬라이드 제작 메모 (PPT용)

| 장 | 추천 visual |
|----|-------------|
| A03 | TRA 축 q70/q90 + unit color |
| A06 | health−damage block diagram |
| A06 | arch ablation bar (RMSE std + worst) |
| A10 | MAIN 표 3행 + hard 강조색 |
| A12 | S30 체크 4항 + ✓ 표 |
| A13 | Claim / No-claim 2열 |

**Deck 이름 제안:** `외삽_50분_사례_CA-CSS_v4_부록.pptx` (본편과 분리)

---

*수치 출처: `results/v4_paper_main/` · `v4_significance/` · `v4_arch_ablation/` · `v4_physics_v2/` · `PAPER_WEAKNESSES_AND_RESULTS.md` (2026-07-25)*
