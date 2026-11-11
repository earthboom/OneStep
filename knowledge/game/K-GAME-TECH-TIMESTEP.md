---
id: K-GAME-TECH-TIMESTEP
title: Separate simulation steps from rendering and tune jump integration
summary: Separate fixed simulation from presentation; scoped UE5.8.3 tests verify3FPS
  state traces, retained debt under finite hitches and one-tick display interpolation.
  Recovery timing is update-start, not presentation completion; global engine/network
  determinism remains untested.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- fixed
- timestep
- Euler
- subpixel
- interpolation
- delta
- time
- 프레임
- accumulator
- backlog
- catchup
- render interpolation
- one tick delay
- jump apex
- per flight
- 고정 시간
- 누적 시간
- 렌더 보간
- 지연 복구
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 V02/V49 independent model:78policy,36actual PIE method-cases,9package
    cost players,normal1x media; no Chaos/global engine/network proof
---
# Separate simulation steps from rendering and tune jump integration

## Guidance

Use a fixed simulation step when stable physics/replay is required, with an accumulator and interpolated presentation. Bound catch-up work. Semi-implicit Euler updates v+=a*dt before x+=v*dt; explicit Euler uses the old velocity. Gameplay jumps may use different rise/fall acceleration. Keep fractional positions or residuals even if displaying integer pixels.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Multiplying by delta time alone does not make arbitrary physics stable or deterministic. Display FPS, simulation tick rate and network tick rate are separate.

## Checks

Proposed: replay identical inputs at 30/60/144 rendering FPS and injected stalls; compare apex, landing and event order.

## Evidence

- [Glenn Fiedler — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) — Author technical article; bounded steps, accumulator and interpolation. Checked 2026-11-07, except items explicitly marked further reading.
- [Glenn Fiedler — Integration Basics](https://gafferongames.com/post/integration_basics/) — Author technical article; explicit and semi-implicit integration. Checked 2026-11-07, except items explicitly marked further reading.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — Creator implementation; integer AABBs and fractional remainder. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V02, V49 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Local Unreal timestep comparison — 2026-11-11

[Native V02/V49 results](../../prototypes/UnrealTechniqueLab/TIMESTEP-RESULTS.md) add78policy checks,3actual PIE worlds at observed30/60/144normal FPS×4cases×3methods=36method-case observations,3matched packaged repeats per method and actual30fps1x media. This is an independent scripted semi-implicit-Euler movement/jump model, not global Unreal/Chaos/CharacterMovement fixed stepping, hardware-input latency or a network deterministic simulation. Existing crowd/validation clocks were not modified.

Adopt fixed60Hz when the tested frame-independent state/command outcomes are required. Both fixed variants retain the same180state samples over a3s horizon across all observed FPS and real50/100/250ms game-thread sleeps. Every case consumes6timestamped commands once, accepts2jumps,rejects2air repeats and lands2times, with finalx540cm/z0 and both fixed peaks145cm. Commands are script simulation timestamps; variable steps split at those command times to isolate integration-size error from input scheduling. Compare per-flight peaks and landing times: a global maximum can hide the hitch-affected first jump behind a later ordinary jump. Fixed60Hz gives a discrete145cm peak here, not the continuous150cm solution. Variable-rate trajectories intentionally differ.

The accumulator processes≤8fixed steps per rendered update and retains debt. Finite250ms delay can require subsequent updates to drain; recovery does not erase the actual stall. Frames/models record offered time, simulation time, debt,steps and command sequence. Declared numeric due/command guard1e-10s and floor tolerance1e-9cm mean conservation within checked tolerance, not bit-exact wall-clock conservation. Horizon3s(behavior)/12s(cost) clips further arrivals and reports them as excess; no within-horizon dropped backlog claim. Sustained overload, unconstrained frame deltas or a production lifetime are not validated by finite-horizon recovery.

Keep simulation/collider authority separate from display interpolation. Native20/20capsule publishes current simulation position, while a collisionless sphere displays current state or previous/current interpolation. Ordinary interpolation has one fixed-tick display delay. Clamp alpha to[0,1]; backlog≥one tick displays current without extrapolation. Independent steady-speed x(t-h) errors and144FPS hold counts validate this scoped presentation behavior, not player-rated smoothness or reduced input latency. Normal30fps video is illustrative and cannot visually prove144FPS presentation or record the real hitches; actual FPS/hitches have separate PIE evidence.

Real floor ray/capsule-block controls and per-step swept component destination checks establish this simple native scene integration. Constant-height offset2cm separates the authored ground projection from native collision; no Chaos contact resolution/slope/jump-controller proof. The reproduced tiny ascending step originally triggered the near-zero floor clamp and caused premature landing/reaccepted input. Require descending/nonpositive vertical velocity as well as near-floor position. Its native policy regression failed before the repair and passes afterward; do not indiscriminately zero positive tiny ascent as numerical noise.

Three matched1280×720 package repeats per variable/fixed/interp method measure one common sphere/body/floor/camera/HUD,2s warmup+10s measured. Selected method only; no deliberate sleep/debug/support queries/full state snapshots/capture. Stage timing includes model,actual native body moves and display publication. Whole12s command/tick totals and10s frame evaluation denominators are different and must be labelled; fixed720ticks/24commands/8accepted/8rejected/8lands cover the whole horizon. Whole wall/cadence remains distinct from CPU subset; no GPU/commercial-character/multi-agent budget promise. Capture and final JSON/exit are excluded.

Fresh read-only review found two evidence gaps, repaired through failing-then-passing tests: absent per-method frame values and a variable first peak replaced by the global apex. Require exactly3method entries and derive per-flight peaks from accepted-command→landing state samples. Final19evidence tests cover these plus state/input/debt/cap/collider/launch/repeat substitutions. Frozen source/config/project/32unchanged assets/module/exe/5package containers/launcher and outputs bind final runs;16older archives retain their original bytes.

Remaining timing limit: recoveryMs is measured to the start of the update that drains debt, not completion of its simulation/render/presentation. Report that name/meaning; do not claim end-to-end visual recovery latency. Source concepts were reread2026-11-11 in Fiedler's Fix Your Timestep and Integration Basics. Exact schedule,cap,ground projection and local outcomes are authored experiment choices, not proof of a particular commercial game.
