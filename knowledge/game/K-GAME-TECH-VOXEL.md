---
id: K-GAME-TECH-VOXEL
title: Extract and stream editable voxel surfaces
summary: Keep shared field samples and one face owner for editable voxel chunks.
  UE 5.8.3 evidence covers exposed and merged block faces, plus uniform-grid Dual Contouring
  with bounded Hermite fitting, shared normals, edits and native query collision.
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
- Dual Contouring
- smooth isosurface
- shared samples
- face saddle
- ambiguous face
- manifold edge
- 등가면
- 표면 오차
- 모호한 면
- 밀도 0
status: active
checked_at: '2026-11-22'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V21 UE 5.8.3 measured block meshing and same-resolution Dual Contouring
    in separate two-chunk fixtures. See each for scoped native surface, collision and cost evidence.
---
# Extract and stream editable voxel surfaces

## Guidance

Use voxel fields when editable volume matters. Separate storage, surface extraction, collision and streaming. Dual contouring uses signed samples plus edge crossings/normals (Hermite data) and a quadratic-error fit; density values alone are not its complete input. Rebuild only affected regions and synchronize border samples.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### dual contouring

Dual contouring uses Hermite data at surface crossings: intersection positions and normals. A quadratic error function (QEF) scores candidate vertices by their fit to those local planes. Check normals and shared boundary samples across chunks when evaluating sharp-feature preservation or seam cracks.

For same-resolution chunks, sample the same world-space scalar field and classify exact isovalue samples consistently. Give each sign-changing grid edge one face owner even when its quad needs cells from both chunks. A planar cell constrains only the normal axis, so use a stable null-space policy. If a face alternates between solid and empty at successive corners, make the face connectivity decision from shared samples and fit one vertex per connected contour component within the cell. Check both triangulations of a folded quad before publishing geometry. [Ju et al. — Dual Contouring of Hermite Data](https://www.cs.rice.edu/~jwarren/papers/dualcontour.pdf) · [Schaefer et al. — Manifold Dual Contouring](https://www.cse.wustl.edu/~taoju/research/dualsimp_tvcg.pdf)

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

The historical block-meshing scope predates the uniform-grid follow-up below.

## Native Unreal V21 uniform-grid Dual Contouring

For adjacent same-resolution chunks, classify the exact isovalue consistently. Give each sign-changing edge one face owner and read neighboring cells through a halo. Use world cell and component keys to produce matching positions and normals in both chunks.

Fit Hermite intersections and normals with a bounded cell-local QEF. Use a stable mass-point policy for unconstrained planar directions. For alternating-sign faces, decide connectivity from shared samples and fit disconnected surface components separately. One vertex for a cell can create an edge with too many incident faces. When a cut folds the initial diagonal, check both triangulations and preserve the perimeter and outward winding. [Ju et al. — Dual Contouring of Hermite Data](https://www.cs.rice.edu/~jwarren/papers/dualcontour.pdf) · [Schaefer et al. — Manifold Dual Contouring](https://www.cse.wustl.edu/~taoju/research/dualsimp_tvcg.pdf)

Check a curved surface, a sharp edge and an exact-zero plane against an independent field. After local and boundary edits, compare face ownership, connected vertex fans, seam normals, visible pixels, native queries and whole-buffer restoration. Compare geometric error and edit-frame cost when choosing a resolution. Measure field sampling, extraction, submission and collision separately. This guidance covers same-resolution neighbors and synchronous triangle queries.
