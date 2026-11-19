# 게임의 히트스캔 조준점과 발사 위치 충돌 확인하기

**K-GAME-TECH-HITSCAN** · 즉시 판정 공격은 조준점을 구한 뒤 실제 시작점에서의 가림을 확인한다. 시작점 중첩과 소유자 제외 규칙을 명시한다.

## 지침

카메라가 옆에 있는 3인칭 게임에서는 카메라 광선으로 조준 의도를 구한 뒤 게임 내 발사점부터 목표점까지의 경로를 판정한다. 카메라에는 표적이 보여도 발사점 앞은 가려질 수 있다. 시작점이 막혔거나 물체 안에 있는 경우의 처리도 정한다. 시각 효과용 궤적은 확정 결과에 맞춰 표시한다.

## 적용 조건과 예외

언리얼의 `UWorld::LineTraceSingleByObjectType`은 지정한 오브젝트 유형에 선분 질의를 한다. `UWorld::OverlapAnyTestByObjectType`은 지정한 자세에서 형상이 선택한 유형과 이미 겹치는지 검사한다. 두 질의의 소유자 제외, 유형 필터, 권위 자세를 일치시킨다. Unity 3D의 `Physics.Raycast`는 시작점을 포함한 콜라이더를 맞히지 않으므로 별도의 중첩 검사가 필요할 수 있다.

## 확인 방법

가림이 없는 자세와 가려진 자세, 형상 안의 시작점, 몸체에서 발사점까지 엄폐물을 가로지르는 경우, 소유자 제외, 목표점 뒤의 장애물을 비교한다. 대상 게임에서 실제 충돌 응답과 권위 애니메이션 시점도 확인한다.

## 근거

Epic과 Unity는 각 엔진의 질의 API를, Riot은 VALORANT의 서버 판정을 설명한다. 기존 Unity와 Unreal의 단순 정적 충돌 검사에서 카메라 광선만 쓸 때의 오탐을 확인했다. 애니메이션 표적, 지연, 서버 상태 조정은 그 검사 범위 밖이다.

- [Unity 6000.0 — Physics.Raycast](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/physics/raycast)
- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode)
- [Epic — UWorld object-type queries](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorld?application_version=5.8)
