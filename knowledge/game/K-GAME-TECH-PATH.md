---
id: K-GAME-TECH-PATH
title: Choose A-star or flow fields by query structure
summary: Choose A* or shared reverse fields by goals and traversal profiles; keep
  graph caches valid. Unlaned opposing streams may need space-time reservations with
  explicit admission, clearance and latency conditions.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- A*
- Dijkstra
- flow
- field
- navigation
- topology
- dynamic-obstacle
- door
- traversal
- reservation
- 길찾기
- 에이스타
- 다익스트라
- 플로필드
- bidirectional
- corridor
- radius
- clearance
- deadlock
- 교행
- 양방향
- 반경
- 통로
- 교착
- 경로장
- 개체
- lifelong
- sustained
- inflow
- queue
- FIFO
- starvation
- overload
- throughput
- unlaned
- time-expanded
- 지속
- 유입
- 개별
- 무한
- 대기
- 차선
- 없는
- 지형
- 시간
- 확장
- 예약
- 과부하
- Unreal
- UE5.8.3
- 언리얼
- PIE
- UnrealEditor
- admission
- queue-cap
- token-bucket
- rejection
- goodput
- 거부율
- 입장
- 제공량
- Unreal Insights
- occlusion query
- horizon pruning
- same-binary
- frame alignment
- 프레임 지연
- packed priority
- heap sift
- PriorityKey
- plannerPeak
- per-request equivalence
- 계획 처리
- owned snapshot
- record DOM
- saveTail
- private commit
- PagefileUsage
- snapshot lifetime
- 스냅샷 저장
- owned async save
- publicationToAck
- pending exit drain
- writer backpressure
- full input lifetime
- 비동기 저장
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped Unity and UE5.8.3 representative, dynamic, opposing and
    static unlaned FIFO evidence; fixed graph/admission/exact schedule limits remain
  admission_evidence: UE5.8.3 paired six-policy overload comparison; accepted latency/all-offered
    goodput/rejection and full frames; finite static graph scope
  hitch_evidence: UE5.8.3 same-binary3paired admission profiles; named frame traces;
    scene-local query suppression and cardinal reservation proof limits
  planner_evidence: UE5.8.3 equivalent packed-priority heap; scoped bit-domain/path/order/native/profile
    and3paired frame evidence
  snapshot_evidence: UE5.8.3 owned records/direct JSON; exact byte/value/order/lifetime/native
    safety,3paired transition/save/process-memory observations
  async_save_evidence: UE5.8.3 detached full input; same-binary owned-sync/async3pairs,
    exact records, queue/failure/pending-exit controls; finished-fixture rendering
    only
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

### Unreal native follow-up — 2026-11-09

[Native results and media](../../prototypes/UnrealTechniqueLab/STAGE2-RESULTS.md) compare reverse weighted fields and A* to independent Floyd-Warshall over1536 directed source/goal pairs, verify zero-cost successor termination and identity/revision rejection, and render a14x9 consumer reaching its goal. This is UE5.8.3 Development graph movement with controlled graph mutation, not NavMesh, CharacterMovement, dynamic obstacles or collision avoidance. Native complete-frame observations retain startup checks and waits; no Unity speedup or population threshold transfers. PIE and crowd ports were pending at that checkpoint; the later gate/dynamic sections below update the current state. Public arrays still permit bypassing revision tracking if callers mutate them directly.

### Editor/runtime gate follow-up — 2026-11-09

[Actual PIE and full-package results](../../prototypes/UnrealTechniqueLab/EDITOR-GATE-RESULTS.md) now close the earlier manual-PIE/reused-cook gap. Camera, hitscan and path each run in WorldType3 through the official Editor automation API, pass73 checks and have native viewport videos. Final full cook and standalone consumers also pass. This does not validate camera collision, animated/network hits, NavMesh or crowd avoidance. Renderer/RHI/D3D11 presentation waits dominate the investigated tail; do not infer a path-kernel problem or adopt diagnostic occlusion/RHI toggles as production defaults. Trace and capture overhead are separate from no-capture frame observations.

### Unreal dynamic obstacles and local reservations — 2026-11-09

