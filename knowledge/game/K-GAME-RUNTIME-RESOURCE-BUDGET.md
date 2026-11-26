---
id: K-GAME-RUNTIME-RESOURCE-BUDGET
title: "Diagnose long frames and choose spawning, pooling or streaming"
summary: "Trace CPU, GPU, I/O and activation separately on a repeatable route. Select a resource strategy according to its measured cost, lifetime, reuse and failure behavior."
kind: method
scope: "Frame time, first entry, resident memory and content streaming on a supported game device."
keywords: ["frame time","rendering optimization","object pool","streaming","resource cache","hitch","PSO","프레임 드롭","렌더링 최적화","오브젝트 풀링","캐시","스트리밍","최초 로딩","메모리 예산","스폰"]
status: active
checked_at: "2026-11-22"
---
# Diagnose long frames and choose spawning, pooling or streaming

## Guidance

Fix device, build, resolution, quality, camera and route. Split first visit, warm-up and steady-state. Read overlapping CPU/GPU work and waits on a timeline. Resolution scaling probes pixel cost, submission timings probe draw calls and state changes, and individual passes distinguish shadows, skinning and particles. Investigate first-entry I/O, decompression, upload and PSO compilation independently. Compare median, p95/p99, over-budget frequency and duration.

Batching and instancing can trade submissions for memory, shader constraints and coarser culling. Occlusion queries have their own synchronization and test costs. Evaluate LOD/HLOD silhouettes and transitions during rapid travel. For GPU-driven rendering measure the work moved onto the GPU and its memory cost. Inspect visual losses after removing a pass.

Spawn on demand if frequency and latency permit. Pool repeatedly expensive objects with an exhaustion policy and reset timers, callbacks, HP and physics state on reuse. Cache expensive derived results using input, version and spatial range as the key. Bake stable work when invalidation is reliable. Stream when travel predicts future demand. Start preload distance at speed × preparation time plus margin, stagger activation, and cancel or release obsolete requests.

## Applicability and exceptions

A downloaded file can still require decompression, upload and activation. A pool retains objects and a cache retains results. Neither removes shader compilation. ARC's resistance to sequential scans was studied for storage caches. Compare scan and revisit workloads before transferring the policy. Procedural geometry that changes gameplay may require generator versions and persistent edits.

## Checks

Run village → forest → skirmish → village on the same device. Capture narrow alleys, open forest, crowds and night separately. Teleport, reverse course, burst-spawn objects and reuse one before its old callback returns. Check readiness latency, peak and retained memory, per-frame activation, visual transitions, cache invalidation and correct state on return. Disk speed, memory pressure and camera behavior can change the result.

## Evidence

The November 22 development practices review compared original mesh/culling papers, shipped engine and streaming talks, profiling manuals and a storage-cache study. Talks were represented by available session descriptions and slides. The village route is a proposed experiment.

[Performance measurement](../code/K-CODE-PERFORMANCE-MEASUREMENT.md) · [Simulation fidelity](K-GAME-NPC-SIMULATION.md)

- [Unity profiling](https://unity.com/how-to/best-practices-for-profiling-game-performance) · [Unreal profiling](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine) · [Unreal Fest frame timing video](https://www.youtube.com/watch?v=dKSHw_8vz3I) · [Unity rendering captures](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/profile-rendering) · [Unreal dynamic resolution](https://dev.epicgames.com/documentation/en-us/unreal-engine/dynamic-resolution-in-unreal-engine)
- [Unreal PSO Precaching](https://dev.epicgames.com/documentation/unreal-engine/pso-precaching-for-unreal-engine) · [Unity PSO warm-up](https://docs.unity.com/en-us/engine/6000.3/manual/materials-and-shaders/shaders/shader-troubleshooting/shader-reduce-stalling/shader-prevent-stutter/shader-pso-trace-warming/shader-pso-introduction) · [Unity draw call optimization](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/reduce-draw-calls/optimizing-draw-calls-choose-method) · [Unity URP GPU culling](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/in-urp/gpu-culling) · [Unreal visibility and occlusion](https://dev.epicgames.com/documentation/en-us/unreal-engine/visibility-and-occlusion-culling-in-unreal-engine)
- [Hoppe, SIGGRAPH 1996 — Paper](https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Hoppe96.pdf) · [Bittner et al., 2004 — Paper](https://www.cg.tuwien.ac.at/research/publications/2004/Bittner-2004-CHC/Bittner-2004-CHC-Paper.pdf) · [Haar and Aaltonen, SIGGRAPH 2015 — Slides](https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf) · [Karis et al., SIGGRAPH 2021 — Talk video](https://www.youtube.com/watch?v=eviSykqSUUw) · [SIGGRAPH materials](https://advances.realtimerendering.com/s2021/Karis_Nanite_SIGGRAPH_Advances_2021_final.pdf)
- [Epic technical documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-technical-details) · [O’Donnell — GDC talk](https://www.gdcvault.com/play/1024612/) · [Joshua Simmons — GDC talk](https://www.gdcvault.com/play/1034412/Upgrading-the-Snowdrop-Engine-for) · [Development team's technical introduction](https://www.massive.se/article/crafting-pandoras-breathtaking-landscape-with-snowdrop/)
- [Nystrom, Object Pool](https://gameprogrammingpatterns.com/object-pool.html) · [Dirty Flag](https://gameprogrammingpatterns.com/dirty-flag.html) · [Unity pooling guidance](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/performance-memory/managed-memory/optimizing-code-managed-memory/reusable-code) · [Elan Ruskin — GDC talk](https://www.gdcvault.com/play/1022268/Streaming-in-Sunset-Overdrive) · [Elan Ruskin — Slides](https://media.gdcvault.com/gdc2015/presentations/Ruskin_Elan_SunsetOverdriveStreaming.pdf)
- [Chad Barb — Video](https://www.youtube.com/watch?v=4BuvKotqpWo) · [Chad Barb — Slides](https://media.gdcvault.com/gdc2017/Presentations/Barb_Chad_EfficientTextureStreaming.pdf) · [Innes McKendrick — GDC talk](https://www.gdcvault.com/play/1024265/Continuous-World-Generation-in-Noby) · [Megiddo and Modha, FAST 2003 — Paper](https://www.usenix.org/legacy/publications/library/proceedings/fast03/tech/full_papers/megiddo/megiddo.pdf) · [World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine)
- [Addressables memory 2.7](https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/MemoryManagement.html) · [DirectStorage](https://learn.microsoft.com/en-us/xbox/gdk/docs/features/console/storage/directstorage/directstorage-overview?view=gdk-2604)
