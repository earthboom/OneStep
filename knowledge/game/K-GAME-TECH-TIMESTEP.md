---
id: K-GAME-TECH-TIMESTEP
title: "Separate simulation steps from rendering and tune jump integration"
summary: "Use a fixed simulation step when stable physics/replay is required, with an accumulator and interpolated presentation. Multiplying by delta time alone does not make arbitrary physics stable or deterministic."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["fixed","timestep","Euler","subpixel","interpolation","delta","time","프레임"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
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

