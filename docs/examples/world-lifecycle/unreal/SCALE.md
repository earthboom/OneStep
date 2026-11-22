# Unreal forest scale experiment

The standalone D3D11 benchmark uses eight distinct Unreal level packages, 3,072 authored trees and 2,048 logical NPCs. It visits forest chunks 0, 2 and 5, strikes the wolf in chunk 5, returns to town, then revisits chunk 5. The scripted observer uses the same sequence, camera and 256 pooled mesh Actors near each visited anchor in every mode. The small example still uses its usual **E**, **Space**, **R** and **S** controls.

## Matched configurations

| Mode | Chunk policy | AI evaluation policy |
| --- | --- | --- |
| `resident-full` | Preload all eight chunks and retain them through town and forest | Evaluate all 2,048 patrol agents each simulation sample |
| `streamed-full` | Load the requested chunk asynchronously and release the previous one | Evaluate all 2,048 patrol agents each simulation sample |
| `resident-scheduled` | Preload and retain all eight chunks | Evaluate the local 256 each sample. Resolve the offscreen position and patrol phase from the common clock at observation. |
| `streamed-scheduled` | Load and release as the player progresses | Evaluate the local 256 each sample and observe offscreen state from the common clock. |

Each independent chunk has 384 trunk and canopy pairs, a ground, a road and a trail marker. They are regular static mesh Actors in this fixture. The route changes anchors through `ULevelStreamingDynamic` with a nonblocking request, then waits for visibility and binding. At stable checkpoints the resident policies have all eight levels loaded. The streamed policies have one in forest and zero in town, with the prior level deregistered. Checkpoint logs include the Unreal instance name so an actual streamed re-entry can be distinguished from retained residency. The mesh pool remains allocated, hides its actors in town and clears their identity bindings. Native recently-on-screen render markers verify that forest checkpoints used real rendering.

The benchmark uses a bounded 30 Hz logical clock for matched progress. Each steady segment observes 24 ticks accrued on Unreal world time. It pauses the schedule during loading, cleanup and warmup. Each ordinary NPC has a stable patrol ID and follows a deterministic loop. A proximity test accompanies its sampled pose. Scheduled mode analytically resolves offscreen positions at a checkpoint and rebinds the same identities and poses on arrival. This policy applies to patrols whose elapsed state has a closed form. Interacting NPCs and irreversible events require explicit schedules and event validation.

The shared save reader handles the unchanged v1 and pre-change v2 fixtures. Starting from v1, the wolf migrates to `forest-wolf-v2` at HP 100. Combat leaves HP 60 and quest 1. Its patrol progresses from 0 to 3 while its view is absent. The saved v2 payload is verified in a fresh process. Starting from the old v2 fixture, the same route begins at HP 60, quest 1, patrol 1 and produces HP 20, quest 1, patrol 4, then reopens it in another process. The compatibility slot keeps the original v2 wolf schema. The ambient population is reconstructed from IDs and the route's session clock at each launch.

## Reproduce

Build the Win64 Development `WorldLifecycleEditor` target as in the [project README](README.md). Then run from this directory in PowerShell.

```powershell
$worldEngine = 'C:\Program Files\Epic Games\UE_5.8\Engine'
$worldPython = "$worldEngine\Binaries\ThirdParty\Python3\Win64\python.exe"
& $worldPython -B .\verify_scale.py --rounds 3 --name scale-rerun
```

The verifier varies configuration order across rounds and uses a new process and output slot for every run. A round uses the original v1 fixture across all four modes, followed after the timed matrix by the v1 migration reopen, old-v2 route and v2 reopen. The verifier checks package levels and geometry counts, native viewport and render state, per-frame work, population and actual pose hashes, distinct process and streamed instance IDs, unchanged fixture digests and exact saved values. Raw engine logs, the summary and compressed frame rows are in `Scratch/<name>`. A smoke invocation can add `--rounds 1 --mode streamed-scheduled --skip-compat` with a fresh output name.

The generated chunk assets are included under `Content/Maps/Scale`. To regenerate, use a disposable Unreal project with Python Editor Script Plugin enabled, copy `Content/Materials` from this example into it and run the installed `UnrealEditor-Cmd.exe` with `-run=pythonscript -script=<absolute-path-to-build_scale_maps.py> -nullrhi -unattended` and the disposable project path. The authoring script uses fixed per-chunk seeds. Each saved map has its own asset identity. [Generator](build_scale_maps.py) · [Observed authoring](Evidence/scale-map-authoring.txt)

