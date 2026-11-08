# 코요테 타임·버퍼·코너 보정

기준 항목: K-GAME-TECH-CONTROLLER · 확인일: 2026-11-07 · 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

점프 요청 시각과 마지막 접지 시각을 기록한다. 입력 버퍼와 접지 유예 조건이 겹치면 점프하고 요청을 한 번만 소비한다. 충돌 검사 뒤 제한된 코너 보정을 적용하고 이동 발판 운동량의 소유권을 정한다. 가속·버튼 해제 감속·공중 제어는 목표 도달 범위에 맞춰 조절한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

셀레스트 수치와 정수 AABB는 특정 게임의 해법이다. 무한 버퍼 점프·벽 통과 보정·운동량 중복 적용을 막는다.

## 적용 전 점검

적용 전 점검: 절벽·착지 직전과 직후 입력, 모서리 접근, 방향 전환, 발판 정지를 여러 프레임레이트에서 확인한다.

## 근거

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html) — 출처의 확인 범위는 아래 원칙을 따른다.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — 출처의 확인 범위는 아래 원칙을 따른다.
- 공식 문서·논문·저자 글은 확인한 본문 범위에 한정한다. 초록·영상 설명만 확인한 경우와 미열람 자료는 영문 정본 Evidence에 명시했다. 예제 코드·영상·제품 성능은 실행 검증하지 않았다.
- 출발 영상: V29, V30, V46. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).

