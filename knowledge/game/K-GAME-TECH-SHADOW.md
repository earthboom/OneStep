---
id: K-GAME-TECH-SHADOW
title: Choose shadow-map resolution and filtering
summary: Choose shadow-map coverage,resolution/filtering and bias from actual contact,self-shadow
  and camera-motion evidence. UE5.8.3 conventional CSM off/low/high bounded pixel/cost
  observations exist;high quality does not guarantee zero acne or shimmer.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["shadow", "map", "PCF", "CSM", "그림자", "cascaded shadow maps", "percentage-closer filtering", "bias", "contact gap", "self shadow", "cascade boundary", "camera registered", "shimmer", "바이어스", "자기 그림자", "캐스케이드", "떨림"]
status: active
checked_at: '2026-11-14'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V03 UE5.8.3:46policy/6PIE+packageworlds/9costs/native1x60s;conventional
    CSM/AAoff/one light,not VSM/Nanite/generalquality
---
# Choose shadow-map resolution and filtering

## Guidance

Use for moving lights or casters. Render light-space depth, then compare the receiver's light-space depth against it. CSM allocates directional-light coverage across camera-frustum intervals; PCF averages comparison results, not ordinary filtered depth. Tune split distances, receiver/caster bias, filter footprint and stabilization separately. Bake static lighting only when its assumptions remain valid.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### cascaded shadow maps

Cascaded shadow maps partition the camera frustum so directional shadows can use different texel densities over distance. Percentage-closer filtering averages the outcomes of depth comparisons. Inspect cascade transitions while moving the camera, then test filter softness at a fixed split arrangement.

## Applicability and exceptions

Acne, peter-panning, cascade seams and camera-motion shimmer are different failures. Historical Direct3D examples do not establish the best UE renderer configuration.

## Checks

Local bounded native checks below cover grazing/thin/contact/selfshadow/bias/cascade/camera-motion pixels and whole-frame costs. Isolated shadow-pass GPU/memory and production-art quality remain unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Microsoft — Cascaded Shadow Maps](https://learn.microsoft.com/en-us/windows/win32/dxtecharts/cascaded-shadow-maps) — Technical article; frustum partitioning and stability sections. Checked 2026-11-07, except items explicitly marked further reading.
- [Bunnell & Pellacini — Shadow Map Antialiasing](https://developer.nvidia.com/gpugems/gpugems/part-ii-lighting-and-shadows/chapter-11-shadow-map-antialiasing) — GPU Gems ch.11; sections 11.1–11.2. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V03 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native Unreal validation — 2026-11-14

The the historical Unreal run and its archived measurements.

UE5.8.3 Win64 Development/DX11 native conventional shadow maps/CSM. One movable directional light,existing engine Lit material/cubes,a same-component two-box procedural shelf/roof,contact/floating/thin/ramp fixtures and slow camera traversal. No new content assets,dependencies,Config/project or engine renderer changes. Runtime-owned settings disable Virtual Shadow Maps,Nanite,ray-traced/distance-field/contact shadows and AA,then restore captured integer CVar values on EndPlay without SaveConfig. Deferred minor:preexisting fractional DistanceScale/TransitionScale values and original CVar priority are not preserved;these runs use dedicated subprocesses and default integer-valued scales. Reuse in a persistent editor needs that restoration repaired. OFF disables this light's casting while keeping illumination. LOW uses2cascades/maxCSMresolution512/filterquality3;HIGH4cascades/max2048/filterquality5. These are configured caps,not measured texture allocations. Both cover6000cm with exponent1,transition.1,distancefade.1,bias.5/slope.5. Multiple settings change together:compare complete tiers,not isolated parameter causality.

46native geometry/tier checks pass after retained46/42RED. Six actual worlds (PIE/package×off/low/high) verify actual main-view light/camera/caster/CVar states. Actual native PNGs bind serial markers to recorded views. Independent ray/AABB visibility,shadow projection and same-shelf self-shadow samples check position,direction(yaw0/90),ground contact and a100cmfloat. Static pixel interior classification excludes an8cm boundary band;off footage is the illumination reference. It checks pixels,not only cast-shadow flags. Bias0,normal.5,excessive5 and grazing10degrees/zerobias are intentional diagnostic cases. Their artifacts are measured outcomes,not requirements that every bad setting look correct. No shadow/low/high metadata substitutions,wrongcamera/light/bias/caster,fakewallFPS and off-as-on pixels pass the evidence tests;each negative fixture first accepts its unchanged baseline.

Nine sequential players rotate off/low/high,low/high/off,high/off/low. Same20s scene/light/geometry/camera input trace,1280x720,DX11,Development,cap0/noVSync;measure[2,18)s. No pixel readback or movie capture in cost runs. Actor CPU covers scripted light/camera/caster publication,not rendering. Whole begin/end wall and start/start cadence include native engine/HUD/view/CVar observation/JSON bookkeeping;GPU is delayed whole-frame RHI timing. Startup/result save/exit and media encoding are outside the window. Three short uncontrolled runs do not establish a hardware-general winner;maximum values and all samples remain in summary. Configured map-resolution caps are not measured VRAM. No isolated shadow-passGPU or memory claim.

Use a controlled shadow-OFF illumination baseline to distinguish shadow location from dark material/unlit faces. Keep position/contact,self-shadow acne,excessive-bias separation,internal cascade transitions,outer distance fade and camera-motion variation separate. Choose bias from actual geometry/light angle/resolution:zero can acne and excessive values detach contacts. High resolution is not a blanket no-shimmer/no-acne guarantee. Temporal rows sample fixed world coordinates in matching OFF/LOW/HIGH native footage,so camera displacement is removed;remaining edge variation includes CSM plus screen sampling/quantization and is not attributed solely to CSM. Uniform split locations are derived from the installed DirectionalLightComponent.cpp GetSplitDistance,near+(6000-near)*i/count;overlap/fade are distinct. The shadow-renderer texture/pass internals are not instrumented. No VSM/Nanite/raytracing/outdoor-scale/engine/framework expansion. White opaque fixed fixtures,AAoff and one light do not certify foliage alpha,animated skinning,multiple lights,Lumen or production art. World geometry is non-colliding visual calibration;this is not a gameplay collision test.

Latest28limited sheets/15without dedicated prototypes.

Temporal precision:edge scan spacing is5cm;contact scan spacing is1cm and image pixel footprint still limits spatial accuracy. No-dark-edge means the ON/OFF ratio did not cross.5 in the scanned strip;weak filtered shadows,outsidecoverage and actual dropout are not distinguished by that count alone. Missing/offscreen samples remain null. Final steady-window metrics exclude the first.25s after light reset/view jump while retaining those frames in raw traces/video.

Preservation count clarification:33prior manifested Source archives plus one legacy traffic-acceptance snapshot folder make34directories. All7114files across those directories are hashed and preserved. The original preservation snapshot counted directories,not manifests;the final gate checks both counts independently.
