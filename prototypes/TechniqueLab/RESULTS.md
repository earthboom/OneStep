# Technique Lab results — 2026-11-07

Three representative stored techniques were implemented and exercised in Unity 6000.0.77f1: elapsed-time camera damping, camera-intent/muzzle-constrained hitscan, and a shared weighted reverse-Dijkstra field. Final Editor PlayMode and three sequential standalone processes each passed 27 assertions plus three real Update timing trials. The Windows build succeeded with zero build errors. These are small experimental scenes, not production-game or player-experience validation.

## Retrieval and adoption trace

| Problem and retrieved knowledge | Decision and implementation | Actual check and adoption condition |
| --- | --- | --- |
| Camera feel changes with rendered FPS; [CAMERA](../../knowledge/game/K-GAME-TECH-CAMERA.md), Guidance | Adopt `1-exp(-rate*dt)` for a stationary framing target; retain 10% per-frame lerp as a sensitivity control. | Synthetic 30/60/144 steps, hitch and zero-dt checks; actual Update trials integrate exactly two seconds. Moving targets, prediction, dead zones and collision require separate checks. |
| Camera sees a target while the weapon is behind cover; [HITSCAN](../../knowledge/game/K-GAME-TECH-HITSCAN.md), Guidance/Checks | Adopt camera aim intent, origin-overlap guards, root-to-muzzle obstruction and first muzzle hit, with explicit layer/trigger filters. Reject camera-only damage in this fixture. | Closed/open/inside/beyond-wall origins, ignored triggers/layers and actual scene controls. Static box colliders only; network authority and pose history remain conditional. |
| Many sources share one exit; [PATH](../../knowledge/game/K-GAME-TECH-PATH.md), weighted successor/zero-cost clauses | Adopt one reverse field for a stable graph/exit. Retain independent A* for comparison and different query structures. Bind cache to graph identity and revision. | Known weighted/directed/zero-cost/unreachable cases, 160 independent Floyd-Warshall comparisons per algorithm, invalidation and door controls. Local collision avoidance and moving-agent reconciliation are separate work. |

## Environment and evidence

- Unity 6000.0.77f1, built-in renderer, Windows standalone Mono2x; no third-party assets or registry packages.
- Windows 11 10.0.26200; i7-12700KF, 20 logical processors, 65,395 MB system memory; RTX 3080 / Direct3D11, 10,053 MB reported graphics memory.
- Build GUID `1fbb60d030dd4a7b81305edd3a7fc38c`; build size 86,307,080 bytes. [Build record](Results/build.json).
- [Final editor report](Results/editor-play-final.json); [player 1](Results/player-run-1.json), [player 2](Results/player-run-2.json), [player 3](Results/player-run-3.json). Their `*-process.json` records preserve native exit code, executable SHA-256, C# source hashes and UTC intervals. All three native exits were 0; the player binary and source hashes match across runs.
- [Analysis script](analyze_results.py) independently checks raw/normalized timing arithmetic, median/p95, work/query counts, equal path checksums, check results and current source identity; [summary](Results/summary.json) retains ranges. Assertions must remain enabled when running this Python script.

The desktop was not isolated from other applications. CPU clocks, thermal state and OS scheduling were not controlled. Runs were sequential, not concurrent with each other. These numbers describe this host, backend, fixture and workload; they are not estimates for mobile, IL2CPP, multiplayer, a complex scene or other engines.

## Behavior and corrections

Initial deliberately incomplete kernels produced [13 failures of 21](Results/red-checks.json); implemented kernels passed [21/21](Results/green-checks.json). A further check exposed a real cache bug: two distinct graphs with equal revision counters incorrectly shared validity ([red: 1/22](Results/red-graph-identity.json)). Binding the owner object as well as revision passed [22/22](Results/green-final-checks.json). The runtime adds five checks through actual scene consumer controls, producing 27/27 in every final engine run.

A controlled early runtime error also exposed a harness bug: assigning the later assertion count erased an already logged error ([old report: failures 0](Results/red-error-sentinel.json)). Accumulating failures preserved the error ([fixed report: failures 1](Results/green-error-sentinel.json)); the actual Unity process exited 2 as intended. This sentinel is an expected failing run, not a normal acceptance failure. Pilot reports/captures predate these corrections and calibrated batches; use only the final editor and three player records for current results.

