# StreamLab results — 2026-11-08

## Outcome

Final PlayMode and three sequential visible Windows release players each passed **23 regression/native checks and 10 declared scenario expectations**. Seven ordinary FIFO streams met collision-free drain and the 240-second request-to-completion criterion. An eighth FIFO stream, the overloaded narrow passage, drained without collision but **failed that response criterion**: 61 IDs exceeded 240 s, maximum 280.0 s. Its expected-adverse classification and `deadlineMet=false` preserve the failure; root harness success does not mean every service target passed.

The latest-first control left request 0 unspawned for 310 simulated seconds while 538 other requests completed. The reservation-disabled control produced an actual swept overlap. These distinguish collision, global no-motion, per-request starvation symptoms and overload latency. A finite experiment cannot observe infinite time. The selected FIFO/full-route design additionally has a conditional finite-service argument below; it is not a guarantee for arbitrary physical crowds.

At eight requested arrivals/s through the choke, whole-frame p95 ranged **3.52–6.10 ms**, while the complete frames following online planning had p95 **20.23–20.52 ms**. All 18 process/case windows met the 16.67 ms whole-frame p95 criterion. All wall frames and deadline misses remain included. See [validated distributions](Results/Stream/summary.json).

## What changed

[Design](STREAM.md), [kernel](Assets/TechniqueLab/StreamKernel.cs), [map/reservations/planner/world](Assets/TechniqueLab/StreamWorld.cs), [independent audit](Assets/TechniqueLab/StreamAudit.cs), [checks](Assets/TechniqueLab/StreamChecks.cs), [pooled native view](Assets/TechniqueLab/StreamView.cs), [harness](Assets/TechniqueLab/StreamRunner.cs) and [editor entry points](Assets/Editor/StreamBatch.cs) form a separate StreamLab scene/build. Prior [TrafficLab](TRAFFIC-RESULTS.md) and [DynamicLab](DYNAMIC-RESULTS.md) remain available. Previous C# identity is checked in [preservation evidence](Results/Stream/preservation.json).

The 32×24 static grid has 1.5-unit cells, baffle/room/choke layouts and eight portals. Every free node has the same four undirected neighbour choices; there are **no lane tags, prescribed stream polylines or direction leases**. Paths are searched from each source/goal request. Bodies have radius .20/.35/.60; the narrow passage fits all supported footprints, with .04 margin. This is unlaned **cardinal graph** navigation, not unrestricted continuous steering or a navmesh. Graph discretization and portal placement remain authored.

A custom time-expanded search considers movement and waits for up to 96 half-second actions. Existing routes are reserved through completion using radius-aware swept separation. The expanded-node index agrees with exhaustive conflict checking for 2,000 deterministic candidate edges. All positive routes include computed turns; .60+.60 following around a corner can conflict even without a vertex/edge-swap conflict, so reservations test the actual swept radius sums. Static reverse distances are admissible search heuristics, not local avoidance. All tested radii fit a free-cell centre; larger bodies require a new clearance graph/check.

Requests have immutable IDs and release epochs. FIFO admission blocks younger work when its head cannot obtain a complete route; unreachable/over-horizon static requests are explicitly rejected. A newly admitted body waits its first action at a portal, moves 1.5 units per action (3 units/s) and despawns at its goal. Routes remain immutable. **Pending requests wait outside the physical world**, and their ages count in response latency. This avoids hiding starvation by counting only spawned agents; it does not simulate hundreds of colliding bodies forced into an occupied portal. The renderer pool cap is 256, not a claim that 256 bodies were active in every test.

## Sustained inflow and per-ID evidence

| Fixture | Requests / completed / rejected | Max active / pending | Last completion s | Max response / pending s | Late IDs (>240s) |
| --- | --- | --- | --- | --- | --- |
| baffles-balanced | 240 / 240 / 0 | 78 / 27 | 86.0 | 35.0 / 6.5 | 0 |
| rooms-crossing | 240 / 240 / 0 | 75 / 26 | 83.5 | 29.0 / 6.0 | 0 |
| choke-balanced | 240 / 240 / 0 | 67 / 108 | 180.0 | 120.5 / 72.5 | 0 |
| baffles-biased | 240 / 240 / 0 | 35 / 148 | 179.0 | 121.5 / 100.0 | 0 |
| choke-overload | 480 / 480 / 0 | 65 / 347 | 339.5 | 280.0 / 232.0 | 61 |
| baffles-long | 1200 / 1200 / 0 | 95 / 71 | 335.0 | 41.5 / 18.0 | 0 |
| rooms-seed19 | 360 / 360 / 0 | 95 / 114 | 110.5 | 52.5 / 32.0 | 0 |
| unreachable-request | 121 / 120 / 1 | 39 / 3 | 79.0 | 24.5 / 1.0 | 0 |

