---
id: K-GAME-TECH-REFLECTION
title: Select reflections by visibility and update requirements
summary: For accurate flat mirrors with off-screen content, render a reflected camera
  and clip to the correct half-space while excluding the mirror. Scoped UE5.8.3 native
  ray/pixel checks and three matched OFF/ON costs verify one projected SceneCapture2D
  mirror; no recursive or production reflection certification.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["reflection", "SSR", "cubemap", "mirror", "거울", "Screen Space Reflections", "Planar Reflections", "planar reflection", "reflected camera", "clip plane", "half space", "self exclusion", "offscreen objects", "평면 반사", "거울 클리핑", "화면 밖", "자기 자신 제외"]
status: active
checked_at: '2026-11-13'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 V16:31policy/50evidence/actualPIE+packaged14cases/6costplayers/normal1xmedia;one
    rigid Unlit projected SceneCapture2D mirror only
---
# Select reflections by visibility and update requirements

## Guidance

For flat accurate mirrors, render a reflected camera view with clipping. For approximate surrounding light, use reflection probes/cubemaps; choose static capture or explicit update policy. SSR traces against available screen depth, so use fallback data for rays leaving the image. Combine methods by roughness, distance and importance.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### Screen Space Reflections

Screen Space Reflections use data visible in the current view, which can cause reflections to disappear at the edge of the screen. Planar Reflections render the scene from a reflected viewpoint for a plane. Move a reflected object out of the main view and compare completeness and GPU time at the chosen quality settings.

## Applicability and exceptions

A mirrored duplicate scene is one historical trick, not the definition of planar reflection. Cubemaps may be updated dynamically. SSR cannot recover unseen geometry.

## Checks

Actual bounded mirror cases and matched whole-frame costs appear below. Built-in actor, SSR/cubemap quality comparisons and isolated GPU pass cost remain unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Epic — Planar Reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/planar-reflections-in-unreal-engine) — Official documentation; SSR comparison and rendering cost. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V16 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native single-mirror evidence — 2026-11-13

The historical Unreal run verifies an authored projected SceneCapture2D mirror in UE5.8.3 Win64 Development/DX11. This is not a test of every built-in PlanarReflection actor property or a reproduction of a source game's shader. Native policy31, saved materials2, evidence tests50, actual PIE and packaged14cases plus setup calibration each, six matched cost players and normal1x media. Latest coverage:19 limited sheets /24 without direct prototypes. Prior Interior FPS gaps remain unverified.

Use a reflected camera and clip the capture to the mirror's front half-space. Reflect point C about base B/unit normal N as C−2N dot(C−B,N); reflect forward/up and rebuild a proper capture basis. Rebuilding reverses capture right relative to directly reflecting main right: project actual mirror world points into that basis instead of applying an arbitrary UV flip. A ShowOnly list containing actual scene components but excluding the mirror prevents self-capture in this one-mirror setup. Installed5.8 requires global clip plane support; both cost arms share this necessary feature setting, so its project-wide shader overhead is not isolated. No renderer/framework optimization.

Checks bind actual camera/projection, meshes/UVs/winding/sections/metadata, transforms, material parents/parameters/target and clip/component lists to independent observer-ray → mirror-point → sampled capture-texel-ray intersections. Projection binding permits only ±1e-10 pixel arithmetic uncertainty at an exact integer boundary; world points retain1e-6cm checks and every expected colour is derived from the actual sampled integer pixel centre. Nonboundary one-pixel substitutions still reject. No native executable or RGB limit changed for this real packaged regression. Stable audits cover camera views, rigid rotation/translation, near/grazing, back/on-plane/threshold rejection, a crossing-plane card and a clip-disabled fault control. Blue is wholly off the main front-view screen yet sampled in reflection. Yellow behind the plane is clipped normally and visible in the fault control. Clipping changes sampled parts of the crossing card. Actual component lists exclude mirror ID-1; black/missing/substituted evidence and incorrect clip/camera/mesh are rejected. Grazing main-view probes in this scene are black and do not certify coloured reflection at grazing. Max linear-HDR RGB error0.000390625 stays below.008; screenshots are separately tone mapped. Capture-call counters demonstrate OFF0 /ON1 per measured frame at actual call sites, not GPU-completion timestamps. Full evidence/sensitivity and review findings are in results.

Bounded scene: one800×500cm rigid mirror, three coloured cards plus behind-plane control, single-sided Unlit/Opaque mirror, two-sided Unlit solid objects, point-sampled640×512HDR target. Finite coordinates abs≤1e7, unit orthogonal basis/normal, front distance>.1cm. Invalid views disable sampling; culled back face can reveal ordinary scene objects rather than a black mirror. Mathematical front validity is separate from near-plane visibility (capture near1cm). Stable age≥.7s checks do not certify every moving-camera pixel. Negative/nonuniform mirror scale, arbitrary geometry/lighting and large coordinates remain unverified.

Matched cost:1280×720/static case0, same source/config/assets/executable,2s warmup+8s measure,three sequential packaged runs perarm in alternating order. off whole-wall p95 10.119–10.409 ms across three repeats; on whole-wall p95 10.737–11.319 ms across three repeats. ON performs a reflected capture each tick; OFF keeps the same allocations and disables capture/sampling. Observer readback/setup/meshbuild/pose/parameter updates/finalsave/exit are outside measurement; HUD/scalar arrays remain inside. Whole wall/cadence and delayed whole-RHI GPU are not isolated reflection-pass cost or pairedCPU/GPUframes. Host load is uncontrolled; these small-scene runs do not certify a production budget. Actual rates are reported, not inferred from a cap.

Choose this approach when accurate flat-mirror parallax/off-screen dynamic objects justify a second scene view. Revalidate real draw calls, triangles, materials, update frequency and screen coverage. Static cubemaps and SSR solve different visibility/update needs. No multiple/recursive mirrors, water, glass, roughness filtering, lighting/shadow fidelity, temporal effects, SSR/Lumen/raytracing comparison or renderer/tool optimization was validated.

Primary mechanism source: [Epic Planar Reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/planar-reflections-in-unreal-engine), rolling page checked2026-11-12(now5.9), for re-rendering/off-screen/cost distinctions. Installed UE5.8 SceneCaptureComponent2D/SceneCaptureRendering API checked2026-11-13 and actual native output establish this implementation; do not transfer version-specific5.9 behavior silently.
