---
id: K-CODE-UE-REMOTE-VIEW-MOVEMENT-OFF
title: Why other players see a frozen view pitch and yaw while a player character's movement replication is off in Unreal
summary: The server learns an autonomous character's control rotation only from ServerMove, and the client stops sending moves when IsReplicatingMovement is false; APawn::PreReplication then keeps replicating the frozen server controller pitch as RemoteViewPitch, so spectators and aim offsets see the pre-attach view. Send the actor-relative view from the owner after APlayerController::UpdateRotation (FaceRotation), and have PreReplication prefer it only while movement replication is off.
kind: reference
scope: Unreal Engine 5 networked games using ACharacter and UCharacterMovementComponent where a player character is attached or driven with SetReplicatingMovement(false) while its own controller keeps possessing it
keywords: [RemoteViewPitch, RemoteViewPitch16, SetRemoteViewPitch, APawn::PreReplication, GetBaseAimRotation, SetReplicatingMovement, IsReplicatingMovement, ReplicateMoveToServer, ServerMove_PerformMovement, SetControlRotation, ServerUpdateCamera, COND_SkipOwner, APlayerController::UpdateRotation, APawn::FaceRotation, AddYawInput, RotationInput, aim offset, spectator head look, attached rider, control rotation]
status: active
checked_at: "2026-11-23"
context:
  engine: Unreal Engine 5.8 source
---

## Guidance

- In normal play the owning client sends its control rotation inside each saved move, and the server applies it in `UCharacterMovementComponent::ServerMove_PerformMovement` with `SetControlRotation`. That is the only stock path that updates the server controller's view for an autonomous character.
- `ReplicateMoveToServer` stores and sends moves only when `CharacterOwner->IsReplicatingMovement()` is true. A design that calls `SetReplicatingMovement(false)` on the client while the character rides, climbs or is attached therefore also stops the view from reaching the server. The server controller rotation freezes at its last value from before the attach, or at whatever a late pre-attach move sets.
- `APawn::PreReplication` sets `RemoteViewPitch` (replicated `COND_SkipOwner`) from the server controller's control pitch whenever the pawn has a controller. Other machines read it through `APawn::GetBaseAimRotation` (for a pawn without a local controller). Animation that feeds view minus actor rotation into an aim offset then shows the frozen pitch, for example a lowered head if the player looked down when attaching.
- A client-to-server RPC that writes `RemoteViewPitch` (or a project's own replicated yaw) directly does not survive: the next `PreReplication` overwrites it from the controller. Repair the channel where it breaks: either apply the received view to the source `PreReplication` reads, or make `PreReplication` prefer the received view only while movement replication is off.
- Prefer sending the view relative to the actor (control minus actor rotation) when the attached body keeps rotating on every machine: the relative value stays constant while the body turns, so no RPC is needed for body rotation, and a late pre-attach move cannot corrupt it.
- Send from a point after the control rotation has absorbed this frame's look input. Look input callbacks (`AddYawInput`, `AddPitchInput`) only accumulate `RotationInput`; `APlayerController::UpdateRotation` applies it with `SetControlRotation` and then calls `APawn::FaceRotation`. A callback that reads the control rotation reads the previous frame's value, so a change-only sender misses the final input. Overriding `FaceRotation` and sending there sees the updated value.
- When a gameplay tag or state that enables sending is set before the attach code snaps the body and view, do not send at that moment: the value is still the pre-attach view. Mark the last-sent value invalid instead and let the next post-update send carry the attached view.
- `APlayerController::ServerUpdateCamera` only refreshes the server camera cache; it does not change the control rotation, so it does not feed `PreReplication`.

## Applicability and exceptions

- Applies when the attached character keeps its own controller. If the controller possesses another pawn (a vehicle), the character has no controller on the server and `PreReplication` stops writing; a direct `SetRemoteViewPitch` then persists.
- Listen-server and standalone hosts read their own controller directly; only remote players' copies are affected. Gate the sender on locally controlled and not authority.
- If the project lets the server apply the received view to the controller, every server check that reads the view during the attached state (aim cones, interaction cancel on view change) starts receiving the player's real view. Decide that explicitly.
- Clear any stored received view when movement replication resumes, or the next attach starts from the previous attach's value when the first packet is lost. Clearing at the start of `PreReplication` while `IsReplicatingMovement()` is true also discards late unreliable packets that arrive after the detach.
- Other features that turn off movement replication (ragdoll, cinematic) usually send no view; gate the override on "a view was received" as well as on movement replication being off. Features that only clamp the view but keep movement replication on make the server discard the received value; gate the sender on movement replication if that RPC traffic matters.
- With an unreliable RPC and change-only sending, losing the last packet before the view settles leaves spectators on the previous value until the next view change. Accept that, resend periodically, or make the RPC reliable after weighing reliable-buffer pressure.
- The per-frame sender runs in `FaceRotation`, which also runs on the server for every received move. Put cheap role filters first and avoid copying the owned tag container there.

## Checks

- Before attaching with movement replication off, look down, attach, then compare the owner's view-minus-actor pitch with a spectator's `GetBaseAimRotation` minus actor pitch. A gap means the view channel is frozen.
- Drive look changes through the real input path in the test (for example Enhanced Input injection); writing the control rotation directly skips the sender under test.
- Make the check discriminating: choose nonzero yaw and pitch inputs so that a removed override (spectator shows zero or the frozen value) fails.
- After detaching, compare the spectator's absolute view with the owner's control rotation, not with the server view: the server view is still moving toward the owner's view as moves resume, and under latency the spectator lags that intermediate value.

## Evidence

Read in the UE 5.8 source on 2026-11-23, `Engine/Source/Runtime/Engine/Private`:

- `Pawn.cpp`: `APawn::PreReplication` sets `SetRemoteViewPitch(GetController()->GetControlRotation().Pitch)` under authority with a controller (around line 1356); `RemoteViewPitch16` is replicated with `COND_SkipOwner` (around line 1341); `APawn::GetBaseAimRotation` uses the replicated pitch without a controller (around line 1027).
- `Components/CharacterMovementComponent.cpp`: `ReplicateMoveToServer` pushes and sends the move only inside `if (CharacterOwner->IsReplicatingMovement())` (around line 9029); `ServerMove_PerformMovement` reads `MoveData.ControlRotation` and calls `SetControlRotation` (around lines 9990 and 10036).
- `PlayerController.cpp`: `AddYawInput` only adds to `RotationInput` (around line 6085); `UpdateRotation` (around line 1033) applies the input and calls `FaceRotation` (around line 1063); `ServerUpdateCamera_Implementation` writes the camera cache only (around line 1836).

Runtime, one studio project, 2026-11-23: attached-rider slots turn off movement replication, and the rider's body rotates with the prop. The fix sends control minus actor rotation from `FaceRotation` while the view clamp is active. `PreReplication` prefers that value while `IsReplicatingMovement()` is false and clears it otherwise. Automated network PIE tests passed on a dedicated server with two clients, in both baseline and high-latency profiles. They covered:

- a level view at attach
- a spectator matching a 40 degree yaw and 20 degree pitch relative view after the body turned more than 90 degrees
- the view following the owner again after detach

Removing the override or the clear makes those checks fail by code trace; mutation runs were not executed. The first version of the test compared the spectator with the server view after detach and failed under high latency for the reason given in Checks.
