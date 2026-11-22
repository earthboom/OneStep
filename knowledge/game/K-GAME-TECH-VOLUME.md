---
id: K-GAME-TECH-VOLUME
title: Separate volumetric appearance from simulated smoke gameplay
summary: Use world-space extinction for environmental volumes and independent density queries for gameplay visibility.
  UE5.8.3 V10 covers door-gated density transfer, dissipation, exact grid boundaries and HUD-independent
  visibility. V27 covers a native cloud layer and view sample cost.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["volumetric", "smoke", "clouds", "Worley", "연막", "구름", "경계누출", "잔상", "Volumetric Fog", "temporal reprojection", "Volumetric Scattering Intensity", "volumetric fog", "density", "anisotropy", "volumetric shadow", "camera cut", "light trail", "reactivation", "볼류메트릭 안개", "광원 잔상", "밀도", "광산란", "V27", "Volumetric Cloud", "cloud fly-through", "cloud layer", "coverage", "parallax", "view sample count", "볼류메트릭 구름", "구름층 통과", "시차", "V10", "gameplay smoke", "density grid", "optical depth", "door transfer", "grid traversal", "smoke dissipation", "시야 판정", "밀도 격자", "연막 소멸", "표시 독립성", "격자 경계", "밀도 임계값"]
status: active
checked_at: '2026-11-22'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 V10 fixed-grid gameplay smoke with native solids and independent visibility,
    and V27 single-layer native clouds. See each for the measured fixture and scope.
---
# Separate volumetric appearance from simulated smoke gameplay

## Guidance

Render participating media using a density field with scattering/extinction; use noise to shape clouds or smoke, then sample light and transmittance. Low-resolution evaluation with temporal reconstruction is a quality/performance tradeoff. For competitive smoke, share authoritative density/visibility rules rather than relying on each client's final image.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Valve's 2023 CS2 patch notes explicitly mention smoke-volume expansion near walls, changes to the stepping function on AMD hardware, and shotgun-created holes. These support an evolving spatial smoke volume, not a published complete solver. Implementation synthesis: separate authoritative smoke occupancy and temporary bullet/grenade perturbations from per-view lighting, then render the shared state with platform-appropriate sampling. Geometry intersection and reconstruction must preserve gameplay visibility across quality levels.

### Volumetric Fog

Unreal's Volumetric Fog uses temporal reprojection to reuse fog samples across frames. Rapidly changing lights can leave trails. Compare moving and static lights, then vary the light's `Volumetric Scattering Intensity` to isolate its contribution to fog from its lighting of opaque surfaces.

### One native cloud layer

When the camera can fly through a cloud or see nearby and far clouds shift by different amounts, use a world-space density field inside a native `UVolumetricCloudComponent` layer. Drive extinction with independent density and coverage parameters. Use a vertical profile to taper extinction to zero at both boundaries. A sky-only view at the same camera pose is a useful baseline for isolating cloud pixels. [Epic — UVolumetricCloudComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UVolumetricCloudComponent?application_version=5.8)

