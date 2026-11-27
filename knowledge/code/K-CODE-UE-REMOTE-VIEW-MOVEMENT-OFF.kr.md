---
id: K-CODE-UE-REMOTE-VIEW-MOVEMENT-OFF
title: Unreal 에서 플레이어 캐릭터의 이동 복제가 꺼져 있는 동안 다른 플레이어에게 시선 pitch, yaw 가 멈춰 보이는 이유
summary: 서버는 자율 캐릭터의 control rotation 을 ServerMove 로만 알고, 클라이언트는 IsReplicatingMovement 가 거짓이면 이동을 보내지 않는다. 그러면 APawn::PreReplication 이 멈춘 서버 컨트롤러 pitch 를 RemoteViewPitch 로 계속 복제해, 관전자와 aim offset 은 붙기 전 시선을 본다. 소유자가 APlayerController::UpdateRotation(FaceRotation) 뒤에 액터 기준 상대 시선을 보내고, PreReplication 은 이동 복제가 꺼진 동안에만 그 값을 우선하게 한다.
kind: reference
scope: ACharacter 와 UCharacterMovementComponent 를 쓰는 Unreal Engine 5 네트워크 게임에서, 플레이어 캐릭터를 SetReplicatingMovement(false) 로 붙이거나 움직이면서 그 캐릭터의 컨트롤러가 계속 빙의하고 있는 경우
keywords: [ClientAdjustPosition, bClientIgnoreMovementCorrections, bIgnoreClientMovementErrorChecksAndCorrection, ClientAuthorativePosition, ServerMoveHandleClientError, bUseLastGoodRotationDuringCorrection, stale correction, RemoteViewPitch, RemoteViewPitch16, SetRemoteViewPitch, APawn::PreReplication, GetBaseAimRotation, SetReplicatingMovement, IsReplicatingMovement, ReplicateMoveToServer, ServerMove_PerformMovement, SetControlRotation, ServerUpdateCamera, COND_SkipOwner, APlayerController::UpdateRotation, APawn::FaceRotation, AddYawInput, RotationInput, aim offset, spectator head look, attached rider, control rotation]
status: active
checked_at: "2026-11-26"
context:
  engine: Unreal Engine 5.8 source
---

## 지침

