---
id: K-GAME-TECH-FOLIAGE
title: Budget dense vegetation across geometry and pixel cost
summary: Use shared crossed masked cards and instancing for repeated grass, while
  measuring pixel coverage separately. Scoped UE5.8.3 tests compare individual/ISM
  with matched effective centre-distance culling; native bounds reference differs,
  and instancing does not remove all shading work.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["foliage", "grass", "LOD", "culling", "instancing", "잔디", "인스턴싱", "컬링", "오버드로", "최적화", "Static Mesh Foliage", "hardware instancing", "overdraw", "masked grass", "alpha holes", "two sided", "instance placement", "sphere edge", "centre cutoff", "reentry", "ISM", "잔디 배치", "거리 컬링", "재진입", "알파 구멍", "양면"]
status: active
checked_at: '2026-11-13'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 V19:37policy/47evidence/4actualPIE+4packaged8cases/12costplayers/normal1xmedia;small
    static Unlit masked patch,noLOD/wind/Nanite/forest
---
# Budget dense vegetation across geometry and pixel cost

## Guidance

Use crossed alpha-tested cards or meshes according to silhouette importance. Cull outside useful visibility, reduce distant detail, batch compatible instances, and animate vertices with spatially coherent wind. Keep draw submission, vertex cost, overdraw and shadow cost as separate budgets.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### Static Mesh Foliage

Unreal's Static Mesh Foliage uses hardware instancing to submit repeated meshes in batches. Overdraw is a different cost: overlapping foliage cards can shade the same screen region repeatedly. Vary card coverage at fixed instance count and inspect GPU time separately from draw submissions.

## Applicability and exceptions

Instancing reduces submission overhead, not all shading work. Cards can cost more pixels than denser opaque geometry. These historical sources do not certify Nanite foliage behavior.

## Checks

Actual static patch instancing/culling,alpha-hole/two-sided/boundary/reentry evidence appears below. Wind/shadows/LOD and isolated overdraw pass costs remain unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Epic, Foliage Mode](https://dev.epicgames.com/documentation/unreal-engine/foliage-mode-in-unreal-engine?lang=en-US) — terminology and applicability of Static Mesh Foliage, hardware instancing, overdraw. This is source evidence. The suggested target checks remain to be run.

- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass) — GPU Gems ch.7; crossed quads and animation. Checked 2026-11-07, except items explicitly marked further reading.
- [Tiago Sousa — Vegetation Procedural Animation and Shading in Crysis](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis) — GPU Gems 3 ch.16; wind animation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V19 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native instancing and culling evidence — 2026-11-13

The historical Unreal run adds scoped UE5.8.3 Win64 Development/DX11: 37 native policy checks, 47 evidence tests, four actual PIE and four packaged behavior worlds, twelve matched cost players and normal1x native media. Latest coverage is 20 limited sheets /23 without direct prototypes. This verifies a small static diagnostic patch, not a whole foliage system; previous missed FPS bands remain unverified.

Use one shared mesh/material for repeated static grass clumps and compare component/submission overhead separately from masked screen coverage. Here one clump is two perpendicular vertical cards (8 vertices /4 triangles), oneLOD/nonNanite, collision/shadows off, local64×96cm bounds centred at0. Actual instance originZ48 puts the base at0. Behavior uses16 clumps, cost1024, with deterministic positions/yaw. Every actual component or ISM instance matrix and shared mesh/material binding is independently checked. Two owned assets hold a linear64×64BGRA8 point/clamp/noMip numeric blade mask and Masked/Unlit/TwoSided material with ISM support; all4096source texels and1344opaque texels match independent values. No realistic lighting/art quality claim.

