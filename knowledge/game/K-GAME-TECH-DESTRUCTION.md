---
id: K-GAME-TECH-DESTRUCTION
title: "Choose authored fracture or runtime topology from gameplay needs"
summary: "For cosmetic damage, authored mesh swaps and debris may be sufficient. Pre-fractured does not mean pre-animated."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["fracture","chaos","destruction","decal","파괴"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Choose authored fracture or runtime topology from gameplay needs

## Guidance

For cosmetic damage, authored mesh swaps and debris may be sufficient. For gameplay-relevant fracture, author Geometry Collections, clustering, collision and damage thresholds. Decide separately whether to simulate precomputed pieces or generate new cuts at runtime; use decals for surface marks.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Pre-fractured does not mean pre-animated. Physics, navigation, replicated state and persistent damage must agree with visual destruction.

## Checks

Proposed: test repeated impacts, obstructed fragments, save/load and multiplayer authority; cap persistent debris.

## Evidence

- [Epic — Geometry Collections User Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/geometry-collections-user-guide) — Official documentation; Geometry Collection authoring. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V14 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