The field and A* were compared separately against Floyd-Warshall on 16 deterministic ten-node directed graphs including zero-cost links (160 source/goal comparisons per algorithm). These bounded cases are useful regressions, not an exhaustive proof for every float weight or graph. The 32×32 scene renders 64 consumers following stored successors. Toggling its door invalidates/rebuilds the field **and resets consumers to safe initial cells**. This demonstrates route stop/resume, not safe reconciliation of agents already traversing a closing door. No local avoidance is implemented.

Actual Windows UI inspection found the three demos and OnGUI controls rendered. `Cycle cover` changed `safe blocked` true → false → true while camera intent stayed true; `Toggle grid door` changed false → true → false and the visible consumers stopped/restarted. `Reset followers` accepted input; its exact instantaneous reset was not instrumented in this UI check. `Quit` exited 0 and the prototype window disappeared ([interactive process](Results/interactive-check-process.json)). These are AI observations in this chat, not user acceptance or a usability study. Automated PNGs use `Camera.Render`, so they capture the world **without OnGUI**; [final player capture](Results/player-run-3.png) was inspected separately from the live controls. UI text is functional prototype presentation, not a finished game HUD.

## Elapsed-time camera response

Start 0, stationary target 10, rate 4, exact integration interval 2 seconds; expected value `10*(1-exp(-8)) = 9.99664497`. Last `dt` is clamped to the remaining interval; all actual step sequences are retained. The reported achieved FPS uses real wall time, not the requested cap.

| Requested FPS | Achieved FPS range, three players | 10% per-frame lerp final | Exponential maximum absolute error |
| --- | --- | --- | --- |
| 30 | 29.993–30.001 | 9.98203182 | 0 at reported float precision |
| 60 | 59.973–59.998 | 9.99996853 | 0.000000954 |
| 144 | 143.888–143.983 | 9.99999619 | 0.000001907 |

All errors were below the predeclared 0.0001 tolerance. This verifies a stationary target's elapsed-time response under these steps. A moving target sampled once per frame does not inherit that exact invariance. Input latency, framing quality, camera collision and player comfort were not measured.

## CPU operation costs

Eight warmup invocations per variant; repeat count doubles during calibration toward a 3 ms timed batch, up to 1,048,576 repetitions. Collect 31 samples per variant, alternating forward/reverse variant order. Each sample is normalized by its repetitions; p95 is nearest-rank sample 30 of 31. Tables give the **range of per-process medians and per-process p95 values** across three players, not a pooled confidence interval. Calibration targets 3 ms; later batches can be shorter (minimum observed player batch 2.1794 ms). Raw batches avoid the pilot's timer-resolution problem. No samples were removed.

Stopwatch covers repeated CPU operations and their checksum/delegate work, with setup, assets, I/O and rendering outside it. Normalized p95 describes repeated batch throughput, not an individual operation's tail latency. It does not measure whole frames or GPU time. Group-level GC collection counts were zero in all player groups; this does not prove zero allocation, and no separate allocation profiler was used. Repeated hot data/poses are intentionally small; cache behavior in a real game can differ.

| Camera operation: 100,000 scalar followers per invocation | Median range ms | p95 range ms |
| --- | --- | --- |
| Fixed 10% lerp | 1.708–1.751 | 1.938–2.194 |
| Exponential computed per follower | 2.429–2.813 | 2.849–3.419 |
| Exponential alpha shared for identical rate/dt | 1.711–1.755 | 1.920–2.086 |

Compute alpha once when the followers actually share rate and `dt`. This CPU math test has no transforms or rendering and is not the cost of a camera system; a single camera does not justify bulk-update optimization.

| Native physics: 1,024 shot resolutions per invocation | Median range ms | p95 range ms | Native queries per shot |
| --- | --- | --- | --- |
| Camera-only, closed offset cover | 0.274–0.298 | 0.309–0.379 | 1 |
| Safe resolve, closed offset cover | 0.973–0.997 | 1.166–1.306 | 5 |
| Camera-only, open | 0.278–0.349 | 0.325–0.415 | 1 |
| Safe resolve, open | 0.932–1.104 | 1.100–1.399 | 5 |
| Safe resolve, muzzle inside cover | 0.396–0.498 | 0.506–0.643 | 2 (early rejection) |

