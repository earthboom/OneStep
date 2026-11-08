---
id: K-GAME-TECH-VOXEL
title: "Extract and stream editable voxel surfaces"
summary: "Use voxel fields when editable volume matters. Block-face meshing and smooth contour extraction solve different art needs."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["voxel","dual","contouring","Hermite","QEF","chunk","복셀"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Extract and stream editable voxel surfaces

## Guidance

Use voxel fields when editable volume matters. Separate storage, surface extraction, collision and streaming. Dual contouring uses signed samples plus edge crossings/normals (Hermite data) and a quadratic-error fit; density values alone are not its complete input. Rebuild only affected regions and synchronize border samples.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Block-face meshing and smooth contour extraction solve different art needs. Fine grids increase memory and rebuild work; seams, topology and collision lag remain engineering problems.

## Checks

Proposed: edit exactly on chunk borders, remove thin features and stream while moving; check visual/collision agreement.

## Evidence

- [Ju et al. — Dual Contouring of Hermite Data](https://www.cs.rice.edu/~jwarren/papers/dualcontour.pdf) — 2002 paper; abstract, Hermite input and QEF method. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V21 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