- 보통 플레이에서 소유 클라이언트는 저장한 이동마다 control rotation 을 담아 보내고, 서버는 `UCharacterMovementComponent::ServerMove_PerformMovement` 에서 `SetControlRotation` 으로 적용한다. 자율 캐릭터의 서버 컨트롤러 시선을 갱신하는 기본 경로는 이것 하나뿐이다.
- `ReplicateMoveToServer` 는 `CharacterOwner->IsReplicatingMovement()` 가 참일 때만 이동을 저장하고 보낸다. 그래서 캐릭터가 타거나, 오르거나, 붙어 있는 동안 클라이언트에서 `SetReplicatingMovement(false)` 를 부르는 설계는 시선이 서버에 가는 것도 멈춘다. 서버 컨트롤러 회전은 붙기 전 마지막 값이나, 늦게 도착한 붙기 전 이동이 정한 값에서 멈춘다.
- `APawn::PreReplication` 은 폰에 컨트롤러가 있으면 언제나 서버 컨트롤러의 control pitch 로 `RemoteViewPitch`(`COND_SkipOwner` 로 복제)를 정한다. 다른 기기는 `APawn::GetBaseAimRotation` 으로 그 값을 읽는다(로컬 컨트롤러가 없는 폰). 시선에서 액터 회전을 뺀 값을 aim offset 에 넣는 애니메이션은 그 멈춘 pitch 를 보여 준다. 예를 들어 붙을 때 아래를 보고 있었으면 머리가 숙여진 채로 보인다.
- 클라이언트에서 서버로 가는 RPC 로 `RemoteViewPitch`(또는 프로젝트가 따로 복제하는 yaw)를 직접 써도 남지 않는다. 다음 `PreReplication` 이 컨트롤러 값으로 덮는다. 끊긴 곳에서 고친다. 받은 시선을 `PreReplication` 이 읽는 원천에 적용하거나, 이동 복제가 꺼진 동안에만 `PreReplication` 이 받은 시선을 우선하게 한다.
- 붙은 몸이 모든 기기에서 계속 돈다면 액터 기준 상대 시선(control 회전에서 액터 회전을 뺀 값)을 보내는 쪽이 낫다. 몸이 돌아도 상대 값은 그대로라 몸 회전 때문에 RPC 를 보낼 필요가 없고, 늦게 온 붙기 전 이동이 비교 대상인 서버 시선을 바꾸지도 못한다.
- 상대 값은 소유자의 액터 회전만큼만 정확하다. 소유자가 붙기 전에 보낸 이동은 붙은 뒤에도 확인되지 않은 채 남고, 서버는 그 이동에 `ClientAdjustPosition` 으로 답한다. 보정에 회전이 없으면 클라이언트는 확인된 이동이 저장한 회전으로 되돌아가고(`bUseLastGoodRotationDuringCorrection` 이면서 `bOrientRotationToMovement` 나 `bUseControllerDesiredRotation`), 붙은 루트에 `SetWorldLocationAndRotation` 을 부르고 이동 모드를 다시 적용한다. 그러면 붙은 몸은 붙이는 코드가 다시 맞출 때까지 붙기 전 위치와 방향에 있고, 그 사이의 `FaceRotation` 송신은 방향 차이만큼 틀린 상대 시선을 보낸다. 패킷 지연에서 이 일은 간헐적으로 일어난다.
- 붙어 있는 동안 소유 클라이언트가 보정을 적용하지 않게 한다. `bClientIgnoreMovementCorrections` 를 켜면 클라이언트는 보정을 버린다(이동 확인은 한다). 소유 클라이언트만 읽으므로 모든 기기에서 켜도 안전하다. 떼기 전에 끄면 뗀 뒤 첫 이동부터 보통 보정이 돌아온다.
- 프로젝트의 `ClientAuthorativePosition` 설정을 확인하지 않았다면 서버의 `bIgnoreClientMovementErrorChecksAndCorrection` 까지 켜지 않는다. 그 설정이 켜져 있으면 오차 검사를 건너뛴 서버는 `ServerMoveHandleClientError` 의 클라이언트 위치를 믿는 분기로 가서 클라이언트가 보낸 위치와 이동 모드를 적용한다. 늦게 온 붙기 전 이동이면 붙은 서버 몸이 옛 위치에서 걷기 모드가 되고, 서버와 클라이언트의 이동 모드가 어긋난다.
- 컨트롤 회전이 이 프레임의 시선 입력을 반영한 뒤에 보낸다. 시선 입력 콜백(`AddYawInput`, `AddPitchInput`)은 `RotationInput` 에 쌓기만 한다. `APlayerController::UpdateRotation` 이 `SetControlRotation` 으로 적용하고 그다음 `APawn::FaceRotation` 을 부른다. 콜백에서 control rotation 을 읽으면 이전 프레임 값이라, 바뀔 때만 보내는 송신은 마지막 입력을 놓친다. `FaceRotation` 을 재정의해 거기서 보내면 갱신된 값을 본다.
- 송신을 켜는 게임플레이 태그나 상태가 붙이는 코드가 몸과 시선을 맞추기 전에 켜지면 그 순간에는 보내지 않는다. 그 값은 아직 붙기 전 시선이다. 대신 마지막으로 보낸 값을 무효로 표시하고, 다음 갱신 뒤 송신이 붙은 시선을 실어 보내게 한다.
- `APlayerController::ServerUpdateCamera` 는 서버 카메라 캐시만 갱신한다. control rotation 을 바꾸지 않으므로 `PreReplication` 에 들어가지 않는다.

## 적용 범위와 예외

