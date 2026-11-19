---
id: K-GAME-TECH-NORMAL
title: Add lighting detail without changing surface topology
summary: Use compatible linear normal textures and tangent handedness for lighting
  detail;scoped UE5.8.3 plane/curve/UV-seam/compression/mip evidence retains geometry
  and fixed collision proxies,with whole-frame GPU/CPU cost limits.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["normal", "map", "tangent", "노멀맵", "tangent-space normal map", "normal map convention", "mirrored UV", "tangent handedness", "green channel", "linear texture", "sRGB", "BC5", "compression", "mip", "normal seam", "탄젠트 부호", "UV 이음새", "초록 채널", "밉", "실루엣", "충돌 유지"]
status: active
checked_at: '2026-11-12'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 V26:33model,20native scenes,320GPUprobes/8seampairs,6cost
    players,1xmedia;fixedboxcollision only,no displacement/skinning/arbitraryseams
---
# Add lighting detail without changing surface topology

## Guidance

Use normal textures when the lighting needs finer surface detail than the mesh. Decode stored vectors in the expected space, transform through a compatible tangent basis, and normalize before lighting. Keep the normal-map convention consistent across baking, import and rendering.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### tangent-space normal map

In a tangent-space normal map, the texture encodes directions relative to the mesh surface. A normal map convention includes the sign of the tangent-space Y direction. Godot expects OpenGL-style normals. Check a known raised feature under a moving light before changing mesh geometry or lighting.

## Applicability and exceptions

Ordinary normal mapping does not change silhouette, collision or actual surface height. A normal map on a 2D sprite needs a lighting pipeline that uses it.

## Checks

Scoped native rotation/mirrored-island seam/compression/forced-mip evidence appears below;production bake/skinning/arbitrary UV/automatic mip behavior remains unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) — Official stable documentation; normal map, transparency and billboard sections; rolling version. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V26 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native normal mapping — 2026-11-12

The historical Unreal run addUE5.8.3 Win64 Development/DX11 plane/curvedpatch materials,33model checks,10scenes each in actualPIE/package,160broad+160fine nativeGPU probes/8seam pairs,3matched flat/normal cost repeats and actual normal1x media. Latest15limited local sheets/28without direct prototypes;not complete subject certification.

Adopt for lighting detail finer than geometry when silhouette/height/contact can remain unchanged. Two400cm surfaces,total612vertices/1024triangles,retain exact source positions/indices across normal variants and same-pose topdown depth-coverage masks. Actual oblique screenshots give a second view. Fixed200×200×10cm box proxies retain center trace hits atz0;they do NOT establish curved-surface collision accuracy. Normal mapping changes shading normals,not mesh topology/displacement. Geometry/contact/occlusion changes require separately verified systems.

Source/export/import convention andbake/runtime tangent basis must agree. Linear128²authored8bitRGB,8SimpleAverage mips,clamp/bilinear/NeverStream;TC_Normalmap actuallyPF_BC5(23),rawTC_VectorDisplacementmap actuallyPF_B8G8R8A8(2). BC5normal sampler reconstructsZ;rawlinear sampler decodes2RGB−1;both normalize before tangent-space Normal input.3single-sided opaque DefaultLit materials sharebasecolor.35/roughness.8. No displacement/WPO/parallax. [Epic4.27 texture properties](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-properties?application_version=4.27) supports linear normal directions/mips/green convention;[compression](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-compression-settings?application_version=4.27) documents formats. Both checked2026-11-12 as historical concepts;actual5.8.3settings/formats/output verified natively,not inferred from rollingdocs.5.8webpages inaccessible/empty;installed shader/API source used.

Right UV island is mirrored across a joined duplicate-vertex boundary:reverseT AND handedness soB stays consistent. Retain actual nativeT/N/B/UV/allindices;the same basis can be right while texture-edge content is discontinuous. Authored centralnormalX=0 band gives a defined seam target. Actual correct seam max0.007818222vector(<.02);wrong right-island sign max0.604054504(>.4).8bitzero encodes128/255,so smallX sign differences can remain. Wronggreen is an expected failure for THIS authored source convention,not a universal DirectX/OpenGL filename rule. Unsupported negative/nonuniform scale,skinning/importer-MikkTSpace bake parity and arbitrary seams remain unverified.

10native scenes:flat,BC5mip0,objectyaw90,lightreversal,correct mirroredseam,wrongrightsign,wronggreen,rawmip0,mip3,mip7. Signed actual GBuffer WorldNormal512×256FloatRGBA is independently checked within.04vector,including quantized source/BC5/filter/GBuffer/half-float/nativebasis/pixel footprint. Installed SceneCapturePixelShader outputs alpha0;use separate scene depth for coverage,not alpha. Bind each checked worldpoint to its independently projected pixel. Broad probes use known quadrant vectors;fine probes derive8bit source→independentbox mip averages→bilinear samples→normal decode. Mip3 can blend across quadrant boundaries;unmipped expectations are wrong nearthose footprints. Fine-stripe variation disappears undercoarse forced mips andmip7 averages symmetric source to near-flat. Raw/BC5 agreement is scoped to this pattern. Production automaticdistance mips,anisotropic/specular temporal artifacts andstreaming are separate.

ONE fresh read-only review found3Important gaps:whole-object UVmirroring lacked joined-seam proof;finalcomparison intent/artifact set could be substituted;pixelcoordinates/nonfiniteGPU could be misbound orhidden.6new sensitivity tests failed before repair,then31evidence tests passed. Added split-island actual pairedGPU probes,session→profile/mode/consumer/fps/capture binding/exactartifact set,independent projection andfinite nonnegativeGPU validation. Zero remains valid unavailable. Initial camera-axis clipping andmip3oracle failures retained/corrected without relaxing.04normal tolerance. ActualcameraLEFTcurved/RIGHTplane label fixed. These are bounded featurechecks,not a generic validation-framework improvement or global enforcement.

|Player|CPUwall p95 ms|Cadence p95 ms|RHI wholeGPU p95 ms|
|---|---:|---:|---:|
|perf-flat-1|1.843|1.876|1.671|
|perf-normal-1|1.827|1.855|1.645|
|perf-flat-2|1.840|1.870|1.647|
|perf-normal-2|1.875|1.908|1.797|
|perf-flat-3|1.845|1.872|1.648|
|perf-normal-3|1.837|1.866|1.647|

Cost:6sequential packagedplayers,1280×720,same2meshes/camera/light/basecolor/roughness,flat(no normal sample) versusBC5mip0,2s staticwarmup+8s measurement,3rotatedpairs. No capture/pixelread/nativebuffer audit/transform updates in cost. Whole CPUwall/cadence differ from delayed RHIGetGPUFrameCycles observations;the latter is wholeGPUframe including possibleplatformbubbles,same-CPUframe pairing andisolatedsampler attribution are unverified. Nonfinite/negativeGPU rejects;zero remains unavailable. Overlapping repeatedtimes in a small staticwindow do not mean zero normalmapping cost or universal savings. Hostload uncontrolled;noGPU-pass attribution,cap tuning,renderer/Present/profiler improvement orproduction extrapolation. See report for fulltails/counts/positiveGPUcoverage.

InheritedNoise57,legacy actualPIE73/package73,41finalassets(36old+5new),20oldsource archives and frozenSource/Config/project/binaries/5containers/launcher are checked separately. Retrieval158cases testslookup,not engine behavior. Native source/rawruns/assets/media remain local evidence and were excluded from prior knowledge-only publication;no new commit/push in this task.
