# 행동·증상·식별자로 이전 사례 찾기

요청자가 쓴 표현과 실패 전에 사례를 찾을 수 있었던 행동을 함께 기록한다. 이전 해결책을 적용하기 전에 환경과 원인, 예방책의 근거를 확인한다.

ID `K-SHARED-INCIDENT-RETRIEVAL` · 방법 · 활성 · 근거 확인 2026-11-23

적용 범위 — 소프트웨어·게임·소설의 짧은 지식 및 사건 기록을 검색하고 재사용할 때

## 지침

작업 전에는 수행할 일과 제약을 알고 있으므로 사건 기록의 `trigger`에 넣는다. 실패 뒤에는 실제로 본 현상과 구별되는 단서를 `symptom`에 당시 표현대로 적는다. 이전 검토를 이어가는 사람을 위해 ID 철자와 구두점을 보존한다. 동일한 원인과 범위를 다룬 항목이 있으면 사람들이 찾지 못했던 표현과 검사를 거기에 보강한다. [KCS, capture in the requester's context](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/030/010/020) · [Sadowski et al., developer search goals](https://research.google/pubs/how-developers-search-for-code-a-case-study/)

## 적용 범위와 예외

검색한 기록의 환경, 구성 요소, 원인 확실성, 예방책 상태와 검증 근거를 비교한다. 조건이 맞는 검증된 검사는 재사용하고, 제안된 검사는 적용 전에 시험한다. 해결된 사례도 검색할 가치가 있다. 비슷한 증상의 원인이 다르면 새 진단이 필요하다. Sun 등의 연구는 세 프로젝트에서 본문과 제품·구성 요소·버전을 결합했다. 해당 연구의 가중치를 이 저장소에서 검증한 것은 아니다. [Sun et al., ASE](https://cs.uwaterloo.ca/~cnsun/public/publication/ase11/ase11.pdf) · [Google SRE incident management](https://sre.google/resources/practices-and-processes/incident-management-guide/)

## 확인 방법

질문 유형별 기대 결과와 표시 한도를 먼저 정한다. 첫 필수 항목의 순위, 모든 필수 ID의 재현율, 혼동하기 쉬운 오답, 빈 결과를 구별해 검사한다. 첫 순위가 높아도 다른 필수 항목이 빠지거나 하위 결과가 틀릴 수 있다. 한국어 조사가 붙은 기술명, 비슷한 긴 식별자와 다른 접미사를 비교한다. 필터와 환경이 같은 독립 질문은 한 번에 보내되 각 답의 적용 조건을 확인한다. [OneStep retrieval contract](../../skills/vegabond-knowledge/references/retrieval.md) · [Stanford CS224U, index at 7:25 and metrics at 20:01–21:13](https://www.youtube.com/watch?v=e8zKKDMAze8)

## 근거

실제 기록 172건에서 경로 탐색 항목에 튜플 정렬과 필드 경계 검사를 추가하자 6위에서 1위로 올랐다. 기존 검색 코드도 수정된 문서에서는 기존 질문을 모두 통과했다. 무엇이 개선됐는지 보려면 같은 문서에서 이전·새 순위 계산기를 비교한다. 별도 회귀 사례가 조사 경계와 정확한 ID 우선순위를 확인했다. 파서 사건은 예방책이 검증됐고 원고 대화 사건은 검사 제안 단계였다. [Pathfinding entry](../game/K-GAME-TECH-PATH.md) · [검색 실험 기록](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-23-korean-retrieval-at-30000.md)

BEIR는 18개 데이터셋의 어휘 검색 기준선을 제시한다. MIRACL은 한국어를 포함한 여러 언어에서 사람이 판정한 관련성을 제공한다. 색인·재순위화·한국어 분석을 검토할 때 실제 기록 유형의 질의로 평가한다. 공개 벤치마크 점수만으로 이 짧은 기록의 정밀도를 예측할 수 없다. [BEIR](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html) · [MIRACL paper](https://aclanthology.org/2023.tacl-1.63/) · [MIRACL language coverage](https://project-miracl.github.io/)
