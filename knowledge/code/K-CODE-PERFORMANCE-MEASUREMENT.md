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
keywords: ["profiling","benchmark","latency","throughput","goodput","tail latency","p95","frame pacing","fixed timestep","token bucket","FIFO","backpressure","Unreal Insights","Timing Insights","occlusion query","Render Hardware Interface","Present","binary heap","snapshot lifetime","working set","private commit","benchmark::DoNotOptimize","성능","프로파일링","프레임 시간","비동기 저장"]
status: active
checked_at: '2026-11-11'
context:
  engine: "Historical UE 5.8.3 Windows D3D11 real-time packaged workloads and separate PIE behavior checks"
  evidence: "Methodology survey and bounded frame, planner, queue and completed-simulation save comparisons; no production guarantee"
---

## Guidance

Define the user operation, workload, correctness contract and budget first. Separate latency for an individual request, throughput per unit time, allocation rate, retained memory and peak process memory. Inspect the system during the benchmark to verify what limits it. In a microbenchmark, consume results and inspect generated work where necessary. `benchmark::DoNotOptimize` helps keep a result observable but still permits optimization of its expression.

**Pooling and caching.** Object pooling (메모리 풀링) reuses allocated storage or object instances. Compare creation and reset costs, allocation rate, retained capacity, cache locality and tail frame time under the same live population. Include pool warmup, release and reacquisition. A lower allocation count can coexist with higher retained memory or stale state. Caching, batching and concurrency likewise have invalidation, latency or contention costs; repeat the end-to-end benchmark after any local improvement.

**Frame time.** In Unreal Insights, use Timing Insights to select a complete frame and inspect Game, Render, Render Hardware Interface (RHI) and available GPU tracks. A callback measures only its own start-to-end interval. Start-to-start cadence also includes time between callbacks. Align work with the named frame and the following cadence interval, retain startup, warmup, steady state, observer overhead, final save and exit boundaries. Clip and union nested or concurrent timer spans before attributing elapsed time. A CPU wait in `Present` identifies a blocked thread. GPU work, display pacing and driver causes require separate evidence. Toggle an occlusion query only as a diagnostic in the same scene and check visibility and GPU cost before keeping the change.

**Equal work.** Compare interleaved runs of the same executable, viewport, rendering settings, data and input schedule. Preserve frame counts, percentiles, maxima and deadline-miss counts per condition. A passing p95 allows individual deadline misses. For a fixed timestep of duration h, verify each row satisfies previous backlog + elapsed wall time − steps × h = new backlog, including any explicitly discarded time as a separate term. Reconstruct arrivals, queue depth, oldest request and each consumer's lifetime. A token bucket allows bursts from accumulated credits and limits admission over time. A FIFO queue admits the oldest eligible item first. Report latency among accepted requests alongside refusals and on-time goodput (original requests completed on time per unit time) at the same offered load. An age measured at spawn omits time spent waiting for admission.

**Algorithm and recording changes.** With a binary heap, precomputed packed priority keys can reduce comparator work. Check representable bit ranges, tie order, per-request paths and expansion counts, then measure the memory added per planner. Fine-grained timers can perturb short calls. Use them for attribution and repeat with coarse tracing and tracing disabled. For recording changes, measure snapshot capture, serialization, write, cleanup, publication-to-acknowledgement and launch-to-exit time. Compare complete output and ownership after the input is changed or destroyed. Backpressure limits accepted work when a writer falls behind. Include active and queued inputs in its byte budget, and measure the producer, encoding buffers and retained history separately. Private commit measures process-private committed memory on Windows. Working set measures resident pages. Periodic samples can miss short-lived peaks.

## Applicability and exceptions

These checks apply to comparable loads with an observable result and trace boundary. A synthetic scene, static route graph, fixed camera, accelerated capture, Debug binary or editor session cannot establish a packaged game's frame deadlines. A bounded queue leaves other memory consumers unbounded. Capacity, latency, fairness, dynamic topology changes, live autosaves and driver-level causes each need evidence in the target workload.

## Checks

- Run the baseline and candidate in alternating order, retaining each denominator, individual missed deadlines and where callbacks cannot see work. Use the original input IDs and identical simulation epochs to detect missing or reordered work.
- Challenge the verifier with a dropped sample, corrupted intermediate counter, wrong executable identity or output with altered order or values. Match build identity against the artifact actually launched.
- For background saves, separate game-thread submission and receipt, worker time, draining and process shutdown. Exercise queue-full, write failure and shutdown with accepted work. A buffered close and rename alone do not establish crash durability.

## Evidence

The primary methodology survey dates to 2026-11-07. Historical UE 5.8.3 Windows/D3D11 comparisons on 2026-11-09–11 exercised the frame, queue, planner and save checks above. They observed deadline misses despite acceptable p95, rendering waits outside planner work, and different capture and finalization costs. The save comparison covered an already-finished simulation. Registered report IDs identify historical evidence. This review checked Epic's profiler description and did not rerun the workloads.

- [Brendan Gregg, Performance Analysis Methodology](https://www.brendangregg.com/methodology.html) · [Active Benchmarking](https://www.brendangregg.com/activebenchmarking.html)
- [Google Benchmark User Guide](https://google.github.io/benchmark/user_guide.html) · [Epic, Timing Insights](https://dev.epicgames.com/documentation/unreal-engine/timing-insights-in-unreal-engine?application_version=5.8)
- [Frame and world checks](../sources.md#src-ue-lab-editor-gate-results-md) · [Variable frame workloads](../sources.md#src-ue-lab-dynamic-results-md) · [Per-consumer checks](../sources.md#src-ue-lab-traffic-results-md)
- [Sustained load](../sources.md#src-ue-lab-stream-results-md) · [Admission](../sources.md#src-ue-lab-admission-results-md) · [Frame attribution](../sources.md#src-ue-lab-hitch-results-md) · [Planner comparison](../sources.md#src-ue-lab-planner-results-md)
- [Snapshot ownership](../sources.md#src-ue-lab-snapshot-results-md) · [Asynchronous publication](../sources.md#src-ue-lab-async-save-results-md)
