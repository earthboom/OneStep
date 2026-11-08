---
id: K-GAME-TECH-BILLBOARD
title: "Orient image impostors for their intended viewing conditions"
summary: "Use image planes for particles, distant vegetation or stylized objects. Intersecting planes, stereo views, shadows, transparency sorting and top-down viewing can reveal the approximation."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["billboard","impostor","빌보드"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Orient image impostors for their intended viewing conditions

## Guidance

Use image planes for particles, distant vegetation or stylized objects. Choose screen-aligned, viewpoint-facing or axis-constrained orientation. Preserve a stable up direction for grounded objects; an atlas can select different view angles when a single image is insufficient.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Intersecting planes, stereo views, shadows, transparency sorting and top-down viewing can reveal the approximation. A billboard is not automatically cheap if it covers many pixels.

## Checks

Proposed: orbit above/below the object, test the production camera and inspect alpha overdraw.

## Evidence

- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) — Official stable documentation; normal map, transparency and billboard sections; rolling version. Checked 2026-11-07, except items explicitly marked further reading.
- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass) — GPU Gems ch.7; crossed quads and animation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V43 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