- 붙은 캐릭터가 자기 컨트롤러를 유지할 때 적용된다. 컨트롤러가 다른 폰(탈것)에 빙의하면 서버에서 그 캐릭터에 컨트롤러가 없어 `PreReplication` 이 쓰지 않는다. 그때는 직접 부른 `SetRemoteViewPitch` 가 남는다.
- 리슨 서버와 단독 실행 호스트는 자기 컨트롤러를 바로 읽는다. 원격 플레이어의 사본만 영향을 받는다. 송신은 로컬 제어이면서 권한이 없는 경우로 거른다.
- 받은 시선을 서버가 컨트롤러에 적용하게 하면, 붙어 있는 동안 시선을 읽는 서버 검사(조준 원뿔, 시선이 바뀌면 상호작용 취소)가 모두 플레이어의 실제 시선을 받기 시작한다. 이것은 따로 정한다.
- 이동 복제가 다시 켜지면 저장한 받은 시선을 지운다. 그러지 않으면 첫 패킷을 잃었을 때 다음 붙기가 이전 붙기의 값에서 시작한다. `IsReplicatingMovement()` 가 참인 동안 `PreReplication` 첫머리에서 지우면 뗀 뒤 늦게 온 비신뢰 패킷도 버려진다.
- 이동 복제를 끄는 다른 기능(래그돌, 시네마틱)은 보통 시선을 보내지 않는다. 재정의 조건에 이동 복제가 꺼짐과 함께 "받은 시선이 있음"도 넣는다. 시선만 제한하고 이동 복제는 켜 두는 기능에서는 서버가 받은 값을 버린다. 그 RPC 트래픽이 문제라면 송신을 이동 복제 여부로 거른다.
- 비신뢰 RPC 를 바뀔 때만 보내면, 시선이 멈추기 직전 마지막 패킷을 잃었을 때 관전자는 다음 시선 변화까지 이전 값에 머문다. 이를 받아들이거나, 주기적으로 다시 보내거나, 신뢰 버퍼 부담을 따져 본 뒤 RPC 를 신뢰로 만든다.
- 매 프레임 송신은 `FaceRotation` 에서 돈다. 이 함수는 서버에서도 받은 이동마다 돈다. 싼 역할 필터를 앞에 두고, 거기서 소유 태그 컨테이너를 복사하지 않는다.

## 점검

- 이동 복제를 끈 채 붙기 전에 아래를 보고 붙은 뒤, 소유자의 시선에서 액터 pitch 를 뺀 값과 관전자의 `GetBaseAimRotation` 에서 액터 pitch 를 뺀 값을 비교한다. 차이가 있으면 시선 경로가 멈춘 것이다.
- 테스트에서 시선 변화는 실제 입력 경로(예: Enhanced Input 주입)로 낸다. control rotation 을 직접 쓰면 검사할 송신을 건너뛴다.
- 판별력이 있게 만든다. yaw 와 pitch 입력을 0 이 아닌 값으로 골라, 재정의를 지웠을 때(관전자가 0 이나 멈춘 값을 보임) 실패하게 한다.
- 늦은 보정 경로를 결정적으로 점검하려면 패킷 지연을 켜서 붙은 뒤에도 저장한 이동이 남게 하고, 소유자의 루트가 붙을 때까지 기다린 뒤, 가장 오래된 저장 이동에 그 이동 자신의 끝 상태로 `ClientAdjustPosition_Implementation` 을 부르고, 루트의 상대 변환과 이동 모드가 바뀌지 않았는지 단언한다. 가장 오래된 이동의 끝 위치나 방향이 붙은 값과 다르다는 것을 전제 조건으로 둔다. 그렇지 않으면 점검이 실패할 수 없다. 해제 때 클라이언트 플래그가 다시 꺼졌는지도 단언한다.
- 뗀 뒤에는 관전자의 절대 시선을 서버 시선이 아니라 소유자의 control rotation 과 비교한다. 이동이 다시 오가면서 서버 시선은 아직 소유자 시선을 따라가는 중이고, 지연에서 관전자는 그 중간 값보다도 늦다.

## 근거

2026-11-23 UE 5.8 소스, `Engine/Source/Runtime/Engine/Private` 에서 읽음:

