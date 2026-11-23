# 플레이어 캐릭터의 이동 복제가 꺼진 동안 다른 플레이어가 굳은 시선 pitch, yaw를 보는 이유 (Unreal)

> 영어 원문 [K-CODE-UE-REMOTE-VIEW-MOVEMENT-OFF.md](K-CODE-UE-REMOTE-VIEW-MOVEMENT-OFF.md)의 번역이다. 헤더 정보: 종류 reference, 상태 active, 확인일 2026-11-23, 엔진 Unreal Engine 5.8 소스.

**요약:** 서버는 자율 캐릭터의 컨트롤 회전을 ServerMove로만 알고, 클라이언트는 `IsReplicatingMovement`가 거짓이면 이동을 보내지 않는다. 그러면 `APawn::PreReplication`이 굳은 서버 컨트롤러 pitch를 `RemoteViewPitch`로 계속 복제해 관전자와 에임 오프셋이 부착 전 시선을 본다. 본인 기기에서 `APlayerController::UpdateRotation` 뒤(`FaceRotation`)에 몸 기준 시선을 보내고, `PreReplication`은 이동 복제가 꺼진 동안에만 그 값을 쓴다.

**범위:** `ACharacter`와 `UCharacterMovementComponent`를 쓰는 Unreal Engine 5 네트워크 게임에서, 자기 컨트롤러가 계속 빙의한 채 `SetReplicatingMovement(false)`로 부착되거나 움직이는 플레이어 캐릭터.

## 지침

- 평소에는 본인 클라이언트가 저장된 이동마다 컨트롤 회전을 싣고, 서버가 `UCharacterMovementComponent::ServerMove_PerformMovement`에서 `SetControlRotation`으로 적용한다. 자율 캐릭터의 서버 컨트롤러 시선을 갱신하는 기본 경로는 이것 하나다.
- `ReplicateMoveToServer`는 `CharacterOwner->IsReplicatingMovement()`가 참일 때만 이동을 저장하고 보낸다. 그래서 탑승, 등반, 부착 중에 클라이언트에서 `SetReplicatingMovement(false)`를 부르는 설계는 시선이 서버로 가는 것도 멈춘다. 서버 컨트롤러 회전은 부착 전 마지막 값이나 늦게 도착한 부착 전 이동이 정한 값에서 굳는다.
- `APawn::PreReplication`은 폰에 컨트롤러가 있으면 서버 컨트롤러의 컨트롤 pitch로 `RemoteViewPitch`(`COND_SkipOwner` 복제)를 채운다. 다른 기계는 `APawn::GetBaseAimRotation`(로컬 컨트롤러가 없는 폰)으로 읽는다. 시선에서 몸 회전을 뺀 값을 에임 오프셋에 넣는 애니메이션은 굳은 pitch를 보여 준다. 예를 들어 부착할 때 아래를 봤으면 고개가 숙여진다.
- `RemoteViewPitch`(또는 프로젝트의 복제 yaw)를 직접 쓰는 클라이언트에서 서버로 가는 RPC는 남지 않는다. 다음 `PreReplication`이 컨트롤러 값으로 덮는다. 채널이 끊긴 곳을 고친다. 받은 시선을 `PreReplication`이 읽는 출처에 반영하거나, 이동 복제가 꺼진 동안에만 `PreReplication`이 받은 시선을 우선하게 한다.
- 부착된 몸이 모든 기계에서 계속 돌면 몸 기준 시선(컨트롤 회전 - 몸 회전)을 보낸다. 몸이 돌아도 값이 그대로라 몸 회전에는 RPC가 필요 없고, 늦게 온 부착 전 이동이 값을 망가뜨릴 수 없다.
- 이번 프레임의 시선 입력이 컨트롤 회전에 반영된 뒤에 보낸다. 시선 입력 콜백(`AddYawInput`, `AddPitchInput`)은 `RotationInput`에 더하기만 한다. `APlayerController::UpdateRotation`이 `SetControlRotation`으로 적용한 뒤 `APawn::FaceRotation`을 부른다. 콜백에서 컨트롤 회전을 읽으면 이전 프레임 값이라, 바뀔 때만 보내는 송신은 마지막 입력을 놓친다. `FaceRotation`을 재정의해 거기서 보내면 갱신된 값을 본다.
- 송신을 켜는 게임플레이 태그나 상태가 부착 코드가 몸과 시선을 맞추기 전에 켜지면 그 순간에 보내지 않는다. 그 값은 아직 부착 전 시선이다. 대신 마지막으로 보낸 값을 무효로 표시해 다음 갱신 뒤 송신이 부착된 시선을 싣게 한다.
- `APlayerController::ServerUpdateCamera`는 서버 카메라 캐시만 갱신하고 컨트롤 회전을 바꾸지 않아 `PreReplication`에 닿지 않는다.

## 적용 범위와 예외

