# Unity world lifecycle example

Open this project in Unity 6000.0.77f1 with Windows Build Support. Choose **World Lifecycle → Prepare and open Town** and press Play. The project uses the built-in render pipeline and generates the Town and Forest scenes, materials, and a packaged copy of the [shared version 1 fixture](../fixtures/legacy-v1.json).

1. Click **Enter forest**. The persistent town camera moves to the forest after Unity loads the additive scene and the wolf view receives its current state.
2. Click **Strike wolf** once. Wolf HP drops from 100 to 60 and the quest advances from 0 to 1.
3. Click **Return to town**. After the forest is unloaded, observe the patrol count increase. Reenter the forest to see the wolf at its updated patrol position with the same HP and quest stage.
4. Click **Save** to write a version 2 snapshot. The manual game uses `Application.persistentDataPath/world-v2.json` and loads that slot on its next launch. Supply `-world-legacy <path>` to use a specific starter file, or `-world-save <path>` to use a different slot.

The game owns the wolf snapshot and advances a coarse patrol every 0.65 seconds of gameplay time while the forest is absent. The `WolfView` stores only the state it presents. The save reader recognizes `forest-wolf` in version 1 and resolves it to `forest-wolf-v2`. It rejects the legacy alias in version 2, validates the whole candidate before applying it, and writes the current schema via a verified temporary file.

## Build and run the probe

```powershell
.\Run-Probe.ps1 -Build -Runs 3
```

The command builds `Build/WorldLifecycle.exe` and launches three separate processes. Each run reads the legacy fixture, exercises the same `EnterForest`, `Strike`, `ReturnToTown`, and `Save` methods used by the buttons, and verifies the saved snapshot after intentionally advancing the live state. It checks that bad inputs preserve the live state and save file. Reports, player logs, and snapshots are written under `Work/`. Omit `-Build` to reuse an existing player, pass `-NoGraphics` for a null graphics device, and use `-Unity` if the editor is installed elsewhere.

An independent codec check uses the .NET 10 SDK.

```powershell
dotnet run --project Checks/SaveContract.csproj -- ../fixtures/legacy-v1.json
```

## Observed on Windows

All three independent Unity 6000.0.77f1 Windows Player runs passed. Each forest entry activated 349 objects. On every return to town, the original view was destroyed and the absent wolf retained HP 60 and quest stage 1. Its patrol advanced from 0 to 1 while the forest was unloaded. Reentry created a new view that received this state. Saving and reloading reproduced schema 2, `forest-wolf-v2`, 60 HP, quest stage 1, and one patrol step. Malformed input, an unsupported schema, and a v2 file with the old alias were rejected without changing the live state or the saved file. [Raw runs and build evidence](Evidence)

| Run | First ready, ms | First max update gap, ms | Revisit ready, ms | Revisit max update gap, ms |
| --- | ---: | ---: | ---: | ---: |
| 1 | 4.42 | 2.11 | 1.46 | 0.30 |
| 2 | 4.64 | 1.74 | 2.64 | 1.12 |
| 3 | 4.04 | 1.75 | 9.88 | 7.88 |
| Post-build pilot | 27.00 | 5.54 | 1.45 | 0.34 |

Each load's request-to-ready interval uses a monotonic clock. It begins immediately before `LoadSceneAsync` and ends after the forest has become Unity's active scene, the camera has moved, and the view has received the snapshot. Update-to-update gaps include the interval straddling the request and the first sample after readiness, so they include scheduling, engine work, and any frame pacing in that window. A first load means the first forest request in a new player process. The operating system cache may still be warm. The revisit follows actual scene unload in that same process.

