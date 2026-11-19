# Elo·TrueSkill·매치메이킹

기준 항목: K-GAME-TECH-MATCH · 확인일: 2026-11-07 · 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

실력 추정과 실제 매치 선택을 분리한다. TrueSkill은 평균과 불확실성으로 실력을 표현해 결과로 갱신하고, Elo는 예상 결과를 이용해 점수를 갱신한다. 매치 탐색은 핑·파티·대기 시간·허용 실력 차이 정책을 추가한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

모든 게임이 파티 최고 실력자만으로 매칭한다고 일반화하지 않는다. 레이팅은 추정치이며 매 경기 승률 50%를 보장하지 않는다.

## 적용 전 점검

적용 전 점검: 신규 유저 수렴·혼합 실력 파티·적은 인구·지연을 평가하고 예상 승률과 실제 결과를 대조한다.

## 근거

- [Microsoft Research — TrueSkill Ranking System](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) — 출처의 확인 범위는 아래 원칙을 따른다.
- 공식 문서·논문·저자 글은 확인한 본문 범위에 한정한다. 초록·영상 설명만 확인한 경우와 미열람 자료는 영문 정본 Evidence에 명시했다. 예제 코드·영상·제품 성능은 실행 검증하지 않았다.
- 출발 영상: V33. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


### Bayesian skill rating

**TrueSkill**은 베이지안 실력 추정치로 플레이어의 평균 실력과 불확실성을 함께 나타낸다. 정보량이 있는 한 경기 결과로 신규 플레이어의 추정치가 기록이 충분한 플레이어보다 크게 변할 수 있다. 매치메이킹 평점(MMR)은 결과 예측 보정과 대기 시간·지역 조건을 분리해 평가한다. Microsoft는 팀 결과에서 개인 추정치를 갱신하는 모델을 설명한다. [Microsoft Research — TrueSkill Ranking System](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/)
