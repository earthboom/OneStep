---
id: K-GAME-TECH-NOISE
title: Generate coherent terrain with gradients and multi-scale noise
summary: Use shared global seeded sampling and world derivatives for continuous heightfields;scoped
  UE5.8.3 four-chunk evidence distinguishes repeat determinism,native precision,seam
  controls and synchronous rebuild frame cost.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["Perlin", "noise", "fractal", "fBm", "terrain", "바이옴", "fractional Brownian motion", "lacunarity", "persistence", "octave", "seed", "deterministic terrain", "negative coordinates", "heightfield", "chunk seam", "analytic derivative", "world normal", "floor", "noise octave", "청크 이음새", "음수 좌표", "시드", "높이장", "법선 이음새"]
status: active
checked_at: "2026-11-19"
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 Perlin/fBm4:57model,12native scenes,2352probes/3120edgepairs,6cost
    players,normal1x media;no caves/fluids/voxels/streaming
---
# Generate coherent terrain with gradients and multi-scale noise

## Guidance

Use coherent noise for spatially continuous variation. Perlin noise computes gradient-dot products at surrounding lattice corners and blends them with smooth interpolation; adding the raw dot products is insufficient. Sum octaves with controlled frequency and amplitude for multi-scale detail. Derive biome fields independently from final mesh construction.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Mojang's 1.18 development notes explicitly separate terrain shaping, biome distribution, noise caves and aquifers. Aquifers give underground regions local water levels; cave carving and noise fields can coexist. For a new generator, treat density d(x,y,z), climate/biome fields and fluid occupancy as separate inputs. Evaluate density including neighbor margins before meshing a chunk, and make cave/biome blending deterministic across boundaries. This is an implementation synthesis, not Mojang's exact density function.

## Applicability and exceptions

A heightfield cannot represent overhangs; density fields can. Exact Minecraft algorithms change by edition/version and are not established from this general reference.

In procedural terrain, an **octave** is one noise layer at a chosen frequency and amplitude. Fractal-noise sums often called fractional Brownian motion (fBm) combine several such layers. **Lacunarity** scales frequency between octaves and **persistence** scales amplitude. Keep the sampled world coordinates consistent across chunk edges. Test neighboring chunks independently, including distant levels of detail where high frequencies can alias. [libnoise — Perlin module parameters](https://libnoise.sourceforge.net/docs/classnoise_1_1module_1_1Perlin.html)

## Checks

Scoped native seed/negative-coordinate/height-normal seam checks appear below;biomes and reachable terrain remain unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf) — 2002 paper; interpolation and gradients. Checked 2026-11-07, except items explicitly marked further reading.
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf) — 2016 author chapter; terrain and multi-scale noise. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V07, V50 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

### Follow-up evidence

