---
id: K-GAME-TECH-SHADOW
title: "Choose shadow-map resolution and filtering"
summary: "Use for moving lights or casters. Acne, peter-panning, cascade seams and camera-motion shimmer are different failures."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["shadow","map","PCF","CSM","그림자"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Choose shadow-map resolution and filtering

## Guidance

Use for moving lights or casters. Render light-space depth, then compare the receiver's light-space depth against it. CSM allocates directional-light coverage across camera-frustum intervals; PCF averages comparison results, not ordinary filtered depth. Tune split distances, receiver/caster bias, filter footprint and stabilization separately. Bake static lighting only when its assumptions remain valid.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Acne, peter-panning, cascade seams and camera-motion shimmer are different failures. Historical Direct3D examples do not establish the best UE renderer configuration.

## Checks

Proposed: inspect grazing surfaces, thin geometry and a slow camera sweep; measure shadow-pass GPU time and memory per quality tier.

## Evidence

- [Microsoft — Cascaded Shadow Maps](https://learn.microsoft.com/en-us/windows/win32/dxtecharts/cascaded-shadow-maps) — Technical article; frustum partitioning and stability sections. Checked 2026-11-07, except items explicitly marked further reading.
- [Bunnell & Pellacini — Shadow Map Antialiasing](https://developer.nvidia.com/gpugems/gpugems/part-ii-lighting-and-shadows/chapter-11-shadow-map-antialiasing) — GPU Gems ch.11; sections 11.1–11.2. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V03 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

