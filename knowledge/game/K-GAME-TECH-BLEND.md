---
id: K-GAME-TECH-BLEND
title: Choose blend operations in the correct colour space
summary: Pair linear source representation with straight/premult/additive/modulate
  contracts;scoped UE5.8.3 native pixels validate HDR,alpha,edges,ordering and authored
  modulate fading,with whole-frame cost limits.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["alpha", "additive", "modulate", "blending", "블렌딩", "AlphaComposite", "premultiplied alpha", "Opacity Mask Clip Value", "straight alpha", "linear colour", "sRGB", "HDR", "double alpha", "transparent edge", "fade white", "blend order", "사전 곱셈", "이중 알파", "알파0", "곱셈 페이드"]
status: active
checked_at: '2026-11-12'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 V45:34model/120methodcases/630RGBprobes/12costplayers/1xmedia;unlit
    BeforeDOF only,no particles/general sorting/renderer optimization
---
# Choose blend operations in the correct colour space

## Guidance

Straight alpha: C=alpha*S+(1-alpha)*D. Additive commonly accumulates S over D; modulate multiplies them. Use linear-light calculations and distinguish premultiplied from straight-alpha assets. Masked materials discard pixels rather than continuously blending them.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### AlphaComposite

In Unreal's `AlphaComposite` mode the source RGB contribution is already weighted by alpha. Multiplying it again darkens translucent edges. For cutouts, `Opacity Mask Clip Value` sets the threshold for discarding fragments in Masked mode. Compare a partially transparent edge over both light and dark backgrounds, and test the threshold separately.

## Applicability and exceptions

Blend mode affects sorting, depth writes and supported lighting. Adding colour does not make effects readable on all backgrounds.

## Checks

