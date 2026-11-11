---
id: K-GAME-TECH-BILLBOARD
title: Orient image impostors for their intended viewing conditions
summary: Choose screen-aligned, camera-position-facing or world-Z-constrained image
  planes. Scoped UE5.8.3 orientation/alpha/occlusion/shadow and3repeat cost evidence;
  pole/sorting/projected-area limits and actual-FPS shortfalls remain explicit.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- billboard
- impostor
- 빌보드
- screen aligned
- camera facing
- world Z
- axis constrained
- camera roll
- UV mirroring
- vertical pole
- cutout shadow
- alpha sorting
- 화면 정렬
- 카메라 바라보기
- 축 고정
- 극점
- 반투명 정렬
- 마스크 그림자
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 V43 partial native:39policy,4assets,207pose observations,9cost
    players,1x media; actual FPS coverage separate from cap and144 not automatically
    verified
  runtime_fps_evidence: 'cap30→22.49FPS, cap60→45.31FPS, cap144→114.02FPS; Requested-FPS
    coverage is incomplete: each missed cap band remains unverified under the existing
    actual-FPS±10% criterion;pose checks pass only at observed rates.'
---
# Orient image impostors for their intended viewing conditions

## Guidance

Use image planes for particles, distant vegetation or stylized objects. Choose screen-aligned, viewpoint-facing or axis-constrained orientation. Preserve a stable up direction for grounded objects; an atlas can select different view angles when a single image is insufficient.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Intersecting planes, stereo views, shadows, transparency sorting and top-down viewing can reveal the approximation. A billboard is not automatically cheap if it covers many pixels.

## Checks

Native scoped checks and actual FPS limits appear in the dated follow-up. Production-camera alpha overdraw,stereo/LOD and general sorting remain unmeasured.

## Evidence

- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) — Official stable documentation; normal map, transparency and billboard sections; rolling version. Checked 2026-11-07, except items explicitly marked further reading.
- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass) — GPU Gems ch.7; crossed quads and animation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V43 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.


### Native Unreal billboard follow-up — 2026-11-11

[V43 native results](../../prototypes/UnrealTechniqueLab/BILLBOARD-RESULTS.md) add39policy checks,4saved owned RGBA/material assets,23situations×3methods×3actual PIE requested-cap runs=207pose observations and3matched1280×720 package cost repeats per method. Actual orbit rates: cap30→22.49FPS, cap60→45.31FPS, cap144→114.02FPS. Requested-FPS coverage is incomplete: each missed cap band remains unverified under the existing actual-FPS±10% criterion;pose checks pass only at observed rates. Normal30fps1x media is separate from actual-FPS/cost evidence.12limited local sheets/31without direct technique prototypes is coverage,not complete certification.

Retrieve BILLBOARD for screen alignment,camera-position-facing and world-Z-constrained image planes,roll/UV mirroring,vertical-pole fallback,cutout/alpha/sorting limits. Screen alignment follows camera right/up;position-facing uses the vector from camera to each object and projected camera up;Z-lock keeps world up and only uses horizontal camera displacement. A two-sided plane uses image right/up and a view axis pointing camera→object. The actual Engine Plane UV requires localX180degree correction;RGB top-left/bottom-left/right markers independently check native rendered orientation.

At direction length≤1e-6cm,coincident position-facing uses history or initial screen frame. Parallel-up projects previous right and uses a deterministic alternative when needed. Axial pole retains valid horizontal history,then projected camera forward,then+X. No unique yaw exists at the pole;Z-locked images are edge-on from overhead. These authored fallbacks do not guarantee arbitrary pole-crossing continuity. Parent negative scale,stereo,atlases,WPO and moving vegetation are untested. Prefer another representation when silhouette/top-down/stereo/intersections expose the approximation.

Saved unlit two-sided opaque/masked/translucent materials use the same asymmetric128×128RGBA texture. Local opaque ignores alpha,masked clips at.5,and translucent yellow half strip differs from full yellow/background while retaining yellow dominance. Tone-mapped RGB is not a linear50%blend equation. Native occluder blocks the center marker. Three translucent planes really overlap in projected bounds and retain a visible red marker;this does not certify all sorting orders or layered composition. Masked solid and transparent-hole shadow receiver samples compare enabled/disabled settings;solid darkens and hole stays lit. Ordinary translucent with the special masked-shadow option disabled leaves both unchanged in this renderer. Other shadow modes/features need target-engine verification. [Epic blend modes](https://dev.epicgames.com/documentation/unreal-engine/material-blend-modes-in-unreal-engine?lang=en-US) and [material properties](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-material-properties) describe the relevant options;local records establish the tested behavior.

Cost workload:512separate native components,same16×32grid120cmspacing,z220,samecamera,masked unlit two-sided/no shadow/no collision;one selected orientation per player,2s warmup+10measured,three rotated orders. Solver/native rotation/readback/lightweight checks and empty sample allocation are the CPU subset;whole wall/cadence are distinct and not GPU completion. No full state logging/readback/capture in cost inputs. Same layout does not imply same projected area/overlap when methods rotate differently;no pure solver/GPU-overdraw/universal speedup conclusion. No no-billboard baseline. Instancing,LOD/streaming/particles/vegetation optimization are outside this prototype.

ONE fresh read-only review found3evidence gaps,each reproduced before repair: a black overlapping marker,a blue replacement for the yellow half strip,and a rectangular masked shadow could pass. Dominant-color/intermediate-intensity and solid+hole receiver checks now reject them.26feature evidence tests and4review sensitivity tests guard the bounded claims. Main/fill light priority1/0 removes a genuine engine warning that covered RGB probes;retained raw framebuffer shows the fault. Standalone OnEndFrame backbuffer read yielded a handled TextureRHI ensure/black image;feature readback moved to viewport OnDrawn after canvas flush,before Present. No performance readback.17older source archives and32prior assets retain bytes. No capture/framework/renderer optimization or publication.

Godot stable and historical GPU Gems ch7were reread2026-11-11 for concepts/crossed image planes,not UE-specific guarantees or current cost. Installed UE5.8.3 APIs,native assets and frozen outputs are the local implementation evidence. Originating V43remains a discovery lead,not independent implementation proof.
