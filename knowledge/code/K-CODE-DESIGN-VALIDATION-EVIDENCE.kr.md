# 후속 작업을 확정하기 전에 위험한 설계 가정에 맞는 근거 고르기

결정을 바꿀 주장에 따라 시나리오, 호출자 측정, 상태 모델, 복구 훈련 또는 플레이테스트를 선택하고 조건과 미검증 범위를 기록한다.

ID `K-CODE-DESIGN-VALIDATION-EVIDENCE` · 방법 · 활성 · 근거 확인 2026-11-25

적용 범위 — 품질 목표, 용량, 상태 전이 또는 복구 가정이 불확실한 소프트웨어·게임 설계

## 지침

어떤 관찰이 선택을 뒤집을지부터 정한다. 품질 목표가 충돌하면 한 설계 변수를 바꿔 어떤 목표가 개선·악화되는지 본다. 용량은 명시한 부하에서 자원을 추정하고 대표 호출을 호출자 쪽에서 잰다. 복구는 확인 응답 전후에 각각 중단해 재시작·정합화·재개까지 상태를 따라간다. 작은 상태 모델로 사람이 추적하다 놓치는 교차 실행을 탐색할 수 있다.

## 적용 범위와 예외

오판 비용이 크고 아직 결정을 바꿀 수 있을 때 실험한다. 모델의 범위는 표현한 상태와 결함에 달려 있고 용량 추정에는 부하 측정이 필요하다. 플레이어가 이해했는지를 보려면 기존 플레이테스트 절차를 이용한다. 설계 검토만으로 실행 결과를 입증할 수 없다. [the existing playtest method](../game/K-GAME-PROTOTYPE-PLAYTEST.md)

## 확인 방법

자동 저장은 확인 응답 후 어떤 버전이 보장되는지 정한다. 응답 직전·직후 장애를 추적한다. 플랫폼 파일 교체 방식에 결론이 달렸다면 의존 작업을 확정하기 전에 대상 런타임에서 확인한다. 수정 후 반례를 반복하고 예측 또는 관찰, 조건, 남은 검사와 담당자를 남긴다.

캐시 만료 간격을 늘려 지연과 최신성의 상충을 드러낸다. 처리량 경계는 요청률과 페이로드 크기를 곱해 구하고 어떤 입력이 두 배가 되면 선택이 뒤집히는지 찾는다. 추정값은 실제 부하를 관찰한 뒤 측정과 비교한다. 튜토리얼은 의도한 행동을 합의하고 이벤트 발생을 검사한 뒤 초보자를 코칭 없이 관찰해 판단에 쓴 단서를 묻는다. 플레이 한 번으로 반례는 찾을 수 있으나 전체 성공률을 추정할 수는 없다. [Review and handoff](K-CODE-ACTIVE-DESIGN-REVIEW.md)

## 근거

ATAM은 품질 상충을 식별하고 Google SRE 워크북 12장은 자원 추정법을 다룬다. DynamoDB 설계의 AWS 모델에서 데이터 손실 가능성을 보인 가장 짧은 경로는 상위 수준 35단계였다. 모델이 다루는 결함을 적고 구현을 따로 검증한다. GitHub의 2018년 네트워크 단절은 43초였으나 성능 저하는 24시간 11분 이어졌다. 정상 복구를 선언하기 전에 밀린 작업 처리와 정합화를 확인한다. 수치는 각 원래 시스템의 사례다. [ATAM](https://sei.cmu.edu/documents/629/2000_005_001_13706.pdf) · [SRE workbook](https://sre.google/workbook/non-abstract-design/) · [AWS paper](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods) · [DynamoDB case excerpt](https://lamport.azurewebsites.net/tla/amazon-excerpt.html) · [GitHub recovery timeline](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/)

Lamport의 강연은 동시 상태에서 보존할 성질을 명시하는 방법을 소개한다. Ambinder의 GDC 발표는 사망 지점 열지도 같은 계측과 함께 직접 관찰과 플레이어 설명을 사용한다. 강연 공식 소개와 공개 Valve 슬라이드에서 확인 가능한 방법이다. [Microsoft Research lecture](https://www.microsoft.com/en-us/research/video/thinking-above-the-code/) · [Valve GDC session](https://gdcvault.com/play/1566/Valve-s-Approach-to-Playtesting) · [Valve slides](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf)
