# 거리·시야각·충돌 질의로 가시성 판정하기

**K-GAME-TECH-TRACE** · 거리와 시야각으로 후보를 먼저 거르고 가림을 검사한다. 대상의 어느 점, 어떤 충돌 채널과 히트 결과를 가시성으로 인정할지 정한다.

## 지침

단위 전방 벡터 f와 표적을 향한 단위 벡터 d에서 `dot(f,d) >= cos(halfFOV)`이면 경계를 포함한 원뿔 안이다. 거리 제곱을 먼저 비교하고 같은 위치인 경우를 정규화 전에 처리한다. 수평 시야는 두 벡터를 지면에 투영하고 3D 시야는 고도 차이도 제한한다. 확산 조명의 Lambert 코사인 항은 표면 법선과 광원 방향으로 입사광을 계산한다.

## 적용 조건과 예외

언리얼 충돌 기반 인식에서 `UWorld::LineTraceSingleByChannel`은 해당 채널의 첫 차단 히트를 반환한다. `FCollisionQueryParams::AddIgnoredActor`로 관찰자를 제외한다. 대상을 맞혀야 보이는 규칙이면 대상 컴포넌트가 그 채널을 차단해야 한다. 목표점까지 가림만 보는 규칙은 끝점에 콜라이더가 없어도 막히지 않은 선분을 허용한다.

## 확인 방법

원뿔 경계, 바로 위, 얇은 벽 뒤, 일부만 노출된 위치를 검사한다. 관찰자 자신의 콜라이더, 히트 없음, 대상 교체, 복수 샘플점을 확인한다. 알려진 방향으로 각도 경계값을 검산한다.

## 근거

Epic의 EQS 문서는 Distance, Dot, Trace 검사를 설명한다. 기존 언리얼 검사는 알려진 한 점과 단순 충돌의 첫 히트 가시성에 한정된다. 복수 샘플을 쓰는 대상, 애니메이션 메시, 게임 인식 행동은 별도 문제다.

- [Epic — EQS Node Reference: Tests](https://dev.epicgames.com/documentation/unreal-engine/eqs-node-reference-tests-in-unreal-engine?lang=en-US)
- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US)
- [Epic — UWorld](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorld?application_version=5.8)
- [Epic — AddIgnoredActor](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/FCollisionQueryParams/AddIgnoredActor?lang=en-US)
