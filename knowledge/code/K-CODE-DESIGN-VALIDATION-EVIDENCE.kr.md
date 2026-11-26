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

모든 호출이 2초 이하여야 한다면 0.8초 49건과 2.0004초 1건을 반례로 쓴다. 이 회차의 P95는 0.8초다. 모든 호출 조건은 실패하므로 호출 위치에서 반올림 전 값으로 판정한다. [프로젝트 측정 이력](../../docs/research/2026-11-23-korean-retrieval-at-30000.kr.md)

## 근거

ATAM으로 캐시 만료 시간을 늘렸을 때 지연과 최신성이 어떻게 달라지는지 보고 실제 지연을 측정한다. SRE 책 12장은 부하, 자원과 저하 상태에서의 운영을 연결한다. 요청률에 페이로드 크기를 곱하고, 어떤 입력이 바뀌면 결정이 달라지는지 찾는다. [ATAM](https://sei.cmu.edu/documents/629/2000_005_001_13706.pdf) · [SRE 책](https://sre.google/workbook/non-abstract-design/) · [AWS 논문](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods) · [GitHub 복구 기록](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/)

AWS DynamoDB 사례의 잠재적 데이터 손실을 드러낸 가장 짧은 모델 경로는 상위 단계 35개였다. 모델이 다룬 장애와 빠진 조건을 기록하고 구현에서도 검사한다. 2018년 10월 GitHub 사례는 43초 연결 끊김과 24시간 11분의 서비스 저하를 기록했다. 복구 실험에서는 백로그 처리, 상태 대조, 정상 쓰기 재개를 각각 추적한다. [DynamoDB 사례 발췌](https://lamport.azurewebsites.net/tla/amazon-excerpt.html)

동시 상태의 보존 조건은 Lamport 강연의 공식 소개에서 출발한다. Ambinder의 GDC 세션 소개와 슬라이드는 플레이 관찰, 플레이어 설명과 사망 위치의 히트맵을 함께 쓴다. 도움 없이 플레이하게 한 뒤 어떤 신호를 보고 선택했는지 묻는다. 히트맵은 행동 위치를 보여 준다. [GDC 세션](https://gdcvault.com/play/1566/Valve-s-Approach-to-Playtesting) [Microsoft Research 강연](https://www.microsoft.com/en-us/research/video/thinking-above-the-code/) · [Valve 발표 자료](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf)
