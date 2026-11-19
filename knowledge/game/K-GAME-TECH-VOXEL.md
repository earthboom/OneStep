---
id: K-GAME-TECH-VOXEL
title: Extract and stream editable voxel surfaces
summary: For editable block terrain, mesh exposed faces using both chunks' occupancy,
  merge compatible faces, and rebuild dirty borders with collision. The native fixture
  measures both approaches.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- voxel
- dual
- contouring
- Hermite
- QEF
- chunk
- 복셀
- dual contouring
- Hermite data
- quadratic error function
- greedy meshing
- exposed face
- chunk seam
- dirty neighbor
- collision cooking
- 노출면
- 재질별 면 병합
- 청크 이음새
- 경계 블록 편집
- 동기 충돌 갱신
status: active
checked_at: '2026-11-20'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V21 UE 5.8.3 block-face and same-material greedy meshing on
    two adjacent editable chunks. Exact coverage, native collision and raster pixels;
    3 matched runs each. Smooth extraction and streaming remain reference research.
---
# Extract and stream editable voxel surfaces

## Guidance

Use voxel fields when editable volume matters. Separate storage, surface extraction, collision and streaming. Dual contouring uses signed samples plus edge crossings/normals (Hermite data) and a quadratic-error fit; density values alone are not its complete input. Rebuild only affected regions and synchronize border samples.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### dual contouring

Dual contouring uses Hermite data at surface crossings: intersection positions and normals. A quadratic error function (QEF) scores candidate vertices by their fit to those local planes. Check normals and shared boundary samples across chunks when evaluating sharp-feature preservation or seam cracks.

## Applicability and exceptions

Block-face meshing and smooth contour extraction solve different art needs. Fine grids increase memory and rebuild work; seams, topology and collision lag remain engineering problems.

## Checks

Proposed: edit exactly on chunk borders, remove thin features and stream while moving; check visual/collision agreement.

## Evidence

- [Ju et al. — Dual Contouring of Hermite Data](https://www.cs.rice.edu/~jwarren/papers/dualcontour.pdf) — 2002 paper; abstract, Hermite input and QEF method. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V21 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Editable block-face meshing in Unreal — 2026-11-20

The local V21 experiment compared one quad per exposed face with greedy coplanar, same-material meshing. Both methods read a shared occupancy field. Dirty the owner for an interior edit and rebuild both chunks after committing a shared-edge edit. Do not emit an interior face between two occupied blocks, even when their materials differ. Use the full material and shading attributes as the merge key when face appearance depends on those properties.

The two-chunk fixture checks subdivisions, exact exposed area and restoration against an independent occupancy model, plus native line-trace and pixel samples. The initial mesh falls from 2,940 to 124 triangles (95.8% fewer). Synchronous collision medians across the runs were 4.417–5.541 ms for individual faces and 0.307–0.380 ms for merged faces. Whole-frame p95 bands overlap at 11.381–12.598 and 11.923–12.931 ms. Track generation, game-thread mesh submission, synchronous collision and edit-frame tails separately. The report has the six measurements and implementation scope. Complex triangle collision is verified for the fixture's queries. Smooth extraction and streaming remain research references.
