#!/usr/bin/env python3
"""Regenerate 외삽_50분_장표별_설명_v5.md from build_presentation_v5.py.

Structure per slide: ⓪ 발표 흐름 → ① 참조 논문 → ② 발표 대본 → ③ 장표·논문 상세
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build_presentation_v5.py"
APPENDIX = ROOT / "part_b_appendix_v5.md"
OUT = ROOT / "외삽_50분_장표별_설명_v5.md"

PDF_META = {
    "xu": ("Xu et al., ICLR 2021", "How Neural Networks Extrapolate", "Xu2021_How_Neural_Networks_Extrapolate.pdf"),
    "pfister": ("Pfister & Bühlmann, 2024", "Extrapolation-Aware Nonparametric Inference", "Pfister2024_Extrapolation-Aware_Nonparametric_Inference.pdf"),
    "bartley": ("Bartley et al., 2019", "Characterizing Extrapolation in Multivariate Response Data", "Bartley2019_Characterizing_Extrapolation_Multivariate.pdf"),
    "eql": ("Martius & Lampert, 2016", "Extrapolation and Learning Equations (EQL)", "Martius2016_Extrapolation_Learning_Equations_EQL.pdf"),
    "nalu": ("Trask et al., NeurIPS 2018", "Neural Arithmetic Logic Units", "Trask2018_Neural_Arithmetic_Logic_Units_NALU.pdf"),
    "runje": ("Runje & Shankaranarayana, ICML 2023", "Constrained Monotonic NN (CMNN)", "Runje2023_Constrained_Monotonic_NN.pdf"),
    "raissi": ("Raissi et al., 2019", "Physics-Informed Neural Networks", "Raissi2019_Physics_Informed_Neural_Networks.pdf"),
    "fesser": ("Fesser et al., 2023", "Extrapolation Failures in PINNs", "Fesser2023_Extrapolation_Failures_PINNs.pdf"),
    "zhu": ("Zhu et al., CMAME 2023", "Reliable Extrapolation of Deep Neural Operators", "Zhu2022_Reliable_Extrapolation_DeepONet.pdf"),
    "ye2022": ("Ye et al., CVPR 2022", "OoD-Bench", "Ye2022_OoD-Bench.pdf"),
    "ye2021": ("Ye et al., 2021", "Theoretical Framework for OOD", "Ye2021_Theoretical_Framework_OOD.pdf"),
    "domainbed": ("Gulrajani & Lopez-Paz, NeurIPS 2020", "DomainBed", "Gulrajani2020_In_Search_of_Lost_Domain_Generalization.pdf"),
    "arjovsky2019": ("Arjovsky et al., 2019", "Invariant Risk Minimization (IRM)", "Arjovsky2019_Invariant_Risk_Minimization.pdf"),
    "ghahramani": ("Ghahramani, 2013", "Bayesian Nonparametrics", "Ghahramani2013_Bayesian_Nonparametrics.pdf"),
    "liu": ("Liu et al., 2023", "OOD Generalization Survey", "Liu2023_OOD_Generalization_Survey.pdf"),
    "aykol": ("Aykol et al., 2021", "Physics-informed ML for Battery Lifetime", "Aykol2021_Physics_ML_Battery_Lifetime.pdf"),
    "li2023": ("Li et al., 2023", "Predicting Battery Lifetime under Varying Conditions", "Li2023_Predicting_Battery_Lifetime_Varying_Conditions.pdf"),
    "note": ("학습노트", "외삽 완전정복", "외삽_완전정복_학습노트.pdf"),
}

PAPER_APPENDIX = {
    "xu": "c-03",
    "pfister": "c-02",
    "bartley": "c-01",
    "eql": "c-04",
    "nalu": "c-05",
    "runje": "c-06",
    "raissi": "c-07",
    "fesser": "c-08",
    "zhu": "c-09",
    "ghahramani": "c-10",
    "ye2022": "c-11",
    "ye2021": "c-13",
    "domainbed": "c-12",
    "arjovsky2019": "c-14",
    "liu": "c-15",
    "aykol": "c-19",
    "li2023": "c-20",
    "note": "",
}

# 장별 「논문 상세」 — 부록 C 10섹션 요약 (PDF 없이 1차 파악)
PAPER_SLIDE_DETAIL: dict[str, list[str]] = {
    "bartley": [
        "**정의:** 훈련 범위 = **Conv(X_train)**. \(x^*\notin\) 훈련 범위 → extrapolation.",
        "**지표:** multivariate **trace/det** of \(\mathrm{Var}(Y|x)\) + cutoff \(c\).",
        "**실험:** 훈련 범위 밖 → MSE↑, PI coverage↓ (sim + lake fish).",
        "**함정:** min–max box는 훈련 범위보다 큼 → extrapolation **과소** 판정.",
        "**고차원:** p↑ → random test가 훈련 범위 밖일 확률↑ (S10).",
        "**Q&A:** “범위 안”이 아니라 “**훈련 범위 안**?”이 정확한 질문.",
    ],
    "pfister": [
        "**정의:** extrapolation = support **밖**에서 \(m(x)=\mathbb{E}[Y|X=x]\) 또는 quantile 평가.",
        "**함수 못 정함:** 유한 데이터 + smoothness만 → 밖 \(m(x)\) **무한히 많음** (S09).",
        r"**가정:** directional derivative **극값** on support → band \([m^-,m^+]\).",
        "**추정:** 안 = NW/RF; 밖 = **partial ID bounds** (band 폭은 데이터만으로 안 좁아짐).",
        "**UQ:** 모델 softmax ≠ 통계 CI — band 넓으면 **정직한** 불확실성.",
        "**Q&A:** 가정 넣어도 검증 필요 (Fesser). Pfister = **명시적** bounds.",
    ],
    "xu": [
        r"**Thm.1:** L-layer ReLU MLP, \(x=tv\), \(t\to\infty\) → \(f_\theta(tv)/t \to A_v v+b_v\).",
        "**메커니즘:** active set 고정 → 마지막 linear piece **연장** = 직선 extrapolation.",
        "**Fig.1:** sin — train OK, test **tangent**. Appendix affine fit R²>0.99.",
        "**Fig.5:** sin+cos φ → 주기 extrap; ReLU mismatch → 오차 **10²–10³**.",
        "**GNN:** linear aggregation; **algorithmic alignment** (Bellman-Ford 등) 시 밖 OK.",
        "**Q&A:** “NN extrapolation?” → “**어떤 φ·구조 가정**이 타깃에 맞나?”",
    ],
    "eql": [
        "**유닛:** +, ×, sin, cos layers; **L1** on weights → sparse **짧은 식**.",
        "**학습:** end-to-end GD — 구조+계수 동시 (symbolic regression).",
        "**extrapolation:** \(g\)가 유닛 **대수 닫힘** → recovered 식 = true \(g\) → **전역**.",
        "**실패:** sin 타깃인데 sin 유닛 없음 → in-sample OK, **out-of-sample 붕괴**.",
        "**실험:** pendulum, ODE synthetic — **expression recovery**.",
        "**Q&A:** 방법① — 가정 = “**함수 family**를 안다”. 틀리면 Xu보다 나쁨.",
    ],
    "nalu": [
        r"**NAC:** \(w_i=\tanh\hat w_i\cdot\sigma(\hat w_i)\in[-1,1]\) → **±1,0** 수렴 → 가감.",
        "**NALU:** gate × (NAC add vs log-exp **mul/div**).",
        "**실험:** train [1,10], test [10,1000] — NALU OK, MLP fail; MNIST arithmetic.",
        "**한계:** init 민감, gradient vanishing, ×÷ at 0 unstable, **비산술** 붕괴.",
        "**후속:** NALU failure papers — 실무 단독 사용 주의.",
        "**Q&A:** 타깃이 **순수 산술**일 때만 강한 가정 주입.",
    ],
    "runje": [
        "**한계(Fig.1):** \(W\ge0\) clip — monotonic O, **\(x^3\)** 같은 비선형 단조 **X**.",
        "**CMNN:** input split, dual path, unsaturated φ, \(W\ge0\) → **monotone + nonlinear**.",
        "**Theorem:** universal approximator for **monotone** functions.",
        "**실험:** cubic, finance, health — **100%** monotonicity, 훈련 범위 밖 **역전 불가**.",
        "**vs C-18:** Liu = MILP **certify** 사후; Runje = **by design** 사전.",
        "**Q&A:** 방법② — “**방향(단조)**만 안다” → 구조에 **내장**.",
    ],
    "raissi": [
        r"**Loss:** \(\mathcal{L}=L_{\mathrm{data}}+\lambda L_{\mathrm{PDE}}\), \(\mathcal{N}[u_\theta]\)=PDE residual.",
        "**Continuous:** (x,t) collocation + autograd; **discrete:** RK in network.",
        "**결과:** Burgers, Schrödinger, NS — **sparse** sensor → field 복원.",
        "**한계:** λ·collocation 밀도 민감; inverse ill-posed; **시간 밖** → Fesser.",
        "**Part II:** PDE **discovery** (별도) — 발표는 Part I 위주.",
        "**Q&A:** physics in loss = **soft 가정**. “참 PDE” ≠ 밖 보증.",
    ],
    "fesser": [
        r"**Setup:** train \(t\in[0,T/2]\), test \((T/2,T]\); Burgers + Allen–Cahn.",
        "**결과:** interp error→0; **extrap L2 폭증** (orders). width/depth↑ → interp만↑.",
        "**silent failure:** \(L_{\mathrm{PDE}}\) 작아도 test time **터짐** (S27).",
        "**Fourier/WWF:** 고주파만 아님; spectral **shift** across time.",
        "**완화:** transfer fine-tune full domain → **~82%** (Burgers), **~51%** (Allen–Cahn) error↓.",
        "**Q&A:** PINN 검증 = **train window 밖** holdout 필수.",
    ],
    "zhu": [
        "**DeepONet:** branch(u) + trunk(y) → \(G(u)(y)\); extrap = **새 input function** u.",
        r"**Complexity:** **2-Wasserstein** \(W_2\) between train/test **function spaces**.",
        "**5 methods:** std, **PDE fine-tune**, multi-fidelity, **abstention**, ensemble.",
        "**결과:** FT-Phys 등 PDE-informed; abstain → acc↑ on **accepted**, coverage↓ 명시.",
        "**trade-off:** capacity↑ → interp↑, extrap **bias-variance** (Fig.).",
        "**Q&A:** 방법④b — reliability = accuracy **×** known coverage.",
    ],
    "ghahramani": [
        "**Aleatoric:** irreducible noise (heteroscedastic). **Epistemic:** lack of knowledge.",
        "**GP:** \(k(x,x')\); far from data → posterior **variance ↑** (closed form).",
        "**DP/IBP:** infinite mixture, latent features — complexity grows with data.",
        "**발표:** S11 '모름'↑; S23 deep ensemble ≈ 불확실성 proxy.",
        "**한계:** GP \(O(n^3)\); deep BNN approximate; calibration separate issue.",
        "**Q&A:** “모름” 신호 ≠ “틀림” 방지 — **둘 다** 필요 (abstention).",
    ],
    "ye2022": [
        r"**\(D_{\mathrm{div}}\):** diversity shift — \(P(X)\) **새 영역** (style, domain).",
        r"**\(D_{\mathrm{cor}}\):** correlation shift — \(P(X)\) 유사, **\(P(Y|X)\)** 변경.",
        "**프로파일:** dataset → 어느 축 dominant? → 방법 선택 근거.",
        "**14 alg vs ERM:** 대부분 **한 축에서만** 이김 — 범용 OOD silver bullet ✗.",
        "**가이드:** Colored MNIST = \(D_{\mathrm{cor}}\); PACS style = \(D_{\mathrm{div}}\) 등.",
        "**Q&A:** S28 — extrapolation **종류** 먼저, 알고리즘 나중.",
    ],
    "ye2021": [
        "**Framework:** OOD = train/test **distribution mismatch** formalize.",
        "**Expansion function:** OOD difficulty quantification — variance amplification.",
        "**Impossibility:** arbitrary OOD without assumption → **no free lunch**.",
        "**IRM 등:** invariant feature **존재 가정** — 깨지면 실패 (C-14).",
        "**연결:** OoD-Bench(C-11) 축 정의의 **이론 선행**.",
        "**Q&A:** “OOD generalize” 주장 전 — **어떤 shift 가정**인지 명시.",
    ],
    "domainbed": [
        "**Motivation:** DG papers — unfair HP, capacity, **test-domain val** → fake gains.",
        "**7 datasets:** PACS, VLCS, OfficeHome, TerraIncognita, DomainNet, …",
        "**14 alg:** ERM, IRM, DANN, CORAL, MMD, … — **same 20-trial random search**.",
        "**숫자:** ERM **66.6%**, IRM **65.4%**, DANN **65.6%**, CORAL **+0.9%p** (avg).",
        "**Rule:** model selection = **train-domain val only** — test domain HP = cheat.",
        "**Q&A:** S29 — “ERM + fair budget” 없는 DG claim **의심**.",
    ],
    "arjovsky2019": [
        "**Setup:** environments \(e\), spurious \(e\)-specific correlation.",
        r"**IRMv1:** \(\min_\Phi\sum_e R^e(\Phi)\) s.t. \(\|\nabla_{w|w=1}R^e(w\cdot\Phi)\|=0\).",
        "**Goal:** \(\Phi\) captures **invariant** (causal) features.",
        "**DomainBed:** fair tune → **ERM ≥ IRM** — spurious 제거 **보장** ✗.",
        "**한계:** nonlinear IRM, environment partition sensitivity.",
        "**Q&A:** “IRM 쓰면 OOD OK?” → **DomainBed에서 재검증**.",
    ],
    "liu": [
        "**Taxonomy:** covariate / label / domain / subpopulation / **temporal** shift.",
        "**Methods map:** invariant learning, aug, causal, UQ, OOD detection.",
        "**vs extrapolation:** 훈련 범위 밖 (Bartley) ⊂ broader OOD — 용어 구분.",
        "**용도:** S27–S28 **맥락** — 본문 deep dive 아님.",
        "**Q&A:** survey = **지도**; 핵심 claim은 primary paper에서.",
    ],
    "aykol": [
        "**Domain:** Li-ion **lifetime** under varying charge/discharge.",
        "**Physics:** SEI growth, thermodynamics → features + CNN/ML.",
        "**Extrapolation:** 새 protocol / C-rate = **훈련 범위 밖** operating point.",
        "**메시지:** same early cycles, **different degradation law** → different life.",
        "**연결:** S09 Pfister 함수 못 정함 **공학 예시**.",
    ],
    "li2023": [
        "**Data:** **225** commercial LFP/graphite cells, diverse protocols.",
        "**Task:** first **15%** cycles → predict **lifetime** (RUL proxy).",
        "**성능:** in-distribution **MAPE ~15%** (early prediction).",
        "**OOD:** varying DoD, fast charge — **extrapolation** 현실 반영.",
        "**연결:** S09 — linear vs exponential fade **가정** 비교.",
    ],
    "note": [
        "**12p** 복습 노트 — 정의·한계·방법·검증 **한글** 요약.",
        "**용도:** 발표 전날 **전체 흐름** 리허설.",
        "**한계:** 논문 depth는 **부록 C** 참조.",
    ],
}


def fmt_paper_slide_detail(key: str) -> str:
    if key not in PDF_META:
        return ""
    author = PDF_META[key][0]
    anchor = PAPER_APPENDIX.get(key, "")
    link = f" → [부록 C #{anchor.upper()}](#{anchor})" if anchor else ""
    lines = PAPER_SLIDE_DETAIL.get(key, [f"상세 → [부록 C](#부록-c){link}"])
    body = "\n".join(f"  {ln}" for ln in lines)
    return f"\n**{author}**{link}\n{body}\n  _→ 부록 C 10섹션 풀 가이드_\n"

NARRATIVE_ARC = """\
오늘 발표는 **한 문장**을 증명하는 구조입니다: *밖을 지탱하는 것은 데이터가 아니라 가정이다.*

