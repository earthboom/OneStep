---
id: K-GAME-TECH-CROWD
title: "Scale crowd decisions separately from crowd rendering"
summary: "Separate neighbour search, local collision safety and global route coordination. For sustained arrivals, track pending IDs and throughput separately; FIFO full-route reservations require controlled admission and exact schedule execution."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["crowd","Mass","avoidance","AI","LOD","spatial","hash","군중","reservation","dynamic-obstacle","국소회피","동적장애물","bidirectional","corridor","radius","clearance","deadlock","교행","양방향","반경","통로","교착","경로장","개체","lifelong","sustained","inflow","queue","FIFO","starvation","overload","throughput","unlaned","time-expanded","지속","유입","개별","무한","대기","차선","없는","지형","시간","확장","예약","과부하"]
status: active
checked_at: '2026-11-08'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Scoped Unity field, obstacle, lane and unlaned FIFO stream evidence; overload response failure retained; no arbitrary crowd/infinite-time empirical guarantee"
---
# Scale crowd decisions separately from crowd rendering

## Guidance

Use spatial partitions to limit neighbor searches, local avoidance for imminent collisions and shared route information for long-range travel. Budget behavior update frequency, animation and render representation independently. Preserve important actors/events when reducing distant simulation detail.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Fauerby's slides specify a regular cell grid over a 2.5D navigation region. Cells store occupancy and annotations; ambient agents use local steering/state machines, while evacuation uses a separately precomputed direction/cost field for each exit. Agents can change exit channels; narrow passages still need authored guidance. A small pool can promote a crowd agent to full NPC behavior on demand. Hot data is separated from full agent state, and cell attributes use separate arrays. These are confirmed 2012 design choices; a modern ECS/Mass implementation is a transfer, not the same engine.

### Local crowd experiment — 2026-11-08

[DynamicLab](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.md) combines a shared route potential with current/destination-cell reservations and yielding. One authority owns topology and reservations; a closing cell is excluded from new routes immediately, but physical closure waits for occupied traversals to drain. Opening and crate relocation update the field and native/visual state without changing agent IDs/positions. Paused controls were tested against native colliders and inspected through the actual Windows UI.

Equal discs (radius 0.20, speed 3 units/s) use cardinal unit-grid movement toward one exit region. Safe scenario minimum separation was 0.999908 units, illustrating the conservative cell spacing; this is not a dense physical-contact or pushing simulation. The 64/256 merge fixtures fully drained in 31.27/101.47 simulated seconds, with an audit every fixed tick and supplementary native obstacle overlap checks per display frame. An avoidance-disabled control deliberately produced overlaps. Final PlayMode and three Windows release players passed 12 regression checks and six scenario expectations each. Eight-ticks-per-frame behavior playback is accelerated; performance uses a separate real-time 60 Hz accumulator.

