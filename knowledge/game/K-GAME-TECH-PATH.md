---
id: K-GAME-TECH-PATH
title: "Choose A-star or flow fields by query structure"
summary: "Choose A* or shared reverse fields by goals and traversal profiles; keep graph caches valid. Unlaned opposing streams may need space-time reservations with explicit admission, clearance and latency conditions."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["A*","Dijkstra","flow","field","navigation","topology","dynamic-obstacle","door","traversal","reservation","길찾기","에이스타","다익스트라","플로필드","bidirectional","corridor","radius","clearance","deadlock","교행","양방향","반경","통로","교착","경로장","개체","lifelong","sustained","inflow","queue","FIFO","starvation","overload","throughput","unlaned","time-expanded","지속","유입","개별","무한","대기","차선","없는","지형","시간","확장","예약","과부하"]
status: active
checked_at: '2026-11-08'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Scoped Unity field, obstacle, lane and unlaned FIFO stream evidence; overload response failure retained; no arbitrary crowd/infinite-time empirical guarantee"
---
# Choose A-star or flow fields by query structure

## Guidance

Use Dijkstra with nonnegative edge costs for distance maps; A* uses f=g+h to prioritize one destination. With admissible heuristics and suitable reopening/termination handling it can retain shortest-path guarantees. For many agents sharing a goal, build a reverse distance field T. On a discrete weighted graph, choose a legal successor minimizing c(u,v)+T(v), or retain the next-hop tree produced by reverse Dijkstra. Choosing the neighbor with the smallest T(v) alone ignores the cost of reaching that neighbor. Reverse directed edges while retaining each original edge's cost; the opposite-direction edge may have a different cost.

Zero-cost edges can connect equal-distance nodes, so strict decrease alone may reject an optimal route and arbitrary equal-cost choices may cycle. Retain an acyclic next-hop tree from strict-improvement relaxations to already settled nodes, or an explicitly verified tie policy that guarantees progress. Invalidate the field and its successors together when topology/costs change.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Local engine evidence — 2026-11-07

[Technique Lab](../../prototypes/TechniqueLab/RESULTS.md) ran final PlayMode and three Windows Mono players. Weighted, directed, zero-cost-cycle, unreachable and invalidation checks passed. Each algorithm was independently compared against Floyd-Warshall for 160 source/goal cases on 16 deterministic ten-node directed graphs. This is bounded regression evidence, not exhaustive proof over all float graphs.

A cache defect was reproduced and corrected: matching revision counters on distinct graph objects do not establish matching topology. Bind a field to both graph identity and revision, and invalidate successors with costs. The prototype assumes changes use `AddEdge`/`SetBlocked`; mutating exposed arrays/lists directly can bypass its revision tracking. It is a single-threaded prototype, not a hardened cache API.

On one 32×32 weighted grid, 512 same-exit distance answers took per-process medians of 18.803–19.967 ms for independent A*, 0.06784–0.06898 ms for one field rebuild plus lookups, and 0.000863–0.000878 ms for cached array lookups. These are repeated CPU batch-throughput measurements on one host. Cached timings omit validity checks per query, successor traversal, path reconstruction, steering and avoidance. Do not treat the ratio as a whole-game speedup or a universal agent-count threshold; all tested batches (32/128/512) favored fields, so the crossover was not located. Select by shared goal/cost profile, rebuild frequency, distinct goals, memory and actual movement cost.

The original 2026-11-07 scene renders 64 successor consumers. Door changes rebuild the field and **reset consumers to safe initial cells**. That historical illustration did not implement in-flight reconciliation or avoidance. The separate 2026-11-08 extension below adds a scoped movement policy without changing that baseline.

### Dynamic movement follow-up — 2026-11-08

[DynamicLab results](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.md) add actual movement checks without resetting agents on topology changes. One world owns routing, current/destination-cell reservations and physical obstacle state. A close request blocks new routes and rebuilds the field immediately; its collider becomes solid only after existing travelers leave. A reopen updates both routes and representation, including while paused. A disc geometrically inside the doorway safely drained before closure (0.4167 simulated seconds in the fixture); followers used the other opening. When both routes were closed, agents waited and resumed on reopening.

The local conflict policy selects an available strictly downhill cardinal neighbor or yields, rotating arbitration order. An exit strip connects to one sink; no nonlocal edge is executed by a mover. This is a conservative equal-disc cooperative grid policy, not general continuous avoidance. Final PlayMode and three release players each passed 12 regressions and six scenario expectations. All 64 and 256 merge agents arrived within the declared 60/120 simulated-second limits, without observed pair/wall/teleport/reservation errors. These bounded results do not prove arbitrary starvation freedom or support opposing traffic, heterogeneous radii, diagonals or instantaneous crushing doors.