These are simulated times, not wall-clock benchmark durations. Long inflow runs for 300 simulated seconds and produces 1,200 distinct requests; only 95 are simultaneously active at peak. Across the eight draining fixtures, 3,120 valid IDs complete per execution, with one explicit unreachable rejection. Minimum safe pair **surface gap** is 0.1106602 units. Independent continuous-segment audit found no pair/wall penetration, teleport or diagonal invalid motion. Global no-motion never exceeded 0.5 s in draining fixtures. Per-body planned waiting is allowed and logged; global activity alone would not certify every ID.

Overload supplies 480 requests in 60 s. At inflow stop, 73 had completed and 347 still awaited admission; peak pending was 347. All eventually finished at 339.5 s, but 61 failed the chosen 240 s response criterion. This is capacity/latency failure, even though it is not permanent FIFO bypass. Ordinary fixtures also have substantial queue costs (up to 121.5 s response); the lab's 240 s diagnostic is not a suitable default gameplay target.

The LIFO control admits at most one newest request per action while two new requests arrive. Request 0 remains oldest and unadmitted at 310 s despite 538 completions; per-ID monitoring detects the condition while global progress remains healthy. The two-body reservation-disabled control collides after 1 s. A stationary-body unit control separately triggers the global stall detector. Raw jobs record creation/admission/completion/rejection, route length/turns, total planned waits and maximum consecutive no-motion, so late IDs and censored/unresolved requests can be inspected instead of disappearing into averages.

### Conditional finite-service argument

In this exact model, a blocked FIFO head prevents younger admissions. Every existing body already has an immutable complete route finishing within the 96-action horizon, so those reservations drain while simulation advances. With no bodies left, a statically reachable head whose shortest route plus mandatory initial wait fits the horizon is found by the finite time-expanded search. Each request has finitely many older IDs at creation; repeat the argument to obtain eventual admission and completion. This is an engineering argument tied to controlled spawning, static geometry, fixed radii, exact schedule execution, finite arrivals per action and functioning search. It is not formal verification or an experimental observation of infinity. No uniform latency/queue bound follows under overload; later requests can face progressively larger finite waits.

Arbitrary physically present agents, unscheduled stops, acceleration, player interference, moving walls, runtime radius changes, perpetual residence at goals or distributed state invalidate the argument and may invalidate safety. Those need replanning with compatible reservations, topology transactions or a different coordinated planner; the old DynamicLab cannot simply be combined by copying its movement policy.

## Independent and native checks

The double-precision auditor independently computes all pair segment gaps and cardinal segment-to-wall distances, including the final arrival action and first portal wait. Native Unity sphere queries read actual pooled body positions/scales at fractions 0/.25/.5/.75/1 of **each** action, with separate model-to-display equality checks and terminal sample counts. These are sampled native checks, not a continuous native collision solver. Performance updates interpolate at 60 Hz between the same action endpoints.

[Stub red kernel](Results/Stream/red-kernel.json), [missing-search failures](Results/Stream/red-search.json), [missing lifecycle failures](Results/Stream/red-lifecycle.json), [green lifecycle](Results/Stream/green-lifecycle.json) and [final PlayMode](Results/Stream/editor-final.json) preserve execution. Deliberately skipping terminal audit segments and replacing radius sums with a fixed diameter failed two independent checks in [audit sensitivity](Results/Stream/red-audit-sensitivity.json); the correct source was restored. Four runtime native checks deliberately corrupt displayed scale/position and confirm mapping errors plus a real wall overlap are detected before restoring the pose. These checks run outside performance sampling.

[Independent review](Results/Stream/review.json) caught endpoint-only/logical-only native evidence and ambiguous overload acceptance. Final code samples actual interpolated transforms and explicitly retains failed response targets. Reviewer found no remaining actionable source issue in the follow-up. Build-time C# snapshots supplement post-exit process hashes.

## Complete-frame cost

