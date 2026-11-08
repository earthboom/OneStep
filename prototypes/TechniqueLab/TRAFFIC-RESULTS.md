# TrafficLab results — 2026-11-08

## Outcome and adoption

Final Unity PlayMode and each of three sequential Windows release players passed **21 regression checks and 11 scenario expectations**: nine safe fixtures plus two deliberately failing-policy controls. All safe opposing streams completed, including 256 discs with radii 0.20/0.35/0.60. No swept pair/wall penetration, teleport, invalid lease, forbidden narrow use or algorithmic global stall was observed in these bounded fixtures. Minimum safe **surface-to-surface** pair gap was 0.0476715 units; it is not a centre-distance metric. This supports conditional use of authored lanes, compatible radius profiles and centralized admission scheduling.

All eighteen process/case windows met the 16.67 ms p95 target. At 256 mixed discs, complete-frame p95 ranged **8.08–8.32 ms**, while tick-bearing controller/native-sync p95 ranged **0.404–0.444 ms** across processes. These are three short runs on one uncontrolled host, not a demonstrated radius-mode speedup or production guarantee. Full distributions and rare misses remain in [summary.json](Results/Traffic/summary.json).

## What actually runs

[Design](TRAFFIC.md), [world](Assets/TechniqueLab/TrafficWorld.cs), [geometry/gate](Assets/TechniqueLab/TrafficGeometry.cs), [independent auditor](Assets/TechniqueLab/TrafficAudit.cs), [checks](Assets/TechniqueLab/TrafficChecks.cs), [native scene view](Assets/TechniqueLab/TrafficView.cs) and [runtime harness](Assets/TechniqueLab/TrafficRunner.cs) are separate from the previous [DynamicLab](DYNAMIC-RESULTS.md). Original algorithms and DynamicLab C# sources were preserved.

The static 128×40 world has a one-unit narrow aperture and four separated wide lanes. Two reverse fields per radius select left/right exits through a coarse four-node hub/corridor graph. Costs 1/2 express narrow/wide preference; they do **not** encode geometric shortest travel. Authored cardinal polylines then move discs at 3 units/s, in fixed 1/60 s ticks. The radius is fixed at spawn. A 0.04 clearance margin allows radius 0.46 but rejects 0.47 in the narrow aperture; radius 0.60 redirects to wide travel. Sharing a field across incompatible footprints is rejected.

Narrow traffic uses FIFO tickets **within each direction**, direction-exclusive leases, full-body release and at most four same-phase admissions while the opposite direction waits. The current phase drains before switching. Separate waiting stems keep incoming queues off the exit path. Wide lane centres are two units apart. Swept proposals use each pair's radius sum, yielding when unsafe. A two-unit spatial grid checks neighbouring bins; coverage relies on supported r≤0.60, speed 3 and dt≤1/30. A 240-tick, 64-disc comparison matches an exhaustive-neighbour motor. Public radius mutation, arbitrary time steps or changed movement bounds bypass these assumptions.

The independent auditor uses double-precision swept separation and wall distances each simulation tick, including terminal arrival segments. It does not call the motor's pair-gap function. Native Unity sphere-wall queries use each actual radius after transform synchronization every behavior display frame. Actors are primitive cylinders scaled to their disc radius, with no animated bodies or physical pushing. Per-frame visibility checks confirm the measured population remains rendered.

## Behavior evidence

| Fixture | Arrived E/W | Simulated seconds | Wide opposing ticks |
| --- | --- | --- | --- |
| narrow-headon | 1 / 1 | 28.6500 | 0 |
| wide-opposing | 1 / 1 | 21.5167 | 88 |
| large-redirect | 1 / 1 | 23.5167 | 0 |
| mixed-64 | 32 / 32 | 42.7333 | 370 |
| mixed-128 | 64 / 64 | 66.6833 | 670 |
| mixed-256 | 128 / 128 | 114.7500 | 1270 |
| reverse-128 | 64 / 64 | 66.6833 | 670 |
| late-west-64 | 32 / 32 | 42.7333 | 370 |
| admission-pause | 32 / 32 | 44.3500 | 370 |

The dense fixtures split directions evenly and exercise all three radius profiles; one quarter uses the narrow route, three quarters the wide lanes. Reverse order records west as the first actual phase. Late west records its first request at tick 90 versus east at tick 1. All safe batches were ≤4 when opposition was pending. Pause/resume retains positions and tickets, stops new admissions, drains active leases and eventually completes. This is **admission control**, not a new physical door closure test; the earlier DynamicLab retains that separate experiment.

