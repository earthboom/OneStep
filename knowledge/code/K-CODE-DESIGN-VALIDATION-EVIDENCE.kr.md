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

모든 호출이 2초 이하여야 한다면 0.8초 49건과 2.0004초 1건을 반례로 쓴다. 이 회차의 P95는 0.8초다. 모든 호출 조건은 실패하므로 호출 위치에서 반올림 전 값으로 판정한다. [프로젝트 측정 이력](K-CODE-RETRIEVAL-SCALE.kr.md)

## 근거

ATAM으로 캐시 만료 시간을 늘렸을 때 지연과 최신성이 어떻게 달라지는지 보고 실제 지연을 측정한다. SRE 책 12장은 부하, 자원과 저하 상태에서의 운영을 연결한다. 요청률에 페이로드 크기를 곱하고, 어떤 입력이 바뀌면 결정이 달라지는지 찾는다. [ATAM](https://sei.cmu.edu/documents/629/2000_005_001_13706.pdf) · [SRE 책](https://sre.google/workbook/non-abstract-design/) · [AWS 논문](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods) · [GitHub 복구 기록](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/)

AWS DynamoDB 사례의 잠재적 데이터 손실을 드러낸 가장 짧은 모델 경로는 상위 단계 35개였다. 모델이 다룬 장애와 빠진 조건을 기록하고 구현에서도 검사한다. 2018년 10월 GitHub 사례는 43초 연결 끊김과 24시간 11분의 서비스 저하를 기록했다. 복구 실험에서는 백로그 처리, 상태 대조, 정상 쓰기 재개를 각각 추적한다. [DynamoDB 사례 발췌](https://lamport.azurewebsites.net/tla/amazon-excerpt.html)

동시 상태의 보존 조건은 Lamport 강연의 공식 소개에서 출발한다. Ambinder의 GDC 세션 소개와 슬라이드는 플레이 관찰, 플레이어 설명과 사망 위치의 히트맵을 함께 쓴다. 도움 없이 플레이하게 한 뒤 어떤 신호를 보고 선택했는지 묻는다. 히트맵은 행동 위치를 보여 준다. [GDC 세션](https://gdcvault.com/play/1566/Valve-s-Approach-to-Playtesting) [Microsoft Research 강연](https://www.microsoft.com/en-us/research/video/thinking-above-the-code/) · [Valve 발표 자료](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf)
