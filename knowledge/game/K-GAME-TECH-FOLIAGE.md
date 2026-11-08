---
id: K-GAME-TECH-FOLIAGE
title: "Budget dense vegetation across geometry and pixel cost"
summary: "Use crossed alpha-tested cards or meshes according to silhouette importance. Instancing reduces submission overhead, not all shading work."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["foliage","grass","LOD","culling","instancing","잔디","인스턴싱","컬링","오버드로","최적화"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Budget dense vegetation across geometry and pixel cost

## Guidance

Use crossed alpha-tested cards or meshes according to silhouette importance. Cull outside useful visibility, reduce distant detail, batch compatible instances, and animate vertices with spatially coherent wind. Keep draw submission, vertex cost, overdraw and shadow cost as separate budgets.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Instancing reduces submission overhead, not all shading work. Cards can cost more pixels than denser opaque geometry. These historical sources do not certify Nanite foliage behavior.

## Checks

Proposed: capture dense low-angle and overhead views; disable wind, shadows and alpha layers separately to identify the limiting pass.

## Evidence

- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass) — GPU Gems ch.7; crossed quads and animation. Checked 2026-11-07, except items explicitly marked further reading.
- [Tiago Sousa — Vegetation Procedural Animation and Shading in Crysis](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis) — GPU Gems 3 ch.16; wind animation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V19 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

