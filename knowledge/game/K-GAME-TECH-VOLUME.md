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

On November 22, 2026, one cooked cloud layer at 0.60–1.35 km was verified in UE 5.8.3 Win64 Development, DX11, 1280×720, on an RTX 3080. The fixture used a deterministic tileable 32³ noise asset, two cloud concentrations at different depths, Sky Atmosphere, one directional sun and an opaque board. The material attenuates extinction near the layer bounds. The renderer's budget was set using view sample count scales of 0.25 and 1.0, with 24 and 96 sample ceilings at the configured cap of 128. Shadow sampling and tracing distances were fixed. The installed 5.8.3 renderer was checked for the cap formula. [Epic — UVolumetricCloudComponent, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UVolumetricCloudComponent?application_version=5.8)

Using matched views with the HUD excluded, density zero changed 0 pixels versus off at an RGB-channel threshold of more than 10/255. Raising coverage from 0.22 to 0.91 increased changed pixels from 197,664 to 371,835. The center horizontal band at 0.40, 0.95 and 1.58 km yielded 0, 21,703 and 0 changed pixels. The continuous climb from 0.40 to 1.60 km passed inside the near concentration and changed 763,623 of 768,000 pixels at the midpoint. A 150 m lateral move shifted the near and far mask centroids by 87.29 and 55.63 px. The opaque board reduced mean pixel change behind it from 37.92/255 to 0.037/255. Sun azimuth 32° versus 151° at fixed elevation changed sky-corrected display luma by a mean 26.54/255 in the cloud region. Native PNGs and a 19.60-second 1× movie cover these views. The authored capture clock and playback both use 30 FPS.

Three uncapped, no-VSync runs per setting used 64 warm-up and 600 measured frames on the same path and layout. The ranges below span each setting's three run p95 values. Whole frame is elapsed begin-to-end wall time. RHI GPU timing is delayed and measures the whole GPU frame. No GPU readings were unavailable. Capture and report export ran outside the measured interval.

| Setting | Whole frame p95 (ms) | Whole GPU p95 (ms) |
| --- | ---: | ---: |
| Off | 9.88–10.12 | 9.28–9.55 |
| Low, ceiling 24 | 9.82–10.41 | 9.52–9.72 |
| High, ceiling 96 | 10.03–10.41 | 9.51–9.74 |

Low showed more visible grain in the high-coverage view. The enabled profiles had overlapping cost ranges and switched GPU p95 ordering in one repeat. Use this result to choose what to test for a flight, close-up cloud or high-coverage sky. Measure inside-volume and dense-coverage views on the target hardware and resolution before choosing a budget. These results apply to one layer, one sun and one opaque occluder. They provide no isolated cloud-pass cost and no evidence for transparent occluders, camera-specific temporal reconstruction settings, weather or cloud shadows on world geometry.

## Native Unreal V10 gameplay smoke visibility

Use one density field and fixed step when game rules need stable smoke visibility. The UE 5.8.3 fixture uses an 18×12×4 grid of 50 cm cells at 30 Hz. A partition allows transfer across only the open doorway's shared faces. Native visibility traces handle solid walls and the door. Geometry-clear segments use a density-times-traversal-length integral. Define one half-open boundary convention and advance all axes tied at an edge or corner so a zero-length contact adds zero optical depth. Aggregate display effects consume the field through a read-only path. [Amanatides and Woo, A Fast Voxel Traversal Algorithm](https://www.eecs.yorku.ca/~amana/research/grid.pdf)

The closed door held the far side at zero density. Opening at tick 120 produced a far-side density sum of 0.849 on that tick. At tick 164 the through-door sightline had optical depth 186.660 and was smoke-blocked against a threshold of 75 density·cm. Reclosing at tick 180 immediately zeroed transfer and kept the existing far-side density (7.336 that tick). On reopening after the source stopped, the sightline passed at sampled tick 252 with depth 58.874, and the entire grid reached zero at tick 293. Native outcomes keep solid occlusion and smoke occlusion distinct. Exact test depths 74.99, 75.00 and 75.01 yielded clear, blocked and blocked. All 16 authored grid cases matched independent plane-intersection integration, including reversed, edge and corner paths.

The visible and hidden HUD runs matched exactly across six full-grid and individual-query snapshots and all 360 ticks' aggregate query and density totals. The visible grid and hidden grid produced measurably different pixels in the open-door probe, while the authoritative marker and status matched. A 14-second native 1× capture records the full cycle and matched hidden segment. The scene covers one applied source and one door. The coefficients, query threshold and measured bounds belong to this fixture.

At 1280×720 on an RTX 3080 and D3D11, three uncapped and uncaptured runs per arm processed 256 offered rays on each of 360 ticks. All runs had 92,160 offered queries and 52,560 wall blocks. Enabled runs each had 11,529 additional smoke blocks and 236,520 cell visits. Both profiles ran the same density and solid-occlusion work. The intervals are ranges of run medians for tick work and of the three run p95 values for whole frames.

| Gameplay smoke query | Density update (ms/tick) | 256-ray batch (ms/tick) | Whole-frame p95 (ms) |
| --- | ---: | ---: | ---: |
| Off | 0.0189–0.0197 | 0.1868–0.1898 | 8.5955–8.9877 |
| On | 0.0189–0.0190 | 0.2025–0.2044 | 8.0766–8.6708 |

The enabled arm added about 0.0140–0.0168 ms to each paired median batch. The whole-frame ranges overlapped. When scaling the technique, measure the number and lengths of geometry-clear rays along with the size of the density grid. Keep a solid-wall check, optical-depth threshold and visualization fidelity as separate concerns. For arbitrary walls, verify agreement between the grid's permitted transfer faces and native collision geometry.