12th Gen Intel(R) Core(TM) i7-12700KF; NVIDIA GeForce RTX 3080; Windows 11  (10.0.26200); Unity 6000.0.77f1, Windows x64 Mono release, D3D11, 1280×720, MSAA 2, vSync 0, visible native window. Each of three sequential processes measures baffles/choke × 2/4/8 requests/s. Run two reverses both layout and rate order. Arrivals are **demand rates**, not guaranteed admission throughput or fixed active counts.

Twenty simulated seconds of prefill and one real warmup second precede six real sampled seconds. Static goal heuristics/renderer pools are warm; novel-goal cache construction is not characterized. Online route search, reservation rebuilding, queue processing, births, completions, display changes and native Transform sync remain inside timed updates. Audit/capture/file I/O are outside; their overhead is not claimed as shipping simulation. All row/counter collection, rendering, presentation and waits remain part of the complete wall interval. Real-time 60 Hz catch-up retains backlog, with at most eight ticks per render frame.

| Layout / requests per second | Actual active range | Max pending | Whole-frame p95 ms | Planning-following whole-frame p95 ms | Worst frame ms | >16.67 ms (total) |
| --- | --- | --- | --- | --- | --- | --- |
| baffles / 2 | 36–39 | 1 | 3.73–5.95 | 1.18–1.67 | 10.77 | 0 |
| baffles / 4 | 55–66 | 17 | 3.81–6.04 | 1.10–1.46 | 10.42 | 0 |
| baffles / 8 | 55–81 | 108 | 3.73–5.89 | 1.12–1.76 | 10.63 | 0 |
| choke / 2 | 37–41 | 0 | 3.65–5.99 | 2.12–3.96 | 11.64 | 0 |
| choke / 4 | 64–67 | 26 | 3.75–6.07 | 20.50–23.49 | 23.49 | 6 |
| choke / 8 | 63–64 | 135 | 3.52–6.10 | 20.23–20.52 | 20.52 | 3 |

Ranges are min/max of per-process percentiles, not pooled confidence. Total **134,145 complete frames**, **9** over 16.67 ms; worst **23.489 ms**. Planning-bearing following frames contain 9 of those misses. Do not infer planning cost from mostly tick-free uncapped rendering, nor from all-frame p95 alone. Each case has 13 planning-bearing updates but 12 matched following wall intervals; one final update per window has no subsequent captured interval (18 unmatched rows total), explicitly excluded from that subset. With 12 samples, the nearest-rank planning-following p95 equals that subset's maximum, not a stable tail estimate. Boundary update counters include both endpoint events and need not equal nominal rate times six seconds. The summary separately retains tick-bearing update/following-wall, planner update/following-wall, p99/max, GC, active/visible/pending distributions, backlog and unmatched final planner rows.

Each update's work belongs to the **next** wall interval. `renderedActive` and `visible` are sampled before current work, so they describe the population associated with that prior rendered interval; they match without newborn culling lag. `active` is the current post-update count. Captures include new requests and completions in every measured window; bodies are not merely a prefilled static population.

Engine timing is asynchronous and deduplicated. 25,230/134,145 GPU fields are unavailable; zero GPU fields are missing, and valid-only GPU statistics do not establish GPU tails. CPU/GPU times are not summed. [Unity Frame Timing Manager](https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/profile-rendering/frame-timing-manager/manager) documents delayed/possibly unavailable data. This is one uncontrolled host, primitives without production animation/shadows/gameplay, three short windows and a small static grid; use target-scene complete-frame checks before adoption.

Two earlier baffles-only players are retained as [pilot preservation](Results/Stream/pilot-preservation.json); actual UI exposed larger choke planning work, so the final matrix adds the bottleneck. They are not pooled with final-source results.

## Native use, reproduction and provenance

Computer Use observed the actual unlaned baffle scene, distinct radii and moving turns. Pause inflow kept request count fixed while existing work drained; freeze/resume, restart choke while frozen, resume inflow and quit worked. [UI observations](Results/Stream/ui-observation.json) and [normal exit](Results/Stream/stream-ui-process.json) distinguish qualitative use from numerical audits. That UI build preceded only the automated measurement-matrix expansion; interactive world/view/control behavior is unchanged. Camera PNGs omit OnGUI. [Baffle active capture](Results/Stream/stream-run-3-baffles-balanced-active.png), [choke overload capture](Results/Stream/stream-run-3-choke-overload-active.png), [measured choke capture](Results/Stream/stream-run-3-choke-arrival-8-per-second.png).

