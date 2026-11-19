# 점프 유예 시간과 입력 버퍼를 한 번만 소비하기

**K-GAME-TECH-CONTROLLER** · 접지 자격과 대기 입력을 따로 추적해 발판을 벗어나거나 착지할 때 한 번의 입력이 최대 한 번의 점프로 이어지게 한다.

## 지침

코요테 타임은 발판을 걸어 벗어난 직후에도 잠시 점프 자격을 유지한다. 점프 버퍼는 착지 직전의 입력을 보관한다. 같은 시뮬레이션 시계로 두 시각을 기록하고, 새 누름을 구분해 실제 도약에 성공했을 때 소비한다. 접지 자격은 실제 접지 전환 때 복구한다. 착지 전에 버튼을 놓으면 취소할지도 정한다. 코너 보정은 모서리에 걸친 몸체를 옆으로 옮기므로 별도의 충돌 검사가 필요하다.

## 적용 조건과 예외

언리얼 엔진 5.8의 `ACharacter::CanJumpWhileFalling`을 재정의하면 조건에 맞는 낙하 중 점프를 허용할 수 있다. `ACharacter::Landed`에서 접촉을 알릴 때 이동 모드는 여전히 Falling이다. 새 접지 모드가 필요하면 `OnMovementModeChanged`에서 확인한다. 실제 도약 시작은 `ACharacter::OnJumped`로 관찰한다.

## 확인 방법

각 만료 시각 직전·경계·직후의 누름, 계속 누르기와 떼기, 걸어서 이탈한 경우와 점프 이탈, 만료 후 착지를 검사한다. 측정한 갱신률별로 입력당 실제 도약 횟수를 비교한다.

## 근거

Celeste 개발자가 설계 기법을 설명하고 Epic 문서는 캐릭터 콜백의 동작을 명시한다. 기존 언리얼 검사는 정적 발판에서의 유예 시간과 버퍼를 다뤘다. 적절한 시간 길이, 이동 발판, 조작감은 대상 게임에서 검증한다.

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html)
- [Epic — ACharacter](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/ACharacter?application_version=5.8)
- [Epic — OnLanded and movement mode](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/ACharacter/OnLanded)
