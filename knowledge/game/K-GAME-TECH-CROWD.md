---
id: K-GAME-TECH-CROWD
title: Scale crowd decisions separately from crowd rendering
summary: Separate collision safety, routing, admission and individual service. Compare
  accepted response with all-offered on-time goodput/rejection; bounded FIFO queues
  require controlled spawning and exact route execution.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- crowd
- Mass
- avoidance
- AI
- LOD
- spatial
- hash
- 군중
- reservation
- dynamic-obstacle
- 국소회피
- 동적장애물
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
  application_status: Scoped Unity streams plus UE5.8.3 dynamic and authored mixed-radius
    opposing Game/PIE evidence; scoped native static unlaned FIFO streams verified;
    no arbitrary/infinite-time guarantee
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
### Native unlaned sustained arrivals — 2026-11-09

[UE5.8.3 StreamLab](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.md) adds25 C++ checks, ten actual PIE and ten full-cook packaged expectations with identical per-ID/action ledgers. Eight FIFO cases complete3120valid requests and explicitly reject one unreachable request. Seven meet240s release-to-completion; overloaded choke is collision-safe and drains but61IDs exceed240s(max280s), so **latency fails**. LIFO completes538later IDs by310s while ID0 remains unadmitted; this is censored individual waiting, not an infinite-time observation. Disabling reservations exposes actual collision. First waits, five native fractions/action and terminal segments reconcile per ID; native capsule, mesh world position/scale and actual wall queries have deliberate corruption controls.

**Conditional use:** static32x24 undirected four-neighbor graph150cm cells, authored portals but no prescribed lanes, fixed20/35/60cm circles and4cm swept margin,300cm/s,0.5s actions, complete≤96action immutable routes, one authority, FIFO controlled admission with pending bodies outside the world and goal disappearance. This is not arbitrary continuous NavMesh, ORCA/PIBT/RHCR, physics pushing, acceleration, mutable radii/topology or unscheduled existing actors. Pending age starts at request, not spawn. For a fixed ID, finitely many older FIFO jobs and finite complete-route service support only a conditional finite-service argument under functioning search/storage/clock and exact execution; perpetual arrivals have no demonstrated uniform latency or bounded queue-memory guarantee.

Choose PATH for graph/radius/horizon fit, CROWD for time-space reservations/admission and collision/deadlock/individual age, PERFORMANCE for representative complete frames. Under overload, budget route capacity, shape arrivals and specify bounded/rejected pending policy; do not hide it by resetting old IDs or raising the deadline. Monitor oldest ID alongside throughput. Dynamic closures need separate occupancy/topology validation and retain earlier synchronous-update limits. Older notes saying native streams pending are superseded only for this bounded static graph contract.

Three sequential native packaged players retain19559 complete frames, baffles/choke×2/4/8requests/sec,20simsec prefill,1real-sec warmup+≥6measure, reversed order run2. Actual births, online reservation/search/admission and completions remain timed with variable active/pending/native render-enabled populations. Overall wall p95 range10.013–11.108ms; measured wall misses101, begin-to-begin cadence misses104; strict no-miss60Hz fails despite good p95. Of wall misses,14carry planning and87do not: do not attribute all tails to search. Planning-current wall max24.671ms and following cadence max24.746ms remain explicit. Current wall ends at End-callback timestamp; subsequent frame-row construction/observer tail remains in begin-to-begin cadence. Preserve these subsets, all raw setup/warmup/tails and unmatched boundaries rather than using overall p95 alone. Async GPU0 is missing; no aligned GPU-tail, cause of nonplanning tails, memory/allocation-rate, cold-goal or Unity speedup claim. Initial pre-callback startup/prefill and final save are outside instrumentation. Five-fraction behavior/15x native video is separate from real-time performance; default visual trails are not physical footprint evidence.

Evidence gates now reconstruct deterministic release epochs and every frame's pending/active/completed and oldest ID from the final lifecycle ledger, plus1e-9s clock/backlog/step conservation and exact planning events. A fresh review found mesh-world-position and release/oldest gaps; native and malformed-evidence RED→GREEN fixes plus96 focused regressions are retained. [Full report and limits](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.md); user acceptance remains separate.


### Native admission/queue comparison — 2026-11-09

[AdmissionLab](../../prototypes/UnrealTechniqueLab/ADMISSION-RESULTS.md) compares six policies under identical offered8requests/sec: FIFO unlimited/1physical admission per second(burst2) × pending cap none/32/64. Two paired workloads480offers/60sec/seed0 and960offers/120sec/seed19 have twelve actual PIE and twelve full-cook standalone ledgers. Tail reject newly offered jobs only; preserve original IDs/request ages and older accepted FIFO order. Immediate queue-full rejection never counts as completed service.240s target remains unchanged.

Short workload: fifo-none-short: 480/480completed, 0.0%rejected, accepted max280.0s, all-offered ontime87.3%; fifo-cap32-short: 160/480completed, 66.7%rejected, accepted max72.0s, all-offered ontime33.3%; fifo-cap64-short: 196/480completed, 59.2%rejected, accepted max95.0s, all-offered ontime40.8%; meter-none-short: 480/480completed, 0.0%rejected, accepted max439.0s, all-offered ontime53.1%; meter-cap32-short: 93/480completed, 80.6%rejected, accepted max54.5s, all-offered ontime19.4%; meter-cap64-short: 125/480completed, 74.0%rejected, accepted max87.0s, all-offered ontime26.0%. Use accepted response together with **all-offered on-time goodput, completion ratio, rejection ratio/reason and throughput**. Bounded queues can lower accepted latency by refusing work; admission throttling does not increase route capacity and can worsen uncapped waiting. Do not pool zero-time rejections into completed latency or reset age at physical spawn. Offer-window throughput and full-drain throughput have different denominators; both are in the report. Every offer is accounted for, with no hidden producer queue/retries/eviction.

