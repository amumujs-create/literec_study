"""Apply v6 slide-text polish to build_presentation_v6.py (run once)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "build_presentation_v6.py"
text = path.read_text(encoding="utf-8")

# Order matters — specific before general
PAIRS = [
    # meta
    (
        '"""Build 외삽 50분 발표자료 v5 — 단일 축(가정) 심화판. 발표자 노트에 대본 전문 포함."""',
        '"""Build 외삽 50분 발표자료 v6 — 말투·용어 정리판 (v5 기반)."""',
    ),
    ("OUT = ROOT / \"외삽_50분_발표자료_v5_심화.pptx\"", 'OUT = ROOT / "외삽_50분_발표자료_v6.pptx"'),
    ("# v5 — 세 가지 질문으로 진행", "# v6 — v5 기반 · 장표 말투·용어 정리"),
    # holdout → 밖 구간 시험
    ('"검증 — hull 밖 holdout · baseline · UQ"', '"검증 — 훈련 범위 밖 시험 · baseline · UQ"'),
    ('"성능 검증: hull 밖 holdout · baseline · UQ"', '"성능 검증: 훈련 범위 밖 시험 · baseline · UQ"'),
    ('"L = L_data + **λ·L_physics** · soft · **holdout** 필수"', '"L = L_data + **λ·L_physics** · soft · **밖 구간 시험** 필수"'),
    ('"Fesser: soft constraint — OOD holdout 재검증 필수."', '"Fesser: soft constraint — OOD 밖 구간에서 재검증 필수."'),
    ('"Feature(Li) · Loss(Aykol) · **holdout**"', '"Feature(Li) · Loss(Aykol) · **밖 구간 시험**"'),
    ('"→ hull 밖 holdout · baseline · UQ 확인"', '"→ 훈련 범위 밖 시험 · baseline · UQ 확인"'),
    ('"② 회귀 holdout 설계"', '"② 밖 구간 시험 설계"'),
    ('"목표 y도 범위 밖이면 **별도** holdout"', '"목표 y도 범위 밖이면 **별도** 시험 세트"'),
    ('"② holdout — 센서·y·시간 **범위 밖**."', '"② 밖 구간 시험 — 센서·y·시간 **범위 밖**."'),
    ('takeaway(s, "hull 밖 holdout · 공정 baseline · UQ 동작"', 'takeaway(s, "훈련 범위 밖 시험 · 공정 baseline · UQ 동작"'),
    ('"IRM/DomainBed=분류 DG · 회귀엔 hull+holdout"', '"IRM/DomainBed=분류 DG · 회귀엔 hull+밖 시험"'),
    ('"검증: hull 밖 holdout"', '"검증: 훈련 범위 밖 시험"'),
    ('"검증 — hull holdout·baseline·UQ."', '"검증 — 밖 구간 시험·baseline·UQ."'),
    # casual → clean
    ('"→ 가정 없이는 외삽 불가"', '"가정 없이는 외삽 불가"'),
    ('takeaway(s, "가중치 자르기: 단조는 얻지만 x³조차 실패 — 표현력 붕괴"', 'takeaway(s, "가중치 자르기: 단조는 얻지만 x³ 실패 — 표현력 저하"'),
    ('"  타깃이 산술 아니면 MLP로 붕괴 · y=a+b 알면 코드가 나음"', '"  타깃이 산술 아니면 MLP 수준으로 퇴화 · y=a+b 알면 코드가 나음"'),
    ('"→ \'모름\'만 구조적으로 커짐 (그림 주황 폭발)"', '"범위 밖에서는 \'모름\'(epistemic)만 구조적으로 커짐"'),
    ('"경계를 넘는 즉시 발산"', '"경계를 넘으면 급격히 벗어남"'),
    ('"  밖은 더 크게 터진다"', '"  밖은 오차가 더 커진다"'),
    ('"        "  시간 외삽 실패 (Fesser 2023)"', '"        "시간축 외삽 실패 사례 (Fesser 2023)"'),
    # S3 assumption slide
    (
        '"훈련점(●)은 세 곡선 공통 · x>2 밖: A선형·B지수·C비선형 → 예측 전부 다름"',
        '"훈련점(●) 동일 · x>2 밖에서 가정별 예측이 **서로 다름**"',
    ),
    # S5 OOD
    ('"(a) OOD — **분포**가 train≠test"', '"(a) OOD — train과 test **분포**가 다름"'),
    ('"extrap ⊂ OOD **종종**, 같지 않음"', '"외삽 ⊂ OOD인 경우 **많음** · 동일 개념 아님"'),
    ('"OOD → ‘분포가 다른가?’"', '"OOD — \'분포가 다른가?\'"'),
    ('"외삽 → ‘**입력**이 hull 밖인가?’"', '"외삽 — \'**입력**이 훈련 범위 밖인가?\'"'),
    # S6 interp
    ('"입력 x가 훈련 범위 안 → 보간"', '"입력 x가 훈련 범위 **안** — 보간"'),
    ('"입력 x가 훈련 범위 밖 → 외삽"', '"입력 x가 훈련 범위 **밖** — 외삽"'),
    ('takeaway(s, "입력이 훈련 범위 안 → 보간, 밖 → 외삽"', 'takeaway(s, "입력이 훈련 범위 안 — 보간 · 밖 — 외삽"'),
    # S8 identifiability
    ('takeaway(s, "훈련 구간 안에서는 맞춰지지만, 밖에서 갈라진다 — 데이터로는 못 고른다"', 'takeaway(s, "훈련 구간 안에서는 맞춰지지만 밖에서 갈라짐 — 데이터만으로는 선택 불가"'),
    # S9 dimension
    ('takeaway(s, "차원 ↑ ⇒ 훈련 범위 안 확률 → 0 — 고차원 테스트는 대부분 이미 외삽"', 'takeaway(s, "차원이 올라가면 새 입력이 훈련 범위 안일 확률 → 0"'),
    ('"외삽은 예외가 아니라 기본값"', '"외삽은 예외가 아니라 **기본 상황**"'),
    # S10 error decomp - clean 과녁 metaphor slightly
    ('"  → 과녁: 손 떨림 · 어디서나 비슷 · 못 줄임"', '"  측정 한계 — 어디서나 비슷 · 줄이기 어려움"'),
    ('"  → 과녁: 조준 틀림 · 가정·모델 바꾸면 줄임"', '"  모델·가정 문제 — 구조를 바꾸면 줄일 수 있음"'),
    ('"  → 과녁: 위치 모름 · 그 구간 데이터 있으면 줄임"', '"  데이터 부족 — 해당 구간 데이터를 모으면 줄임"'),
    # S11 Xu
    ('"재해석: NN 외삽 불능 ❌ — \'밖 가정\'을 이미 함"', '"재해석: NN이 외삽을 \'못\' 하는 것이 아니라 밖 **가정**을 이미 함"'),
    ('takeaway(s, "ReLU NN — 밖에서 직선 (Xu Thm.1) · φ마다 밖 가정 다름"', 'takeaway(s, "ReLU NN — 밖에서 직선 (Xu Thm.1) · 활성화마다 밖 가정이 다름"'),
    # S12 summary
    ('takeaway(s, "2부 정리 — 질문을 바꿔라: \'외삽 되나?\' → \'모델의 가정이 내 문제와 맞나?\'"', 'takeaway(s, "2부 정리 — \'외삽 되나?\' 대신 \'모델 가정이 문제에 맞는가?\'"'),
    # S14 method map
    ('"대가: soft loss · **밖 검증**"', '"대가: soft loss · **밖 구간 시험** 필수"'),
    # S18 monotonic problem
    ('content_header(s, "3부 · 방법 2", "방향만 안다 (a) — 단조를 강제하면 표현력이 죽는다")', 'content_header(s, "3부 · 방법 2", "방향만 안다 (a) — 단순 강제는 표현력을 희생한다")'),
    ('"(b) 가중치 전부 양수: 단조는 되나 사실상 직선 — x³ 실패"', '"(b) 가중치 전부 양수: 단조는 되나 직선에 가까워짐 — x³ 실패"'),
    ('"  표현력을 죽인다 — (b)"', '"  표현력이 저하됨 — (b)"'),
    # S19 CMNN
    ('takeaway(s, "② CMNN — 방향만 **구조**로 고정"', 'takeaway(s, "② CMNN — 방향을 **구조**로 고정"'),
    ('"다음 ③ — feature·physics loss (mechanism)"', '"다음 ③ — Feature · Physics loss"'),
    # S22 physics
    ('"고 DoD 학습 → 저 DoD 시험 — **train hull 밖**"', '"고 DoD 학습 → 저 DoD 시험 — **훈련 범위 밖**"'),
    ('"순수 ML 외삽은 비선형 실제와 **괴리** — 물리는 OOD에서도 성립"', '"순수 ML 외삽은 비선형 실제와 **괴리** — 물리 법칙은 OOD에서도 성립"'),
    # S23 UQ
    ('"UQ: ‘품질 5.2 (불확실↑)’ · 기권: ‘**예측 안 함** → 재측정’"', '"UQ: \'품질 5.2 (불확실↑)\' · 기권: \'**예측 안 함** — 재측정\'"'),
    ('"고위험: **틀린 답 1번 > 기권 1번**(실험·재측정)"', '"고위험 영역: **틀린 숫자 1번 > 기권 1번**"'),
    # S26 validation
    ('content_header(s, "3부 · 성능 검증 ①", "왜 **회귀 extrap** 검증이 별도인가 — 밖에서도 확신")', 'content_header(s, "3부 · 성능 검증 ①", "왜 **회귀 extrap** 검증이 별도인가"'),
    ('takeaway(s, "테스트가 범위 안이면 외삽 점수는 오인 · 모델은 밖에서도 높은 확신"', 'takeaway(s, "시험이 범위 안이면 외삽 성능을 **과대평가** · 밖에서도 과신할 수 있음"'),
    # S27 checklist
    ('content_header(s, "3부 · 성능 검증 ②", "**회귀** 외삽 성능 주장 전 — 체크 4개")', 'content_header(s, "3부 · 성능 검증 ②", "**회귀** 외삽 주장 전 — 확인 4항목"'),
    ('"min–max box만으로 \'밖\' 판정 **금지**"', '"min–max만으로 \'밖\' 판정 **금지** — hull 사용"'),
    # S28 summary takeaways
    ('takeaway(s, "밖을 지탱하는 것은 데이터가 아니라 가정이다"', 'takeaway(s, "밖을 지탱하는 것은 데이터가 아니라 **가정**"'),
    ('"회귀 extrap: 정의 → 원인 4 → 대응 + hull 검증"', '"회귀 extrap: 정의 · 원인 4 · 대응 + 밖 구간 시험"'),
    # roadmap takeaway
    ('takeaway(s, "외삽 정의 → 실패 원인 4 → 대응법 + 성능 검증"', 'takeaway(s, "정의 · 실패 원인 4 · 대응법 · 성능 검증"'),
]

for old, new in PAIRS:
    if old not in text:
        print("MISSING:", old[:60])
    else:
        text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
print("polished:", path.name)