From this directory:

```powershell
./Run-Editor.ps1 -Method StreamBatch.Checks -Report checks.json -Log stream-checks.log
./Run-Editor.ps1 -Method StreamBatch.Play -Report editor-final.json -Log stream-editor-final.log -Graphics
./Run-Editor.ps1 -Method StreamBatch.Build -Log stream-build.log
./Run-Stream.ps1 -Session stream-ui -Interactive
./Run-Stream.ps1 -Session stream-run-1 -Visible -Order 0
./Run-Stream.ps1 -Session stream-run-2 -Visible -Order 1
./Run-Stream.ps1 -Session stream-run-3 -Visible -Order 0
python analyze_stream.py
```

CLI Checks runs 19 kernel/lifecycle/audit regressions; PlayMode/player adds four native sensitivity checks for 23. Batch PlayMode intentionally omits performance, because a normal continuously rendered player is required. [Build](Results/Stream/build.json) has zero errors. [Build-time source snapshot](Results/Stream/build-source.json), current source, three assembly hashes/build GUIDs and process manifests agree. [Analyzer](analyze_stream.py) verifies per-ID accounting, late/unresolved IDs, FIFO order, finite route lengths, native fractions/terminal counts, active visibility, demand generation, all wall rows, timing coverage, comparison order and identities. Raw final [run 1](Results/Stream/stream-run-1.json.gz), [run 2](Results/Stream/stream-run-2.json.gz), [run 3](Results/Stream/stream-run-3.json.gz) use byte-identical roundtrip compression with [manifest](Results/Stream/compression.json).

## Reuse and evidence boundaries

Problem → [PATH](../../knowledge/game/K-GAME-TECH-PATH.md) for searched/time-expanded routes plus [CROWD](../../knowledge/game/K-GAME-TECH-CROWD.md) for geometric conflicts, throughput and individual service → conditional complete-route/FIFO admission → actual streamed bodies, independent audits and per-ID ledger → observed safe drain, overload deadline failure, starvation/collision controls and whole-frame costs → existing knowledge updated. This method requires control over admission and exact route execution; it does not solve spontaneous crowds already occupying arbitrary locations.

All three new declared retrieval queries missed their required entries before the update: [before](Results/Stream/retrieval-before.json). Existing entries receive inspected sustained/unlaned/queue/starvation conditions and terms. [After](Results/Stream/retrieval-stream.json) and prior 60 regressions total **63/63**. [Catalog](Results/Stream/catalog-check.json) retains 69 entries and [document checks](Results/Stream/document-checks.json) verify canonical links, evidence identity and human companion existence without reading human-only translations. Four limited technique sheets have local engine evidence; the other 39 remain unvalidated locally. Search recall does not establish autonomous selection quality for unseen projects.

The full existing knowledge-tool suite also passed **75/75**: [final log](Results/Stream/knowledge-tests.txt). Its initial [sandbox run](Results/Stream/knowledge-tests-sandbox.txt) had two failures and eleven errors: `test_fixture_paths_cannot_escape_project`, `test_preparation_never_overwrites_existing_project`, `test_prepared_projects_use_actual_catalog_and_search_without_answer_key` and `test_rubric_covers_inputs_but_is_not_a_semantic_automated_test` hit temporary-directory permission errors; `test_resolved_symlink_cannot_escape_configured_root` could not create its test link/junction; `test_missing_yaml_keeps_structured_dependency_error` saw PyYAML even under Python -S because the package path had been injected directly through PYTHONPATH. Rerunning unchanged tests outside the restricted process, in an owned workspace temp directory, with the existing package exposed only through normal site initialization resolved those environment issues. No package installation, test assertion change or game-source change was made. [Environment record](Results/Stream/knowledge-suite-environment.json) retains the invocation and boundaries.

Primary research checked 2026-11-08, **abstracts only**: [Li et al., RHCR](https://arxiv.org/abs/2005.07371) frames continuously renewed goals with bounded-window coordination; [Okumura et al., PIBT](https://arxiv.org/abs/1901.11282) attaches finite reachability to a graph cycle condition; [Ma et al., online pickup/delivery](https://arxiv.org/abs/1705.10868) restricts guarantees to well-formed instances. Our custom full-route admission/search is not those algorithms and inherits none of their theorems or benchmark counts. This task's mechanisms are supported by its own scoped engine evidence.
