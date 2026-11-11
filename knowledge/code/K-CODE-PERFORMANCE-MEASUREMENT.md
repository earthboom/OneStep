---
id: K-CODE-PERFORMANCE-MEASUREMENT
title: Measure representative workloads before trading clarity for optimization
summary: Set relevant latency, throughput and memory budgets, characterize the workload
  and locate the limiting work before optimizing. Check that a benchmark measures
  the intended operation and preserve correctness and maintainability alongside measured
  gains.
kind: reference
scope: Application and systems performance decisions including game frame-time and
  allocation costs; tools and measurement interpretation remain runtime-specific
keywords:
- profiling
- benchmark
- latency
- throughput
- allocation
- cache
- performance-budget
- 성능
- 프로파일링
- 벤치마크
- 할당
- 프레임시간
- 측정
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
  evidence_check: Named original author papers or official text sections inspected;
    specific limits in Evidence; local Unreal trace evidence checked 2026-11-09
  application_status: Scoped UE5.8.3 frame/CPU wait trace method executed; no universal
    optimization or driver-level cause proven
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

# Measure representative workloads before trading clarity for optimization

## Guidance

Source observations: Gregg begins with a stated problem and workload, then selects CPU, waiting or resource analysis according to the limiting behavior [S1]. His active-benchmarking method inspects the system while a benchmark runs to identify what it actually stresses [S2]. Google Benchmark documents repetition, timing choices and compiler-elimination caveats [S3].

Proposed method: define the important user operation and acceptable cost before expanding a performance-sensitive design. Record build mode, hardware/runtime, dataset, load and measurement boundary. Separate end-to-end latency from a local microbenchmark and distinguish retained memory, allocation rate and peak working set.

Inspect where the time or memory goes. Compare the smallest justified algorithm, data-layout, allocation or scheduling change under the same contract and representative conditions. Record costs introduced by caching, batching, pooling, shared state or concurrency, including invalidation and lifetime obligations. Keep a clear baseline and recheck the complete operation after a local improvement.

### Local Unreal trace follow-up — 2026-11-09

[Actual PIE, final package and instrumented hitch investigation](../../prototypes/UnrealTechniqueLab/EDITOR-GATE-RESULTS.md) distinguish complete-frame cadence from scalar/Actor subsets, fixed-time capture, async counters and nested trace scopes. In these D3D11 fixtures, GameThread waits on renderer/RHI/presentation dominate investigated tails; a query-off control removes a query wait without eliminating presentation stalls. This supports locating the limiting work before tuning pathfinding. It does not prove a driver cause or a production rendering change. The older open-Editor and latest closed-Editor/light-mobility contexts are not an isolated optimization comparison. The first trace retains incomplete original launch provenance; the others bind actual source/binary identity.

### Native dynamic-frame acceptance follow-up — 2026-11-09

[Unreal dynamic crowd](../../prototypes/UnrealTechniqueLab/DYNAMIC-RESULTS.md) retains44740 rendered frames and reconciles measured duration with cadence, wall cost, real-time steps and retained backlog. A fresh review reproduced acceptance of missing counters/cadence and fabricated tiny walls; six malformed-evidence regressions now reject those records. Require these independent arithmetic checks alongside exact source/build/scenario identity; a native `passed` flag and positive scalar samples cannot certify six seconds of complete frames.

This fixture also distinguishes a passing p95 from a hard deadline: all18 p95 values meet16.67ms while54 synchronous topology-change+native-sync calls coincide with all54 measured misses. Their15.594–19.539ms cost is not planner-only. Preserve every startup/setup/warmup and measured sample, distinguish render-enabled component counts from pixel visibility, and do not confuse accelerated behavior movies or audit-enabled behavior costs with real-time performance. No target-game optimization or general throughput guarantee was executed.

### Per-frame and consumer-coverage acceptance — 2026-11-09

[Native opposing traffic](../../prototypes/UnrealTechniqueLab/TRAFFIC-RESULTS.md) exposed three further evidence gaps: valid final totals still accepted corrupted intermediate backlog/ticks/components/warmup population; aggregate native query count did not establish per-ID coverage; recorded identity fields were not checked against the final built artifact. Seven malformed-data regressions reproduced these holes before correction;59 focused regressions pass afterward.