- [Mojang — Java 1.18 experimental world generation](https://www.minecraft.net/en-us/article/new-world-generation-java-available-testing) — Official historical development notes; release scope distinguished from snapshot behavior. Checked 2026-11-07.
- [Mojang — Bedrock 1.18.0 release notes](https://feedback.minecraft.net/hc/en-us/articles/4414284658701-Minecraft-Caves-Cliffs-Part-II-1-18-0-Bedrock) — New biome/cave generation and aquifers; edition/version retained. Checked 2026-11-07.

## Native seeded heightfield evidence — 2026-11-12

The historical Unreal run implements an authored seeded2D Perlin adaptation and normalized4octave fBm on4adjacent nativeUE5.8.3 chunks,64×64cells/65×65vertices each,50cm spacing,16900vertices/32768triangles.57model checks,6scenes each in actualPIE/package,2352independent native probes,3120shared-edge pairs,3matched cost repeats per profile and actual normal1x media. Latest14limited local technique sheets/29without direct prototypes;not complete subject certification.

Hash seed with uint32 floor-lattice coordinates;negative coordinates use floor,not truncation. Eight unit gradients,quintic fade,conservative divide-by-sqrt2 field normalization;fBm defaultfrequency.000625/cm,lacunarity2,persistence.5,amplitude450cm,divide by sum of octave weights. Source concepts from [Perlin2002](https://mrl.cs.nyu.edu/~perlin/paper445.pdf) and [PCGbookchapter4](https://www.pcgbook.com/chapter04.pdf),reread2026-11-12. Hash,parameter bounds,2Dadaptation and engine representation are authored choices,not exact Perlin2002/Minecraft reconstruction. Do not import historical performance numbers.

Generate global integer sample=(chunkIndex*cells+localIndex) before scaling;share seed/settings across chunks. Use world analytic derivatives with the octave frequency chain rule and normalize(-dHdx,-dHdy,1). A finite-difference alternative needs a common world neighborhood/halo;per-chunk one-sided edge differences can break normal continuity despite matching heights. Correct native shared height/normal errors were exact0(acceptance1e-6cm/1e-6vector). Deliberate chunk-local height coordinates yielded96.235647cm height seams;world-correct heights with local edge normals yielded.10062494normal-vector seams while heights stayed0. Both negative controls are rejected as terrain implementations. Normals matching is not equal triangle slopes or collision smoothness.

Same seed42 and reversed chunk generation order reproduce all source/native array hashes WITHIN each compiled target;all64ordered performance seed outputs reproduce across3packaged runs. Negative-domain seed777 at origin(-3,-2) is independently checked. Separately compiled Editor/package source-double hashes differ and max normal source error differs by~1.6e-17;this is a failed cross-target byte-equality assumption,not evidence of arbitrary nondeterminism within a build. Actual published native hashes,probes,edges,indices and face records match EXACTLY across consumers. No cross-compiler/platform/version source bit determinism claim. Keep original exact-comparison failure and test native mutations separately. Source-double→nativefloatposition tolerance5e-5cm,16bitdecodednormal1e-4vector;never replace field determinism checks with only a loose native tolerance.

Important repaired failure:initial self-consistent arrays/oldCPUwinding oracle passed but single-sided terrain was invisible. InstalledUE StaticMeshOperations computes Cross(DPosition2,DPosition1). Test against actual enginePlane/reversedPlane,correct indices{A,D,B,A,C0,D},check every actual native triangle and inspect actual lit screenshots. Facing regression1/55failed→57pass. No two-sided/culling/renderer workaround.29independent evidence tests reject missing/wrong probes,shared-edge data,seed/octave/negative-domain substitutions,false controls,repeat/source/native digest mutations,missing/reversed face evidence,clock/consumer/launch/copy substitutions. Preserve failed captures as evidence;self-consistency alone does not prove rendering.

|Run|Generation p95 ms|Mesh publication p95 ms|Whole wall p95 ms|Whole max ms|
|---|---:|---:|---:|---:|
|perf-perlin-1|0.657|36.065|38.653|39.719|
|perf-perlin-2|0.647|36.458|38.989|39.674|
|perf-perlin-3|0.676|36.225|39.043|39.913|
|perf-fbm-1|1.495|35.955|39.332|39.835|
|perf-fbm-2|1.441|36.504|39.926|40.272|
|perf-fbm-3|1.472|36.255|39.646|40.347|

Conditions:Win64 Development/DX11/i7-12700KF/RTX3080,1280×720,identical4chunks/camera/material/light,no collision/shadows,2s staticwarmup,64orderedseeds0..63 with4complete mesh replacements per frame,3CPUtailframes,3rotated Perlin1/fBm4 pairs. Generation=field/derivatives/arrays/indices;publication=MeshDescription/nativefastbuild/SetStaticMesh+origin. Whole wall/cadence includes per-seed hash/JSONrow outside subset timers. No audits/debug/capture in cost. Publication dominates;whole-frame p95~39–40ms exceeds16.67ms60FPS budget. This synchronous replacement workload is unsuitable for per-frame60FPS under these conditions. Static build-once/off-critical-frame use remains conditional on separately checked lifecycle/frame budget;no async/streaming feature was implemented. Engine-managed old mesh resource release/GC,peak memory and GPU drain are unverified;3CPUtailframes do not bound those. Full wall/cadence is not GPU/Present-only time. No universal timing guarantee or renderer optimization.

Scoped input limits:finiteoctaves1..8,freq(0,1],lacunarity1..4,persistence0..1,amplitude0..1e5cm,absworld≤1e7cm,scaledlattice≤2^30;cells2..128,spacing1..1000cm,chunkindices±1024subjectdomain. Invalid inputs reject atomically. A heightfield has one height perxy:overhangs,caves,fluids,voxels,biomes,LOD transitions,large-world precision,collision/navigation and reachability remain unverified. No streaming/renderer/validation-framework expansion. Existing19source archives/36assets preserved;inheritedEasing104/corePIE73/package73 pass. Native reports/source/media remain local evidence,excluded from prior knowledge-only publication;no new commit/push in this task.