[Native UE5.8.3 results](../../prototypes/UnrealTechniqueLab/DYNAMIC-RESULTS.md) now revalidate the scoped equal-radius shared-exit model in six actual PIE and six packaged fixtures, with13 C++ checks and actual capsule/box/pose queries. Five safe scenarios fully drain;256 agents take98.6833 simulated seconds. Closing a geometrically occupied door blocks new routing immediately and waits0.4s before physical closure, without resets. A reservation-disabled control completes11/32 in10s and detects8959 repeated swept overlaps; this expectation pass is detector sensitivity, not safe movement. Native endpoint overlaps and same-time swept pairs, including terminal segments, remain separate observations.

Adopt **conditionally** for one motion authority, equal20cm discs,300cm/s cardinal travel in100cm cells, one exit strip, queues, goal disappearance and deferred closure. Native query-only capsules with explicit poses do not validate forces, pushing, CharacterMovement, NavMesh, ORCA or arbitrary trajectories. At that checkpoint native mixed-radius opposing traffic and sustained unlaned inflow were pending; the traffic follow-up below adds only the former, while older Unity stream evidence remains separate. Reject transferring those proofs or performance numbers between engines. Finite safe drains do not establish general deadlock/starvation freedom.

Three separate no-capture packaged players retain44740 complete frames with64/256/512 constant active/render-enabled bodies. At512 reserved agents whole-frame p95 is3.849–3.953ms and tick-bearing controller/sync p95 is2.382–2.403ms. All18 short-window p95 values meet16.67ms, but54 measured misses coincide with large topology-change work. The54 synchronous change+native-sync calls cost15.594–19.539ms; planner-only cost was not isolated. **Reject this unchanged synchronous policy for a strict no-miss60Hz budget**; budget and revalidate staged/incremental updates while preserving revision and deferred-close ownership before frequent changes. GPU snapshots were available but asynchronous; no aligned GPU-tail or shipping guarantee follows. Per-frame allocations/recording are included; memory allocation rate was not measured. Native render-enabled counts mean collision-enabled capsules/unhidden visible meshes, not an occlusion/pixel-visibility count. Fixed-time videos are4x behavior evidence, not timing inputs.

Reuse checks: verify current+destination reservations, stale-field rejection, geometric body occupancy at closure, no pose/ID reset, paused native collider updates, swept terminal segments, safe complete drain and an overlap-detecting unsafe control. Separately verify actual population, retained catch-up backlog, full frame/cadence duration and asynchronous counter availability; a `passed` summary alone is insufficient. [Independent acceptance](../../prototypes/UnrealTechniqueLab/crowd_contracts.py) and34 focused regressions cover the observed scope.

### Unreal opposing fixed-radius lanes — 2026-11-09

[UE5.8.3 native traffic results](../../prototypes/UnrealTechniqueLab/TRAFFIC-RESULTS.md) now separately verify26 C++ checks, eleven actual PIE and eleven packaged expectations: nine safe fixtures plus collision-safe deadlock and collision controls. Fixed20/35/60cm bodies use actual capsule footprints and radius sums. Mixed256 completes128east+128west in114.5667 simulated seconds; minimum safe **surface gap** is5.000000cm. Actual native positions are independently swept-audited every behavior tick, including terminal segments; per-agent native query counts reconcile with arrival/final ticks. Field feasibility applies to both exits, and60cm profiles reject the100cm narrow opening with4cm margin.

**Conditional adoption:** one authority, authored cardinal lanes/holding stems, fixed circles,300cm/s,dt≤1/30, games permitting queues/turns and disappearance at exits. Direction-exclusive narrow leases preserve FIFO within direction, cap phase admissions at4 while opposition waits, and release after the full body clears the mouth+margin. A pair-safe/no-admission control deadlocks without collision, so shared fields plus reactive pair safety alone are **rejected** as a progress policy. This does not implement ORCA, CharacterMovement, arbitrary NavMesh steering, pushing or dynamic shape/path mutation. Native sustained unlaned inflow remains pending. Finite completion is not perpetual fairness or general starvation freedom; retain individual waits as well as throughput/global stalls.

