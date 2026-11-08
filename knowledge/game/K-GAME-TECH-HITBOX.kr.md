# 공격·피격 판정과 히트스톱

기준 항목: K-GAME-TECH-HITBOX · 확인일: 2026-11-07 · 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

공격 영역·피격 영역·이동 충돌을 분리한다. 시뮬레이션 상태·프레임에 따라 공격을 활성화하고 공격 ID로 의도치 않은 중복 피해를 막는다. 무적·유예는 설계가 요구하는 곳에 적용한다. 히트스톱 동안 멈추는 시계와 유지되는 입력 버퍼를 정한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

충돌·관대한 판정 원리에서 도출한 실무 설계안이며 모든 게임의 공통 구현은 아니다. 작은 피격 영역은 선택 사항이고 빠른 이동에는 스윕 검사가 필요할 수 있다.

## 적용 전 점검

적용 전 점검: 프레임별 영역·동시 타격·얇은 표적 고속 통과를 확인하고 히트스톱을 꺼 비교한다.

## 근거

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html) — 출처의 확인 범위는 아래 원칙을 따른다.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — 출처의 확인 범위는 아래 원칙을 따른다.
- 공식 문서·논문·저자 글은 확인한 본문 범위에 한정한다. 초록·영상 설명만 확인한 경우와 미열람 자료는 영문 정본 Evidence에 명시했다. 예제 코드·영상·제품 성능은 실행 검증하지 않았다.
- 출발 영상: V42. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).