For a60Hz accumulator, verify every row `B_i = B_(i-1) + wallDelta_i - steps_i/60`, monotonic elapsed/ticks, bounded catch-up, and component times contained in work/frame time. Final totals alone cannot certify all intermediate rows. Check constant active/render-enabled count throughout warmup as well as measurement. Reconcile each consumer's query count with its lifetime including terminal tick, and require the observed source/config/project/module/player/harness hashes to match an immutable identity derived from the verified build. Hash presence alone is not identity verification. Exact event IDs bind event-current and following cadence costs without an arbitrary timer threshold. These are executed fixture checks, not a universal profiler or adversarial attestation scheme.

## Applicability and exceptions

Measurement is not a reason to postpone an already required real-time or memory constraint until late production. Debug results, artificial hot caches and unrepresentative inputs do not automatically transfer to release behavior. DoNotOptimize does not prevent every optimization inside an expression. A pool may retain memory and a cache may worsen locality or correctness; more concurrency can increase contention.

## Checks

Proposed checks: was the intended operation executed and its result consumed? Is the observed limiter consistent with the proposed explanation? Does a repeated gain matter against the relevant budget, including tail behavior? Compare failure and cleanup behavior, review readability cost, and retain environment/results. This reference does not claim a measured optimization of the current repository.

## Evidence