Native scoped dark/bright/HDR,controlled overlap,source-edge andlinear-equation checks appear below;particle/general-sorting/production integration remains unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Epic — Material Blend Modes](https://dev.epicgames.com/documentation/en-us/unreal-engine/material-blend-modes-in-unreal-engine) — Official documentation; masked, translucent, additive and modulate modes. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V45 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native colour-blending evidence — 2026-11-12

The historical Unreal run adds scoped UE5.8.3 Win64 Development/DX11 straight alpha, premultiplied AlphaComposite, additive and fading modulate.34 final model checks;15 scenes×4 methods×2 actual PIE/package consumers=120 method-case observations,600 foreground and30 absolute background RGB probes;3 matched cost repeats per mode and actual normal1x media. Latest16 limited local sheets/27 without direct prototypes;not full subject certification.

Choose the source representation AND blend contract together. Straight uses aS+(1−a)D. AlphaComposite uses P+(1−a)D,with P already premultiplied in LINEAR light;scale both P and alpha for global fading. Wrong premult-as-straight double-multiplies coverage;straight-as-premult leaks RGB at alpha0. Additive here is D+aS:installed5.8 shader weights emissive by Opacity before hardware1+1. Raw modulate is D×S and ignores Opacity for RGB;to preserve the background at zero coverage,this authored material explicitly uses D×((1−a)+aS),fading toward white. Do not transfer that fade to raw Modulate as an automatic engine feature.

Use texture sRGB according to data meaning. This fixture's numeric-linear32² uncompressed BGRA8 source has RGBbytes204/51/102 and alpha stripes0/64/128/255;its paired premult source rounds linearRGB×alpha. A separate same-byte sRGB source is decoded before blending and leaves alpha linear. All use bilinear/clamp,no mips,NeverStream. Arbitrary premultiplied-sRGB baking/import,atlas padding/mips andother filters remain unverified. Premultiply in linear light rather than encoded colour space;check transparent edges using the actual asset/sampler/mode combination.

Native scenes cover dark/bright alpha0/.5/1,HDRalpha.5,A→B/B→A order,bilinear edges,three wrong-pipeline controls,sRGB andopaque foreground occlusion. Explicit z andSortPriority test controlled ordering,not automatic intersecting-geometry/particle sorting. Straight/premult depend on order;additive/modulate pairs commute within rounding in this same-mode fixture. Mixed-mode ordering is separate. Single-sided Unlit/BeforeDOF materials do not certify lit/fog/refraction paths.

Read actual SCS_SceneColorHDR512²FloatRGBA before tone mapping;absolute background values,including HDR2.4 retained near2.39844,verify linear scale independently. Final display screenshots are tone mapped and are not the arithmetic evidence. Reconstruct each source UV from the checked world→pixel projection and pixel CENTRE,then independently bilinear sample bytes/alpha,premult quantization,sRGB decode andordered equations. Nearby desired edge points can map to one pixel;no subpixel-resolution claim. Normal maximum channel error0.002343750(<.008declared quantization/filter/half-float bound). Wrong-pipeline controls must BOTH disagree with intended composition and agree with their independently computed actual wrong formula.

Native plane vertices/UVs/indices andactual material/scale/order are retained. Initial packaged EnginePlane CPU read crashed because cooked CPU buffers were not retained. Keep original exit3/log/fingerprint. A CPU-read contract failed1/34,then an authored4vertex/2triangle runtime quad withCPUaccess enabled passed34. Same100cmshape/UV;built once before warmup,no newasset orrendereroptimization. A native guard fails safely ifCPUaccess is absent. All finalconsumers/cost/media reran on rebuiltSource/binaries. Strict identity then caught five omitted unchanged Normal assets in the launcher inventory;complete53-asset records reran with unchangedSource/binaries/materials(finalbehaviorv3,cost/mediav2). Original incomplete records and identities retained. Existing21 sourcearchives/41assets unchanged;12ownedBlendassets added,total53. Initial copyrestoremtime cachedstub andorder-test uninitialized temporaries were corrected;deterministic policyRED28/33→GREEN33 preceded the laterCPUregression. These are local preparation findings,not a build-tool improvement.

31 independent evidence tests reject fabricated pixels/expectations,HDRclamp,gamma/order/premult/occlusion errors,missingedges/modes,projection/UV/material/scale substitutions,capture/launch/profile/artifact changes,copiedrepeats,missingcostsetup,missingCPUflag andnonfiniteGPU. Missingcostsetup detector first failed,then passed. ONE fresh read-only review found no Critical/Important findings before the later packagedCPU-read defect;that defect was independently reproduced/repaired afterward,no rereview. InheritedNormal33/coreactualPIE73/package73 run on finalfrozenartifacts. Lookup162 cases is distinct from runtime proof.

| Player | Whole CPUwall p95 ms | Cadence p95 ms | RHI wholeGPU p95 ms |
|---|---:|---:|---:|
| perf-straight-1-v2 | 1.952 | 1.981 | 1.725 |
| perf-premult-1-v2 | 1.945 | 1.976 | 1.733 |
| perf-additive-1-v2 | 1.961 | 1.999 | 1.811 |
| perf-modulate-1-v2 | 1.952 | 1.980 | 1.726 |
| perf-straight-2-v2 | 1.964 | 1.994 | 1.789 |
| perf-premult-2-v2 | 1.952 | 1.983 | 1.73 |
| perf-additive-2-v2 | 1.950 | 1.978 | 1.727 |
| perf-modulate-2-v2 | 1.949 | 1.979 | 1.731 |
| perf-straight-3-v2 | 1.953 | 1.985 | 1.747 |
| perf-premult-3-v2 | 1.959 | 1.994 | 1.753 |
| perf-additive-3-v2 | 1.937 | 1.966 | 1.724 |
| perf-modulate-3-v2 | 1.959 | 1.985 | 1.73 |

Cost:12 sequential packaged players,1280×720,samecamera/background and64 independent planes in4regions×16overlappinglayers,alpha.25,matching source strip/geometry/coverage/pass;ONEselectedmode per run. Actual64surface materialparent/blend,alpha/tint/transform/scale/order checked beforewarmup.2s staticwarmup+8smeasurement,three rotatedorders. No capture/readback/audit/transform updates in cost. Setup/runtimequad/materialbuild,warmup,finalsave/exit excluded;scalar arrays andHUD stay in fullframe. Whole CPUwall/cadence and delayed RHIGetGPUFrameCycles observations are distinct;GPUvalues are not isolated blend-pass/sampler costs orsameCPUframe pairing andmay repeat reportedresults/includeplatformbubbles. Nonfinite/negative fails;zero unavailable. Hostload/window scheduling uncontrolled;compare allranges/tails,not universal savings. This is not64full-screen layers,a particle system orproductionbudget. No renderer/sorting/Present/profiler/framework expansion.

Adopt additive after checking bright backgrounds/HDR display readability;linear correctness alone does not make it visible. Adopt premult when preparation/filter/composition agree,not as a fix for every sorting problem. Use explicit order/depth policies for the actual game. Native source/rawruns/assets/media remain local evidence excluded from prior knowledge-only publication;no commit/push for this task.

Sources:[Epic Material Blend Modes](https://dev.epicgames.com/documentation/en-us/unreal-engine/material-blend-modes-in-unreal-engine),checked2026-11-12,rollingpage returned5.9. Mode concepts support the reference;installed5.8.3TranslucentRendering.cpp/BasePassPixelShader.usf/SceneCapturePixelShader.usf andactualruns establish this path. Broad lighting claims in rollingdocs are not transferred to other modern rendering paths. Fade rule,sourcepattern andworkload are authored choices;timings are local observations.

Retrieval correction: broad Korean edge keywords caused three generic UI layout/spacing requests to retrieve BLEND. Removed those ambiguous metadata terms while preserving the existing symptom-conditioned dark-alpha-edge alias. All162 unchanged cases then passed,including the three forbidden-hit cases. This is scoped knowledge tagging,not a search-framework change.