Camera-only is a deliberately incorrect damage rule behind this cover, so its lower time is not an equivalent replacement. Safe queries comprise camera ray, muzzle/root overlaps, root-to-muzzle and muzzle-to-intent rays in open/closed poses. The 0.025 overlap radius is fixture-specific; adapt units, self-collision exclusions, origin policy, moving colliders and authoritative pose sampling. Unity documents that a ray starting inside a collider does not detect that collider ([Unity 6000.0 Physics.Raycast, Remarks](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/physics/raycast)); an outgoing muzzle ray alone is insufficient for this case.

| 32×32 weighted grid: 512 same-exit distance answers per invocation | Median range ms | p95 range ms |
| --- | --- | --- |
| 512 independent A* distance searches | 18.803–19.967 | 20.455–21.145 |
| One field rebuild + 512 distance lookups | 0.06784–0.06898 | 0.08364–0.09039 |
| Existing valid field: 512 distance lookups | 0.000863–0.000878 | 0.001009–0.001158 |

The cached case is array reading plus checksum; it excludes rebuilding, validation per query, successor traversal, path reconstruction, collision, avoidance and steering. A* uses reusable workspaces and a Manhattan lower bound on this grid; generic graphs use zero heuristic. All variants return equal aggregate distance checksums. Fields were already faster at the smallest tested batch of 32; this experiment does **not** locate a universal crossover count. Use a field when many queries share the same goal and compatible graph/cost profile; include rebuild frequency, goals/profiles, memory and movement work in the real budget. Sparse unrelated destinations can favor independent searches.

Graph validity assumes mutations use `AddEdge`/`SetBlocked`; public arrays/lists can bypass revision tracking. The kernels assume finite, nonnegative costs/rates/time steps and valid indices; input validation, encapsulation and concurrent mutations need production hardening.

## Reproduce

From this directory in PowerShell, with the installed Unity path in `Run-Editor.ps1` adjusted if necessary:

```powershell
./Run-Editor.ps1 -Method LabBatch.Checks -Report checks-new.json -Log checks-new.log
./Run-Editor.ps1 -Method LabBatch.Prepare -Log prepare-new.log
./Run-Editor.ps1 -Method LabBatch.Play -Graphics -Report editor-new.json -Log editor-new.log
./Run-Editor.ps1 -Method LabBatch.Build -Log build-new.log
./Run-Player.ps1 -Session player-run-1
./Run-Player.ps1 -Session player-run-2
./Run-Player.ps1 -Session player-run-3
python ./analyze_results.py
./Run-Player.ps1 -Session interactive-check -Interactive
```

Use new session names to preserve historical evidence; the analysis script intentionally reads `player-run-1/2/3` and final editor filenames. A rerun under another name needs an explicit analysis-input change. Close this project in the Editor before CLI runs. `LabBatch.Prepare` writes the small scene/materials; Build regenerates the ignored `Build` folder. `-Graphics` is required for the PlayMode capture. `-InjectError` with Play intentionally produces exit 2. Existing local Unity licensing worked only outside the execution sandbox; sandbox initialization could not query system identity. No credentials or licensing settings were changed.

`Application.targetFrameRate` is a requested pace, with `vSyncCount=0` for this experiment. Unity warns desktop software pacing can microstutter and that the Editor setting affects only Game view ([Unity 6000.0 targetFrameRate, Remarks](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/application/targetframerate)). The cap trials validate response against recorded elapsed steps, not display smoothness.

## Knowledge returned

Updated CAMERA, HITSCAN and PATH with this local evidence and conditions; GUIDE and RESEARCH-USE distinguish these three engine experiments from the other 40 technique sheets and earlier hypothetical evaluations. The implementation remains an isolated prototype, with no production integration, network test, GPU profile or player study.

After these updates, strict game-catalog validation passed for 69 entries with zero errors/warnings. Existing declared retrieval cases passed 23/23 common, 11/11 game application and 20/20 extended cases ([common](Results/retrieval-common.json), [game](Results/retrieval-game.json), [extended](Results/retrieval-extended.json)). These are discoverability regressions, distinct from runtime correctness and autonomous decisions on unseen tasks. Independent code/evidence review found no remaining correctness blocker within the stated scope; its qualifications are retained above.

## Offline reanalysis contract

The current [analysis procedure](ANALYSIS.md) separates retained-data/source checks from optional recorded-binary verification. All four analyzers default to read-only stdout; missing builds are explicit, `--require-binaries` makes them failures, and any available hash mismatch fails in either mode. Save only with `--output` to a new file; historical results are never implicitly rewritten. This procedure does not rerun Unity or change the measurements above.
