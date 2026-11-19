---
id: K-GAME-TECH-TIMESTEP
title: Separate simulation steps from rendering and tune jump integration
summary: Accumulate elapsed time and advance the simulation in fixed increments. Budget catch-up and
  interpolate presentation separately from authoritative state.
kind: reference
scope: Game development. For a bounded fixed-step model with residual time below h, interpolate the
  previous and current transforms with alpha=residual/h.
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
- fixed timestep
- semi-implicit Euler
- explicit Euler
status: active
checked_at: '2026-11-11'
---
# Separate simulation steps from rendering and tune jump integration

## Guidance

An accumulator holds elapsed time not yet simulated. For each fixed step h that is due, update state and subtract h. Decide how to handle backlog when a per-frame catch-up limit is reached. Semi-implicit Euler updates velocity before position, while explicit Euler uses the old velocity. Keeping fractional position allows subpixel motion even on an integer display.

## Applicability and exceptions

For a bounded fixed-step model with residual time below h, interpolate the previous and current transforms with alpha=residual/h. This draws about one simulation tick behind the elapsed-time trajectory. Keep collisions and input on the simulation clock. Sustained overload requires an explicit time-loss, slowdown or capacity policy.

## Checks

Replay the same timestamped commands at different render cadences and through hitches. Reconcile offered time with simulated time, retained debt and discarded time. Compare apex and landing for each flight. A near-floor tolerance must also consider descent before treating a tiny ascent as a landing.

## Evidence

Fiedler derives accumulator scheduling and integrator behavior. Thorson documents fractional movement in an integer collision model. Earlier scripted movement checks covered finite hitch recovery and display interpolation. They leave engine-wide physics determinism, presentation-complete recovery time and network replay untested.

- [Glenn Fiedler — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)
- [Glenn Fiedler — Integration Basics](https://gafferongames.com/post/integration_basics/)
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html)