Three sequential packaged players preserve54200 complete frames in64/128/256 uniform/mixed comparisons. Mixed256 whole-frame p95 spans2.875–3.297ms; tick-bearing controller/sync p95 spans1.080–1.220ms. Measured deadline misses total0; raw startup/setup/warmup and all tails remain. Real-time performance is separate from8ticks/frame behavior and4x video. Async CPU/render/wait/GPU values do not establish aligned GPU tails; render-enabled flags are not pixel visibility. Geometry/profile setup is outside measured windows, while native motor/guard/gate/sync remain inside. Admission pause/resume is timed, not physical topology rebuilding. A separate new-build DynamicLab regression retains that earlier synchronous-update limitation; static traffic does not fix it or establish a Unity speedup.

Carry these checks into a target game: radius-compatible routes for both goals, bounded-bin versus exhaustive neighbors, actual capsule scale/pose binding, full-body lease release, reverse/late ticket order, pause/drain/resume, independent unequal-radius/terminal sensitivity, safe complete E/W drain and both failure controls. For evidence, reconcile each frame's wall delta, retained accumulator and executed steps, native ticks/component-time containment, warmup population, exact event frame IDs, per-ID native query coverage and immutable source/build/harness identity. The observed review gaps were fixed and59 focused regressions pass.

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
### Native unlaned sustained arrivals — 2026-11-09

[UE5.8.3 StreamLab](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.md) adds25 C++ checks, ten actual PIE and ten full-cook packaged expectations with identical per-ID/action ledgers. Eight FIFO cases complete3120valid requests and explicitly reject one unreachable request. Seven meet240s release-to-completion; overloaded choke is collision-safe and drains but61IDs exceed240s(max280s), so **latency fails**. LIFO completes538later IDs by310s while ID0 remains unadmitted; this is censored individual waiting, not an infinite-time observation. Disabling reservations exposes actual collision. First waits, five native fractions/action and terminal segments reconcile per ID; native capsule, mesh world position/scale and actual wall queries have deliberate corruption controls.

**Conditional use:** static32x24 undirected four-neighbor graph150cm cells, authored portals but no prescribed lanes, fixed20/35/60cm circles and4cm swept margin,300cm/s,0.5s actions, complete≤96action immutable routes, one authority, FIFO controlled admission with pending bodies outside the world and goal disappearance. This is not arbitrary continuous NavMesh, ORCA/PIBT/RHCR, physics pushing, acceleration, mutable radii/topology or unscheduled existing actors. Pending age starts at request, not spawn. For a fixed ID, finitely many older FIFO jobs and finite complete-route service support only a conditional finite-service argument under functioning search/storage/clock and exact execution; perpetual arrivals have no demonstrated uniform latency or bounded queue-memory guarantee.

Choose PATH for graph/radius/horizon fit, CROWD for time-space reservations/admission and collision/deadlock/individual age, PERFORMANCE for representative complete frames. Under overload, budget route capacity, shape arrivals and specify bounded/rejected pending policy; do not hide it by resetting old IDs or raising the deadline. Monitor oldest ID alongside throughput. Dynamic closures need separate occupancy/topology validation and retain earlier synchronous-update limits. Older notes saying native streams pending are superseded only for this bounded static graph contract.

Three sequential native packaged players retain19559 complete frames, baffles/choke×2/4/8requests/sec,20simsec prefill,1real-sec warmup+≥6measure, reversed order run2. Actual births, online reservation/search/admission and completions remain timed with variable active/pending/native render-enabled populations. Overall wall p95 range10.013–11.108ms; measured wall misses101, begin-to-begin cadence misses104; strict no-miss60Hz fails despite good p95. Of wall misses,14carry planning and87do not: do not attribute all tails to search. Planning-current wall max24.671ms and following cadence max24.746ms remain explicit. Current wall ends at End-callback timestamp; subsequent frame-row construction/observer tail remains in begin-to-begin cadence. Preserve these subsets, all raw setup/warmup/tails and unmatched boundaries rather than using overall p95 alone. Async GPU0 is missing; no aligned GPU-tail, cause of nonplanning tails, memory/allocation-rate, cold-goal or Unity speedup claim. Initial pre-callback startup/prefill and final save are outside instrumentation. Five-fraction behavior/15x native video is separate from real-time performance; default visual trails are not physical footprint evidence.

