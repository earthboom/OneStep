---
id: K-GAME-TECH-EASING
title: "Choose curves by endpoint and timing constraints"
summary: "Map normalized time to progress before interpolating a value. Ease curves describe interpolation, not automatically physically correct motion."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["easing","Bézier","smoothstep","smootherstep","interpolation","베지에"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Choose curves by endpoint and timing constraints

## Guidance

Map normalized time to progress before interpolating a value. Smoothstep 3t²-2t³ has zero endpoint slopes; quintic 6t⁵-15t⁴+10t³ also has zero endpoint second derivatives. A cubic Bézier is a parametric curve; for CSS-style timing solve its x parameter before reading y. A generic cubic does not reproduce every bounce exactly.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Ease curves describe interpolation, not automatically physically correct motion. Repeated easing towards a target differs from evaluating a finite-duration animation.

## Checks

Proposed: evaluate endpoints, derivatives, overshoot and interruptions; use the same duration under changing FPS.

## Evidence

- [W3C — CSS Easing Functions Level 1](https://www.w3.org/TR/css-easing-1/) — 2023 candidate recommendation draft; cubic Bézier input/output mapping. Checked 2026-11-07, except items explicitly marked further reading.
- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf) — 2002 paper; interpolation and gradients. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V47, V59 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

