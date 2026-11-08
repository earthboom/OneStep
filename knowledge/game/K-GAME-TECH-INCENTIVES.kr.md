# 반복 보상·공격 유도·리스크와 리워드

기준 항목: K-GAME-TECH-INCENTIVES · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

설계 종합안: 반복 선택의 시간·자원 비용·실패 결과·대안을 정한다. 효율 업그레이드·자동화는 숫자 증가뿐 아니라 작업 방식도 바꿀 수 있다. 공격 회복·시간 압박은 교전을 유도할 수 있지만 안전한 전략과 실력대별로 비교한다. 기존 경제·전투 항목을 먼저 참조한다.

### 추가 조사로 보완한 구현

블러드본 프로듀서 Masaaki Yamagiwa는 피격 후 짧은 시간에 반격해 잃은 체력 일부를 되찾고 회복 가능량을 게이지에 표시한다고 설명한다. 적용 구현안은 회복 가능 피해 풀·만료 시각을 추적하고 적격 타격으로 상한 내 회복하는 방식이며 갱신·중첩은 명시적으로 설계해야 한다. 이는 처치 회복과 다르다. DOOM GDC 발표는 전진 전투의 원출처지만 설명만으로 자원 드롭 수식을 확정하지 않는다.

## 적용 조건과 한계

블러드본의 짧은 회복 창은 프로듀서 설명으로 확인했다. 정확한 피해 비율·시간·DOOM 드롭 알고리즘은 별도 문제다. 보상이 재미의 증거나 신중한 플레이를 금지할 근거는 아니다.

## 적용 전 점검

적용 전 점검: 소극적·공격적·최적화 전략을 비교하고 성장 시간·회복 기회·선택권 체감을 확인한다.

## 근거

- [Ian Schreiber — Probability and Randomness](https://gamebalanceconcepts.wordpress.com/2010/07/28/level-4-probability-and-randomness/)

### 추가 조사 출처

- [Masaaki Yamagiwa — Bloodborne combat details](https://blog.playstation.com/2014/08/13/bloodborne-on-ps4-new-combat-details/) — Producer-authored Regain System discussion; historical 2014 design account, not exact frame/percentage data.
- [id Software/GDC — Embracing Push Forward Combat](https://www.youtube.com/watch?v=2KQNpQD8Ayo) — 2018 official talk description only; detailed formulas not verified.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V05, V17, V34. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).
