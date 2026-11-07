---
id: "K-CODE-PERFORMANCE-MEASUREMENT"
title: "Measure representative workloads before trading clarity for optimization"
summary: "Set relevant latency, throughput and memory budgets, characterize the workload and locate the limiting work before optimizing. Check that a benchmark measures the intended operation and preserve correctness and maintainability alongside measured gains."
kind: "reference"
scope: "Application and systems performance decisions including game frame-time and allocation costs; tools and measurement interpretation remain runtime-specific"
keywords: ["profiling", "benchmark", "latency", "throughput", "allocation", "cache", "performance-budget", "성능", "프로파일링", "벤치마크", "할당", "프레임시간", "측정"]
status: "active"
checked_at: "2026-11-07"
context: {"evidence_check": "Named original author papers or official text sections inspected; specific limits in Evidence", "application_status": "Source-based reference and proposed synthesis; no local implementation or runtime validation"}
---

# Measure representative workloads before trading clarity for optimization

## Guidance

Source observations: Gregg begins with a stated problem and workload, then selects CPU, waiting or resource analysis according to the limiting behavior [S1]. His active-benchmarking method inspects the system while a benchmark runs to identify what it actually stresses [S2]. Google Benchmark documents repetition, timing choices and compiler-elimination caveats [S3].

Proposed method: define the important user operation and acceptable cost before expanding a performance-sensitive design. Record build mode, hardware/runtime, dataset, load and measurement boundary. Separate end-to-end latency from a local microbenchmark and distinguish retained memory, allocation rate and peak working set.

Inspect where the time or memory goes. Compare the smallest justified algorithm, data-layout, allocation or scheduling change under the same contract and representative conditions. Record costs introduced by caching, batching, pooling, shared state or concurrency, including invalidation and lifetime obligations. Keep a clear baseline and recheck the complete operation after a local improvement.

## Applicability and exceptions

Measurement is not a reason to postpone an already required real-time or memory constraint until late production. Debug results, artificial hot caches and unrepresentative inputs do not automatically transfer to release behavior. DoNotOptimize does not prevent every optimization inside an expression. A pool may retain memory and a cache may worsen locality or correctness; more concurrency can increase contention.

## Checks

Proposed checks: was the intended operation executed and its result consumed? Is the observed limiter consistent with the proposed explanation? Does a repeated gain matter against the relevant budget, including tail behavior? Compare failure and cleanup behavior, review readability cost, and retain environment/results. This reference does not claim a measured optimization of the current repository.

## Evidence

- [S1] Brendan Gregg, [Performance Analysis Methodology](https://www.brendangregg.com/methodology.html), Problem Statement / Workload Characterization / CPU Profile / Off-CPU Analysis.
- [S2] Gregg, [Active Benchmarking](https://www.brendangregg.com/activebenchmarking.html), Summary / Active Benchmarking / Statistics.
- [S3] [Google Benchmark User Guide](https://google.github.io/benchmark/user_guide.html), CPU Timers / Preventing Optimization / Reporting Statistics.
- Author/official text checked 2026-11-07; linked talks were not viewed and no benchmark or performance experiment was executed here.
