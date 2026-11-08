# 내적·시야각·레이캐스팅

기준 항목: K-GAME-TECH-TRACE · 확인일: 2026-11-07 · 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

단위 전방 f와 방향 d의 시야 원뿔 판정은 dot(f,d)>=cos(반시야각)이다. 거리→각도→차폐 추적 순으로 거른다. 길이 0인 방향을 처리하고 지면 투영 여부를 정한다. 트레이스 채널·무시 대상·단순/복합 충돌·여러 표적점이 실제 가시성 정의를 결정한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

내적의 [-1,1] 범위는 정규화 벡터를 전제한다. 각도 안에 있어도 보인다는 뜻은 아니다. 람베르트 확산반사의 max(0,n dot l)는 같은 연산의 별도 셰이딩 용도다.

## 적용 전 점검

적용 전 점검: 얇은 엄폐물 뒤·시야각 경계·동일 위치 대상을 확인하고 선과 노멀을 시각화한다.

## 근거

- [Epic — EQS Node Reference: Tests](https://dev.epicgames.com/documentation/unreal-engine/eqs-node-reference-tests-in-unreal-engine?lang=en-US) — 출처의 확인 범위는 아래 원칙을 따른다.
- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US) — 출처의 확인 범위는 아래 원칙을 따른다.
- 공식 문서·논문·저자 글은 확인한 본문 범위에 한정한다. 초록·영상 설명만 확인한 경우와 미열람 자료는 영문 정본 Evidence에 명시했다. 예제 코드·영상·제품 성능은 실행 검증하지 않았다.
- 출발 영상: V18, V38. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).

