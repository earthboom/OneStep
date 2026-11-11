---
id: K-GAME-TECH-EASING
title: Choose curves by endpoint and timing constraints
summary: Use normalized elapsed time for finite transitions;scoped UE5.8.3 four-curve
  pause/restart/reverse evidence distinguishes scriptedHz from realFPS,position continuity
  from velocity,and policy values from native transform tolerance.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- easing
- Bézier
- smoothstep
- smootherstep
- interpolation
- 베지에
- 보간 전환 시간
- 전환 시간
- normalized time
- transition duration
- camera transition
- tween
- pause resume
- restart
- reverse
- asymmetric curve
- current value
- position continuity
- velocity discontinuity
- 역재생
- 전환 중단
- 현재값 재시작
- 끝점
status: active
checked_at: '2026-11-12'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 V47/V59 partial native:104policy,96PIE method-cases,12cost
    players,1x media;scripted30/60/144Hz distinct from actualFPS;no physics/UI/blending
    proof
  actual_fps: cap30→23.21FPS, cap60→45.66FPS, cap144→110.32FPS;missed requested rendering
    bands remain unverified
---
# Choose curves by endpoint and timing constraints

## Guidance

Map normalized time to progress before interpolating a value. Smoothstep 3t²-2t³ has zero endpoint slopes; quintic 6t⁵-15t⁴+10t³ also has zero endpoint second derivatives. A cubic Bézier is a parametric curve; for CSS-style timing solve its x parameter before reading y. A generic cubic does not reproduce every bounce exactly.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Ease curves describe interpolation, not automatically physically correct motion. Repeated easing towards a target differs from evaluating a finite-duration animation.

## Checks

Native scoped checks and actualFPS limits are recorded below;production collision/velocity-continuous retargeting remain unverified.

## Evidence

- [W3C — CSS Easing Functions Level 1](https://www.w3.org/TR/css-easing-1/) — 2023 candidate recommendation draft; cubic Bézier input/output mapping. Checked 2026-11-07, except items explicitly marked further reading.
- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf) — 2002 paper; interpolation and gradients. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V47, V59 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


## Retrieval distinction — 2026-11-11

For a camera transition whose authored duration is wrong, retrieve EASING for normalized elapsed-time progress and endpoint constraints together with CAMERA for follow damping. TIMESTEP covers simulation accumulation and previous/current presentation, not the authored duration of an easing transition. This routing clarification repairs a demonstrated existing camera-timing lookup miss after adding timestep evidence; no new engine/easing validation or source recheck is implied.

## Native Unreal finite-duration transitions — 2026-11-12

[V47/V59 results](../../prototypes/UnrealTechniqueLab/EASING-RESULTS.md) add104policy checks,scripted30/60/144Hz and irregular time inputs,96method-case observations in3actual PIE worlds,3matched cost repeats per curve and actual normal1x media. Observed native frame-update rates:cap30→23.21FPS, cap60→45.66FPS, cap144→110.32FPS. ScriptedHz is not renderingFPS;missed requested bands remain unverified. Existing BILLBOARD FPS shortfalls are preserved. Latest13limited local sheets/30without direct technique prototypes,not complete certification.

Adopt Linear for constant normalized progress,Smoothstep for zero endpoint slope,Smootherstep for zero endpoint first/second derivatives,and cubicBezier for authored/asymmetric timing. This local Bezier uses default(.25,.1,.25,1),solves x(s)=t then y(s),at most48bisection iterations;finite x controls0..1 and authored y bound[-4,4]. Input clamps0..1 while output remains unclamped;(.3,-.5,.7,1.5)overshoots in the actual native scene. Unlike CSS this helper does not extrapolate input outside0..1. [W3C](https://www.w3.org/TR/css-easing-1/) supports the x-input/y-output convention;[Perlin2002](https://mrl.cs.nyu.edu/~perlin/paper445.pdf) supports polynomial endpoint properties. Both reread2026-11-12;historical noise timing is not this benchmark.

Use elapsed/duration for authored completion time. Repeated easing from the current value toward a target is a different contract. Start captures finite from/to/nonnegative duration;0seconds completes once,same-value segments still consume duration. Invalid inputs reject atomically. The bounded state machine discards excess dt after reaching an endpoint rather than automatically applying it to a new segment. Pause freezes cursor/value;Resume continues remaining active time. Restart samples CURRENT value as new start toward a new target/duration,preserving position and cumulative completion count. Reverse changes direction on the SAME original curve/cursor,including after completion and while paused;it retraces asymmetric timing instead of swapping endpoints and restarting. Remaining time is cursor distance to endpoint. Zero-duration reverse rejects;an already reached requested endpoint does not duplicate completion. These are authored local semantics,not a universal tween-library standard.

Position-continuous restart does not guarantee velocity continuity;reverse can flip velocity. Polynomial endpoint derivatives do not remove these interruption effects. Overshoot may violate collision/target bounds. Prototype bodies are collisionless native cubes:do not transfer these results to collision-safe doors,platforms,characters,network determinism or full animation blending. Springs/physics/UI integration/player-rated feel remain unverified.

Native8cases cover2s normal→hold,pause.6/resume1.1→finish2.5,restart.7→newtarget1.7,reverse.7→return1.4,completed2→reverse2.2→return4.2,zero duration,Bezier overshoot and invalid operations. Events split at authored timestamps,not hardware input delivery. Independent age-based equations and de Casteljau reference check state/cursor/value,direction,completion,event order and actual native xyz. Runtime ages relate to monotonic wall within5ms Tick-entry→logging uncertainty;clamped case endpoints allow one recorded frame interval.33s total is independently bounded. Capture uses separate fixed30simulation increments,not real-time timing proof.

Confirmed precision boundary:policy reached400cm but SetWorldLocation kept399.9999445cm. Installed UE5.8.3 SceneComponent InternalSetWorldLocationAndRotation uses vector Equals with1e-4cm default tolerance,so tiny movement can be skipped. Retain separate policy-value1e-7cm and actual one-axis component1e-4cm checks;do not loosen policy/time checks to match native tolerance or force offset hacks. Failingpilot-v2-60 and source-backed correction remain in results.

Cost:512separate cubes,same grid/camera/material/size/no shadow/no collision,selected curve only,1280×720,2s warmup+10s measurement,three rotated orders=12players. CPU subset includes per-component curve evaluation/native location publication/readback;it does not measure pause/restart/reverse command costs. Full wall/cadence remain distinct from GPU/Present completion. No full state/pixel/capture logging in cost runs. Identical phase is intentionally evaluated per component;not an optimized shared-curve or instancing design. Different curve positions can alter screen coverage,so full-frame differences do not isolate solver/GPU savings.

ONE fresh read-only review found missing wall-age/total-duration coupling and self-equal but fabricated event values could pass. Three sensitivity failures reproduced both gaps;independent timing/event-value checks repaired them.30final evidence tests reject those plus absent/wrong methods,wrongBezier evaluation,paused/restarted/reversed timelines,duplicate completion,clamped overshoot,policy endpoint error,clock relabel,launch and copied-repeat substitutions. 104policy,inheritedBillboard39,legacy actualPIE2tests/73 and packaged73 use final frozen Source/Config/project/36unchanged assets/module/exe/5containers/launcher.18older source archives retain bytes. No renderer/framework optimization,cap tuning,commit or push.