- [S1] Brendan Gregg, [Performance Analysis Methodology](https://www.brendangregg.com/methodology.html), Problem Statement / Workload Characterization / CPU Profile / Off-CPU Analysis.
- [S2] Gregg, [Active Benchmarking](https://www.brendangregg.com/activebenchmarking.html), Summary / Active Benchmarking / Statistics.
- [S3] [Google Benchmark User Guide](https://google.github.io/benchmark/user_guide.html), CPU Timers / Preventing Optimization / Reporting Statistics.
- Author/official text checked 2026-11-07; linked talks were not viewed. No experiment was executed during that source survey; subsequent scoped local trace evidence is linked above.
### Native unlaned sustained arrivals — 2026-11-09

[UE5.8.3 StreamLab](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.md) adds25 C++ checks, ten actual PIE and ten full-cook packaged expectations with identical per-ID/action ledgers. Eight FIFO cases complete3120valid requests and explicitly reject one unreachable request. Seven meet240s release-to-completion; overloaded choke is collision-safe and drains but61IDs exceed240s(max280s), so **latency fails**. LIFO completes538later IDs by310s while ID0 remains unadmitted; this is censored individual waiting, not an infinite-time observation. Disabling reservations exposes actual collision. First waits, five native fractions/action and terminal segments reconcile per ID; native capsule, mesh world position/scale and actual wall queries have deliberate corruption controls.

**Conditional use:** static32x24 undirected four-neighbor graph150cm cells, authored portals but no prescribed lanes, fixed20/35/60cm circles and4cm swept margin,300cm/s,0.5s actions, complete≤96action immutable routes, one authority, FIFO controlled admission with pending bodies outside the world and goal disappearance. This is not arbitrary continuous NavMesh, ORCA/PIBT/RHCR, physics pushing, acceleration, mutable radii/topology or unscheduled existing actors. Pending age starts at request, not spawn. For a fixed ID, finitely many older FIFO jobs and finite complete-route service support only a conditional finite-service argument under functioning search/storage/clock and exact execution; perpetual arrivals have no demonstrated uniform latency or bounded queue-memory guarantee.

Choose PATH for graph/radius/horizon fit, CROWD for time-space reservations/admission and collision/deadlock/individual age, PERFORMANCE for representative complete frames. Under overload, budget route capacity, shape arrivals and specify bounded/rejected pending policy; do not hide it by resetting old IDs or raising the deadline. Monitor oldest ID alongside throughput. Dynamic closures need separate occupancy/topology validation and retain earlier synchronous-update limits. Older notes saying native streams pending are superseded only for this bounded static graph contract.

Three sequential native packaged players retain19559 complete frames, baffles/choke×2/4/8requests/sec,20simsec prefill,1real-sec warmup+≥6measure, reversed order run2. Actual births, online reservation/search/admission and completions remain timed with variable active/pending/native render-enabled populations. Overall wall p95 range10.013–11.108ms; measured wall misses101, begin-to-begin cadence misses104; strict no-miss60Hz fails despite good p95. Of wall misses,14carry planning and87do not: do not attribute all tails to search. Planning-current wall max24.671ms and following cadence max24.746ms remain explicit. Current wall ends at End-callback timestamp; subsequent frame-row construction/observer tail remains in begin-to-begin cadence. Preserve these subsets, all raw setup/warmup/tails and unmatched boundaries rather than using overall p95 alone. Async GPU0 is missing; no aligned GPU-tail, cause of nonplanning tails, memory/allocation-rate, cold-goal or Unity speedup claim. Initial pre-callback startup/prefill and final save are outside instrumentation. Five-fraction behavior/15x native video is separate from real-time performance; default visual trails are not physical footprint evidence.

Evidence gates now reconstruct deterministic release epochs and every frame's pending/active/completed and oldest ID from the final lifecycle ledger, plus1e-9s clock/backlog/step conservation and exact planning events. A fresh review found mesh-world-position and release/oldest gaps; native and malformed-evidence RED→GREEN fixes plus96 focused regressions are retained. [Full report and limits](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.md); user acceptance remains separate.


### Measure equal offered demand and refusals — 2026-11-09

[Native admission comparison](../../prototypes/UnrealTechniqueLab/ADMISSION-RESULTS.md) holds offered load8/sec while varying FIFO admission rate(unlimited/1per sec burst2) and pending cap(none/32/64). Compare accepted latency against all-offered on-time goodput/rejection and throughput; silently reducing offered demand or dropping queued IDs invalidates the comparison. Twelve paired PIE/standalone fixtures and three sequential packaged6policy players preserve live births, online plans/admissions/rejections/completions and variable populations.120simsec prefill exercises capped queues and sustained unbounded backlog;1real-sec warmup+≥6measure, reverse policy order run2.

All22389 observed frame pairs retained; measured wall misses103, cadence misses97 at16.667ms. Inspect per-policy current planning wall/following cadence, all setup/warmup and unmatched boundaries. Current wall ends at End timestamp; following cadence includes row-observer tail. Initial pre-callback startup/prefill and final save excluded; later setup/prefill and case snapshot/ledger construction included, so maxima can contain diagnostic work. Async CPU/render/wait/GPU are not frame-aligned GPU tails; GPU0missing. No memory/allocation-rate/cold-goal guarantee. Motion blur disabled consistently for this experiment; no speedup claim against older differently rendered StreamLab. A pending cap does not cap retained history or erase offered work. Do not infer planner causality from every frame miss or use p95 alone to claim strict60Hz.


### Attribute before changing frame settings — 2026-11-10

[UE5.8.3 Insights experiment](../../prototypes/UnrealTechniqueLab/HITCH-RESULTS.md) maps exact GFrameCounter to named Game Frame N, checks trace duration containment and retains observer/end tails. Nonplanning query waits, planning work, Present and scene-prefill setup are separate. Clip and union timer intervals; inclusive ancestors overlap and must not be added. CPU wait timers locate blocking, not ultimate driver/DWM/power cause; GPU tracks have separate availability. A one-variable diagnostic is a hypothesis check, not untraced speedup proof. Use three interleaved baseline/optimized players from the same executable with exact1280x720, offered8/sec, six policies,120simsec prefill,1real-sec warmup+≥6measure and order0/1/0. Compare exact original-ID routes/admission/rejection/credits/lifecycle at common simulated boundaries, not only aggregate throughput.

Baseline measured wall/cadence misses 88/80 over16779frames; optimized 29/20 over20804frames. Denominators differ with render speed; retain per-run/per-policy p95,max,deadline counts,current-plan/following cadence and all phases. Query suppression is local to a flat non-occluding viewport; do not transfer to occluded3D without visibility/GPU checks. Planner and Present tails remain, so p95 or reduced counts do not prove strict60Hz. Initial pre-callback prefill and final save remain outside callback wall, visible separately in trace. Pending/history allocation and cold-goal costs remain unmeasured. See raw native Insights exports and same-binary untraced evidence, not historical103misses as a causal baseline.


### Find repeated heap work inside a planner — 2026-11-10

The [actual UE5.8.3 equivalent-heap experiment](../../prototypes/UnrealTechniqueLab/PLANNER-RESULTS.md) separates whole-frame/current-plan/following cadence and opt-in internal clocks. Initial aggregate diagnostics attributed55–56% of plan time to heap sifts and17–18% to collision queries under three unlimited-admission policies; rebuild was small. These cycle reads perturb short calls: use them for diagnosis, then turn them off in final coarse Insights and untraced same-binary3paired players. Never use detailed timings as final frame speedup. A planning-bearing wall maximum can contain case-snapshot work; separately select maximum online planning (plannerPeak), retaining both exact named-frame windows and all observer/setup tails. CPU Present wait does not establish ultimate driver/display/GPU cause.

Equivalent packed `(time+distance,distance,state)` keys remove repeated division/modulo/heuristic lookup from sift comparisons. Final reference wall/cadence misses27/19 over23274frames; improved11/2 over21292frames. See per-run online-begin p95/max and full frame distributions in the report rather than historical different-build timings. Equal expanded/Safe/candidate/heap-call counts and exact per-request paths/orders/service are verified, so less timed work is not hidden by skipped requests or failed searches. Extra preallocated heap payload595968bytes per planner is explicit; no allocation-rate/cold-start/memory improvement or universal deadline guarantee follows.


### Snapshot boundaries are not the whole recording cost — 2026-11-11

The [native owned-snapshot comparison](../../prototypes/UnrealTechniqueLab/SNAPSHOT-RESULTS.md) separates request DOM/path/ledger creation, immutable capture, initial setup/five transitions, root build/deferred conversion/serialization/write/local cleanup and launch→observed exit. Initial diagnosis found request DOM5.39–6.04ms inside6.19–6.86ms boundaries; paths0.38–1.00ms are a nested subset, not additive. Final same-binary3pairs keep1280x720/8offers/sec/sixpolicies/prefill/warmup/order and include coarse timers/memory observer in both variants; detailed clocks/trace/capture are off. Reference wall/cadence misses10/1, streamed0/0. Inspect all per-run boundary/save/exit costs and output/frame denominators; lower capture cost alone is not total improvement.

Callback wall ends before final save and has no following cadence at exit. Preserve the full named final Insights frame/saveTail and native lifecycle, not an apparent no-stall claim from measured p95. Windows process working set/private commit and lifetime peaks include startup/render/frame-observer data; external20ms samples are lower-bound samples, not exact allocation rates. Logical per-record JSON-value count0 means record DOM avoided, not all allocations0. Owned raw array/path/string capacities replace DOM and are not net process growth. Frame counts affect retained observer memory. Signed boundary growth, save-time peaks and retained bytes stay attached. Synchronous final save/Present/dynamic-update/history-memory limits remain.


### Measure background-save publication, completion and drain separately — 2026-11-11

The [native owned-sync/async verification](../../prototypes/UnrealTechniqueLab/ASYNC-SAVE-RESULTS.md) compares three interleaved same-binary owned-sync/owned-async pairs,1280x720/8offers per second/six unchanged policies and identical planner/snapshot settings. Typed frame storage and detached standard encoder are common to both; representation savings versus historical frame DOM are not attributed to dispatch. Measure GT capture+submit, actual worker serialize/write/release, publication→ack, GT receipt/finalize, queue charge/count, drain-frame wall/next cadence, shutdown drain, launch→exit and process private/working-set lifetime peaks. Inclusive parent/child scopes and overlapping GT/worker spans are not additive. Async can lower publication blockage without lowering total CPU, total file latency or peak memory.

Main diagnostic rows seal at original fixture completion; extra sidecar rows account for final frozen-scene rendering during save. This verifies finished-fixture output, not live autosave while simulation mutates. A callback sampled before publication excludes save; retain full native named publication-through-finalize frames/worker scopes. External20ms private samples are lower bounds; OS peaks sampled at ack do not certify every shutdown allocation. Queue2/64MiB limits accepted-input capacities, excluding producer, allocator overhead, FString/UTF8 output, rendering and unbounded retained history. A bounded queue is not a total process-memory bound. Prior Present/dynamic rebuild/fairness limits remain independent.
