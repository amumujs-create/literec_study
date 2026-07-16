# 외삽 발표자료 v3.1 Outline

## 파일

- **PPT**: `외삽_50분_발표자료_v3.pptx` (37장, ~2.1MB)
- **재생성**: `python3 build_ppt_v3.py`

## 스토리라인 (ACT 구조)

```
PROLOGUE  → 왜 외삽인가 + 로드맵
ACT 1     → 외삽 기초 (보간/외삽, Hull, UQ)        → Section 1 정리
ACT 2     → OOD 기초 (정의, shift, 목표)           → Section 2 정리
ACT 3     → OOD 알고리즘 (ERM, IRM, DRO, DomainBed) → Section 3 정리
ACT 4     → NN 외삽 (ReLU, EQL, NALU, PINN)        → Section 4 정리
ACT 5     → N-CMAPSS 사례 (APEX-Guard)             → Section 5 정리
EPILOGUE  → 4가지 열쇠 + Q&A
```

## Figure 재점검 (v3.1)

| 슬라이드 | Figure | 변경 |
|----------|--------|------|
| OOD란? | `ood_shift_diagram.png` | Liu SCM(부적합) → 자체 diagram |
| IRM 동기 | `irm_fig3_colored_mnist_setup.png` | Fig 3 (Colored MNIST setup) |
| IRM 결과 | `irm_fig4_results_bars.png` | Fig 4 (bar chart) |
| PINN 원리 | `raissi_pinn_solution.png` | 텍스트 페이지 → Burgers solution |
| PINN 실패 | `fesser_pinn_failure_fig1.png` | 유지 |
| GroupDRO | `groupdro_spurious_examples.png` | 이름·crop 정리 |

## 디자인

- 연한 배경 + 좌측 accent stripe
- 슬라이드마다 **핵심 한 줄** 박스
- Figure **캡션** (출처 명시)
- **섹션 정리** 슬라이드 (번호 + 다음 ACT 안내)
