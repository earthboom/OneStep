# Technique Lab

A small, isolated Unity 6000.0.77f1 experiment requested to validate stored game techniques. This is a reproducible prototype and measurement harness, not a production game or a benchmark of other engines/platforms.

## Design and acceptance

Use the installed Unity editor and a built Windows player. No external assets, registry packages, networking or existing game project are required. Built-in physics provides actual scene raycasts; MonoBehaviour Update drives the running demonstrations. Retain raw sample distributions and hardware/build identity before summarizing costs.

| Technique | Comparison and behavior contract | Acceptance evidence |
| --- | --- | --- |
| Camera damping | Per-render-frame 10% lerp versus rate-4 exponential damping. A stationary target's two-second response should depend on elapsed time, while moving targets and collision are outside that guarantee. | Engine checks at 30/60/144 synthetic step sequences and a hitch sequence, plus real Update sequences with requested caps and measured rates. Absolute numeric error <=0.0001. |
| Hitscan | Camera intent versus camera-only damage. Validate a muzzle path, origin overlap and weapon-root obstruction against native Unity colliders. | Camera can see the target while a wall blocks the muzzle; open path hits; inside/beyond-wall muzzle cannot bypass cover; false layer/trigger hits are excluded. |
| Shared weighted field | One reverse-Dijkstra field and legal next-hop lookups versus independent A* requests to the same exit. Store original directed edge costs and prevent zero-cost successor cycles. | Known graph costs, unreachable state, topology invalidation and independent shortest-cost comparisons; rendered grid agents consume the field. Local avoidance is not provided. |

For CPU measurements, warm each workload, collect repeated batches, record every sample, median/p95 and work count, and keep setup/asset creation/file I/O outside timed sections. Report cached field queries separately from rebuilding the field. Camera bulk-update and raycast batches measure those operations, not a whole-frame budget or GPU performance. Repeat standalone measurement sessions; do not transfer this machine's numbers to mobile, multiplayer or production scenes.

## Layout

- `Assets/TechniqueLab`: the three algorithms, independent checks, runtime harness and visual scene consumer.
- `Assets/Editor`: engine probe, check/build/play entry points.
- `Results`: red/green evidence, editor/play/player records and captures.
- `Build`: generated Windows executable, ignored by Git.

The task is complete only after actual editor compilation, meaningful failed-then-passed checks, editor PlayMode, a Windows player build and player execution, inspected captures, measurement records and scoped knowledge updates. Missing capabilities remain explicit; mathematical checks alone do not satisfy engine execution.

## Run and results

Open `Assets/TechniqueLab.unity` in the installed Unity editor and enter Play, or run `./Run-Player.ps1 -Session interactive-check -Interactive` after building. The window exposes Reset followers, Cycle cover, Toggle grid door and Quit. Door changes reset visual consumers to safe starting cells; this prototype does not implement in-flight reconciliation or local avoidance.

[Measured results and reproduction commands](RESULTS.md) document final PlayMode, three standalone sessions, real UI inspection and the raw evidence. [analyze_results.py](analyze_results.py) validates final reports and source identity. CPU batches are calibrated toward 3 ms, with 31 alternating-order samples per variant; raw batches and normalized invocation times are both preserved. Automated PNGs capture the world camera without OnGUI; live controls were checked separately. `Build`, `Library` and logs are generated local files, excluded by the prototype's `.gitignore`.

## Dynamic extension

The separate `Assets/DynamicLab.unity` scene adds deferred obstacle transactions and current/destination-cell local reservations without resetting moving agents. [Design and scope](DYNAMIC.md) and [whole-frame results](DYNAMIC-RESULTS.md) distinguish safe movement, missed performance targets and incomplete GPU timings. Build with `./Run-Editor.ps1 -Method DynamicBatch.Build -Log dynamic-build-final.log`, then use `./Run-Dynamic.ps1 -Session dynamic-ui -Interactive` or measured `-Visible` sessions. The original scene and historical build/evidence remain intact.


## Bidirectional traffic extension

`Assets/TrafficLab.unity` adds authored opposing lanes, fixed unequal radii, radius-compatible corridor fields and narrow direction leases. [Design](TRAFFIC.md) and [results](TRAFFIC-RESULTS.md) retain safe completion, collision/deadlock sensitivity controls and three visible whole-frame measurement runs. Build through `TrafficBatch.Build`, run `Run-Traffic.ps1 -Interactive` or sequential `-Visible` sessions, and validate with `analyze_traffic.py`. Existing scene/source/evidence remain intact; the new admission pause is separate from DynamicLab's physical obstacle transactions.


## Unlaned sustained-stream extension

`Assets/StreamLab.unity` adds per-request unlaned grid search, immutable full-route space-time reservations, external FIFO admission and persistent ID accounting. [Design](STREAM.md) and [results](STREAM-RESULTS.md) retain ordinary completion, overload response failure, starvation/collision controls and three visible baffles/choke measurement matrices. Use StreamBatch.Build, Run-Stream.ps1 and analyze_stream.py. Prior scenes/source/evidence remain separate.

## Offline reanalysis contract

The current [analysis procedure](ANALYSIS.md) separates retained-data/source checks from optional recorded-binary verification. All four analyzers default to read-only stdout; missing builds are explicit, `--require-binaries` makes them failures, and any available hash mismatch fails in either mode. Save only with `--output` to a new file; historical results are never implicitly rewritten. This procedure does not rerun Unity or change the measurements above.
