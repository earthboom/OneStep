# Large forest streaming and offscreen AI benchmark

This extends the [town and forest examples](README.md) with an opt-in workload. The comparison is between four configurations of the large example on the same engine and machine. The original small example provides a compatibility regression check.

## Workload and decision

Use eight independently loadable forest chunks and 2,048 logical NPCs, distributed as 256 per chunk. Exercise the same controls along town → chunk 0 → chunk 2 → chunk 5 → combat → town → chunk 5. Each visible region uses the same local representation in all modes. Chunk partitioning changes how much of the forest is loaded. AI scheduling changes the work performed for offscreen NPCs while retaining their persistent identity and the required state at gameplay checkpoints.

| Mode | Forest residency | Offscreen AI |
| --- | --- | --- |
| `resident-full` | All forest chunks | Full per-frame work |
| `stream-full` | Only the chunks needed for the route | Full per-frame work |
| `resident-coarse` | All forest chunks | Scheduled, coarse updates |
| `stream-coarse` | Only the chunks needed for the route | Scheduled, coarse updates |

The four configurations let the streaming comparison keep AI scheduling fixed and the AI comparison keep residency fixed. The `resident-full` to `stream-coarse` comparison estimates the combined effect in this workload. Any change in when the same content is prepared is part of the streaming cost. Record preload and transitions as well as steady play.

Unity generates 700 scene objects per chunk, including terrain, trees, rocks and NPC views, then renders to a 1280 × 720 D3D11 target in the Windows Player. The probe checks rendered pixels. Unreal uses separately authored level packages with 384 trees per chunk and a pool of 256 local views, in a 960 × 540 standalone D3D11 world. Its `streamed` and `scheduled` flags correspond to the `stream` and `coarse` columns above.

## Evidence and acceptance

