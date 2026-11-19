# 공격 판정·피격 판정·이동 충돌 분리하기

**K-GAME-TECH-HITBOX** · 공격 활성 시간에 맞춰 충돌 질의를 자르고 차단 히트가 없어도 유효한 접촉을 공격·대상별로 한 번만 처리한다.

## 지침

히트박스는 공격 활성 영역, 허트박스는 피해를 받는 영역, 이동 충돌은 몸체가 이동할 수 있는 공간을 나타낸다. 공격 활성화마다 식별자와 이미 영향을 받은 대상 집합을 둔다. 선형 고속 이동에서는 직전·현재 사이에서 공격이 활성화된 시간 구간만 스윕한다. 규칙이 허용하면 시작 시 중첩도 검사한다.

## 적용 조건과 예외

언리얼의 `UWorld::SweepMultiByChannel`은 선택한 채널에서 가장 가까운 차단물까지의 접촉을 모은다. 반환 불리언은 차단 히트 여부다. 접촉만 있어도 게임에 유효할 수 있으므로 false일 때도 `FHitResult` 배열을 확인한다. 구체의 직선 스윕은 선형 궤적을 가정한다. 회전하는 사지와 움직이는 대상에는 추가 샘플이 필요할 수 있다.

## 확인 방법

프레임 사이에 완전히 통과하는 경우, 활성 시작·종료 경계, 피격부 앞의 벽, 소유자 접촉, 한 공격의 반복 적중을 검사한다. 접촉만 있는 경우도 독립적으로 확인한다. 히트스톱은 어떤 시계가 멈추고 입력 버퍼가 계속되는지 별도로 정한다.

## 근거

Epic은 질의 계약과 충돌 응답을, Thorson은 해당 게임의 충돌과 보정 설계를 설명한다. 기존 언리얼 관찰은 직선 구체 궤적과 고정 수직 표적에 한정된다. 애니메이션 접촉, 히트스톱, 네트워크, 전투 체감은 별도 평가 대상이다.

- [Epic SweepMultiByChannel](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/Engine/UWorld/SweepMultiByChannel?application_version=5.5)
- [collision response reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/collision-response-reference-in-unreal-engine)
- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html)