This policy fits shared-goal grids that permit queues and deferred closure. It does not establish opposing-flow liveness, general starvation freedom, arbitrary agent radii, continuous moving-obstacle prediction or a velocity-space solver. The [ORCA authors](https://gamma-web.iacs.umd.edu/ORCA/) describe reciprocal collision avoidance through velocity constraints/optimization; those assumptions and guarantees cannot be transferred to this reservation prototype. No ORCA, Mass or original Hitman implementation was reproduced here.

Rendered frame results include movement, native transform synchronization, rendering and presentation/waits. At 512 active agents, controller/sync p95 was 0.130–0.144 ms but whole-frame p95 was 2.87–3.15 ms. All final count/mode combinations met the 16.67 ms p95 target in three short windows; earlier captures had deadline misses, and host load was uncontrolled. Missing GPU timing fields are reported as missing, not zero cost; GPU tail performance is unvalidated. Treat adoption as conditional on the actual complete-frame budget and scene, not entity count or a field microbenchmark. Unsafe route-only timing is a sensitivity comparison, not an equivalent safe replacement.

### Opposing streams and unequal footprints — 2026-11-08

[TrafficLab](../../prototypes/TechniqueLab/TRAFFIC-RESULTS.md) adds radius-compatible corridor fields and authored cardinal lanes with direction-exclusive narrow leases. Fixed radii 0.20/0.35/0.60 use their actual sums for swept guards and an independent audit; a 0.04 margin rejects oversized narrow travel. Coarse four-node route costs express corridor preference, not geometric optimality. Fields select compatible long-range travel; lane separation, holding areas and phase scheduling supply progress under the tested central authority.

Final PlayMode and three release players each passed 21 regressions and 11 expectations (nine safe, two sensitivity controls). Both streams of 64/128/256 mixed discs finished; the 256 fixture took 114.7500 simulated seconds. The minimum safe pair surface gap was 0.0476715 units. Reverse and delayed requests, simultaneous wide opposing traffic, admission pause/drain/resume and terminal arrival audits were exercised. A gate-disabled pair-safe control deadlocked without collision; removing the pair guard exposed overlap. Collision freedom alone does not establish liveness.

At 256 active/visible mixed discs, complete-frame p95 was 8.08–8.32 ms across three processes; tick-bearing controller/sync p95 was 0.404–0.444 ms. All eighteen process/case windows met the 16.67 ms p95 target. Full-frame misses and missing GPU timings are retained. Uniform/mixed order was reversed in run two; uncontrolled host load and short windows prevent a causal radius-mode speedup claim. See the report for all counts and distributions.

Adopt conditionally for authored lanes/holding areas, fixed circular footprints, one motion authority and games allowing queues/turns. Directional FIFO and capped phases are bounded evidence, not a proof under perpetual arrivals. No arbitrary navmesh steering, runtime radius mutation, pushing, accelerated bodies or distributed conflicts were validated. Radius cap 0.60, speed 3 and dt≤1/30 bound the spatial-bin coverage. Admission pause is not physical obstacle closure; the older DynamicLab scope remains separate.

### Unlaned sustained inflow and individual service — 2026-11-08

[StreamLab](../../prototypes/TechniqueLab/STREAM-RESULTS.md) searches undirected four-neighbour obstacle grids instead of assigning lanes. A custom time-expanded search reserves each fixed-radius body's entire finite route; FIFO admission stops younger work when the head cannot plan. Pending requests remain outside the physical world but count toward per-ID latency. First portal waits, swept radius sums and terminal actions are independently audited, with actual displayed transforms/scales sampled natively inside every action. This is unlaned graph coordination with controlled spawning, not arbitrary physical crowd steering.

Final PlayMode and three release players each passed 23 regression/native checks and ten declared expectations: seven ordinary streams met safe drain and 240 s response, one overloaded stream safely drained but **failed** that latency target, and two controls detected starvation/collision. The overloaded 480-request choke had 61 late IDs, maximum response 280.0 s. A newest-first control left request 0 unspawned for 310 s while 538 others completed. Track release-to-admission and release-to-completion, oldest unresolved IDs, active immobility and queue growth; throughput alone cannot detect starvation. Finite traces do not observe infinity.

The FIFO finite-service argument depends on immutable complete plans, static reachable geometry fitting the horizon, exact scheduled movement, finite older IDs and a progressing clock. If the head blocks, younger admission stops and existing finite plans drain. This permits eventual service in this model, while overload still has no uniform queue/latency bound. Existing arbitrary bodies, forced occupied spawns, unexpected stops, dynamic walls/radii, acceleration and decentralized conflicts invalidate these assumptions. Goal disappearance and external queueing are material requirements.

At eight requested arrivals/s through the choke, whole-frame p95 was 3.52–6.10 ms; planning-bearing following-frame p95 was 20.23–20.52 ms in three short visible players. Full-frame misses, online planning/births/completions, actual active/visible population and GPU gaps are retained. Arrival demand is not a fixed actor count. Adoption remains conditional on target latency, admission control and representative planning-bearing complete-frame budgets.

## Applicability and exceptions

The component percentile above is per rendered frame. Uncapped rendering includes many frames without a 60 Hz movement tick; the report separates simulation-bearing component frames and their following wall intervals. Use that subset when budgeting simulation work, while retaining every frame for complete-frame statistics.

The original 2012 slides now substantiate the cell map, exit fields, behavior and NPC promotion. Their PS3 timings and counts are historical examples, not modern performance guarantees. Mass Avoidance remains version/platform-dependent.

## Checks

Profile bottlenecks, narrow exits, stopped groups and LOD transitions; log overlaps and stuck actors. Executed local subset: occupied closure, complete blockage/reopen, discrete obstacle relocation, 64/256 shared-exit merges, unsafe overlap control, repeated crate controls, paused native synchronization and arrival-segment audit sensitivity. TrafficLab below extends opposing traffic in authored lanes; production crowd animation, LOD and arbitrary continuous-body interaction remain untested.

## Evidence

- [Epic — Mass Avoidance Overview](https://dev.epicgames.com/documentation/unreal-engine/mass-avoidance-overview-in-unreal-engine?lang=en-US) — Official documentation; spatial hash, local avoidance and debug output; marked Experimental. Checked 2026-11-07, except items explicitly marked further reading.
- [Kasper Fauerby — Crowds in Hitman: Absolution](https://www.gdcvault.com/play/1015315/Crowds-in-Hitman) — Earlier pass: GDC 2012 abstract only. The original slides subsequently supplied the algorithm details cited below; the full talk was not viewed. Checked 2026-11-07.
- Originating channel shorts: V01 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [Kasper Fauerby — Crowds in Hitman: Absolution slides](https://media.gdcvault.com/gdc2012/slides/Programming%20Track/Fauerby_Kasper_CrowdsInHitman.pdf) — PDF pp.7–15 cell map/steering, pp.18–20 reactions, p.28 NPC promotion, pp.32–36 data layout; slide text inspected, benchmark not reproduced. Checked 2026-11-07.

- Local evidence: [full results and scope](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.md), [world](../../prototypes/TechniqueLab/Assets/TechniqueLab/CrowdWorld.cs), [checks](../../prototypes/TechniqueLab/Assets/TechniqueLab/CrowdChecks.cs), [final player](../../prototypes/TechniqueLab/Results/Dynamic/dynamic-run-1.json.gz), [raw analysis](../../prototypes/TechniqueLab/Results/Dynamic/summary.json). Source concepts and this custom implementation remain distinct.
- [ORCA original project](https://gamma-web.iacs.umd.edu/ORCA/), description/publications: author account of reciprocal velocity-space conditions; inspected 2026-11-08, not implemented locally. [Unity 6000.0 Frame Timing Manager](https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/profile-rendering/frame-timing-manager/manager), data availability/platform support: delayed and possibly unavailable GPU observations; inspected 2026-11-08.


- Traffic follow-up evidence: [results and reproduction](../../prototypes/TechniqueLab/TRAFFIC-RESULTS.md), [independent audit](../../prototypes/TechniqueLab/Assets/TechniqueLab/TrafficAudit.cs), [final PlayMode](../../prototypes/TechniqueLab/Results/Traffic/editor-final.json), [validated distributions](../../prototypes/TechniqueLab/Results/Traffic/summary.json). [Li et al., corridor symmetry](https://mapf.info/index.php/Main.SKoen20k), [LaValle footprint/C-space](https://lavalle.pl/planning/node161.html) and [fixed-path coordination](https://lavalle.pl/planning/node325.html) checked 2026-11-08; motivation and model distinctions, not an implemented CBS/complete-planner guarantee.


- Sustained stream evidence: [results and conditions](../../prototypes/TechniqueLab/STREAM-RESULTS.md), [per-ID/frame validation](../../prototypes/TechniqueLab/Results/Stream/summary.json), [final PlayMode](../../prototypes/TechniqueLab/Results/Stream/editor-final.json). Primary abstracts checked 2026-11-08: [RHCR](https://arxiv.org/abs/2005.07371), [PIBT](https://arxiv.org/abs/1901.11282), [online pickup/delivery](https://arxiv.org/abs/1705.10868). Guarantee conditions inform scope; those algorithms/theorems were not reproduced.