The gate-disabled, pair-safe head-on control had 0/2 arrivals and reached 5 seconds of global no-motion, with no penetration. Disabling both gate and pair guard produced a swept overlap. Thus collision safety alone did not establish progress, and the audit detects a genuinely unsafe comparison. Local waiting is allowed: the largest consecutive individual no-motion wait among safe fixtures was 12.3333 simulated seconds, including the deliberate pause; mixed 256 reached 10.9667 s. The global stall check does not promise a per-agent wait bound or fairness under perpetual arrivals. Completion deadlines were 120 s for pairs, 180 s for 64/128 and 300 s for 256, in simulated time. Behavior playback runs eight ticks per rendered frame; these durations are not wall-clock performance timings.

Red/green evidence: [stub failures](Results/Traffic/red-contracts.json) → [green contracts](Results/Traffic/green-contracts.json); [world failures](Results/Traffic/red-world.json) → [corrections](Results/Traffic/green-world.json); [auditor mutation failures](Results/Traffic/red-audit-sensitivity.json) → [final PlayMode](Results/Traffic/editor-final.json). Corrections covered clearance, swept radius sums, gate exclusion/batching/pause, double-counted wait time, omitted Dense(8) slots and actual ticket-order reversal. Deliberately replacing the independent auditor's radius sum with a fixed diameter and skipping terminal segments made two direct checks fail; both were restored before the final build. Independent review found no blocker in the bounded motor/gate/audit, and requested stronger reverse/late/auditor regressions; those are in final evidence.

## Complete-frame measurement

Hardware: 12th Gen Intel(R) Core(TM) i7-12700KF; NVIDIA GeForce RTX 3080; Windows 11  (10.0.26200); Unity 6000.0.77f1, Windows x64 Mono release, Direct3D11, 1280×720, MSAA 2, vSync 0. The player window remained visible. Comparison order was mixed/uniform, uniform/mixed, mixed/uniform for each count. Both modes use identical centres, corridors, renderer, camera and speed; uniform discs are all radius 0.35. Initialization, profile-field construction, auditing, capture and file I/O lie outside performance sampling; no TrafficLab topology rebuild is timed. The runtime collision guard, gate and Transform synchronization stay inside.

After one second warmup, each case records six seconds with a real-time 60 Hz accumulator, retaining backlog (maximum eight catch-up ticks per frame). No actor reaches an exit or respawns during these windows. Every wall interval, active and visible population, update time, engine CPU/main/render/present/GPU timing and GC count is retained. Admission pauses at measured 1.5 s and resumes at 3 s. Event component work belongs to its current update and the **following** wall interval, preserved separately in summary events.

| Active discs | Radius mode | Whole-frame p95 ms | Tick-bearing controller/sync p95 ms | Worst frame ms | >16.67 ms % (runs 1/2/3) |
| --- | --- | --- | --- | --- | --- |
| 64 | uniform | 2.89–4.21 | 0.132–0.140 | 10.82 | 0.000 / 0.000 / 0.000 |
| 64 | mixed | 2.80–3.53 | 0.135–0.140 | 9.91 | 0.000 / 0.000 / 0.000 |
| 128 | uniform | 3.57–3.89 | 0.253–0.271 | 10.54 | 0.000 / 0.000 / 0.000 |
| 128 | mixed | 3.59–7.62 | 0.250–0.272 | 10.05 | 0.000 / 0.000 / 0.000 |
| 256 | uniform | 8.13–8.28 | 0.402–0.485 | 10.16 | 0.000 / 0.000 / 0.000 |
| 256 | mixed | 8.08–8.32 | 0.404–0.444 | 10.53 | 0.000 / 0.000 / 0.000 |

Ranges are the min/max of **per-process** percentiles, not pooled confidence intervals. Total 131,052 complete wall frames; 0 exceeded 16.67 ms; worst frame 10.817 ms. Do not round a rare miss rate to zero or discard stalls. At uncapped rendering many frames have no simulation tick; the table uses the tick-bearing controller subset. Its following wall subset, all-frame controller distribution, p99/max, backlog, GC and event rows remain in the summary. A controller timer is not the whole-frame budget.

Unity timing data is asynchronous and deduplicated by timestamp; its engine samples are not one-to-one aligned with wall rows. 23,429 of 131,052 engine observations had unavailable GPU time. Zero means missing; GPU valid-only statistics are not GPU-tail evidence. Do not sum CPU and GPU timing. The [official Frame Timing Manager documentation](https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/profile-rendering/frame-timing-manager/manager) describes delayed/possibly unavailable observations. A source/managed-assembly hash and build GUID bind all final runs to the current C# source; [build record](Results/Traffic/build.json) reports zero errors.

## Actual controls and captures

The native Windows window was inspected through Computer Use: freeze, restart mixed 64 while frozen, pause admission, resume motion, resume admission and quit. Different radii and cyan/red streams were visible; wide lanes advanced while the narrow entrance waited, then narrow leases/direction switching resumed. Both directions showed 24 arrivals with 16 narrow actors remaining at a later observation. This qualitative control test complements, rather than replaces, automated completion/audits. [UI observations](Results/Traffic/ui-observation.json) and [native exit record](Results/Traffic/traffic-ui-process.json) retain scope and exit code zero. Camera-generated PNGs show world geometry only; OnGUI is not captured in those PNGs.

