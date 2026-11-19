# 입력·출력 무작위성과 천장·셔플백

기준 항목: K-GAME-TECH-RANDOM-DESIGN · 확인일: 2026-11-07 · 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

불확실성이 언제 공개되고 결과를 얼마나 바꾸는지 구분한다. 셔플백은 보충 전까지 비복원 추출하며 천장은 실패 후 조건부 확률을 바꾸거나 결과를 보장한다. 첫 성공 확률은 p_n*이전 실패확률의 곱이며 여기서 평균 대기와 긴 실패 꼬리를 계산한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

입력 랜덤이 항상 좋거나 출력 랜덤이 항상 나쁜 것은 아니며 출처 설계자들의 견해도 다르다. 확률을 바꾸면 독립·고정 확률 시행과 다른 과정이 된다.

## 적용 전 점검

적용 전 점검: 평균·백분위·최대 불운 길이·주머니 경계 반복을 비교하고 선택 이해도를 플레이테스트한다.

## 근거

- [Ian Schreiber — Probability and Randomness](https://gamebalanceconcepts.wordpress.com/2010/07/28/level-4-probability-and-randomness/) — 출처의 확인 범위는 아래 원칙을 따른다.
- [Keith Burgun — Randomness and Game Design](https://www.gamedeveloper.com/design/randomness-and-game-design) — 출처의 확인 범위는 아래 원칙을 따른다.
- [A Defense of Randomness in Competitive Games](https://www.gamedeveloper.com/design/a-defense-of-randomness-in-competitive-games) — 출처의 확인 범위는 아래 원칙을 따른다.
- 공식 문서·논문·저자 글은 확인한 본문 범위에 한정한다. 초록·영상 설명만 확인한 경우와 미열람 자료는 영문 정본 Evidence에 명시했다. 예제 코드·영상·제품 성능은 실행 검증하지 않았다.
- 출발 영상: V09, V44. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


### input randomness

**입력 무작위성(input randomness)**은 플레이어가 선택하기 전에 불확실한 정보를 공개한다. **출력 무작위성(output randomness)**은 행동을 확정한 후 결과를 정한다. 같은 추첨도 의사결정 시점에 따라 대응 기회가 되거나 이미 감수한 위험의 결과가 된다. 천장형 확률은 이전까지 모두 실패했다는 조건에서 성공률을 계산하고 독립 추첨과 대기 분포를 비교한다. 평균이 같아도 장기간 실패하는 비율은 다를 수 있다. [Keith Burgun — Randomness and Game Design](https://www.gamedeveloper.com/design/randomness-and-game-design)
