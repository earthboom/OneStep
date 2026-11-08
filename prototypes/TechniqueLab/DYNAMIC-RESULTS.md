# Dynamic obstacles, local avoidance and whole frames — 2026-11-08

The dedicated DynamicLab scene extends the original prototype without resetting movers when obstacles change. Final Editor PlayMode and three sequential Windows release players each passed **12 regression checks and six scenario expectations** (five safe scenarios plus an unsafe sensitivity control). Safe scenarios completed without observed pair/wall penetration, teleport, reservation error or stale-field consumption. Whole-frame measurements were collected from genuinely rendered players. The 16.67 ms p95 target passed across all three runs in **6/6** count/mode combinations. This is evidence for these windows and movement conditions, not a stable 60 FPS shipping guarantee.

## Mechanism and adoption trace

[PATH](../../knowledge/game/K-GAME-TECH-PATH.md) supplied shared-goal distance fields and topology invalidation; [CROWD](../../knowledge/game/K-GAME-TECH-CROWD.md) separated routing, local conflict avoidance and rendering. Adopted: single-owner four-neighbor grid, equal discs of radius 0.20, speed 3 units/s, unit-cost travel, one right-edge exit region, two single-cell wall openings. A zero-cost connection from each exit-strip node to one sink computes the shared potential; movers never execute nonlocal edges.