Conditional use only under static graph/fixed footprints/whole immutable routes/exact scheduled execution/external waiting/goal disappearance.1/sec and32/64are experiment settings, not optimal/general capacity. If every offer must be served, these drop policies do not meet that requirement; specify upstream backpressure with original demand age retained or change route/service capacity and revalidate. Inspect per-source portal/radius and second-half acceptance, not just aggregate rejection: deterministic batching/tail-drop can bias source access. Accepted FIFO does not establish fair new-request acceptance; no source-fair scheduler or retry policy is implemented. Pending cap excludes active units and **does not bound retained job/ledger history, allocations or total memory**. No arbitrary NavMesh/physics/dynamic geometry/infinite-time fairness guarantee. Prior dynamic-update and nonplanning frame-tail issues remain separate.

18C++ policy checks,8native policy-label/shape/visual-world-pose/query corruption groups and127focused regressions are retained. Independent replay reconstructs every offer, rejection decision, eligible FIFO prefix, token refill/spend and oldest pending ID; native first/interior/terminal samples reconcile with accepted lifetimes. See [results](../../prototypes/UnrealTechniqueLab/ADMISSION-RESULTS.md) for measured whole-frame tradeoffs and actual15x video. This is local engineering synthesis/empirical evidence, not a transferred network/crowd theorem or universal default.


### Insights-confirmed admission hitches — 2026-11-10

[Actual same-binary trace and three-pair experiment](../../prototypes/UnrealTechniqueLab/HITCH-RESULTS.md) identifies two different costs: render hardware-query waits in this flat non-occluding viewport and online time-space planning. Preserve exact named Game Frame alignment, CPU/render/RHI blocking relationships and clipped inclusive scope unions; do not add overlapping ancestors or infer driver/display/power root cause. Use the actual trace for attribution and untraced equal-demand players for performance comparison. Baseline measured wall/cadence misses 88/80; optimized 29/20, three finite runs each. All startup/setup/warmup and event-current/following tails remain attached. Queries are disabled only for this diagnostic viewport. Occluded3D content requires separate visibility/GPU measurement; this is not a global renderer default.

Squared synchronous swept checks with a near-boundary original-math fallback and start-only edge bins preserve the supported cardinal one-cell150cm/radius20..60cm/margin4cm contract (max reach124cm). A verified sole-cell-cut next-free-boundary lower bound prunes only impossible96action states, retaining original A* priority/tie order. Revalidate for alternate openings, diagonal/long moves, bigger/mutable footprints or topology mutation; exact reservations remain the collision authority. First math/index-only trace still had20.10ms online begin and was insufficient. Final traces still retain planner/Present tails; these fixes do not establish strict60Hz or fix earlier dynamic rebuild spikes.

Twelve final packaged completed fixtures exactly match previous per-ID paths/policy/action/audit records; two actual PIE fixtures agree. Three baseline/optimized pairs match every common simulated lifecycle/path/token/queue boundary. Source service/rejection/latency remains unchanged: no faster rendering claim may hide dropped offers, younger spawn clocks or altered policy. New18C++ checks (including50,000 collision decisions), existing policy18/stream25/traffic26/crowd13/representative73 and148Python checks include wrong viewport/profile rejection. Fixed-time15x native media are separate from timing. Infinite-horizon fairness, retained-history memory/allocations, cold goals, arbitrary NavMesh/physics/dynamic geometry remain unverified.


### Faster search must preserve individual service — 2026-11-10

The [actual UE5.8.3 equivalent-heap experiment](../../prototypes/UnrealTechniqueLab/PLANNER-RESULTS.md) preserves every original request's exact path, admission/completion/rejection epoch, admission order/token/FIFO ledger and native5fraction/terminal audits. Twelve packaged completed fixtures match prior records; two actual PIE fixtures match package; three same-binary real-time pairs match common-epoch lifecycles. Full expanded/collision/heap work counts also agree in diagnostic comparisons. Do not infer preserved service from aggregate throughput alone or silently defer admission/reset spawn age to distribute CPU work. Pending/external/full immutable route/disappearance/static cardinal footprint conditions remain. Overload deadline failures, source acceptance bias, finite versus infinite fairness and retained history memory limits remain unchanged.


### Observer optimization must keep every offered record — 2026-11-11

The [native owned-snapshot comparison](../../prototypes/UnrealTechniqueLab/SNAPSHOT-RESULTS.md) replaces retained per-value record DOM with complete owned typed records/direct output. Original jobs/paths/admission/completion/rejection/order/token/action/native5fraction/terminal audits match across12packaged fixtures,2actual PIE and3real-time pairs. No requests/fields/refusals/path nodes are dropped, reordered or assigned younger spawn ages. Movement safety/throughput/rejection and overload deadline/source fairness limits remain unchanged. Faster recording does not create route capacity or prove infinite fairness. External pending/full immutable schedules/static cardinal footprint and retained-history memory caveats still apply.


### Keep crowd service and save queue admission distinct — 2026-11-11

The [native owned-sync/async verification](../../prototypes/UnrealTechniqueLab/ASYNC-SAVE-RESULTS.md) moves fully owned diagnostic serialization/file writing to a worker while original offered IDs/ages/path/admission/completion/rejection/token/ledger and full native movement audits remain equal. Writer overflow is a separate diagnostic submission result and must never become game-request rejection or reset an agent age. The prototype has one final save per fixture; queue2stress and explicit write failure are compiled worker controls. No record/agent is dropped to improve performance. Native12completed fixtures+2PIE and3paired policies preserve original service/safety. Async saving does not raise route capacity, prove infinite fairness, remove source bias or fix dynamic-update spikes.
