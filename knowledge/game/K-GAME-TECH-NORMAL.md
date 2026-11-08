---
id: K-GAME-TECH-NORMAL
title: "Add lighting detail without changing surface topology"
summary: "Use normal textures when the lighting needs finer surface detail than the mesh. Ordinary normal mapping does not change silhouette, collision or actual surface height."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["normal","map","tangent","노멀맵"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Add lighting detail without changing surface topology

## Guidance

Use normal textures when the lighting needs finer surface detail than the mesh. Decode stored vectors in the expected space, transform through a compatible tangent basis, and normalize before lighting. Keep the normal-map convention consistent across baking, import and rendering.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Ordinary normal mapping does not change silhouette, collision or actual surface height. A normal map on a 2D sprite needs a lighting pipeline that uses it.

## Checks

Proposed: rotate the light, mirror UVs and inspect seams; test compression and lower mip levels.

## Evidence

- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) — Official stable documentation; normal map, transparency and billboard sections; rolling version. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V26 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