The local avoidance method reserves current and destination cells, chooses a free downhill neighbor or yields, and rotates arbitration order. This conservative cooperative rule keeps roughly one-cell spacing despite smaller discs; it trades throughput and free-form movement for simple safety conditions. It is not ORCA, and inherits none of ORCA's velocity-space guarantees. Opposing traffic, different radii, diagonals, continuous obstacle velocities, forces and animated bodies require new design/checks. The [ORCA authors' formulation](https://gamma-web.iacs.umd.edu/ORCA/) was consulted to distinguish that alternative; its implementation and performance were not reproduced.

Closing a cell immediately blocks it for new routes and rebuilds the field. Its physical collider waits until existing reservations drain, then becomes solid. Reopening refreshes routes immediately. A crate moves by removing one cell obstacle and requesting another; this is discrete topology change, not continuous rigid-body obstacle prediction. IDs and positions survive all changes. Arrival removes agents at the exit strip, while door/obstacle changes never respawn them. The original scene's reset-at-door illustration remains a separate historical baseline.

## Behavior evidence

| Scenario | Arrived / agents | Simulated seconds | Overlapping pair observations |
| --- | --- | --- | --- |
| occupied-door | 16/16 | 16.35 | 0 |
| all-blocked | 32/32 | 34.23 | 0 |
| moving-crate | 32/32 | 17.68 | 0 |
| dense-64 | 64/64 | 31.27 | 0 |
| dense-256 | 256/256 | 101.47 | 0 |
| avoidance-disabled-control | 11/32 | 10.00 | 8979 |

The first five rows are safe-mode completion tests. The last row intentionally disables avoidance, stops after ten simulated seconds, and must detect overlap; its incomplete evacuation is not counted as a safe result. Overlap observations repeat across ticks, not unique incidents. In the occupied-door case the disc was geometrically inside the door volume at the request, and closure committed **0.4167 simulated seconds** later; all 16 arrived and 15 used the alternate opening. All-routes-blocked safely waited between close at 2 s and reopen at 6 s. Neither behavior is an instantaneous crushing-door simulation.

Behavior playback runs eight 1/60-second ticks per rendered frame; these evacuation times are simulated time, not measured real-time performance. An independent geometric audit observes each tick, including terminal movement segments; native Unity CheckSphere queries inspect actual obstacle colliders once per behavior display frame. The pair audit interpolates the recorded short cardinal step segments; walls are checked geometrically at step endpoints. These checks cover the declared small steps, not arbitrary curved trajectories or fast external rigid bodies. Full-frame performance uses a separate real-time 60 Hz accumulator with audits disabled.

## Failed-then-passed corrections

- [Initial minimal kernels](Results/Dynamic/red-lifecycle.json): five failures of eight; the implemented lifecycle passed [eight checks](Results/Dynamic/green-lifecycle.json).
- Independent review found repeated crate movement selecting walls, paused controls leaving visual/native state stale, and arrival removal skipping the final audit segment. [Four regressions failed](Results/Dynamic/red-review.json); cycling valid floor cells, synchronizing public controls and retaining previous-active status passed all twelve in the [final PlayMode report](Results/Dynamic/dynamic-editor-final.json). The terminal-audit test deliberately injects an overlap at arrival.
- The occupied-door scenario was strengthened to require actual geometric body occupancy, beyond a reserved destination. [The previous trigger failed](Results/Dynamic/red-body-coverage.json); requesting later inside the volume passed. Earlier rendered measurements remain in `Results/Dynamic/pre-body-capture`, with their deadline misses intact. Current-source performance windows are reported below; the earlier and later batches are not silently pooled.
- [Final player 1](Results/Dynamic/dynamic-run-1.json.gz), [player 2](Results/Dynamic/dynamic-run-2.json.gz), [player 3](Results/Dynamic/dynamic-run-3.json.gz) contain all observations. Their process manifests preserve exit 0, current source hashes, executable hash and managed-assembly hash. [Build](Results/Dynamic/build.json): release Mono2x, timing stats enabled, zero errors. [Analyzer](analyze_dynamic.py) validates structure, geometry outcomes, continuous wall-row numbering, timing arithmetic, constant active counts, counter coverage and source/binary identity; [summary](Results/Dynamic/summary.json).
- Actual public-window checks confirmed paused close/open state changes, repeated crate control, restart/resume and Quit. [UI observation](Results/Dynamic/ui-observation.json) and [native process record](Results/Dynamic/dynamic-ui-process.json). These are AI observations, not user acceptance or a player study. Camera.Render images exclude OnGUI: [512-agent scene](Results/Dynamic/dynamic-run-3-agents-512-reserved.png), [occupied pending door](Results/Dynamic/dynamic-run-3-occupied-door-pending.png).

## Whole-frame results

Unity 6000.0.77f1, Windows 11, i7-12700KF, RTX 3080, Direct3D11, release Mono; actual render size **1280×720**, vSync 0, MSAA 2, uncapped during measurement. The 64×40 scene renders unlit cylinders, floor, wall/door/crate boxes, exit strip and OnGUI. No skinning, production art, shadows workload or gameplay/network systems are represented. Build GUID `e99bbee9006c4aae9df6459b830c168d`. Three sequential processes use comparison orders reserved/route-only, reversed, then original; counts progress 64/256/512.

Each case warms for one second and records six seconds; all 149,913 wall intervals are retained. Active counts stayed exactly 64/256/512 throughout, with no arrival/respawn during the windows. Close-main, place-crate and reopen-main events occur inside every measured case. Full frame intervals include game loop, simulation, native physics/transform synchronization, rendering, presentation/waits, instrumentation and host scheduling. JSON writes, scene setup and captures are outside the windows. Frame interval is throughput timing, not input-to-photon latency. CPU and GPU activities overlap and must not be added.

Ranges below are the minimum/maximum of each process's statistic, not pooled confidence intervals. Percentiles use nearest rank. No frame stalls, GC events or deadline misses were trimmed: 1 measured frames exceeded 16.67 ms, with a maximum 19.11 ms. Meeting a p95 target does not mean every frame met the deadline. The unsafe route-only comparison retains equivalent counts/rendering but has different collision behavior; its timing is not an equivalent safe replacement.

| Agents / mode | Wall median ms | Wall p95 ms | Engine CPU-frame p95 ms | Frames >16.67 ms |
| --- | --- | --- | --- | --- |
| 64 / Reserved | 0.33–0.35 | 2.23–2.61 | 2.21–2.57 | 0.000–0.000% |
| 64 / Route only | 0.32–0.34 | 2.29–2.59 | 2.28–2.54 | 0.000–0.010% |
| 256 / Reserved | 0.43–0.44 | 2.55–3.03 | 2.54–2.99 | 0.000–0.000% |
| 256 / Route only | 0.43–0.45 | 2.63–3.02 | 2.62–2.98 | 0.000–0.000% |
| 512 / Reserved | 0.54–0.57 | 2.87–3.15 | 2.86–3.10 | 0.000–0.000% |
| 512 / Route only | 0.55–0.58 | 2.83–3.18 | 2.82–3.12 | 0.000–0.000% |

| Reserved agents | Controller/sync per-frame p95 ms | Simulation-bearing controller/sync p95 ms | Render-thread p95 ms | Positive GPU samples |
| --- | --- | --- | --- | --- |
| 64 | 0.063–0.073 | 0.087–0.110 | 0.185–0.202 | 91.6–93.6% |
| 256 | 0.094–0.102 | 0.137–0.158 | 0.275–0.289 | 91.4–92.6% |
| 512 | 0.130–0.144 | 0.169–0.215 | 0.341–0.357 | 90.8–91.3% |

Controller timing includes obstacle transactions, fixed-step movement, transform/native synchronization and its event instrumentation; it excludes the rest of Unity/rendering. At uncapped render rates, many frames execute no 60 Hz movement tick. The separate simulation-bearing column includes only frames that actually ran one or more movement steps; use it when budgeting a tick rather than confusing idle rendering frames with simulation work. Raw wall intervals include every frame, and the summary also records the following interval associated with each simulation-bearing row. The maximum observed obstacle-transaction timer was 0.275 ms. Raw event frame IDs connect that component work to the following whole-frame interval; they do not prove all stalls were caused by rebuilding. The maximum retained simulation backlog was 0.016667 s; excess wall time is kept for bounded catch-up rather than discarded. This small controller cost does not establish a whole-game frame budget.

**GPU limitation:** 11,887/149,913 GPU fields were unavailable (zero), with per-case positive coverage 90.5–93.9%. Raw zero fields remain in the source reports; valid-only observations are separately labelled in the summary. We withhold GPU-tail validation and do not use zero as a free frame. Render-thread/CPU timing and all wall intervals were retained. Unity documents asynchronous delayed availability and possible GPU resource failures ([Frame Timing Manager, availability](https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/profile-rendering/frame-timing-manager/manager)); timestamps are deduplicated, and GPU results are not aligned to the current event frame.

All six final count/mode combinations met the p95 target in each of the three short windows. Earlier rendered captures had 512-agent reserved p95 24.61–31.24 ms. No performance optimization was established between those and the final batch: the occupied-body test/pending display changed, and host load was uncontrolled. Preserve both batches rather than claiming that those changes fixed frame pacing.

The desktop, other applications, GPU load, clocks and thermal state were not isolated or controlled. Presentation waits and frame-time variation are observed; their precise root cause is not established by this experiment. Adoption remains **conditional**: reprofile the actual target scene/hardware and investigate the complete frame/presentation path before promising stable 60 FPS. Do not infer a universal supported agent count from these six-second windows.

## Reproduce and applicability

From this directory, close this project in the Editor before CLI runs. Use the Unity path configured in Run-Editor.ps1. Existing local licensing required execution outside the sandbox; no credentials/settings were changed.

```powershell
./Run-Editor.ps1 -Method DynamicBatch.Play -Graphics -Report dynamic-editor-final.json -Log dynamic-editor-final.log
./Run-Editor.ps1 -Method DynamicBatch.Build -Log dynamic-build-final.log
./Run-Dynamic.ps1 -Session dynamic-run-1 -Visible -Order 0
./Run-Dynamic.ps1 -Session dynamic-run-2 -Visible -Order 1
./Run-Dynamic.ps1 -Session dynamic-run-3 -Visible -Order 0
python ./analyze_dynamic.py
./Run-Dynamic.ps1 -Session dynamic-ui -Interactive
```

`-Visible` is required for measured players: hidden/batch pilots returned zero render/GPU counters and were rejected. Their lossless raw evidence is retained as gzip pilot files, separate from the three accepted rendered measurement sessions. Preserve historical files by choosing new session names and explicitly changing analyzer input names. The analysis requires assertions enabled. Open `Assets/DynamicLab.unity` for manual engine use; public controls expose pause, doors, crate, restart and Quit.

Use this approach for centrally owned grid agents sharing a reachable exit/cost profile where queuing and deferred closure are acceptable. Revalidate collision clearance, mutation ownership, closing policy, liveness and frame budget with actual agents. For a door that must close immediately onto a body, define push/crush/cancel behavior separately. This experiment supplies no general starvation proof, multi-authority protocol or continuous-crowd solver. PATH/CROWD and the retrieval guide now link these outcomes and conditions; cumulative limited engine evidence covers four technique sheets, with 39 still unvalidated in a local engine.

## Storage and retrieval verification

The strict game catalog passed 69 entries with zero errors/warnings ([record](Results/Dynamic/catalog-check.json)). Existing retrieval checks passed 23 common, 11 game application and 20 extended cases. Three new symptom/mechanism/frame-budget cases initially passed 2/3: a traversal/topology query omitted PATH from the first three results ([red](Results/Dynamic/retrieval-dynamic-red.json)). PATH's summary and topology/door/traversal identifiers were clarified; the same unchanged cases then passed 3/3 ([result](Results/Dynamic/retrieval-dynamic.json)). All 57 cases pass after the update. This tests declared discoverability, not autonomous decisions on unseen requests. Raw gzip identity and document links/translation-pair existence are checked separately; human translations are generated from canonical/authored sources without reading their contents.
