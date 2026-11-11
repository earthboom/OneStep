---
id: K-GAME-TECH-DUNGEON
title: Generate levels from a traversability contract
summary: Choose generation by topology and movement constraints. UE5.8.3 BSP1000seed
  native tests pass; full1536cell replacement every frame measured21.61–22.13ms p95,
  so use loading/pre-generation conditionally rather than claiming a60FPS runtime
  replacement budget.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- procedural
- dungeon
- BSP
- random
- walk
- grammar
- 절차적생성
- seed
- room corridor
- capsule clearance
- connectivity
- farthest exit
- 던전
- 시드
- 방 통로
- 연결성
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 V40/V56 BSP:1024policy,1000actual PIE+1000package
    seeds,3matched1000seed costs,native1x media; flat capsule only; per-frame full
    replacement fails60FPS budget
---
# Generate levels from a traversability contract

## Guidance

Choose a room graph, spatial partition, random walk or grammar according to the desired topology. Establish start-to-goal connectivity, then instantiate compatible rooms, doors and encounters. Separate seeded topology generation from decoration so cosmetic changes do not unexpectedly change routes.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Graph connectivity does not prove platformer reachability, key availability or acceptable difficulty. Different Spelunky, Rogue, Isaac and Dead Cells versions should not be assigned one universal algorithm.

## Checks

Proposed: generate a large reproducible seed set, validate movement-aware reachability and key ordering, retain failing seeds.

## Evidence

- [Shaker et al. — Constructive Generation Methods for Dungeons and Levels](https://www.pcgbook.com/chapter03.pdf) — 2016 author chapter; representation, BSP, agents and platform levels. Checked 2026-11-07, except items explicitly marked further reading.
- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — Author interactive article; graph representation and heuristic search. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V40, V56 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Local Unreal BSP dungeon — 2026-11-11

[Native V40/V56 results](../../prototypes/UnrealTechniqueLab/DUNGEON-RESULTS.md) implement one authored BSP variant, not a reconstruction of Spelunky/Rogue/Isaac/Dead Cells. The PCG book chapter3section3.2 was reread2026-11-11: hierarchical partitions, rooms in leaves and connections between sibling subtrees informed the design. Exact dimensions, seed stream, corridor order and capsule contract are local engineering choices.

Use a representation contract first. This prototype partitions the solid-bordered inner48×32grid, cell200cm, depth4/min split child8cells. Random inset rooms are at least3×3cells; ordered sibling representative centers connect by one-cell orthogonal L corridors. Room rectangles are disjoint; corridor/room intersections are allowed. Start is first room center; exit is the farthest four-neighbor floor cell, with smallest linear index breaking ties. A local FRandomStream and fixed traversal order reproduce the complete ordered room list, floor bits and endpoints. Isolate decorative randomness when adding decoration; this prototype has none. Same local5.8.3 implementation is verified, not cross-version/cross-platform binary determinism or diverse/fun level quality.

1024policy checks include repeated main seeds0..999, extreme signed seeds, small/non-square/max supported dimensions, depths0/8 and malformed inputs. Independent flood/rectangle/border checks do not call the generator's flood routine. Disconnected/overlapping/border-corrupt controls demonstrate rejection; there is no regenerate-until-pass retry. Model domain W/H10..128,depth0..8; native geometry evidence below is the main48×32shape only.

Both actual PIE and packaged consumers instantiate all1000ordered seeds as native cube floor/wall instances. Each checks every floor center for34cm-radius/88cm-halfheight capsule clearance and floor support, every solid center for blocking, every adjacent floor edge by native capsule sweep and all-floor reachability over those native edges. A real CapsuleComponent then sweeps the shortest centerline route from start to exit. Flat floorZ0, capsule centerZ90 (bottom2cm), walls200cm. Handcrafted one-cell corridor controls require ordinary capsule pass,101/110capsule reject and inserted wall reject. Logical connectivity alone is insufficient; instance mapping and collision shape/clearance must agree. These are constant-height flat-grid checks, not gravity, CharacterMovement, slope/jump, NavMesh, lock/key progression, enemy placement, subjective pacing or general free-space navigation.

Three identical1280×720 uncapped packaged runs measure2s warmup then seeds0..999, one generation+full native geometry replacement per frame, followed by3CPU wall tail frames. Record pure layout CPU, placement game-thread time, full wall frames/cadence/max/deadlines, total generation-to-drain wall time and process memory. Native audit/capture/debug overlays are absent from cost input. Layout/instance identity is the same across consumers and all repeats. Placement timing does not synchronously drain GPU; whole wall frames and tails are CPU-observed rendering/Present throughput, not GPU duration/completion proof. No universal frame-budget claim; use measured replacement hitches to decide loading/pre-generation versus gameplay-time use, and remeasure target assets/counts. No scheduling/streaming/tool/renderer optimization was added.

Cadence samples are previous begin→current begin; first includes the warmup transition and last precedes generation999. They are not per-seed completion latency. Memory samples are after placement, before appending the current result and before drain; last sample is not post-drain retained memory. Result-record accumulation contributes to growth; process-reported peak includes startup/warmup and is distinct from the sampled maximum. Three native media seeds1/42/777 at30simulation/30playback FPS show normal routes1x; rejection controls are recorded native audit results, not a separately filmed control scene.

Source/config/project/unchanged32assets/module/exe/5package containers/launcher/output identities bind actual runs, and distinct launches/raw frames prevent demonstrated repeat substitution. Independent result checks retain failing seeds rather than relying on native passed=true. New evidence remains scoped to V40/V56 room/corridor generation and flat capsule traversability; complete gameplay or a named commercial game's generator is untested.

Measured adoption decision: generation p950.0273,0.0273,0.0273ms; placement GT p959.540,9.562,9.347ms; whole-wall p9521.847,22.129,21.608ms. All3000measured seed frames exceed16.667ms. Conditionally adopt seeded topology/native geometry for loading or pre-generation; reject this1536cell full replacement every gameplay frame for60FPS in the measured workload. Do not attribute the remaining wall time to a particular GPU/render stage without a separate profile.
