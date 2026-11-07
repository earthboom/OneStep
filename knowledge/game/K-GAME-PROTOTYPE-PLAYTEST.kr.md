# 설계 불확실성에 맞춰 시제품과 플레이테스트 구성

사람 전용 번역. AI는 영문 K-GAME-PROTOTYPE-PLAYTEST.md를 사용한다.

ID: K-GAME-PROTOTYPE-PLAYTEST. 유형: 참고 자료. 상태: 사용 가능. 근거 확인일: 2026-11-07.

요약: 기획을 확대하기 전에 중요한 가정을 반박할 수 있는 최소 플레이 표현을 선택한다. 관측 행동·해석·제안 수정·수정 빌드의 실제 개선 근거를 구별한다.

적용 범위: 장르별 게임 설계 시제품·사용성·경험 조사. 고정 일정·표본 수·자동 실행 권한을 뜻하지 않는다.

검색어: prototype, playtest, hypothesis, usability, iteration, vertical-slice, telemetry, 프로토타입, 플레이테스트, 가설, 시제품, 검증, 재미

## 활용 지침

출처 관찰: Experimental Gameplay Project 저자들은 조작 가능한 핵심 메커니즘부터 작은 탐색 빌드를 만들었던 방법을 설명한다 [S1]. Valve 개발자 Ken Birdwell은 외부 플레이어에게 힌트를 주지 않고 관찰하며 결과를 설계에 반영한 사례를 설명한다 [S2]. 게임 조사자 Graham McAllister는 이번 관찰로 답할 수 있는 질문의 우선순위를 맞추도록 제안한다 [S3].

응용 방법: 불확실한 주장과 그것이 실패하면 바뀔 결정을 정한다. 질문에 맞춰 종이 모델·그레이박스·상호작용 시제품·대표 통합 구간을 고른다. 질문에 필요한 피드백은 포함하고 생략 시스템·임시 전제를 표시한다.

답을 가르치지 않는 과제를 준비한다. 행동과 막힘을 관찰한 뒤 이해한 내용을 묻는다. 초심자와 숙련자를 구분하고 빌드·조건을 기록한다. 발견을 근거 있는 최소 변경으로 연결하고 수정 빌드에서 관련 관찰을 반복하며 반대 근거를 보존한다.

## 적용 조건과 예외

7일 프로젝트와 Valve 세션은 역사적 사례이며 보편 일정·표본 수가 아니다. 조작 실험으로 느낌을 살펴볼 수 있지만 완전한 게임의 증거는 아니다. 종이 모델은 실행 타이밍을, 세련된 통합 구간은 콘텐츠 생산 비용을 숨길 수 있다. 사용성·버그·균형·경험·성능 질문을 구별하며 모집·제작·자료 수집·배포에는 실제 작업 범위가 필요하다.

## 확인 항목

제안 점검: 과제가 잘못된 가정을 드러낼 수 있는가? 관찰자의 힌트가 문제를 가리는가? 행동 기록만으로 원인을 단정하지 않는가? 수정은 기록에 그치지 않고 재시험했는가? 표본·표현의 한계를 밝히며 작은 성공으로 잔존이나 전체 이용자 선호를 입증하지 않는다.

## 근거

- [S1] Experimental Gameplay Project 저자들의 [7일 이내 시제품 제작 회고](https://www.gamedeveloper.com/game-platforms/how-to-prototype-a-game-in-under-7-days), 2005. Development·Build the Toy First 원문 확인.
- [S2] Ken Birdwell의 [The Cabal](https://www.gamedeveloper.com/design/the-cabal-valve-s-design-process-for-creating-i-half-life-i-), 1999. Pearls Before Swine의 플레이테스트·설계 수정 원문 확인.
- [S3] Graham McAllister의 [목적 정렬](https://grahammcallister.com/playtesting-book/step-1-alignment-on-clear-purpose), 가설 도입부와 Step 1 Outcome의 저자 공개 본문 확인.
- 확인일 2026-11-07. 이번 작업에서 실제 게임으로 점검을 수행한 것은 아니다.