These headless batch runs initialized Direct3D 11 on a GeForce RTX 3080 with a Core i7-12700KF. The reported gaps measure the game loop during this workload. Windowed frame presentation, GPU time, and a production-world frame budget require separate profiling. [Unity Player arguments](https://docs.unity.com/en-us/engine/6000.0/manual/unity-editor/command-line-arguments/player)

Unity API references. [LoadSceneAsync](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/scenemanagement/scenemanager/loadsceneasync) · [SceneManager](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/scenemanagement/scenemanager)

## Large forest experiment

```powershell
.\Run-Scale.ps1 -Build
```

This builds the same Windows Player for all four configurations and runs 16 fresh processes. Each configuration appears once per round and once in each launch position. Two rounds start with the [v1 fixture](../fixtures/legacy-v1.json) and two with the [v2 save produced by the earlier Player](../fixtures/legacy-v2.json). All timing and save output goes to `Work/scale-*/`. Use `-Smoke` for one streamed, scheduled-AI run and omit `-Build` to use the current Player.

| Configuration | Forest residence | NPC updates |
| --- | --- | --- |
| `resident-full` | All eight scenes load before leaving town and stay resident | All 2,048 NPCs each tick |
| `stream-full` | Load the destination additively, then unload the previous scene | All 2,048 NPCs each tick |
| `resident-coarse` | All eight scenes stay resident | Nearby NPCs each tick, offscreen NPCs every 12 ticks |
| `stream-coarse` | Load the destination additively, then unload the previous scene | Nearby NPCs each tick, offscreen NPCs every 12 ticks |

The route is town → chunks 0, 2 and 5 → combat → town → chunk 5. The eight packaged Unity scenes each contain a textured 72×72 terrain mesh, 176 trees, 88 rocks, and 256 NPC views. The same camera and nearby NPC bindings apply at every settled stop. The persistent simulation owns 2,048 NPC records independently of the scene objects. Offscreen updates batch deterministic patrol steps. A new view can evaluate the precise state at the current tick even between those updates. Both residency modes run unused-asset cleanup on the return to town.

Each run has 552 fixed logical ticks. The six steady stops receive 72 ticks each and the five transitions receive 24 ticks each. A slower transition can span extra rendered updates without advancing the route beyond its prescribed transition ticks. The recorded frame intervals are wall-clock gaps between Unity `Update` calls. They include rendering and sampling overhead between those calls. Startup preload, transition, and steady frames have separate labels. The camera renders one 1280×720 D3D11 target per sampled frame, with VSync disabled and no application frame cap. A pixel readback checks that the camera produced a varied forest image and runs after measurement. No window presentation or GPU execution time is reported. [Unity Camera.Render](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/camera/render)

Windows process memory is sampled every 16 measured updates and at the named checkpoints. The recorded private bytes represent committed private memory and working set represents currently resident pages. The peak is the highest sampled value during the route and can miss short-lived allocations. The town value is the checkpoint after unload and 72 offscreen ticks. The results cover a warm-process context and do not control the operating system cache. [Windows process memory counters](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters_ex)

### Measured results

All 16 standalone Unity 6000.0.77f1 runs passed on a Core i7-12700KF and RTX 3080. The frame percentiles are nearest rank within each run and the table reports the median of four run-level values. Memory uses MiB. [Run summaries](Evidence/scale/summary.json) · [Compressed raw reports](Evidence/scale/raw.json.gz)

| Mode | Steady p50 / p95 / p99, ms | Transition p95, ms | Town private / working set, MiB | Sampled peak private / working set, MiB |
| --- | ---: | ---: | ---: | ---: |
| Resident / full | 0.468 / 0.648 / 0.794 | 0.800 | 400.0 / 216.8 | 401.0 / 217.5 |
| Streamed / full | 0.440 / 0.633 / 0.783 | 0.935 | 374.8 / 206.4 | 375.7 / 207.0 |
| Resident / scheduled | 0.464 / 0.628 / 0.755 | 0.799 | 401.4 / 216.8 | 401.5 / 217.4 |
| Streamed / scheduled | 0.456 / 0.628 / 0.839 | 0.970 | 371.9 / 204.2 | 373.1 / 204.7 |

Streaming reduced process memory with either AI schedule. In the combined comparison, the initial preload phase fell from 41.11 ms to 1.62 ms, while the first destination's readiness moved from 1.01 ms to 7.37 ms and revisit readiness from 0.08 ms to 3.86 ms. The steady p95 moved slightly lower and the steady p99 moved higher. The largest observed steady update gap was 4.698 ms for the resident/full control and 2.733 ms for streamed/scheduled. The timing data shows a tradeoff across phases for this workload.

Full-rate AI made 1,130,496 simulation evaluations, including 1,032,192 offscreen. Scheduled AI made 184,320 evaluations, including 86,016 offscreen. All configurations produced identical complete-population digests at the matched ticks. The combat target kept 65 HP, and its patrol counter went from 60 at combat to 76 after the town dwell and 92 on revisit. Streamed mode destroyed its old view and presented the current authoritative state on a new view. Each run loaded its original v1 or v2 fixture, rejected invalid candidates, verified its v2 output, and left the input bytes intact. The original small example also passed on this build. [Small-example regression](Evidence/scale/small-regression.json)

To revalidate a full four-round run and regenerate the summary, use the standard-library verifier with the output directory reported by the PowerShell runner.

```powershell
python verify_scale.py "./Work/scale-<timestamp>" ./Work/verified-summary
```