For 512 active agents in the new 64×40 rendered scene, full-frame p95 ranged 2.87–3.15 ms across final processes, while controller/native-transform synchronization p95 ranged 0.130–0.144 ms. All final count/mode combinations met the 16.67 ms p95 target in three short windows; earlier captures had deadline misses, and host load was uncontrolled. The old distance-array microbenchmark cannot predict this budget. Whole-frame stalls remain included. GPU fields had missing observations, so GPU tail latency remains unvalidated. Adopt conditionally after actual scene/hardware profiling and a compatible closing policy; do not replace complete-frame costs with the small field-query cost.

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

The dynamic experiment's controller percentile is per rendered frame. At uncapped render rates many frames run no 60 Hz movement tick; inspect its separate simulation-bearing subset before budgeting tick work. Full-frame statistics retain every frame.

Pathfinding is not local collision avoidance. Agent radius, diagonal corner cutting, changing obstacles and unequal terrain costs must be represented explicitly.

## Checks

Proposed: compare A* and field-following costs against Dijkstra on small weighted/directed maps, including unequal outgoing costs, zero-cost cycles, unreachable goals and topology changes. For example, c(S,A)=100,T(A)=1 versus c(S,B)=1,T(B)=2 must select B (3 total), not A (101). These arithmetic checks do not establish collision-safe movement or an engine/plugin's API contract.

Executed local subset: known graph cases and an independent Floyd-Warshall oracle, acyclic successor termination, topology invalidation, distinct graph identity, equal distance checksums and scene door rebuilds. Repeat with actual navigation data, agent profiles, update frequency and movement/avoidance before production adoption.

## Evidence

- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — Author interactive article; graph representation and heuristic search. Checked 2026-11-07, except items explicitly marked further reading.
- [Amit Patel — Flow Field Pathfinding for Tower Defense](https://www.redblobgames.com/pathfinding/tower-defense/) — Author article; all-sources/one-destination search. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V36 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

- Follow-up checked 2026-11-07: Patel's A* introduction, Movement costs code, adds the current movement cost during relaxation; the tower-defense article uses came_from and distinguishes its unweighted BFS demonstration from weighted Dijkstra. The weighted successor, directed reversal and zero-cost progress clauses above are engineering derivations, checked with [three supplemental graph counterexamples](../../skills/vegabond-knowledge/tests/game-application/weighted-flow-cases.json), not quoted vendor guarantees or a game runtime test.
- Subsequent local engine experiment: [results and reproduction](../../prototypes/TechniqueLab/RESULTS.md), [graph/field/A* implementation](../../prototypes/TechniqueLab/Assets/TechniqueLab/WeightedField.cs), [independent checks](../../prototypes/TechniqueLab/Assets/TechniqueLab/LabChecks.cs), [graph-identity failure](../../prototypes/TechniqueLab/Results/red-graph-identity.json), [corrected checks](../../prototypes/TechniqueLab/Results/green-final-checks.json), [raw player example](../../prototypes/TechniqueLab/Results/player-run-1.json) (`path.*`, `consumer.door-*` and distance benchmarks). This adds local runtime evidence without changing the historical hypothetical-test results.


- Dynamic follow-up: [results, raw runs and reproduction](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.md), [owned world/transactions](../../prototypes/TechniqueLab/Assets/TechniqueLab/CrowdWorld.cs), [independent geometric audit](../../prototypes/TechniqueLab/Assets/TechniqueLab/CrowdAudit.cs), [final PlayMode](../../prototypes/TechniqueLab/Results/Dynamic/dynamic-editor-final.json), [analysis](../../prototypes/TechniqueLab/analyze_dynamic.py). Actual execution scope: cardinal equal discs, unit grid, one exit region, deferred closure, Unity 6000.0.77f1 Windows release Mono.


- Traffic follow-up evidence: [results and reproduction](../../prototypes/TechniqueLab/TRAFFIC-RESULTS.md), [independent audit](../../prototypes/TechniqueLab/Assets/TechniqueLab/TrafficAudit.cs), [final PlayMode](../../prototypes/TechniqueLab/Results/Traffic/editor-final.json), [validated distributions](../../prototypes/TechniqueLab/Results/Traffic/summary.json). [Li et al., corridor symmetry](https://mapf.info/index.php/Main.SKoen20k), [LaValle footprint/C-space](https://lavalle.pl/planning/node161.html) and [fixed-path coordination](https://lavalle.pl/planning/node325.html) checked 2026-11-08; motivation and model distinctions, not an implemented CBS/complete-planner guarantee.


- Sustained stream evidence: [results and conditions](../../prototypes/TechniqueLab/STREAM-RESULTS.md), [per-ID/frame validation](../../prototypes/TechniqueLab/Results/Stream/summary.json), [final PlayMode](../../prototypes/TechniqueLab/Results/Stream/editor-final.json). Primary abstracts checked 2026-11-08: [RHCR](https://arxiv.org/abs/2005.07371), [PIBT](https://arxiv.org/abs/1901.11282), [online pickup/delivery](https://arxiv.org/abs/1705.10868). Guarantee conditions inform scope; those algorithms/theorems were not reproduced.
