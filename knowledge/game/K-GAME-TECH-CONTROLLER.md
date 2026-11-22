---
id: K-GAME-TECH-CONTROLLER
title: Implement forgiving platformer input as explicit state windows
summary: Track ground eligibility and a pending jump press separately so one press can survive a ledge
  or landing transition and cause at most one jump.
kind: reference
scope: Game development. For Unreal Engine 5.8 characters, `ACharacter::CanJumpWhileFalling` permits
  a subclass to authorize a falling jump under its rules.
keywords:
- coyote
- jump
- buffering
- corner
- correction
- acceleration
- 조작감
- 코요테타임
- 점프버퍼링
- 착지
- 입력씹힘
- 코너보정
- ground credit
- released tap
- landing latch
- CanJumpWhileFalling
- 중복 점프
- 착지 입력
- ACharacter::CanJumpWhileFalling
- ACharacter::Landed
- OnMovementModeChanged
- ACharacter::OnJumped
status: active
checked_at: '2026-11-19'
---
# Implement forgiving platformer input as explicit state windows

## Guidance

Coyote time briefly retains jump eligibility after walking off a ledge. Jump buffering retains an early press until a landing permits it. Timestamp both on the same simulation clock. Give a new press an identity, consume it on successful launch and rearm ground eligibility only on a genuine grounded transition. Decide explicitly whether releasing before landing cancels a request. Corner correction shifts a near-miss clear of geometry. Resolve it inside the current jump movement without issuing another jump request.

## Applicability and exceptions

For Unreal Engine 5.8 characters, `ACharacter::CanJumpWhileFalling` permits a subclass to authorize a falling jump under its rules. `ACharacter::Landed` signals contact while movement mode is still Falling. Use `OnMovementModeChanged` when the decision requires the new grounded mode. `ACharacter::OnJumped` reports a jump that actually started.

## Checks

Test the instant before, at and after each expiry, holding and releasing a press, walking off versus jumping off, and landing after an expired press. Count actual launches per request across different measured update rates.

For corner correction, mirror the lip and vary the required lateral shift through the configured limit. Include a wide ceiling, an occupied side path, high upward speed and a moving base. Verify both swept segments, then check the resulting apex, penetration and landing. Run the same input with correction off and on and record observed cadence separately from any timestep used to capture video.

## Evidence

Celeste's creator describes the design techniques. Epic documents the character hooks. Prior Unreal checks covered coyote time and buffering on static platforms. Window lengths, moving platforms and player feel require target-game tests.

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html)
- [Epic — ACharacter](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/ACharacter?application_version=5.8)
- [Epic — OnLanded and movement mode](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/ACharacter/OnLanded)

## V30 corner correction for a planar Unreal character

Attempt correction on upward blocking contact during falling physics. Search nearby lateral offsets in ascending distance on the movement plane. Sweep the capsule sideways from contact and up along the unused movement to check clearance past its rounded cap. Commit both displacements with native sweeps. Roll the pair back and preserve the original hit response if either committed sweep blocks. Allow at most one success per ascent and retain the original jump identity, coyote window and buffer. [Epic — MoveUpdatedComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UMovementComponent/MoveUpdatedComponent)

Check mirrored lips at the correction limit, wide and low ceilings, a blocked side path, fast ascent and takeoff from a vertically moving base. Verify capsule clearance, landing and duplicate-jump prevention. Lateral shifts can change landing position. Measure observed frame cadence separately from capture timing and inspect contact frames. Extend collision checks for moving obstacles, slopes, custom gravity, root motion or network prediction.
