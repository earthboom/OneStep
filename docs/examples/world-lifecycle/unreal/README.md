# Unreal town and forest

[Run the expanded forest benchmark](SCALE.md) to measure eight forest chunks and 2,048 logical NPCs on the same standalone D3D11 route.

**E** follows the road from town to the forest. **Space** strikes the wolf for 40 HP and advances the quest. **R** returns to town and unloads the forest. Wait in town until the patrol counter advances, then press **E** again. The wolf returns at its new patrol position with the HP and quest state from combat. **S** saves the current journey. Relaunch to restore it.

## Build and play

Run from this directory in PowerShell with Unreal Engine 5.8.3 and its Win64 C++ toolchain. Adjust the installation path if needed.

```powershell
$worldEngine = 'C:\Program Files\Epic Games\UE_5.8\Engine'
$worldRoot = (Get-Location).Path
$worldProject = Join-Path $worldRoot 'WorldLifecycle.uproject'
$worldTemp = Join-Path $worldRoot 'Scratch\BuildTemp'
New-Item -ItemType Directory -Force $worldTemp | Out-Null
$env:TMP = $worldTemp
$env:TEMP = $worldTemp
$env:UBA_ROOT = Join-Path $worldRoot 'Scratch\UBA'
& "$worldEngine\Build\BatchFiles\Build.bat" WorldLifecycleEditor Win64 Development "-Project=$worldProject" -WaitMutex -NoHotReloadFromIDE -NoUBA -NoXGE "-Log=$worldRoot\Scratch\build.log"
```

```powershell
& "$worldEngine\Binaries\Win64\UnrealEditor.exe" $worldProject /Game/Maps/Town -game -windowed -ResX=960 -ResY=540 '-DDC=(InstalledEnginePak,InstalledLocal)' -NoZenAutoLaunch "-LocalDataCachePath=$worldRoot\Scratch\DDC"
```

The default local save is `Saved/WorldLifecycle/Slot.json`. Pass `-WorldSave=<path-to-an-unused-slot>` to start with the shared v1 fixture and preserve your existing slot. The included Unreal map and material assets were authored from engine primitives with [`build_maps.py`](build_maps.py). The script creates new maps, so run it in a disposable project with the Python Editor Script Plugin and an empty Maps folder to regenerate them.

## Trace the journey

- [`WorldLifecycleMode`](Source/WorldLifecycle/Private/WorldLifecycleMode.cpp) is the standalone authority. Town stays loaded while the forest enters through a nonblocking `ULevelStreamingDynamic` request. Combat starts after the streamed level is visible and the map-owned wolf actor has begun play. Returning removes the streaming registration and waits for the level and active presentation to be gone before starting the offscreen patrol clock.
- The authority holds HP, quest stage and patrol count by stable NPC ID. `UWorld::GetTimeSeconds()` advances one patrol step every 0.25 game seconds spent in town after an unload. The tiny simulation advances at most one step per tick and skips catch-up after a long stall. A fresh presentation component copies authoritative state into the new map actor and sets its track position.
- [`WorldNpcState`](Source/WorldLifecycle/Private/WorldNpcState.cpp) maps the v1 ID to `forest-wolf-v2`, validates a candidate before replacing state, and writes v2 to a pending file before moving it into the slot. The example writes a tiny local JSON snapshot synchronously. Its scope is a single local writer and a subsequent ordinary process restart.

## Repeat the probe

```powershell
$worldPython = "$worldEngine\Binaries\ThirdParty\Python3\Win64\python.exe"
& $worldPython -B .\verify_lifecycle.py --runs 3 --renderer nullrhi --name verify-rerun
& $worldPython -B .\verify_lifecycle.py --runs 3 --renderer d3d11 --name verify-rendered-rerun
```

The verifier launches three standalone processes with separate, initially absent save files, then reloads the last v2 file in a fourth process. Simulated Unreal key events use the same input bindings as standalone play. For every lifecycle launch it asserts the exact sequence of migration, first visibility, combat, unload, one offscreen patrol step, revisit, save and rejected read of an unsupported schema. It also checks the recorded actor projection, canonical save on disk, and unchanged legacy fixture bytes. Raw logs and a machine-readable result go into the fresh `Scratch/<name>` directory.

The transition clock uses monotonic `FPlatformTime::Seconds()`. Request latency runs from the `LoadLevelInstance` request through this GameMode’s observation of visibility and the wolf projection plus camera switch. `maxTickGapMs` is the largest elapsed interval between GameMode tick samples during the transition, including the partial interval from the request to the first sample. NullRHI figures describe CPU-side loading, world activation and game-thread cadence in this small standalone Editor game. They exclude GPU work and the first presented frame. Process restarts isolate in-memory worlds while the OS file cache and derived data cache may warm across runs. Streaming detach removes the level from the active world. Memory reclamation is determined by Unreal garbage collection.

## Observed runs

All four [NullRHI processes](Evidence/observed-nullrhi.json) exited cleanly on UE 5.8.3 and Windows 11 with an Intel i7-12700KF. The 151,138-byte forest package produced 100 entries in the loaded level's actor array. Each lifecycle hit changed HP from 100 to 60 and quest from 0 to 1. The detached wolf advanced from patrol step 0 to 1 before the new forest instance appeared. The new instance and the fresh v2 process both projected HP 60, quest 1 and patrol 1.

| Process | First visibility (ms) | First max tick gap (ms) | Revisit visibility (ms) | Revisit max tick gap (ms) | Unload (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 20.616 | 8.411 | 19.085 | 6.678 | 3.708 |
| 2 | 15.209 | 5.862 | 10.007 | 5.785 | 0.896 |
| 3 | 16.592 | 5.670 | 24.375 | 6.618 | 3.188 |

The [D3D11 matrix](Evidence/observed-d3d11.json) ran the same probe in three fresh, windowed standalone Editor game processes at 960 × 540, after an earlier rendered sanity run. All three and the v2 restart created a D3D11 device on the NVIDIA GeForce RTX 3080. These timings still use the game-thread visibility and tick observations. They do not report GPU frame time or time to first present.

| Process | First visibility (ms) | First max tick gap (ms) | Revisit visibility (ms) | Revisit max tick gap (ms) | Unload (ms) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 56.170 | 17.335 | 40.778 | 9.103 | 18.603 |
| 2 | 52.852 | 15.482 | 46.843 | 14.659 | 12.439 |
| 3 | 55.900 | 12.980 | 60.073 | 10.960 | 24.146 |

The [build excerpt](Evidence/build.txt) records the Win64 compilation and link. Installed UBT also wrote its default diagnostic trace under Local AppData. The [map authoring excerpt](Evidence/map-authoring.txt) records both packages being generated. The first generator run logged eight warnings while probing for missing material assets on a fresh project. Seven [altered-log controls](Evidence/oracle-controls.json) confirm that the verifier rejects examples including a still-registered forest, lost offscreen health, double patrol, stale projection and a lost quest on restart.