Do not assume equal numeric cull distances imply equal visible coverage. Installed5.8 default CPU primitive distance uses its bounding sphere edge (r.DistanceCullToSphereEdge=1); instance draw-distance uses its centre. Keep renderer settings unchanged and map the authored1000cm centre cutoff to individual max=1000−actual bounds radius and ISMend1000. The crossed-card vertex sphere radius is57.6888204cm (sqrt(32²+48²)), not the AABB-corner radius. Record actual component bounds/cached limits and effective scalability;rederive after mesh bounds,scale or engine changes. Exact equality1000 is visible under the checked float predicates;1001/1300 disappear and999 reappears using the SAME live component/instance. Hard culling can pop;fade/LOD behavior is outside this result.

Correctness combines native geometry/material/UV/section/metadata/placement/cull settings/capture membership with actual linear-HDR pixels. Independent projection,D3D11eight-fractional-bit raster snapping,perspectiveUV and point-alpha sampling determine expected depth/colour. Front/back patches contain observed pixels from both winding orientations;single-clump blade/hole probes distinguish cutout from opaque cards. Four arms ×eight cases in actualPIE and packaged worlds match;maximumRGBerror0.000484452 stays below the unchanged.008 bound. Display screenshots are tone-mapped1280×720, not the numeric640×512 observer. Expected1024OFF/182ON centre-distance survivors are not GPU-visible counts:frustum and occlusion also apply. Sparse cost probes complement full placement/settings and behavior evidence;they do not prove every hidden instance's pixels.

Matched cost:three sequential packaged runs perarm (individual/ISM ×cullingOFF/ON),same1024placements/mesh/material/camera/config/executable,1280×720,2s warmup+8s measurement. Only the chosen representation is allocated;1024components versus1ISM is the intended representation difference. Setup/registration/GPU calibration,observer readback,finalsave/exit are outside measurement;HUD/scalar arrays remain included. Per-frame declared build/read deltas are zero, with no measured camera/placement/cull updates. Default dynamic batching stays enabled,not forced off for a favorable result. individual-off: whole wall p95 9.984–10.222 ms; whole-RHI draw medians [865, 865, 865]. ism-off: whole wall p95 9.390–9.666 ms; whole-RHI draw medians [27, 27, 27]. individual-on: whole wall p95 9.546–9.942 ms; whole-RHI draw medians [149, 149, 149]. ism-on: whole wall p95 9.621–9.737 ms; whole-RHI draw medians [27, 27, 27]. Whole wall/cadence,delayed wholeGPU and whole-RHI draw samples are distinct from isolated foliage passes or pairedCPU/GPUframes. Host load is uncontrolled;no universal speedup/production budget or isolated alpha-overdraw claim. Setup/memory/update costs were not separately benchmarked.

One fresh review exposed unvalidated recorded cvars and execution environment. Five negative cases first failed, then the checker required all four unchanged renderer/scalability values,consumer/mode/required arguments,actual5.8.3/D3D11 log and the final matrix. Required artifact hashes reject missing or substituted data. No renderer settings or general verification framework changed. First package compilation also caught editor-only NaniteSettings access:guard the assignment and inspect actual runtime HasValidNaniteData();both final builds and native runs pass. Failed GPU reads return failed audit evidence before array indexing. Details and scope are in the linked report.

Adopt when repeated static clumps make component/submission overhead significant, while validating actual masked density/view angles/GPU costs. This prototype excludes LOD,wind,Nanite,large forests/streaming,collision/interaction,lit shadows and renderer/tool improvements. Prefer a locally profiled content choice;instancing does not remove all pixel work. [Epic ISM documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/instanced-static-mesh-component-in-unreal-engine) supports grouping repeats;the rolling5.9 page is not a5.8LOD guarantee. Installed5.8 SceneVisibility/InstanceCulling and actual outputs establish this cull mapping. GPU Gems source mechanisms below are historical,not current hardware performance promises. No commit/push.

Measured adoption judgment: whole-RHI draw medians fell from865 individual/OFF and149 individual/ON to27 in both ISM arms. Whole-frame p95 gains were modest;adding culling to ISM did not establish a consistent additional gain in this small static scene. Use actual frame/GPU evidence,not only expected distance-survivor counts,when deciding to adopt culling.
