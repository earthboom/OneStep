---
id: K-GAME-TECH-CONTROLLER
title: Implement forgiving platformer input as explicit state windows
summary: Timestamp jump requests and last grounded state. Celeste values and integer-AABB
  rules are a particular game solution.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
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
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 coyote/buffer native policy68, actual PIE30/60/144,3paired
    standalone observations; other controller mechanisms and player feel untested
---
# Implement forgiving platformer input as explicit state windows

## Guidance

Timestamp jump requests and last grounded state. Permit a jump while its input buffer and ground-grace conditions overlap, then consume the request once. Add bounded corner correction after collision tests, and specify moving-platform momentum ownership. Tune acceleration, release deceleration and air control against intended challenge reach.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Celeste values and integer-AABB rules are a particular game solution. Do not permit infinite buffered jumps, correction through walls, or accidental momentum duplication.

## Checks

Proposed: test inputs just before/after ledges and landings, corner approaches, reversals and moving-platform stops at several frame rates.

## Evidence

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html) — Creator text; coyote time, buffering, corner correction and momentum storage. Checked 2026-11-07, except items explicitly marked further reading.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — Creator implementation; integer AABBs and fractional remainder. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V29, V30, V46 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Local Unreal input-window implementation — 2026-11-11

[Native controller results](../../prototypes/UnrealTechniqueLab/JUMP-RESULTS.md) implement only coyote time and jump buffering (V29,V46) with one actual UE5.8.3 CharacterMovement capsule and two platforms. Authored inclusive windows100ms/120ms use one simulation clock. Rising-edge request IDs, explicit success consumption and spent ground credit prevent repeated/extra air jumps; real walking transitions rearm. Released taps remain pending until expiry; holding creates no new request. A valid-at-landing request is latched once to the next movement update. CanJumpWhileFalling supplies the engine permission; Landed alone still has Falling mode, so use the completed movement-mode transition.

Compiled policy68 checks cover exact inside/boundary/outside times, consumed/held/air/spent-credit/reset/released input and next-update landing. Native rendered PIE runs cover four profiles at observed rates near30/60/144, nine cases each (108), in twelve actual PIE worlds. Real press/release/land/OnJumped/frame/velocity records check the released tap before landing, unique jump request IDs, expired inputs, no air spam and rearming. RequestedFPS alone is insufficient: a packaged30request observed23.42 and was rejected; PIE behavior is separately accepted at measured rates. Same-source standalone package supplies three matched performance pairs and normal-speed videos. This consumer distinction and the failed rate remain explicit, with no renderer/Present adjustment.

Performance pairs keep one character, same scene/physics/grounded inputs,1280x720,2s warmup+10s measure and6requests/6jumps. Per-policy timer noise and whole-frame cadence remain separate; no frame speedup, production-scale budget or subjective game-feel claim. Screenshots and complete decoded30fps videos show simulation1x. This adds partial evidence for CONTROLLER, not its corner correction/V30, moving-platform momentum, wall jumps, animation, networking or variable-height integration. Choose grace/buffer/cancellation based on level challenge and player tests; these constants and released-tap policy are not verified Celeste values.
