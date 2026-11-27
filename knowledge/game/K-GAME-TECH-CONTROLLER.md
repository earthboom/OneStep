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

Only attempt correction for an upward blocking contact during falling physics. Search nearby offsets in ascending distance on the movement plane. Sweep the capsule sideways from the contact and farther along the unspent upward movement to check clearance past the rounded cap. Commit the side displacement and the unspent movement with native sweeps. If either committed sweep is blocked, revert the pair and preserve the original hit response. A successful correction uses no new jump credit and can occur once per ascent. [Epic — MoveUpdatedComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UMovementComponent/MoveUpdatedComponent)

The lab searches in 1 cm increments up to 10 cm for a 22 cm-radius capsule locked to the XZ plane. The side correction is visible and can change landing position. Tune the limit and tie-breaking against the target character and platform spacing. Recheck slopes, complex collision, custom gravity, animation root motion, network prediction and moving obstacles before applying the same rule to those cases. The moving-base example is a vertically translating takeoff base with the ceiling held still.

On 2026-11-21, the DX11 Win64 Development package passed 270 scenarios across 18 runs. Both sides, the 9 and 10 cm candidates, fast ascent and moving-base takeoff succeeded with correction enabled. The 11 cm requirement, wide ceiling and blocked side path preserved the ordinary collision response. Sampled penetrations and duplicate jump requests were zero. The coyote and buffer windows retained their native acceptance and expiry behavior.

At observed mean rates of about 30, 60 and 144 FPS, each profile ran three repeats at 1280×720 on an i7-12700KF and RTX 3080. BeginFrame-to-EndFrame p95 ranges are in milliseconds.

| Observed FPS | Off | On |
| --- | ---: | ---: |
| 30 | 33.417–33.418 | 33.393–33.471 |
| 60 | 16.732–16.780 | 16.734–16.803 |
| 144 | 7.029–7.044 | 7.041–7.044 |

The correction path measured p95 0.030 ms and maximum 0.0925 ms across 78 timed attempt frames after warmup. The full-frame results include frame pacing. For adoption, also inspect contact-frame cost and how many characters can hit obstacles in the same frame. The separate media run used fixed 30 Hz for normal-speed playback.
