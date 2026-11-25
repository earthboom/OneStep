---
id: K-CODE-ACTIVE-DESIGN-REVIEW
title: "다음 구현자가 설계를 실제로 사용해 보는 독립 교차검토"
summary: "원래 요청에서 기대 결과를 독립적으로 정한 뒤, 다음 구현자가 설계대로 호출을 추적한다. 두 결과가 처음 갈라진 지점을 수정하고 같은 사례로 재검사한다."
kind: method
scope: "요구 해석이나 누락된 계약에 따라 합격 판정이 달라지는 소프트웨어 설계 검토와 인수인계"
keywords: ["design review","independent review","active design review","ARID","acceptance criteria","cross-check","설계 검수","설계 리뷰","설계 검증","교차검토","교차검증","크로스체크","인수인계","설계 완성도","요구사항 누락","구현 착수","개발 설계를 구현에 넘기기 전에","동료 검토","설계 인계","호출 절차"]
status: active
checked_at: 2026-11-25
---

# 다음 구현자가 설계를 실제로 사용해 보는 독립 교차검토

## 지침

검토자에게 원래 요청과 동작을 정의하는 원문을 먼저 준다. 정상 입력 하나와 두 해석이 서로 다른 결과를 내는 사례 하나의 기대값을 쓰게 한다. 이후 설계를 제공하고 호출 절차나 의사코드를 작성하게 한다. 없는 규칙을 추측해야 하는 첫 단계를 기록한다. 제품 정책은 결정권자에게, 기술적 미확인 사항은 원문 계약이나 실험에 대조한다.

## 적용 범위와 예외

공유 API, 소유권 이전, 저장과 복구처럼 인계 단계에서 보장이 달라질 수 있는 작업에 쓴다. 표시 문구만 바꾸고 판정이 명확하다면 해당 표시를 바로 확인한다. 문헌을 종합한 방법이며 리뷰어의 합의만으로 구현 동작을 입증할 수 없다.

## 검사

예를 들어 작업 폴더에는 피드백 파일 두 개가 있지만 지정 접수함에는 영문만 있다. 기대 접수 상태를 정하고 호출자가 확인하는 경로를 따라간다. 누락 파일을 보완한 뒤 같은 검사를 반복한다. 상태 전환의 기대 결과와 근거, 구현 후에만 할 수 있는 검사를 함께 인계한다. [OneStep 접수 계약](../../feedback/README.md)

## 근거

NASA §4.4는 기술 요구의 충족 여부와 의도된 사용에 맞는지를 구분한다. ARID §2.2는 실제 사용자가 설계대로 호출해 보게 한다. Porter 등의 실험은 사람이 요구 명세를 시나리오별로 검사한 결과이며 Huang 등의 연구는 LLM의 외부 피드백 없는 추론 교정을 다룬다. 두 실험 모두 OneStep에서 AI 설계 검토의 효과를 측정하지 않았다. [NASA 핸드북](https://www.nasa.gov/reference/4-4-design-solution-definition/) · [ARID 보고서](https://www.sei.cmu.edu/documents/1962/2000_004_001_13685.pdf) · [Porter 외](https://www.cs.umd.edu/~basili/publications/technical/T101.pdf) · [Huang 외](https://arxiv.org/abs/2310.01798) · [조사 보고서와 자료별 한계](../../docs/research/2026-11-25-design-review-and-cross-check.kr.md)

검토 깊이와 참여자를 고를 때는 설계 문서 작성 비용과 영향받는 팀의 역할에 대한 실무자 경험도 참고한다. [Malte Ubl의 구글 설계 문서 경험](https://www.industrialempathy.com/posts/design-docs-at-google/)