1. **도입 (S01–S03)** — “무엇을 말할지”와 “가정이 뭔지”를 먼저 고정합니다. 여기서 용어가 흔들리면 2·3부 전체가 헷갈립니다.
2. **1부 (S04–S07)** — 외삽을 **좌표계**로 정의합니다. “입력이 훈련 범위 안/밖인가?”만 보면 됩니다. S07에서 “안은 잘 맞는데 밖은 터진다”는 직관을 만든 뒤, **왜 그런지**를 2부로 넘깁니다.
3. **2부 (S08–S13)** — 실패 원인 네 가지를 **데이터 → 규모 → 불확실성 → 신경망** 순으로 쌓습니다. S09가 심장, S12–S13이 “그럼 어떻게 하지?”로 3부에 연결됩니다.
4. **3부 전반 (S14–S26)** — 가정을 **직접 넣는** 방법 지도. 약한 가정(단조)부터 강한 가정(수식·PDE)까지, 모를 때는 UQ·기권으로 넘깁니다.
5. **3부 후반 (S27–S30)** — “밖에서도 된다”는 **주장을 어떻게 검증할지**. 방법만 알면 끝이 아니고, 범위·벤치·공정 비교까지 봐야 합니다.
6. **엔딩 (S31–S33)** — 질문을 다시 바꿔서 닫습니다: *“외삽 되나?” → “내 가정이 맞고, 검증했나?”*
"""

SLIDE_FLOW: dict[int, dict[str, str]] = {
    1: {
        "role": "오프닝 — 오늘 50분의 **결론을 미리** 말합니다.",
        "from_prev": "— (시작)",
        "to_next": "“구체적으로 어떻게 풀지” → **S02 로드맵**으로 넘깁니다.",
        "natural": "청중에게 **네 파트**만 짚어 주고, 끝까지 따라올 **한 문장**을 약속합니다.",
    },
    2: {
        "role": "지도 — 1·2·3부가 **왜 이 순서**인지 보여 줍니다.",
        "from_prev": "S01에서 결론을 들었으니, “그걸 어떻게 채울지” **목차**로 연결.",
        "to_next": "목차 다음엔 용어. **S03 ‘가정’**을 안 고정하면 뒤가 전부 추상적입니다.",
        "natural": "세 상자를 **정의 → 원인 → 대응·검증** 스토리로 읽어 주세요.",
    },
    3: {
        "role": "★ 용어 고정 — 오늘 **‘가정’**의 뜻을 하나로 못 박습니다.",
        "from_prev": "로드맵에서 3부가 ‘가정 넣기’라고 했으니, **가정이 뭔지** 먼저.",
        "to_next": "용어가 잡혔으니 **1부** — 외삽을 **입력 위치**로 정의합니다 (S04–S07).",
        "natural": "그림에서 **같은 점·다른 밖**을 천천히. “데이터는 같고 가정만 다르다”를 입에 붙이세요.",
    },
    4: {
        "role": "1부 표지 — 오늘 내내 쓸 **좌표계**를 소개합니다.",
        "from_prev": "S03에서 ‘밖은 가정이 정한다’고 했으니, **‘밖’이 어디인지**부터.",
        "to_next": "좌표계의 첫 질문: **이 입력, 범위 안인가 밖인가?** → S05.",
        "natural": "“5분짜리 정의 파트”라고 **길이·목적**만 짧게 예고.",
    },
    5: {
        "role": "핵심 정의 — **보간 vs 외삽**을 입력 기준으로 고정.",
        "from_prev": "1부 시작. “모델이 외삽?”이 아니라 **“지금 넣는 입력이 밖?”**.",
        "to_next": "입력 기준이 잡혔으니, **훈련 범위**를 수학적으로 (S06).",
        "natural": "키·몸무게·겨울 수요 예 — **일상 예** 하나만 짚고 그림 약속(음영=범위)을 걸어 두세요.",
    },
    6: {
        "role": "훈련 범위 = **convex hull** — ‘범위’를 정확히.",
        "from_prev": "S05에서 “범위 안/밖”을 썼으니, **범위가 정확히 뭐냐**.",
        "to_next": "정의가 끝났으니 **왜 위험한지** 감각 — 다항식 사례 (S07).",
        "natural": "min–max 상자와 hull 차이는 **한 줄**만. “오늘은 hull 기준”이라고 못 박기.",
    },
    7: {
        "role": "1부 마무리 — **안의 성적 ≠ 밖의 성적**을 눈으로.",
        "from_prev": "정의·범위를 잡았으니, “그래서 뭐가 문제?” **직관** 하나.",
        "to_next": "“왜 다른 질문일 수밖에 없나?” → **2부 실패 원인** (S08).",
        "natural": "“여기서 교훈 하나만” → **2부로 넘기는 브릿지**. 청중이 S08을 기대하게.",
    },
    8: {
        "role": "2부 표지 — 실패 **네 가지** 예고.",
        "from_prev": "S07에서 “안≠밖”을 봤으니, **왜 그런지 이유**를 나열.",
        "to_next": "첫 이유, 오늘 **가장 중요한 장** — 데이터만으론 못 고름 (S09).",
        "natural": "‘한계’가 아니라 **‘왜 틀리는지’** — 톤을 원인 분석으로.",
    },
    9: {
        "role": "★ 2부 심장 — **식별 불가** = 관통 문장의 증명.",
        "from_prev": "2부 첫 카드. S03 그림의 **논문 버전**.",
        "to_next": "함수를 못 고르는 건 **원리** 문제, 다음은 **규모** 문제 (S10).",
        "natural": "배터리 예 → **“데이터는 말 안 해준다”** → **“그럼 가정”**으로 S03과 닫기.",
    },
    10: {
        "role": "규모 — 고차원에선 **테스트가 거의 전부 밖**.",
        "from_prev": "S09가 ‘원리’였으면, S10은 **현실 데이터** 이야기.",
        "to_next": "밖이 흔해지면, 밖에서 **뭐가 터지는지** — 불확실성 (S11).",
        "natural": "“우리 데이터도 이미지·센서” — **청중 데이터**에 한 번 연결.",
    },
    11: {
        "role": "해부 — 밖에서 **‘모름’(epistemic)** 이 커짐.",
        "from_prev": "밖이 많다는 걸 알았으니, **오차가 왜 커지는지** 쪼개기.",
        "to_next": "일반 ML뿐 아니라 **신경망도** — Xu (S12).",
        "natural": "과녁 비유 후 “UQ는 3부 끝에” **가볍게 예고**만.",
    },
    12: {
        "role": "★ 2부 클라이맥스 — ReLU는 밖에서 **직선** (Xu) + **다른 φ Q&A**.",
        "from_prev": "“NN은 다를 거야?” → **아니다, 밖 가정**을 이미 함.",
        "to_next": "왜 직선인지 **메커니즘** + 2부 총정리 (S13).",
        "natural": "ReLU=직선(증명). tanh=포화, sin=주기 — **φ=밖 선언**. φ만으론 부족 → **S16**.",
    },
    13: {
        "role": "2부 마무리 — **질문 전환** + 3부로.",
        "from_prev": "Xu 정리 **왜** 성립하는지 3단, 그다음 **2부 한 줄 요약**.",
        "to_next": "“가정을 골라 넣자” → **3부 표지** (S14).",
        "natural": "“외삽 되나?” → “**내 가정이 맞나?**” — 이 문장을 **크게**.",
    },
    14: {
        "role": "3부 표지 — **대응법** + **성능 검증** 두 덩어리.",
        "from_prev": "2부에서 문제를 봤으니, **대안**과 **검증**.",
        "to_next": "먼저 방법 **전체 지도** (S15).",
        "natural": "27분 중 앞은 방법·뒤는 검증 — **시간 배분** 한 번만.",
    },
    15: {
        "role": "방법 지도 — 가정 **강도 스펙트럼**.",
        "from_prev": "3부 시작. “뭘 넣을 수 있나?” **한 장 지도**.",
        "to_next": "지도의 **입구** — 활성화가 타깃과 맞는지 (S16).",
        "natural": "①함수족 ②방향 ③물리 ④모를 때 — **네 칸**을 왼쪽→오른쪽으로.",
    },
    16: {
        "role": "입구 — **활성화·구조 정렬** (Xu Fig.5 맥락).",
        "from_prev": "지도에서 ①번 들어가기 **전 체크**.",
        "to_next": "정렬 OK면 **함수족** — EQL (S17), NALU (S18).",
        "natural": "“가정 넣기 전에 **이미 하고 있는 가정** 확인” — Xu S12와 echo.",
    },
    17: {
        "role": "방법 ①a — **EQL** (수식 유닛).",
        "from_prev": "함수족 **강한 가정** 첫 예.",
        "to_next": "같은 계열 **NALU** (S18) — 산술 구조.",
        "natural": "“맞으면 전역, 틀리면 전역 실패” **trade-off** 한 번.",
    },
    18: {
        "role": "방법 ①b — **NAC/NALU** (Fig.2 (a)(b) 분리).",
        "from_prev": "EQL과 **같은 ①번 칸**, 다른 구현.",
        "to_next": "강한 가정 대신 **방향만** 아는 경우 → S19.",
        "natural": "그림 **(a) NAC → (b) NALU** 순으로 · ±1 수렴은 **목표·보장 ❌** · 실무에서 “식까지는 모르지만 **단조**는 안다”로 **②번으로 넘기기**.",
    },
    19: {
        "role": "방법 ②a — **단조**가 왜 실무적 가정인지.",
        "from_prev": "①번(함수족)에서 **약한 가정**으로 내려옴.",
        "to_next": "구현 — **CMNN** (S20).",
        "natural": "배터리·수명·재고 — **방향** 예 하나.",
    },
    20: {
        "role": "방법 ②b — **CMNN**.",
        "from_prev": "단조 문제 **정의** → **구조로 강제**.",
        "to_next": "방향보다 더 강한 **물리·PDE** → S21.",
        "natural": "Runje vs Liu — **설계 vs 사후 검증** 한 줄 비교.",
    },
    21: {
        "role": "방법 ③a — **PINN** (물리 in loss).",
        "from_prev": "②번 다음, **PDE·법칙**을 아는 경우.",
        "to_next": "PINN도 **밖에서 깨짐** — 반례 (S22).",
        "natural": "“soft 가정” — **참 PDE ≠ 밖 보증** 미리.",
    },
    22: {
        "role": "방법 ③b — **PINN 반례** (Fesser).",
        "from_prev": "PINN **낙관**을 깨는 장.",
        "to_next": "가정을 못/안 넣을 때 — **UQ·기권** (S23–S24).",
        "natural": "“방법 넣어도 **검증**” — S27 예고.",
    },
    23: {
        "role": "방법 ④a — **UQ** (모름을 신호로).",
        "from_prev": "S11 **모름** 항 — 여기서 활용.",
        "to_next": "UQ도 부족하면 **예측 안 함** (S24).",
        "natural": "softmax ≠ epistemic — **Pfister band**와 짧게 연결.",
    },
    24: {
        "role": "방법 ④b — **기권·abstention** (Zhu).",
        "from_prev": "④a에서 **불확실하면 말하지 말자**.",
        "to_next": "네 방법 **한 장에** — S25 종합.",
        "natural": "“정확도 × 커버리지” — **정직한 시스템** 톤.",
    },
    25: {
        "role": "종합 ① — 실패 원인 ↔ 대응 **매칭表**.",
        "from_prev": "2부 네 이유 + 3부 네 방법 **짝짓기**.",
        "to_next": "실무 **선택 가이드** (S26).",
        "natural": "표를 **위에서 아래로** 읽으며 “이유→대응”.",
    },
    26: {
        "role": "종합 ② — **뭘 고를지** 결정 트리.",
        "from_prev": "매칭表 다음, **선택** 질문.",
        "to_next": "방법 고른 뒤 — **주장 검증** 파트 (S27).",
        "natural": "“가정 넣었으면 끝?” → **아니, 검증**으로 S27.",
    },
    27: {
        "role": "성능 검증 **동기** — 왜 벤치·범위 확인이 필요한지.",
        "from_prev": "대응법 끝. “밖에서도 된다” **믿을 근거**.",
        "to_next": "체크 ① **OoD-Bench** (S28).",
        "natural": "Fesser·S22 echo — **가정+검증** 세트.",
    },
    28: {
        "role": "검증 ① — **OoD-Bench** (밖 종류 분류).",
        "from_prev": "“어떤 밖을 테스트했나?”",
        "to_next": "검증 ② **DomainBed** — 공정 비교 (S29).",
        "natural": "near vs far OOD — **한 예**만.",
    },
    29: {
        "role": "검증 ② — **DomainBed** (공정 HP·ERM).",
        "from_prev": "범위 다음, **비교가 공정했나**.",
        "to_next": "실무 **체크리스트 4항** (S30).",
        "natural": "“ERM + fair budget” — **논문 숫자** 짧게.",
    },
    30: {
        "role": "검증 ③ — **발표자·실무 4항 체크**.",
        "from_prev": "벤치 두 개 → **내 프로젝트에 적용**.",
        "to_next": "전체 **한 장 요약** (S31).",
        "natural": "청중에게 “돌아가서 **네 가지**만 확인” — 행동 유도.",
    },
    31: {
        "role": "전체 요약 — **질문·가정·검증** 삼각형.",
        "from_prev": "3부·검증 끝. **한 장으로 회수**.",
        "to_next": "시간 남으면 **필독 3편** (S32).",
        "natural": "S01 **관통 문장** 다시 — 처음과 **닫힘**.",
    },
    32: {
        "role": "필독 3편 — **어디서부터 읽을지**.",
        "from_prev": "요약 다음, **심화 학습** 안내.",
        "to_next": "Q&A (S33).",
        "natural": "Xu / Pfister / DomainBed — **역할별** 한 줄.",
    },
    33: {
        "role": "Q&A — **남는 질문** + 참고문헌.",
        "from_prev": "—",
        "to_next": "— (마무리)",
        "natural": "예상 Q: “그럼 NN 쓰면 안 되나?” → **“가정 맞추고 검증하라”**.",
    },
}


def fmt_slide_flow(n: int) -> str:
    flow = SLIDE_FLOW.get(n)
    if not flow:
        return ""
    lines = [
        f"**이 장 역할:** {flow['role']}",
        "",
        f"**앞에서:** {flow['from_prev']}",
        "",
        f"**다음으로:** {flow['to_next']}",
    ]
    if flow.get("natural"):
        lines.extend(["", f"**말로 이어 붙이기:** {flow['natural']}"])
    return "\n".join(lines) + "\n"


SLIDE_NAMES = [
    "타이틀", "로드맵", "용어 고정 — 가정(Assumption)", "1부 표지 · 외삽 정의",
    "보간 vs 외삽", "convex hull", "대표 사례 — 다항식", "2부 표지 · 실패 원인 (4)",
    "실패 원인 ① — 함수 못 고름", "실패 원인 ② — 훈련 범위", "실패 원인 ③ — 불확실성",
    "실패 원인 ④ — Xu Thm.1", "ReLU 메커니즘 + 2부 정리", "3부 표지 · 대응·검증",
    "대응법 지도", "입구 — 활성화 매칭", "방법 1a — EQL", "방법 1b — NALU",
    "방법 2a — 단조 문제", "방법 2b — CMNN", "방법 3a — PINN", "방법 3b — PINN 반례",
    "방법 4a — UQ", "방법 4b — 예측 안 함", "종합 (1)", "종합 (2) — 선택 가이드",
    "성능 검증 — 동기", "성능 검증 ① — OoD-Bench", "성능 검증 ② — DomainBed", "성능 검증 ③ — 체크 4항",
    "전체 요약", "필독 3편", "Q&A · 참고문헌",
]

EXTRA_REFS: dict[int, list[str]] = {
    1: ["xu", "pfister", "domainbed"],
    2: ["bartley"],
    3: ["pfister", "xu", "runje", "raissi", "zhu"],
    4: ["bartley"],
    5: ["bartley", "xu"],
    6: ["bartley", "ye2022"],
    7: ["pfister"],
    9: ["pfister", "aykol", "li2023"],
    10: ["bartley", "ye2022"],
    11: ["ghahramani", "zhu"],
    12: ["xu"],
    13: ["xu"],
    15: ["eql", "nalu", "runje", "raissi", "fesser", "zhu"],
    16: ["xu"],
    23: ["ghahramani"],
    25: ["xu", "eql", "runje", "raissi", "fesser", "ghahramani", "zhu"],
    27: ["fesser", "bartley", "liu"],
    28: ["ye2022", "ye2021", "liu"],
    29: ["domainbed", "arjovsky2019"],
    30: ["bartley", "ye2022", "domainbed"],
    33: ["xu", "pfister", "bartley", "eql", "nalu", "runje", "raissi", "fesser", "zhu", "ye2022", "domainbed", "note"],
}


def _extract_note_block(text: str) -> str:
    """Join Python implicit string literals in note(...)."""
    parts = re.findall(r'"((?:[^"\\]|\\.)*)"', text)
    return "".join(parts).replace("\\n", "\n").strip()


_CARD_RE = re.compile(
    r'card_text\(\s*s,\s*Inches\([^)]+\),\s*Inches\([^)]+\),\s*Inches\([^)]+\),\s*Inches\([^)]+\),\s*'
    r'"([^"]+)",\s*\[(.*?)\]',
    re.S,
)


def _parse_bullets(raw: str) -> list[str]:
    return [b.strip() for b in re.findall(r'"([^"]*)"', raw) if b.strip()]


def extract_slide_detail(block: str, slide: dict) -> str:
    """Build ③ body from PPT builder source (cards, figures, takeaway)."""
    parts: list[str] = []

    kicker = slide.get("kicker") or ""
    title = slide.get("title") or ""
    if kicker or title:
        parts.append(f"**장표 제목:** {kicker} — {title}".rstrip(" — "))
    if slide.get("subtitle"):
        parts.append(f"**부제:** {slide['subtitle']}")

    if slide.get("kind") == "section":
        pm = re.search(r"points=\[(.*?)\]", block, re.S)
        if pm:
            pts = _parse_bullets(pm.group(1))
            if pts:
                parts.append("\n**이 부 표지 — 다룰 내용**")
                parts.extend(f"- {p}" for p in pts)

    figs: list[str] = []
    for m in re.finditer(r'ASSETS / "([^"]+\.png)"', block):
        figs.append(f"`_assets/{m.group(1)}`")
    for m in re.finditer(r'add_paper_fig\(s,\s*"([^"]+)"', block):
        cap = ""
        cm = re.search(
            rf'add_paper_fig\(s,\s*"{re.escape(m.group(1))}"[^)]*caption="([^"]*)"',
            block,
        )
        if cm:
            cap = f" — {cm.group(1)}"
        figs.append(f"`_assets/paper_figs/{m.group(1)}`{cap}")
    if figs:
        parts.append("\n**그림**")
        parts.extend(f"- {f}" for f in dict.fromkeys(figs))

    cards = [(m.group(1), _parse_bullets(m.group(2))) for m in _CARD_RE.finditer(block)]
    if cards:
        parts.append("\n**장표 핵심 (카드)**")
        for ct, bullets in cards:
            parts.append(f"\n*{ct}*")
            parts.extend(f"- {b}" for b in bullets)

    tm = re.search(r'takeaway\(s,\s*"([^"]*)"(?:,\s*"([^"]*)")?', block)
    if tm:
        parts.append("\n**하단 takeaway**")
        parts.append(f"- **{tm.group(1)}**")
        if tm.group(2):
            parts.append(f"- {tm.group(2)}")

    cm = re.search(r'credit\(s,\s*"([^"]*)"', block)
    if cm:
        parts.append(f"\n**출처:** {cm.group(1)}")

    return "\n".join(parts).strip() + "\n"


def parse_slides(build_text: str) -> list[dict]:
    slides: list[dict] = []
    lines = build_text.splitlines()
    i = 0
    current: dict | None = None
    block_lines: list[str] = []

    def flush() -> None:
        nonlocal current, block_lines
        if current:
            block = "\n".join(block_lines)
            current["block"] = block
            current["detail_md"] = extract_slide_detail(block, current)
            slides.append(current)
        current = None
        block_lines = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("# ── S1 타이틀") or line.startswith("# ── S2 ") or line.startswith("# ── S3 NEW"):
            flush()
            current = {"papers": [], "note": "", "kicker": "", "title": "", "subtitle": ""}
            block_lines = [line]
            i += 1
            continue
        if line.startswith("section_slide("):
            flush()
            block = line
            j = i + 1
            while j < len(lines) and ")" not in lines[j]:
                block += "\n" + lines[j]
                j += 1
            block += "\n" + lines[j]
            ms = re.findall(r'"([^"]+)"', block)
            current = {
                "kind": "section",
                "kicker": "",
                "title": ms[0] if ms else "",
                "subtitle": ms[1] if len(ms) > 1 else "",
                "papers": [],
                "note": "",
            }
            block_lines = [block]
            i = j + 1
            continue
        if line.startswith("# ── S") and "NEW" not in line and "타이틀" not in line:
            flush()
            current = {"kind": "content", "kicker": "", "title": "", "subtitle": "", "papers": [], "note": ""}
            block_lines = [line]
            i += 1
            continue
        if current is not None:
            block_lines.append(line)
            if "content_header(s," in line:
                m = re.search(r'content_header\(s,\s*"([^"]*)",\s*"([^"]*)"', line)
                if m:
                    current["kicker"] = m.group(1)
                    current["title"] = m.group(2)
            if line.strip().startswith("note("):
                nblock = line
                j = i + 1
                while j < len(lines):
                    nblock += "\n" + lines[j]
                    block_lines.append(lines[j])
                    if re.search(r"\)\s*$", lines[j].strip()):
                        break
                    j += 1
                inner = re.search(r"note\([^,]+,\s*(.*)\)\s*$", nblock, re.S)
                if inner:
                    current["note"] = _extract_note_block(inner.group(1))
                i = j + 1
                continue
            if line.strip().startswith("note(prs.slides[-1]"):
                nblock = line
                j = i + 1
                while j < len(lines):
                    nblock += "\n" + lines[j]
                    block_lines.append(lines[j])
                    if re.search(r"\)\s*$", lines[j].strip()):
                        break
                    j += 1
                inner = re.search(r"note\([^,]+,\s*(.*)\)\s*$", nblock, re.S)
                if inner:
                    current["note"] = _extract_note_block(inner.group(1))
                i = j + 1
                continue
            if "pdf_btn(s," in line and "pdf_btn(s, key" not in line:
                pm = re.search(r'pdf_btn\(s,\s*"([^"]+)"', line)
                if pm and pm.group(1) not in current["papers"]:
                    current["papers"].append(pm.group(1))
        i += 1
    flush()

    slides[0]["kicker"] = "타이틀"
    slides[0]["title"] = "외삽 (Extrapolation) — 훈련 범위 밖 예측"
    slides[0]["detail_md"] = (
        "**장표 제목:** 타이틀 — 외삽 (Extrapolation) — 훈련 데이터 밖에서 모델은 무엇을 하는가\n"
        "**부제:** 1부 외삽 정의 · 2부 실패 원인 · 3부 대응법 + 성능 검증\n"
    )
    if len(slides) >= 32:
        slides[31]["papers"] = ["xu", "runje", "domainbed"]
    return slides


def fmt_refs(keys: list[str]) -> str:
    keys = [k for k in dict.fromkeys(keys) if k in PDF_META]
    if not keys:
        return "_개념·종합 장 — 아래 상세·[부록 C](#부록-c) 참조._\n"
    rows = ["| 논문 | PDF | 부록 |", "|------|-----|------|"]
    for k in keys:
        a, b, c = PDF_META[k]
        anc = PAPER_APPENDIX.get(k, "")
        ref = f"[#{anc.upper()}](#{anc})" if anc else "부록 C"
        rows.append(f"| {a} — {b} | `{c}` | {ref} |")
    return "\n".join(rows) + "\n"


def main() -> None:
    build = BUILD.read_text(encoding="utf-8")
    appendices = APPENDIX.read_text(encoding="utf-8") if APPENDIX.exists() else "_부록 파일 없음_\n"

    slides = parse_slides(build)

    parts: list[str] = [
        "# 외삽 50분 발표 — 장표별 설명 (v5 심화)\n",
        "**대응 PPT:** `외삽_50분_발표자료_v5_심화.pptx` (33장)  ",
        "**관통 문장:** 밖을 지탱하는 것은 데이터가 아니라 **가정(Assumption)** 이다.\n",
        "---\n",
        "## 이 문서 읽는 법\n",
        "| 구분 | 보면 되는 곳 |",
        "|------|-------------|",
        "| **발표 중 (대본만)** | 각 장 **슬라이드** → **⓪ 발표 흐름** → **① 참조 논문** → **② 발표 대본** |",
        "| **준비·복습 (상세)** | `---` 아래 **③ 장표·논문 상세** |",
        "| **논문 전체 파악** | **Part B · [부록 C](#부록-c)** (23편 — 문제·방법·결과·한계) |",
        "\n> **구조:** 슬라이드 미리보기 → **⓪ 흐름·연결** → 논문 표 + 대본 / `---` 아래 = 장표 내용 + 논문 요약 / **부록 C** = 논문별 풀 가이드\n",
        "\n> 미리보기 PNG: `_assets/slide_previews/S01.png` … (`python3 export_slide_previews.py`로 재생성)\n",
        "\n---\n",
        "## 목차·시간\n",
        "| 부 | 장 | 시간 | 내용 |\n",
        "|----|-----|------|------|\n",
        "| 도입 | S01–S03 | 3분 | 로드맵·용어(가정) |\n",
        "| 1부 | S04–S07 | 5분 | **외삽 정의** — 보간/외삽·훈련 범위 |\n",
        "| 2부 | S08–S13 | 15분 | **실패 원인** — 밖 예측이 깨지는 이유 4가지 |\n",
        "| 3부 | S14–S30 | 27분 | **대응법 + 성능 검증** — 가정 넣기·주장 확인 |\n",
        "| 엔딩 | S31–S33 | 3분 | 요약·필독·Q&A |\n",
        "\n---\n",
        "## 발표 스토리라인\n",
        NARRATIVE_ARC,
        "\n---\n",
        "## 대본만 빠르게 (② 링크)\n",
    ]

    for idx, sl in enumerate(slides):
        n = idx + 1
        sid = f"S{n:02d}"
        name = SLIDE_NAMES[idx]
        parts.append(f"- [{sid} · {name}](#{sid.lower()}) → ②")

    parts.append(
        "\n---\n"
        "# Part A · 장표별 가이드\n"
        "> 장마다 **⓪ 흐름 → ① 논문 → ② 대본** (`---` 위) · **③ 상세** (`---` 아래).\n"
    )

    for idx, sl in enumerate(slides):
        n = idx + 1
        sid = f"S{n:02d}"
        name = SLIDE_NAMES[idx]
        anchor = sid.lower()
        keys = list(sl.get("papers") or [])
        for k in EXTRA_REFS.get(n, []):
            if k not in keys:
                keys.append(k)

        parts.append(f"\n## {sid} · {name} {{#{anchor}}}\n")
        preview = f"_assets/slide_previews/{sid}.png"
        if (ROOT / preview).exists():
            parts.append(f"**슬라이드 {n}/33**\n")
            parts.append(f"![{sid} 슬라이드]({preview})\n")
        else:
            parts.append(f"_슬라이드 미리보기 없음 — `python3 export_slide_previews.py` 실행_\n")
        flow_md = fmt_slide_flow(n)
        if flow_md:
            parts.append("### ⓪ 발표 흐름\n")
            parts.append(flow_md)
        parts.append("### ① 참조 논문\n")
        parts.append(fmt_refs(keys))
        parts.append("### ② 발표 대본\n")
        note = (sl.get("note") or "").strip() or "_대본 없음_"
        parts.append(f"```text\n{note}\n```\n")
        parts.append("---\n")
        parts.append("### ③ 장표·논문 상세\n")
        parts.append(sl.get("detail_md") or "")

        if keys:
            parts.append("\n**논문 상세 (이 장)**\n")
            for k in keys:
                if k in PDF_META:
                    parts.append(fmt_paper_slide_detail(k))
            parts.append("_전문·수식·실험 숫자 → [부록 C · 참조 논문 상세 정리](#부록-c)_\n")
        parts.append("\n---\n")

    parts.append("\n# Part B · 부록\n\n")
    parts.append(appendices or "_부록 없음_\n")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"saved {OUT} slides={len(slides)}")


if __name__ == "__main__":
    main()