- 부착된 캐릭터가 자기 컨트롤러를 유지할 때 해당한다. 컨트롤러가 다른 폰(탈것)을 빙의하면 서버에서 캐릭터에 컨트롤러가 없어 `PreReplication`이 쓰지 않고, 직접 쓴 `SetRemoteViewPitch`가 남는다.
- 리슨 서버와 단독 실행 호스트는 자기 컨트롤러를 바로 읽는다. 원격 플레이어의 사본만 영향을 받는다. 송신은 로컬 조종이면서 권한이 아닌 경우로 거른다.
- 서버가 받은 시선을 컨트롤러에 반영하게 하면, 부착 중 시선을 읽는 모든 서버 판정(조준 원뿔, 시선 변화로 인한 상호작용 취소)이 플레이어의 실제 시선을 받기 시작한다. 명시적으로 결정한다.
- 이동 복제가 다시 켜지면 저장한 받은 시선을 지운다. 그러지 않으면 첫 패킷을 잃었을 때 다음 부착이 지난 부착의 값에서 시작한다. `IsReplicatingMovement()`가 참일 때 `PreReplication` 시작에서 지우면 내린 뒤 늦게 도착한 Unreliable 패킷도 버려진다.
- 이동 복제를 끄는 다른 기능(래그돌, 시네마틱)은 보통 시선을 보내지 않는다. 덮어쓰기는 이동 복제가 꺼진 것과 함께 "받은 시선이 있음"으로도 거른다. 시선만 클램프하고 이동 복제는 켜 두는 기능은 서버가 받은 값을 버린다. 그 RPC 양이 중요하면 송신을 이동 복제 상태로 거른다.
- Unreliable RPC와 바뀔 때만 보내기를 쓰면, 시선이 멈추기 전 마지막 패킷을 잃었을 때 관전자는 다음 시선 변화까지 이전 값에 머문다. 이를 받아들이거나, 주기적으로 다시 보내거나, reliable 버퍼 부담을 따진 뒤 RPC를 reliable로 한다.
- 매 프레임 송신이 도는 `FaceRotation`은 서버에서도 받은 이동마다 돈다. 싼 역할 필터를 먼저 두고, 거기서 보유 태그 컨테이너를 복사하지 않는다.

## 점검

- 이동 복제가 꺼지는 부착 전에 아래를 보고 부착한 뒤, 본인의 시선 - 몸 pitch와 관전자의 `GetBaseAimRotation` - 몸 pitch를 비교한다. 차이가 있으면 시선 채널이 굳은 것이다.
- 테스트는 실제 입력 경로(예: Enhanced Input 주입)로 시선을 바꾼다. 컨트롤 회전을 직접 쓰면 검사 대상인 송신을 건너뛴다.
- 판별력이 있게 한다. 0이 아닌 yaw, pitch 입력을 골라 덮어쓰기를 지우면(관전자가 0이나 굳은 값을 보임) 실패하게 한다.
- 내린 뒤에는 관전자의 절대 시선을 서버 시선이 아니라 본인 컨트롤 회전과 비교한다. 서버 시선은 이동이 다시 오면서 본인 시선 쪽으로 옮겨 가는 중이고, 지연이 있으면 관전자는 그 중간값보다 늦는다.

## 근거

2026-11-23에 UE 5.8 소스 `Engine/Source/Runtime/Engine/Private`에서 읽었다.

- `Pawn.cpp`: `APawn::PreReplication`이 권한과 컨트롤러가 있으면 `SetRemoteViewPitch(GetController()->GetControlRotation().Pitch)`를 부른다(1356행 부근). `RemoteViewPitch16`은 `COND_SkipOwner`로 복제된다(1341행 부근). `APawn::GetBaseAimRotation`은 컨트롤러가 없으면 복제된 pitch를 쓴다(1027행 부근).
- `Components/CharacterMovementComponent.cpp`: `ReplicateMoveToServer`는 `if (CharacterOwner->IsReplicatingMovement())` 안에서만 이동을 넣고 보낸다(9029행 부근). `ServerMove_PerformMovement`는 `MoveData.ControlRotation`을 읽어 `SetControlRotation`을 부른다(9990행, 10036행 부근).
- `PlayerController.cpp`: `AddYawInput`은 `RotationInput`에 더하기만 한다(6085행 부근). `UpdateRotation`(1033행 부근)이 입력을 적용하고 `FaceRotation`을 부른다(1063행 부근). `ServerUpdateCamera_Implementation`은 카메라 캐시만 쓴다(1836행 부근).

런타임, 한 스튜디오 프로젝트, 2026-11-23: 탑승 슬롯이 이동 복제를 끄고, 탑승자의 몸이 프랍과 함께 돈다. 수정은 시선 클램프가 켜진 동안 `FaceRotation`에서 컨트롤 회전 - 몸 회전을 보낸다. `PreReplication`은 `IsReplicatingMovement()`가 거짓일 때 그 값을 우선하고, 아니면 지운다. 데디케이티드 서버와 클라이언트 2명의 자동화 네트워크 PIE 테스트가 기본 프로필과 높은 지연 프로필 모두에서 통과했다. 테스트는 다음을 덮었다.

- 부착할 때 수평 시선
- 몸이 90도 넘게 돈 뒤 관전자가 몸 기준 yaw 40도, pitch 20도 시선과 일치하는지
- 내린 뒤 시선이 다시 본인을 따르는지

덮어쓰기나 지우기를 없애면 그 점검이 실패한다는 것은 코드 추적으로 확인했고, 변이 실행은 하지 않았다. 테스트의 첫 판은 내린 뒤 관전자를 서버 시선과 비교했다가, 점검 절에 적은 이유로 높은 지연에서 실패했다.