Evidence gates now reconstruct deterministic release epochs and every frame's pending/active/completed and oldest ID from the final lifecycle ledger, plus1e-9s clock/backlog/step conservation and exact planning events. A fresh review found mesh-world-position and release/oldest gaps; native and malformed-evidence RED→GREEN fixes plus96 focused regressions are retained. [Full report and limits](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.md); user acceptance remains separate.


### Route capacity versus request admission — 2026-11-09

[AdmissionLab](../../prototypes/UnrealTechniqueLab/ADMISSION-RESULTS.md) separately compares offered8/sec with FIFO rate/queue controls on the same static radius-compatible time-space graph. Query CROWD for accepted latency/all-offered goodput/rejections and PERFORMANCE for complete frames. A smaller queue or slower admission does not create a larger/faster route; accepted response alone can improve by refusing service. Preserve request age outside the world. Existing exact-route/external-admission/goal-disappearance limits remain, with no arbitrary NavMesh/physics or general capacity theorem transfer.


### Conditional choke horizon pruning — 2026-11-10

[Actual UE5.8.3 trace/fix](../../prototypes/UnrealTechniqueLab/HITCH-RESULTS.md) preserves exact paths with squared swept checks/start-only bins only for cardinal150cm/radii20..60cm/margin4cm. Verify the sole choke cut; next-free boundary+static distance is only a96action impossibility lower bound, never a changed A* tie order. An alternate opening disables it.18compiled checks include50,000 collision comparisons and blocked/released/alternate/same-side cases. Full per-ID paths/service remain equal in12packaged cases and three paired real-time players. Final online-begin maxima do not improve consistently; do not claim this pruning solves the planner tail. See PERFORMANCE for frame/query attribution and CROWD for unchanged admission/service limits. Dynamic topology, long/diagonal motion and larger/mutable radii require a new proof/test.


### Preserve A* ties when caching priority keys — 2026-11-10

The [actual UE5.8.3 equivalent-heap experiment](../../prototypes/UnrealTechniqueLab/PLANNER-RESULTS.md) keeps original graph/schedule/collision rules and changes heap representation only. Integer key `(f<<27)|(distance<<17)|state` exactly implements lexicographic `(time+distance,distance,state)` because74496states fit17bits and distances0..767 fit10bits. Compute once on insertion; retain parent/seen/goal rules and original state on pop.100000priority pairs,180random map/reservation path+expansion comparisons and six complete policy ledgers verify total order and paths. Larger graphs/horizons, weighted/negative/float priorities, heuristic mutation or different tie rules require a new encoding proof; do not truncate/saturate. Additional595968bytes preallocated payload is a memory tradeoff. Query PERFORMANCE for measured speed and observer overhead; faster planning does not enlarge route capacity.


### Keep owned paths when recording a completed planning window — 2026-11-11

The [native owned-snapshot comparison](../../prototypes/UnrealTechniqueLab/SNAPSHOT-RESULTS.md) copies complete admitted paths into an owned record snapshot before the old world is replaced, verifies source mutation/destruction isolation, and writes exact legacy path order/numeric values later. A shared reference into mutable or destroyed planner/world storage is insufficient. Capture includes all original IDs/rejections and current cursor/waits, not just arrived agents. This changes diagnostics/storage, not path priority, feasibility or admission. Query PERFORMANCE for full capture/save/memory costs and PIE for byte/lifetime checks; current full SaveMain is game-thread-only, not a tested background writer.


### Transfer complete frozen paths with background output — 2026-11-11

The [native owned-sync/async verification](../../prototypes/UnrealTechniqueLab/ASYNC-SAVE-RESULTS.md) extends owned path snapshots to all save inputs. Current/case paths, IDs, cursor/waits, coverage, strings, ledger arrays and metadata survive source mutation/destruction; original path/field/record order and values remain exact. Moving only paths while keeping live world/root/frame references is insufficient. Worker output does not change planner tie breaks, admission priority, schedules or feasibility. Query PIE for ownership/lifetime/exactness and PERFORMANCE for capture, drain, memory and shutdown cost. Tested geometry remains static cardinal grid/radii20..60cm/external waiting/full immutable schedules, not arbitrary NavMesh or physics.
