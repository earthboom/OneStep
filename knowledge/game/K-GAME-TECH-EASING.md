---
id: K-GAME-TECH-EASING
title: Choose curves by endpoint and timing constraints
summary: Evaluate a finite transition from normalized elapsed time. Define what happens to position,
  velocity and completion when the transition is interrupted.
kind: reference
scope: Game development. For a finite tween, pause can freeze the cursor, restart can take the current
  displayed value as its new start, and reversal can traverse the same cursor backwards.
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
- SetWorldLocation
- cubic Bézier
status: active
checked_at: '2026-11-19'
---
# Choose curves by endpoint and timing constraints

## Guidance

For positive duration, clamp elapsed/duration to [0,1], evaluate a curve and interpolate the endpoints. Linear interpolation keeps speed constant. `smoothstep` uses 3t²−2t³ with zero endpoint slopes. Perlin's quintic `smootherstep` also has zero second derivatives at the ends. For a CSS-style cubic Bézier timing function solve x(u)=t before using y(u). Asymmetric control points reveal mistakes that a linear curve hides.

## Applicability and exceptions

For a finite tween, pause can freeze the cursor, restart can take the current displayed value as its new start, and reversal can traverse the same cursor backwards. Restart can change velocity and reversal can flip it. For Unreal component motion, `SetWorldLocation` publishes a world-space transform. A swept root can stop before the requested position if collision blocks it.

## Checks

Test endpoints and overshoot, zero duration, pause/resume, restart and reverse mid-curve or after completion. Check single completion delivery, sample the actual component transform separately from the solver value, and distinguish elapsed wall time from synthetic samples.

## Evidence

W3C specifies Bézier timing and Perlin derives the quintic polynomial. Earlier collisionless component checks observed position-continuous restart, curve reversal and small transform rounding differences. Some requested display rates were missed. Collision, maintained velocity and player feel require separate checks.

- [W3C — CSS Easing Functions Level 1](https://www.w3.org/TR/css-easing-1/)
- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf)
- [Epic — Set World Location](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/USceneComponent/K2_SetWorldLocation?application_version=5.8)