World captures: [active mixed 256](Results/Traffic/traffic-run-3-mixed-256-active.png), [simultaneous wide traffic](Results/Traffic/traffic-run-3-wide-opposing-active.png), [measured 256 mixed](Results/Traffic/traffic-run-3-agents-256-mixed.png).

## Reproduce and evidence

From this directory, use the installed Unity 6000.0.77f1 editor through the wrappers:

```powershell
./Run-Editor.ps1 -Method TrafficBatch.Checks -Report checks.json -Log traffic-checks.log
./Run-Editor.ps1 -Method TrafficBatch.Play -Report editor-final.json -Log traffic-editor-final.log -Graphics
./Run-Editor.ps1 -Method TrafficBatch.Build -Log traffic-build.log
./Run-Traffic.ps1 -Session traffic-ui -Interactive
./Run-Traffic.ps1 -Session traffic-run-1 -Visible -Order 0
./Run-Traffic.ps1 -Session traffic-run-2 -Visible -Order 1
./Run-Traffic.ps1 -Session traffic-run-3 -Visible -Order 0
python analyze_traffic.py
```

The wrappers wait for their owned player and record exits, times, comparison order and identities. Run measurement processes sequentially. Batch PlayMode intentionally omits performance cases because it does not continuously render a normal Game view. Use [analyze_traffic.py](analyze_traffic.py) to validate behavior, actual fixture metadata, populations/visibility, timing coverage, wall-row completeness, ordering and current source hashes. Raw final players: [run 1](Results/Traffic/traffic-run-1.json.gz), [run 2](Results/Traffic/traffic-run-2.json.gz), [run 3](Results/Traffic/traffic-run-3.json.gz). [Lossless compression manifest](Results/Traffic/compression.json) verifies original byte lengths and SHA-256 on decompression; the analyzer supports raw or gzip JSON. Process identities use the matching `traffic-run-N-process.json` files.

## Decision trace and remaining scope

Problem → [PATH](../../knowledge/game/K-GAME-TECH-PATH.md) for goal/profile-compatible routing plus [CROWD](../../knowledge/game/K-GAME-TECH-CROWD.md) for neighbour guards and coordination → **conditional** lane/lease adoption → radius-aware route rejection, swept guard and direction scheduling → nine safe fixtures and two sensitivity controls → actual frame distributions and limits recorded back in those entries. Pure shared fields are insufficient for opposing-flow liveness; a small query cost does not settle rendering cost. Original DynamicLab's equal-radius/single-exit claims remain scoped to that older scene.

The new Korean retrieval questions initially missed PATH/CROWD in two of three declared cases: [before](Results/Traffic/retrieval-before.json). Existing entries received the verified corridor/radius terms and conditions; [after](Results/Traffic/retrieval-traffic.json), all three passed. All 57 prior declared retrieval regressions also passed, for **60/60** total. [Strict catalog validation](Results/Traffic/catalog-check.json) covers 69 game entries; [document checks](Results/Traffic/document-checks.json) cover canonical links, human companion existence and compressed evidence identity without reading human-only translations. These tests check declared discoverability, not autonomous judgment on unseen projects. Cumulative engine coverage remains four limited technique sheets; 39 still lack local runtime validation. [Independent review record](Results/Traffic/review.json) retains its scope and follow-ups.

Adopt conditionally where lanes and holding areas can be authored, the game permits queues and turns, one authority owns motion, circular radii remain fixed, and the target scene passes safety/completion/frame checks. Reject a universal deadlock-free or free-flow interpretation. Arbitrary navmeshes, curves, accelerated bodies, physical pushing, dynamic radius mutation, perpetual spawning, decentralized/network conflict and unannounced moving obstacles require a new design and tests. The two controls identify failures without establishing completeness of the successful custom scheduler.

Research checked 2026-11-08: [Li et al., ICAPS 2020, corridor symmetry](https://mapf.info/index.php/Main.SKoen20k) motivates opposing-corridor coordination; CBS/corridor-reasoning algorithms were not implemented. [LaValle C-space obstacles](https://lavalle.pl/planning/node156.html) and [translation/Minkowski discussion](https://lavalle.pl/planning/node161.html) inform footprint clearance; inflated AABBs here conservatively overapproximate rounded disc corners. [Fixed-path coordination](https://lavalle.pl/planning/node325.html) separates authored travel paths from scheduling. This gate is an engineering synthesis and inherits no completeness guarantee from those sources.

## Offline reanalysis contract

The current [analysis procedure](ANALYSIS.md) separates retained-data/source checks from optional recorded-binary verification. All four analyzers default to read-only stdout; missing builds are explicit, `--require-binaries` makes them failures, and any available hash mismatch fails in either mode. Save only with `--output` to a new file; historical results are never implicitly rewritten. This procedure does not rerun Unity or change the measurements above.
