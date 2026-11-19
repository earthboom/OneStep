---
id: K-GAME-TECH-INTERIOR
title: Fake inaccessible interiors with ray-box mapping
summary: Use local-space ray-box intersections for decorative, inaccessible planar
  window rooms. Scoped UE5.8.3 GPU/geometry checks cover parallax, edges, UV mirrors
  and positive affine transforms; actual 30/60/144 FPS bands remain unverified.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["interior", "mapping", "window", "인테리어매핑", "장식창문", "비진입창문", "interior mapping", "ray-box intersection", "ray box", "aperture", "facade occlusion", "grazing view", "UV mirror", "nonuniform scale", "window parallax", "가짜방", "창문 시차", "비진입 창문", "광선 상자"]
status: active
checked_at: '2026-11-12'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: 'Partial UE5.8.3 V15 verification: 48 policy / 50 evidence tests,
    576 window observations / 14400 pixel pairs, nine cost players and 1x media. Actual
    30/60/144 FPS bands UNVERIFIED; unlit point atlas, non-enterable.'
---
# Fake inaccessible interiors with ray-box mapping

## Guidance

Use on windows whose rooms cannot be entered. Transform the view ray into room-local coordinates, intersect an implicit room box, and sample the corresponding wall/floor/ceiling texture. Introduce room variation without authoring full interior meshes.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### interior mapping

Interior mapping uses a ray-box intersection in room-local coordinates to determine which interior surface appears behind a facade. Check grazing views and nearby cameras where parallax errors or the lack of real geometry become visible.

## Applicability and exceptions

The room is a shading illusion: it does not automatically provide real collision, navigation, shadows or interactive furniture. Close grazing views reveal limits.

## Checks

Native camera, edge/facade, transform, UV and epsilon checks are summarized below. Actual FPS bands, entry, lighting, glass, furniture and streaming remain unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Joost van Dongen — Interior Mapping](https://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.pdf) — 2008 author manuscript; abstract and ray intersections. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V15 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native ray-box mapping evidence — 2026-11-12

The historical Unreal run provides scoped Win64 Development/DX11 evidence: 48 policy/atlas/time/mesh metadata checks, 50 evidence tests, 576 actual window observations / 14,400 candidate-reference pixel pairs and three matched packaged cost runs per representation. **Verification is partial: final actual 30/60/144 FPS bands were not reached and remain unverified.** Scripted time inputs and normal 1x capture do not establish actual FPS. Latest coverage: 18 limited sheets / 25 without direct prototypes.

Implementation order: transform camera to room-local space → undo aperture UV mirror to recover the physical front point → normalize the inward ray → find the nearest box exit plane → calculate face UV → apply intended texture mirror. Positive nonuniform scale, rotation and translation are checked; UV mirroring is not negative geometry scale. Authored bounds: finite UV [0,1], Mirror 0/1, sizes 1..10000 cm, absolute camera components ≤1e7, CameraZ>1e-4. Reject Dz≥-1e-6; skip axes with absolute direction ≤1e-6; resolve ties X/Y/Z. CPU invalid input preserves output; GPU returns finite black. These are local bounds, not source-game values or large-coordinate certification.

Four 180×140 cm windows use depths 100/160/220/280 cm. The shared 320×64 atlas contains five 64² gradient/checker faces; all 20,480 actual source texels are independently checked. It is numeric linear BGRA8, point/clamp, LOD0, no mips, uncompressed. Materials are single-sided Opaque/Unlit. Apertures use two triangles / one section; actual five-wall rooms use ten triangles / **five sections per room**. Shared facade: 21 rectangles / 42 triangles. The actual-geometry reference is collisionless and does not verify entry, physics or navigation.

Eighteen cases cover 12 normal camera/transform/mirror/depth cases and six wrong/invalid/synthetic epsilon controls. Actual moving/stable audits use 5×5 points including .01/.99 borders. Independent calculations bind native mesh, UV, winding, sections, parameters, camera/projection, visibility and capture lists to pixel-center rays and source texels. Pixel rounding can move an intended window point onto the facade: 161 final pairs were classified accordingly. Maximum RGB error .006832682 remains below the unchanged .008 bound. Linear HDR numerical evidence differs from tone-mapped screenshots. Synthetic camera uniforms test near-zero XY and near-parallel Z input/output, not physical views or GPU instruction counts.

Adoption checks learned here: use actual recorded camera axes within a justified native orientation bound; account for DX11 1/256-pixel vertex snapping and perspective UV at point-texel boundaries separately for each representation; reject handled runtime ensures even when pixels and exit code pass; initialize owned runtime mesh UV density metadata. The real failures, RED→GREEN regressions and final reruns are linked in the results. Initial black/equal captures were rejected and repaired with per-view component lists. One fresh review found missing edge/epsilon coverage, which was repaired without a repeated review. All final native consumers use the corrected v2 executable; older higher-FPS runs cannot certify it.

At 1280×720, four static windows, two seconds warmup and eight seconds measurement, whole-wall p95 ranges across three runs were: flat 10.406–10.745 ms; mapping 10.517–10.890 ms; actual geometry 10.493–10.562 ms. Measurement excludes captures, readback, mesh builds, transforms, MID updates and final save/exit; HUD/scalar arrays remain included. Setup and GPU calibration precede warmup. Whole wall/cadence and delayed whole-GPU counters are distinct from isolated shader cost. Ranges overlap; the five-section geometry baseline is unoptimized, host scheduling was uncontrolled, and four windows do not establish a universal speedup or city budget. Moving-camera MID update cost was not isolated.

Choose mapping for inaccessible decorative planar windows needing box-like parallax; choose flat textures if parallax adds no value; construct real spatial content for entry, collision, navigation, furniture or close interaction. Lighting, glass, reflections, filtering/mips, curved facades, negative geometry scale, arbitrary building corners, streaming and large coverage need separate validation. Recheck actual assets, view angles, lifecycle and frame tails. No renderer/framework expansion or publication occurred.

Source: [Joost van Dongen's 2018 author article](https://joostdevblog.blogspot.com/2018/09/interior-mapping-real-rooms-without.html), checked 2026-11-12, supports ray/plane/UV mechanics and regular-box/furniture limits. Today's direct 2008 PDF fetch timed out; its historical 2026-11-07 check remains separate. Old float4 optimization and UE4 function availability were not assumed for UE5.8. Installed engine APIs plus actual builds establish this authored path.
