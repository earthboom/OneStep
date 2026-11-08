---
id: K-GAME-TECH-REFLECTION
title: "Select reflections by visibility and update requirements"
summary: "For flat accurate mirrors, render a reflected camera view with clipping. A mirrored duplicate scene is one historical trick, not the definition of planar reflection."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["reflection","SSR","cubemap","mirror","거울"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Select reflections by visibility and update requirements

## Guidance

For flat accurate mirrors, render a reflected camera view with clipping. For approximate surrounding light, use reflection probes/cubemaps; choose static capture or explicit update policy. SSR traces against available screen depth, so use fallback data for rays leaving the image. Combine methods by roughness, distance and importance.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

A mirrored duplicate scene is one historical trick, not the definition of planar reflection. Cubemaps may be updated dynamically. SSR cannot recover unseen geometry.

## Checks

Proposed: move a reflected object off-screen, change the camera angle, and compare static/dynamic captures and GPU pass costs.

## Evidence

- [Epic — Planar Reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/planar-reflections-in-unreal-engine) — Official documentation; SSR comparison and rendering cost. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V16 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