Keep the trace distances, shadow sample scale, atmosphere, material, resolution and camera path fixed when comparing view sample scales. The view-ray sample ceiling limits the renderer's budget. Distance-based sampling and transmittance-based early termination can reduce the work on individual rays. Compare stills and fly-throughs together, then choose a sample setting against the target scene's frame and GPU budgets. [Epic — Volumetric Cloud Component Properties](https://dev.epicgames.com/documentation/unreal-engine/volumetric-cloud-component-properties-in-unreal-engine)

## Applicability and exceptions

Valve's dated patch notes confirm smoke-volume behavior; its complete density solver, replication and ray-marching code remain undisclosed. Volumetric appearance is distinct from fluid simulation and equal competitive visibility still needs target-game tests.

## Checks

Proposed: test moving lights, camera cuts, inside-volume views, depth edges and visibility agreement under different quality settings.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Epic — Volumetric Fog](https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine) — Density, scattering, temporal reprojection and performance sections. Checked 2026-11-07, except items explicitly marked further reading.
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf) — 2016 author chapter; terrain and multi-scale noise. Checked 2026-11-07, except items explicitly marked further reading.
- [u/smilefr — Optimized volumetric clouds](https://www.reddit.com/r/Unity3D/comments/1u8g138/i_finally_have_optimzied_volumetric_clouds/) — Original implementation account; quarter-resolution compute rendering and depth-edge upsample. Self-reported, no benchmark reproduced. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V10, V27 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

### Follow-up evidence

- [Valve — Counter-Strike 2 June 2023 update notes](https://store.steampowered.com/news/posts/?appids=730&enddate=1689630041&feed=steam_announce%2F1000) — Official dated notes, VOLUMETRIC SMOKE sections; source code and cross-client determinism not disclosed. Checked 2026-11-07.

## Native Unreal fog validation — 2026-11-17

The historical Unreal run,[probe incident](../../records/code/R-CODE-UE-FOG-PROBES.md),archived measurements.

UE5.8.3 Win64 Development/DX11,1280x720. One native ExponentialHeightFog component,one movable spot light,11prebuilt unlit boxes including an occluder and4white/black depth pairs. Existing62assets/project/Config/dependencies/renderer/shared tools unchanged. LOW gridPixelSize16/Z64,HIGH8/Z128;shadow quality5,maxshadowresolution1024,conventional shadows andAAoff are fixed across arms. These are grid controls,not measured GPU memory allocations. OFF hides the entire fog and disables volumetric fog while receiving the same authored parameter/light/camera requests. Default temporal reprojection remains ON with historyweight.9/historymiss4samples;the extra HIGH no-history movie is a diagnostic control,not a performance arm. Runtime CVar values are restored after EndPlay and exact9value restoration is checked in actual PIE. Dedicated single-owner fixture;CVar priority flags and simultaneous differently configured worlds are not certified.

24s/12two-second phases:zero density,base.012,max.05,g=.7,volumetricshadowOFF,shadowON,lateral camera sweep,camera cut,lightOFF,lightON,fogOFF,fogON. Actual extinction10,heightfalloff.2,fogcomponentheight200cm,viewdistance5000cm,spotposition(0,1500,260),intensity500000,inner/outer20/35degrees. Policy ranges density[0,.05],g[-.9,.9],extinction[0,10]reject invalid/nonfinite values atomically;these are owned policy bounds,not a claim the raw engine setters enforce them. Rendered scene exercises density0/.012/.05 andg0/.7 at extinction10. Actual native views,applied settings,scene transforms,opaque-depth probe visibility and main-view pixels are checked.4depth pairs atx±400,y-300/200/700/1200,z220 avoid near-probe occlusion. Six actual PIE/package worlds,9costs and4movies retain identical phase requests;wall times/trajectories are sampled on their actual frames rather than asserted bit-identical. Real FSceneView.bCameraCut is required at the authored cut;OFF movie target-color/projection checks corroborate actual moving/cut camera geometry.

Nine sequential packaged players rotate OFF/LOW/HIGH,LOW/HIGH/OFF,HIGH/OFF/LOW. Same24s script,camera,scene,light,density and shadow settings;cap0/noVSync,no fixed step,ReadPixels or movie capture in costs. Steady[2,24)s includes all active/interruption phases. OnBeginFrame/OnEndFrame wall andbegin-to-begin cadence include engine work and waits;wholeGPU timer is delayed and is not an isolated fog pass or a synchronized per-phase GPU measurement. Observer/HUD/JSON work is included;startup,precreation,final serialization/exit andPNG/video work excluded. All positive GPU samples are retained. Host load is uncontrolled and three repeats show variation;do not infer that HIGH is faster from a lower whole-frame percentile or subtract percentiles to claim isolated fog cost.

Normal1x movie clock is30simulation/30playback,not proof of actual30FPS rendering. Transition residual is sampled every4pixels in the fixed scene ROI against the last12frames median of the new state,normalized by the before/after median difference. Settling requires3consecutiveframes at<=10%;otherwise the result is censored within the two-second phase. Native PNG and decoded MP4 results are both retained. Camera motion/cut compares HIGH with the same-source no-history control in an edge band derived from actual OFF geometry. No-history has jitter/sampling noise and is not physical ground truth;differences must not all be called ghosts or fog leakage. LOW/HIGH image differences are relative comparisons,not an artifact-free reference.

The first intentionally hidden-fog stub passed native flags but the pixel gate correctly rejected it(.1046/255mean change). Visible initial extinction1 produced only.6043/255base-density change and the old slanted depth-probe layout hid far targets behind nearer cubes. A ray/AABB first-hit test failed. Preserve these preliminary players and exact source snapshots;they are not final performance evidence. The fixture was changed to extinction10 andx±400 probe columns;the latter passes independent first-hit checks. Both fixture changes were made before the final freeze,so the combined visual change is not an extinction-only causal A/B. No engine defect or renderer optimization is claimed.

Use for bounded environmental fog/mist and lighting appearance. A shadowing wall attenuates the light contribution;it does not remove global fog density or provide authoritative gameplay visibility. No CS2-style smoke occupancy,cloud generation,fluid,network orrenderer/framework optimization. Fixed one spot/opaque unlit boxes/one machine/24s;no transparent-material,large outdoor,arbitrary light count or hardware-general budget guarantee. ViewDistance is a volume evaluation setting,not a tested hard gameplay cutoff;this test covers target depth/silhouette/screen boundaries,not complete far-fallback matching. Actual rendering is measured only for the stated density/g values. CVar values are restored,but production multiworld integration needs separate ownership. User visual-quality review/acceptance remains pending.

[Epic Volumetric Fog](https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine),checked2026-11-17,currentpage5.9:general density/scattering/grid/history behavior only;not a pinned5.8API proof. Installed5.8.3ExponentialHeightFogComponent/VolumetricFog.cpp/usf were checked for local setters,grid/history/cut rejection and density*extinction. External performance examples are not our measured budget. Original source research and CS2claims remain separately dated2026-11-07. Latest30limited sheets/13without dedicated prototypes;not all originating shorts certified.

## Native Unreal V27 cloud validation

Use a tileable world-space noise field, independent density and coverage controls, and extinction taper at the upper and lower bounds. Check a zero-density control and a matched sky-only frame. Move the camera below, through and above the layer. Compare displacement at different depths, check opaque foreground occlusion and account for sky changes when comparing sun directions.

Hold material, trace distances and shadow sampling constant when tuning the view sample scale. The ceiling constrains the sample budget, with actual sampling affected by distance and early termination. Inspect grain in dense and inside-volume views and measure frame and GPU cost on target hardware. This guidance covers a bounded native cloud layer and opaque foreground occlusion. [Epic — UVolumetricCloudComponent, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UVolumetricCloudComponent?application_version=5.8)

## Native Unreal V10 gameplay smoke visibility

Use a fixed-step density field. Permit transfer across shared doorway faces while open and stop transfer on closure. Preserve density that already crossed the door so it can dissipate. Verify agreement between native collision geometry and the grid transfer boundaries. Check solids first and record wall and smoke occlusion as distinct outcomes.

Integrate density times path length on a geometry-clear ray. Use one half-open cell convention, step every axis tied at a boundary and give point touches zero length. Specify the optical-depth threshold's inclusion rule. Compare against an independent plane-intersection calculation for zero density, threshold neighbors, reversed segments, and face and corner contacts. [Amanatides and Woo — A Fast Voxel Traversal Algorithm](https://www.eecs.yorku.ca/~amana/research/grid.pdf)

Keep display reads separate from density writes and compare the same field snapshot and ray with shading enabled and hidden. Measure updates and queries separately. When scaling, consider both the grid size and how many unblocked rays actually traverse the grid, including their path lengths.
