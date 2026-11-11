---
id: K-GAME-TECH-HITBOX
title: Keep attack, hurt and physical collision contracts distinct
summary: Separate attack, hurt and physical collision; scoped UE5.8.3 tests verify
  active-time-clipped sphere sweeps, owner filtering and one damage per attack-target.
  Static upright targets only; hitstop/full combat remain untested.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- hitbox
- hurtbox
- hitstop
- collision
- 피격
- attack window
- sphere sweep
- active clipping
- duplicate damage
- attack identity
- hurt capsule
- blocking status
- 히트박스
- 허트박스
- 중복 피격
- 고속 통과
- 공격 활성 구간
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 V42:40policy,174actual PIE observed30/60/144,3paired
    package costs,native1x media; static linear sphere only; hitstop untested
---
# Keep attack, hurt and physical collision contracts distinct

## Guidance

Separate attack volumes, damage-receiving volumes and movement collision. Activate attacks on simulation states/frames and assign attack identities to avoid unintended repeat hits. Use grace windows or invulnerability only where the design requires them. Hit-stop should specify which clocks pause and which input buffers continue.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

This is a proposed combat engineering contract derived from collision/forgiveness principles, not a verified universal commercial hitbox recipe. Smaller hurtboxes are a choice; high-speed motion may require swept tests.

## Checks

Proposed: visualize volumes frame-by-frame, test simultaneous hits and movement through thin targets, and replay with hit-stop disabled.

## Evidence

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html) — Creator text; coyote time, buffering, corner correction and momentum storage. Checked 2026-11-07, except items explicitly marked further reading.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — Creator implementation; integer AABBs and fractional remainder. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V42 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Local Unreal attack/hurt/physical separation — 2026-11-11

[Native V42 results](../../prototypes/UnrealTechniqueLab/HITBOX-RESULTS.md) add scoped UE5.8.3 evidence: attack sphere8cm, hurt capsule20/60cm (thin control radius1), physical capsule50/90cm. Physical bodies ignore the dedicated attack query and block Pawn; query-only hurt components overlap attack. Registry filtering/owner exclusion and one monotonic attack-ID/target ledger prevent self/unknown/duplicate/stale damage. Same/stale Begin cannot reset the set; End rejects later callbacks; a new attack may hit again. No HP/combo/combat AI/network authority or hitstop implementation.

Use endpoint overlap only when its sampling sensitivity is acceptable. Previous/current linear sphere sweep is clipped to the active integer-us interval [open,close); initial overlap is queried explicitly, then the nonzero segment is swept. Start inside blocking wall rejects; contacts are ordered by returned time then target ID. Native multi-query bool reports blocking status, so false with overlapping touches must still process the output array. This is supported by installed5.8.3 World.h and actual touch-only controls, not just API-name inference. The1us boundary fixtures are injected logical inputs, not hardware input precision or proof that a long injected segment equals a real frame.

40policy checks and29cases×6actual PIE worlds=174 at observed30/60/144FPS cover thin/fast passage, inside/tangent/outside±.001cm, open/close boundaries, short active windows, clipping before/after crossing, initial/held overlap, duplicate hurt components, second attack, owner-ignore/control, multiple/equal-time targets, channel ignore, walls before/after/start and wrong-generation callback. Endpoint intentionally misses the fixed fast and short-window controls and can accept a destination beyond an intervening wall. It is a sensitivity/cost baseline, not a safe wall-aware equivalent. Native capsule dimensions/transform/query outcome remain unchanged; scripted before/after Pawn sweeps are not a full CharacterMovement safety trial.

Retained numeric limitation: sweep accepts hurt fractions strictly below wallFraction-1e-7. This favors a wall in exact/near ties and may reject an extremely close preceding hurt contact. No sub-guard wall boundary was validated; do not promise exact unguarded contact ordering. All geometry is known static upright capsules and a sampled linear sphere path: moving targets, rotating blades, curved paths, destruction/ID reuse and arbitrary meshes require separate tests.

Three matched1280x720 uncapped packaged pairs,2s warmup+10s measured, selected strategy only and no debug draw/capture, each produce the same30damage events/attack-target order at ordinary750cm/s. Sweep adds a start overlap plus segment query per active evaluation; endpoint uses one. Report query/policy and complete wall frame/cadence p95/max separately. Script trajectory/attack setup is outside the microtimer but inside complete frames; common HUD/collision scene has no rendered character, so this is not a production combat/GPU budget. Frozen source/config/project/32unchanged assets/binaries/5package containers and output hashes bind results to launches; independent intervals/raw frame arrays reject copied repeats. Native30fps1x media is separate from unbiased cost data.

External API evidence: [Epic SweepMultiByChannel](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/Engine/UWorld/SweepMultiByChannel?application_version=5.5) describes overlap touches before the first blocking hit and the bool meaning (5.5 page); [collision response reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/collision-response-reference-in-unreal-engine) distinguishes query-only and responses (rolling5.9 page). Checked2026-11-11; installed5.8.3 headers/build/runtime establish local behavior. These sources do not prescribe the1us ledger/window design or prove a commercial game's implementation. Smaller hurtboxes remain a game-design choice, not player-rated forgiveness evidence.
