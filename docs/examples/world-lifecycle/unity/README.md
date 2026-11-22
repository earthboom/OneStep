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
