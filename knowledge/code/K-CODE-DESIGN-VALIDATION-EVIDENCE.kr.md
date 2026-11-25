---
id: K-CODE-DESIGN-VALIDATION-EVIDENCE
title: "위험한 설계 가정에 맞는 검증 방법 선택"
summary: "설계 결정을 바꿀 수 있는 가정에 맞춰 시나리오, 호출자 실측, 상태 모델, 복구 연습, 플레이테스트를 선택한다. 근거의 적용 조건과 남은 검사를 함께 기록한다."
kind: method
scope: "품질 목표, 용량, 상태 전환 또는 복구 조건이 불확실한 소프트웨어·게임 아키텍처 결정"
keywords: ["architecture evaluation","ATAM","design validation","state model","model checking","recovery exercise","capacity planning","설계 검증","검증 방법","가정 검증","위험 분석","모델 검사","복구 검증","성능 추정","설계 반례","상태 전이"]
status: active
checked_at: 2026-11-25
---

# 위험한 설계 가정에 맞는 검증 방법 선택

## 지침

어떤 관찰이 나오면 결정을 바꿀지 먼저 정한다. 품질 목표가 충돌하면 설계 변수 하나를 바꾸어 어느 목표가 개선되고 어느 목표가 악화되는지 본다. 용량은 부하 가정을 밝히고 자원을 추정한 뒤 대표 사례를 호출자 위치에서 실측한다. 복구는 완료 응답 직전·직후에 중단하고 재시작, 데이터 정합성 회복, 정상 동작 재개까지 추적한다. 작은 상태 모델로 사람이 놓치기 쉬운 사건 순서도 탐색할 수 있다.

## 적용 범위와 예외

잘못된 가정의 비용이 크고 결과가 아직 결정을 바꿀 수 있을 때 실험에 투자한다. 모델 검사 결과는 포함한 상태와 장애에 한정되고 용량 추정에는 실제 부하 측정이 필요하다. 플레이어의 이해 여부가 쟁점이면 [기존 플레이테스트 지식](../game/K-GAME-PROTOTYPE-PLAYTEST.kr.md)을 쓴다. 설계 문서 검토만으로 런타임이나 플레이 경험을 입증할 수 없다.

## 검사

자동 저장이라면 완료 표시 후 보존해야 할 버전을 정하고 완료 직전과 직후에 중단했을 때를 추적한다. 판정이 플랫폼의 파일 교체 보장에 달렸다면 그 보장에 의존하는 작업에 착수하기 전에 해당 런타임에서 확인한다. 설계 수정 후 동일한 반례를 재검사하고, 예측과 관찰을 구분해 조건·남은 검사·담당자를 기록한다.

## 근거

ATAM은 서로 충돌하는 품질 속성을 드러낸다. Google SRE 책 12장은 자원 추정 사례, AWS 논문은 모델이 밝혀낸 사건 순서 결함, GitHub 회고는 연결 복구와 서비스 회복의 시차를 보여 준다. 실제 프로젝트의 측정값은 별도로 구해야 한다. [ATAM](https://sei.cmu.edu/documents/629/2000_005_001_13706.pdf) · [SRE 책](https://sre.google/workbook/non-abstract-design/) · [AWS 논문](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods) · [GitHub 복구 기록](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/) · [조사 보고서와 자료별 한계](../../docs/research/2026-11-25-design-review-and-cross-check.kr.md)

동시 상태의 보존 조건을 명세하는 출발점은 Lamport 강연을, 플레이어 행동을 직접 관찰하고 설명을 들어 해석하는 방법은 Ambinder의 GDC 발표 자료를 참고한다. [Microsoft Research 강연](https://www.microsoft.com/en-us/research/video/thinking-above-the-code/) · [Valve 발표 자료](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf)
