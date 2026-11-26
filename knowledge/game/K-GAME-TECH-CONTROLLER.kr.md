---
id: K-GAME-TECH-CONTROLLER
title: 시간 창으로 구현하는 플랫폼 게임 점프 입력 보조
translation_of: K-GAME-TECH-CONTROLLER.md
---
# 시간 창으로 구현하는 플랫폼 게임 점프 입력 보조

## 지침

코요테 타임은 발판을 벗어난 직후 짧게 점프를 허용한다. 점프 버퍼는 착지보다 조금 이른 입력을 보관한다. 두 시간 창은 같은 시뮬레이션 시계로 기록한다. 새 입력마다 ID를 할당하고 실제 점프가 시작되면 그 입력을 소비한다. 발판 위에서 다시 점프할 자격은 실제 착지로 돌아왔을 때 갱신한다. 착지 전에 버튼을 놓았을 때 예약을 취소할지도 정한다. 점프 모서리 보정은 현재 점프의 충돌 해결에 포함하며 새 점프 입력을 발행하지 않는다.

## 적용 조건

언리얼 5.8 캐릭터의 CanJumpWhileFalling으로 공중에서 허용할 점프를 판정한다. Landed는 이동 모드가 아직 Falling일 때 접촉을 알린다. 지면 모드 전환이 필요하면 OnMovementModeChanged를 사용한다. OnJumped는 실제 점프가 시작됐는지 기록하는 데 쓴다.

## 적용 전 확인

시간 창 만료 직전·정각·직후, 버튼 홀드·해제, 발판에서 걸어 나감·점프해 나감, 만료 후 착지를 확인한다. 실제로 관측한 업데이트 속도별로 입력마다 몇 번 점프가 시작됐는지 센다.

모서리는 좌우를 반전하고 필요한 옆 이동 거리를 허용 상한 안팎으로 바꿔 본다. 넓고 낮은 천장, 옆 경로를 막는 벽, 빠른 상승, 움직이는 발판을 포함한다. 두 이동 구간을 스윕한 뒤 최고점·겹침·착지를 확인한다. 같은 입력으로 끔/켬을 비교하고, 영상 캡처용 고정 시간 간격과 실측 프레임 간격을 구분한다.

## 근거

첫 언리얼 검증은 고정 발판에서 코요테 타임과 점프 버퍼를 다뤘다. 시간 창의 길이와 조작감은 적용할 게임에서 확인한다.

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html)
- [Epic ACharacter](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/ACharacter?application_version=5.8)
- [Epic OnLanded와 이동 모드](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/ACharacter/OnLanded)

## 언리얼 평면 캐릭터의 V30 모서리 보정

공중 이동 물리에서 상승 중 위쪽 장애물에 막힌 경우만 보정을 시도한다. 이동 평면에서 가까운 오프셋부터 찾는다. 접촉 위치에서 옆 경로를 스윕하고, 캡슐의 둥근 끝이 제약을 넘을 수 있도록 남은 상승 방향으로 더 멀리 스윕한다. 후보가 비어 있으면 옆 이동과 남은 상승 이동을 실제 스윕으로 적용한다. 둘 중 하나라도 막히면 두 이동을 되돌리고 원래 충돌 응답을 사용한다. 상승 한 번에 성공할 수 있는 보정은 한 번이며 새 점프 자격은 사용하지 않는다. [Epic MoveUpdatedComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UMovementComponent/MoveUpdatedComponent)

시험에서는 반경 22cm의 XZ 평면 캡슐에 1cm 간격으로 최대 10cm를 탐색했다. 옆 이동은 착지 위치도 바꿀 수 있다. 적용할 캐릭터와 플랫폼 간격을 기준으로 상한과 양쪽이 모두 열려 있을 때의 우선 방향을 정한다. 경사면, 복잡한 충돌 형상, 커스텀 중력, 루트 모션, 네트워크 예측과 움직이는 장애물은 별도의 적용 검증이 필요하다. 움직이는 발판 사례에서는 이륙 지지대가 수직 이동했고 천장은 고정했다.

## 실제 프레임 측정 — 2026-11-21

같은 UE 5.8.3 Win64 Development 패키지의 1280×720 DX11 장면에서 30·60·144FPS마다 같은 입력으로 끔/켬을 각각 3회 비교했다. i7-12700KF와 RTX 3080에서 18회, 270개 사례가 모두 통과했다. 보정을 켜면 좌우 모서리, 9·10cm 후보, 빠른 상승과 이동 발판 이륙이 통과했다. 11cm가 필요한 경우와 낮은 천장·옆 벽에서는 기존 충돌 응답을 유지했다. 프레임 표본에서 관통과 중복 점프가 없었고 코요테 타임과 점프 버퍼의 허용·만료 동작이 유지됐다.

| 실측 FPS | 끔 전체 프레임 p95 (ms) | 켬 전체 프레임 p95 (ms) |
| --- | ---: | ---: |
| 30 | 33.417–33.418 | 33.393–33.471 |
| 60 | 16.732–16.780 | 16.734–16.803 |
| 144 | 7.029–7.044 | 7.041–7.044 |

준비 시간 이후 보정을 시도한 78프레임의 보정 경로는 p95 0.030ms, 최대 0.0925ms였다. 전체 프레임에는 FPS 제한에 따른 대기가 포함된다. 실제 게임에 적용할 때는 같은 프레임에 여러 개체가 부딪히는 장면과 접촉 프레임 비용을 따로 확인한다. 영상은 별도 실행에서 30Hz로 캡처해 30FPS로 재생했다.