## What the measurements cover

The `OnBeginFrame` hook records monotonic intervals between Unreal game-loop frames with a reserved array of plain samples. The runner separates resident preload and startup, acquisition and teardown transitions, warmup, steady and explicit garbage-collection frames. The steady intervals enter the measured phase after the same 0.15 game-second warmup. Transition duration is request to observed visibility and binding, or observed removal for the town return. The frame that requests a transition contributes to the transition group. Each row includes measured NPC evaluations, and the verifier recomputes nearest-rank P50, P95 and P99 and the observed maximum. Output serialization occurs after the sampler stops. Startup before the route hook and GPU execution or presentation time fall outside the observation boundary. [Runtime and sampler](Source/WorldLifecycle/Private/WorldScaleRun.cpp) · [Verifier](verify_scale.py)

The engine's Windows process counters provide private commit, current working set, and OS-reported peak commit and peak working set. Checkpoints include town with normal retention, forest before and after combat, town immediately after detach, town after a full garbage collection invoked identically in every mode, and revisit. The fixture records the cleanup frame separately because collection itself can hitch. Reported process memory includes the standalone Editor runtime, allocator reserves, resident packages and pooled views. Machine and shader caches may warm between process launches. The workload uses static engine primitives and analytic patrols, with the same observer across configurations.

## Observed results

Three fresh processes ran each configuration on Unreal 5.8.3, Windows 11, an Intel i7-12700KF and an RTX 3080. The verifier confirmed a 960 × 540 window, an active D3D11 device, native on-screen rendering, VSync 0 and `t.MaxFPS` 0. All modes produced identical population and visible pose hashes at the matched checkpoints. The cases represent this 6,176-geometry-actor sample and a fixed near-view workload. [Run summary](Evidence/scale-summary.json) · [Raw frame rows](Evidence/scale-frames.json.gz) · [Build](Evidence/scale-build.txt)

| Mode | Median steady frames per run | Steady P50 / P95 / P99 (ms) | Worst steady (ms) | Transition P95 (ms) | Worst transition (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `resident-full` | 980 | 3.61 / 9.24 / 9.95 | 17.75 | 9.33 | 9.65 |
| `streamed-full` | 1,143 | 2.98 / 8.91 / 9.61 | 11.58 | 20.65 | 34.04 |
| `resident-scheduled` | 995 | 3.59 / 9.14 / 9.84 | 11.19 | 8.93 | 9.61 |
| `streamed-scheduled` | 1,154 | 3.00 / 8.93 / 9.53 | 15.22 | 23.10 | 29.10 |

Quantiles are medians of per-process nearest-rank results. Worst values are maxima across the three runs. There were 30 resident-baseline transition samples and 168 combined-mode transition samples across their three processes. Forest-only steady P95 was 9.46 ms in `resident-full`, 9.10 ms in `streamed-full`, 9.20 ms in `resident-scheduled` and 9.05 ms in `streamed-scheduled`. The per-anchor distributions and startup and cleanup rows are in the summary.

| Mode | Offscreen town private commit (MiB) | Peak working set through revisit (MiB) | Initial preload (ms) | First entry (ms) | Revisit (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| `resident-full` | 2,410.1 | 2,228.3 | 662.1 | 5.7 | 3.8 |
| `streamed-full` | 2,314.6 | 2,154.5 | 9.3 | 96.1 | 78.3 |
| `resident-scheduled` | 2,411.1 | 2,230.1 | 660.5 | 4.9 | 9.2 |
| `streamed-scheduled` | 2,311.1 | 2,152.8 | 10.1 | 97.4 | 78.2 |

The two residency policies move cost between preload and arrival. The combined policy used about 99 MiB less private commit at the offscreen town checkpoint, with a 97.4 ms first-entry wait. Scheduling cut measured evaluation work from 2,048 per steady frame to 256 in the forest and zero in town. The two streamed configurations had nearly the same all-route steady P95. This simple patrol workload shows the reduction in work more clearly than an incremental change in overall frame cadence.

Separate launches reopened the v1 migration, played the genuine pre-change v2 slot through the same scaled route, and reopened the new v2 output. The unchanged fixture digests and the canonical wolf state are in the [compatibility observations](Evidence/scale-compatibility.json). The [small example regression](Evidence/scale-small-regression.json) retains its original one-hit, one-patrol-step outcome and a clean v2 reopen on the expanded binary.