- `Pawn.cpp`: `APawn::PreReplication` 은 권한이 있고 컨트롤러가 있을 때 `SetRemoteViewPitch(GetController()->GetControlRotation().Pitch)` 를 부른다(1356행 부근). `RemoteViewPitch16` 은 `COND_SkipOwner` 로 복제된다(1341행 부근). `APawn::GetBaseAimRotation` 은 컨트롤러가 없으면 복제된 pitch 를 쓴다(1027행 부근).
- `Components/CharacterMovementComponent.cpp`: `ReplicateMoveToServer` 는 `if (CharacterOwner->IsReplicatingMovement())` 안에서만 이동을 넣고 보낸다(9029행 부근). `ServerMove_PerformMovement` 는 `MoveData.ControlRotation` 을 읽고 `SetControlRotation` 을 부른다(9990, 10036행 부근).
- `Components/CharacterMovementComponent.cpp`, 2026-11-26 읽음: 두 보정 플래그의 기본값은 false 다(795, 796행 부근). 서버는 `if (!bIgnoreClientMovementErrorChecksAndCorrection)` 안에서만 오차 검사와 보정을 한다(10539행 부근). `ClientAdjustPosition_Implementation` 은 `bClientIgnoreMovementCorrections` 가 켜져 있으면 이동을 확인한 뒤 바로 돌아간다(11261행 부근). 마지막 정상 회전으로 되돌리는 처리는 콘솔 변수 `bUseLastGoodRotationDuringCorrection`(기본 1)로 걸러진다(330, 11331행 부근). 오차 검사를 건너뛰고 `ServerShouldUseAuthoritativePosition` 이 참이면(10615~10628행 부근, game network manager 의 `ClientAuthorativePosition` 을 읽음) 서버는 클라이언트 위치로 `SetWorldLocation` 을, 클라이언트 이동 모드로 `ApplyNetworkMovementMode` 를 부른다(10485~10494행 부근).
- `PlayerController.cpp`: `AddYawInput` 은 `RotationInput` 에 더하기만 한다(6085행 부근). `UpdateRotation`(1033행 부근)은 입력을 적용하고 `FaceRotation` 을 부른다(1063행 부근). `ServerUpdateCamera_Implementation` 은 카메라 캐시만 쓴다(1836행 부근).

실행, 한 스튜디오 프로젝트, 2026-11-23: 붙이는 탑승 슬롯이 이동 복제를 끄고, 탑승자의 몸은 소품을 따라 돈다. 수정은 시선 제한이 켜진 동안 `FaceRotation` 에서 control 회전에서 액터 회전을 뺀 값을 보낸다. `PreReplication` 은 `IsReplicatingMovement()` 가 거짓인 동안 그 값을 우선하고, 아니면 지운다. 자동 네트워크 PIE 테스트가 전용 서버와 클라이언트 둘에서, 기본과 고지연 프로필 모두 통과했다. 다룬 경우:

- 붙을 때 수평 시선
- 몸이 90도 넘게 돈 뒤 관전자가 yaw 40도, pitch 20도의 상대 시선과 맞음
- 뗀 뒤 시선이 다시 소유자를 따라감

재정의나 지우기를 없애면 코드 추적상 이 점검들이 실패한다. 변형 실행은 하지 않았다. 처음 테스트는 뗀 뒤 관전자를 서버 시선과 비교했고, 점검 절에 적은 이유로 고지연에서 실패했다.

실행, 같은 프로젝트, 2026-11-26: 붙은 뒤 상대 시선 점검이 고지연에서 간헐적으로 실패했다. 결정적인 늦은 보정 테스트(점검 절)는 클라이언트 플래그 없이 3회 중 3회 실패했다. 두 보정 플래그를 모두 켜자 프로젝트가 `ClientAuthorativePosition` 을 켜 두었기 때문에 탑승 스위트 57건 중 34건이 "movement mode server=1 client=0" 으로 실패했다. 클라이언트 플래그만 켜자 관련 없는 맵 콘텐츠 점검 하나를 빼고 스위트가 통과했고, 대상 테스트 둘은 10회 반복에서 10회 모두 통과했다.