- Verify both committed input fixtures. [The v1 fixture](fixtures/legacy-v1.json) starts with HP 100, quest stage 0 and patrol step 0. [The v2 fixture](fixtures/legacy-v2.json) is the unchanged slot written by the previous Unity Player's published run 1. It contains the same state as the previous Unreal slot, including HP 60, quest stage 1 and patrol step 1. Its SHA-256 is `44cb52114209ca4edd9154941b9e2824bdd1703b24e1c57036b6d75c0b055053`. Verify the canonical ID, round-trip result, and state during absence and after re-entry. Also verify the durable state of the larger logical NPC population where it affects equivalence.
- Use the same executable, renderer, settings and input route across configurations within each engine. Repeat in fresh processes and record run order, host, sample counts, and any pilot or outlier relevant to interpretation. OS file caches can remain warm across processes. The Unity and Unreal workloads are comparable in structure; their assets and engine timings are different.
- Capture wall-clock game-loop cadence in milliseconds, with steady and transition samples marked separately. Report per-run percentiles and the median of the repeated run-level statistics. Keep readiness measurements and startup or preload time separately where available. A main-loop cadence interval does not identify how much time the GPU spent on a frame.
- Measure private committed bytes and working-set bytes from the same sampler and at the same route checkpoints. Label sampled peak and town-after-unload separately. A level can leave the active world while engine or graphics resources remain cached. Use the resident chunk and NPC work counts to confirm that the intended mechanism actually changed. [Windows process memory metrics](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters_ex) · [Unity unused asset release](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/resources/unloadunusedassets) · [Unreal level streaming](https://dev.epicgames.com/documentation/en-us/unreal-engine/level-streaming-in-unreal-engine)

The existing example and the new modes share the loader and save format. Keep the small example runnable by default, and route all measured runs through actual engine Player or Game execution. Record any deliberate simplifications of the NPC decision workload and the exact scope of the equivalence checks.

## Unity observations

Unity 6000.0.77f1 ran four fresh Windows Players per configuration, with each mode occupying each run-order position once. Each mode used v1 twice and v2 twice. The results are medians of the four per-process nearest-rank measurements. Town memory is sampled after unloading and resource cleanup, at the end of the offscreen stage. The peak columns are the largest observed samples per process during the route, including preload. [Unity run instructions](unity/README.md) · [Unity evidence summary](unity/Evidence/scale/summary.json)

| Mode | Steady p50 / p95 / p99 (ms) | Transition p95 (ms) | Town private / working set (MiB) | Sampled peak private / working set (MiB) |
| --- | ---: | ---: | ---: | ---: |
| `resident-full` | 0.468 / 0.648 / 0.794 | 0.800 | 400.0 / 216.8 | 401.0 / 217.5 |
| `stream-full` | 0.440 / 0.633 / 0.783 | 0.935 | 374.8 / 206.4 | 375.7 / 207.0 |
| `resident-coarse` | 0.464 / 0.628 / 0.755 | 0.799 | 401.4 / 216.8 | 401.5 / 217.4 |
| `stream-coarse` | 0.456 / 0.628 / 0.839 | 0.970 | 371.9 / 204.2 | 373.1 / 204.7 |

Streaming with full AI saved about 25 MiB of town private commit. With both switches enabled, the saving was about 28 MiB and transition p95 rose by 0.17 ms. Scheduled updates reduced offscreen NPC work over the identical 552-tick route from 1,032,192 to 86,016. The overall steady p95 change was only about 0.02 ms, and the combined steady p99 increased. These are offscreen D3D11 render-loop timings. The player read back a forest image to verify render output. Display pacing, GPU time and VRAM require different measurements.

Median preload changed from 41.11 to 1.62 ms, first-visit readiness from 1.01 to 7.37 ms, and revisit readiness from 0.08 to 3.86 ms. The resident mode pays to prepare all chunks at startup. The streamed mode loads each visited chunk at its point of use.

## Unreal observations

UE 5.8.3 ran three fresh processes per configuration with an i7-12700KF, RTX 3080 and D3D11. Each entry below is the median of the three per-process measurements. Steady and transition frame figures are nearest-rank percentiles of game-loop intervals. Memory uses MiB. Town memory is taken at the end of the offscreen stage, after the explicit cleanup performed in all four configurations. Peaks are OS process peaks observed at route checkpoints and can include initialization. [Unreal run instructions and evidence](unreal/SCALE.md)

| Mode | Steady p50 / p95 / p99 (ms) | Transition p95 (ms) | Town private / working set (MiB) | Peak private / working set (MiB) |
| --- | ---: | ---: | ---: | ---: |
| `resident-full` | 3.61 / 9.24 / 9.95 | 9.33 | 2,410 / 2,225 | 2,470 / 2,228 |
| `streamed-full` | 2.98 / 8.91 / 9.61 | 20.65 | 2,315 / 2,140 | 2,377 / 2,155 |
| `resident-scheduled` | 3.59 / 9.14 / 9.84 | 8.93 | 2,411 / 2,226 | 2,475 / 2,230 |
| `streamed-scheduled` | 3.00 / 8.93 / 9.52 | 23.10 | 2,311 / 2,133 | 2,378 / 2,153 |

Disabling offscreen evaluation with the forest still resident cut town checks from 2,048 to zero per steady frame. Near the player, scheduled mode evaluates 256 NPCs per steady frame. Steady p95 changed by about 0.10 ms in the resident pair. Streaming with full AI already saved about 96 MiB of town private commit and increased transition p95 by 11.32 ms. Combined with scheduling, the saving was about 99 MiB and transition p95 was 23.10 ms. This workload supports the reduction in work and memory. Its three-process tail measurements support only a small change in steady cadence.

Resident preload shifted time out of later visits. The median preload took 662.09 ms with all chunks resident and full AI, and 10.15 ms in the streamed/scheduled case. Median first visit readiness changed from 5.72 to 97.39 ms, with a revisit change from 3.78 to 78.23 ms. Readiness is elapsed request-to-usable time across frames. Counts of transition frames differ substantially by mode, so the transition percentiles are coarse estimates.

## State and compatibility results

- Unity completed 16 distinct Windows Player processes. Both input fixtures retained their original bytes. The loader preserved their starting states, and each run read back its new v2 slot. Population digests agreed at matching ticks for every configuration within each input version. The patrol target `1297` retained 65 HP and advanced while no local view existed. In streamed mode, a newly loaded view projected its current state on re-entry. [Native run data](unity/Evidence/scale/raw.json.gz) · [Original route regression](unity/Evidence/scale/small-regression.json)
- Unreal completed 12 measured processes and three separate compatibility launches. Matching checkpoints compared the population and visible pose hashes. The detached wolf retained HP 60 and quest stage 1 from the v1 route. Its patrol advanced to 3 and a fresh process restored the saved result. The original v2 fixture opened at HP 60, quest stage 1 and patrol step 1. After the larger route it reopened at HP 20, quest stage 1 and patrol step 4. Both input hashes remained unchanged. [Native run data](unreal/Evidence/scale-frames.json.gz) · [Compatibility evidence](unreal/Evidence/scale-compatibility.json) · [Original route regression](unreal/Evidence/scale-small-regression.json)

The existing slot format continues to store the canonical wolf and quest state. The larger population check applies to the active session, including unloading and re-entry. The benchmark's scheduled behavior is deterministic patrol evaluation. It exercises the cost and ownership boundary for offscreen AI with a bounded, reproducible workload.
