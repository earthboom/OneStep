# Pulse Arena

Clear the targets with **Space**. The targets recharge on the game world's clock, and presses during that interval leave the score and deadline intact. **Tab** cycles through available encounters. Each encounter retains its own score and cooldown until the game world ends.

## Build and play

Run from this project directory in PowerShell with Unreal Engine 5.8.3, its Win64 C++ toolchain, and Python 3.11 or later. Adjust the engine path for your installation.

```powershell
$arenaEngine = 'C:\Program Files\Epic Games\UE_5.8\Engine'
$arenaRoot = (Get-Location).Path
$arenaProject = Join-Path $arenaRoot 'PulseArena.uproject'
$arenaTemp = Join-Path $arenaRoot 'Scratch\BuildTemp'
New-Item -ItemType Directory -Force 'Evidence', $arenaTemp | Out-Null
$env:TMP = $arenaTemp
$env:TEMP = $arenaTemp
$env:UBA_ROOT = Join-Path $arenaRoot 'Scratch\UBA'
& "$arenaEngine\Build\BatchFiles\Build.bat" PulseArenaEditor Win64 Development "-Project=$arenaProject" -WaitMutex -NoHotReloadFromIDE -NoUBA -NoXGE "-Log=$arenaRoot\Evidence\rerun-build.log"
```

For interactive play, launch the same game mode with rendering enabled.

```powershell
& "$arenaEngine\Binaries\Win64\UnrealEditor.exe" $arenaProject /Engine/Maps/Entry -game -windowed -ResX=960 -ResY=540 '-DDC=(InstalledEnginePak,InstalledLocal)' -NoZenAutoLaunch "-LocalDataCachePath=$arenaRoot\Scratch\DDC"
```

To repeat the checked headless matrix with fresh staged game directories, run the verifier with a fresh evidence name.

```powershell
python -B .\verify_pulse.py matrix --baseline baseline-scoped --name matrix-rerun
```

The pre-extension command was `python -B .\verify_pulse.py baseline --name baseline-scoped`, run after compiling with just A present. The saved baseline `result.json` contains the observed input outcomes and the consumed binary and content hashes. Its `source.json` one level up records the pre-extension project input hashes used by the matrix verifier. Rebuilding and running the matrix writes local commands, staged files, and full logs under the fresh evidence directory.

## Authoring and lifecycle

Add a JSON file to `Content/Encounters`. Its basename is the encounter ID. Set a nonblank `title` of up to 48 characters, `cooldownSeconds` from 0.25 to 10, and integer `targets` from 1 to 12. The local player controller registers the built-in practice range first and scans authored files in filename order in `BeginPlay`. Invalid files and a conflicting `practice` ID produce a warning and are skipped. Encounters use the same pulse rule and declare no pack-to-pack dependency. These packs are loose startup data in the supported standalone Editor game mode.

The engine opens `/Engine/Maps/Entry` and creates the configured game mode, local player controller, and HUD. The player's `InputComponent` binds Space and Tab. The headless probe feeds engine key events to `APlayerController::InputKey` so it reaches the same handlers. The controller owns all encounter state for the local game session. `UWorld::GetTimeSeconds()` governs readiness, and a world timer schedules the scripted key events. `EndPlay` clears the probe timer handle. Each verified launch opened a fresh world, logged controller shutdown, and ended at exit 0. The checked scope is startup registration, local play, and ordinary world shutdown. Runtime pack changes, packaged distribution, multiplayer, and visual rendering were outside the verification scope.

## Evidence

| Launch | Files in the engine's consumed encounter directory | Encounters played in order | Windows exit |
| --- | --- | --- | ---: |
| [Baseline](Evidence/baseline-scoped/a-only/result.json) | A.json | Practice, A | 0 |
| [Core](Evidence/matrix/core/result.json) | Empty | Practice | 0 |
| [A only](Evidence/matrix/a-only/result.json) | A.json | Practice, A | 0 |
| [B only](Evidence/matrix/b-only/result.json) | B.json | Practice, B | 0 |
| [Both](Evidence/matrix/both/result.json) | A.json, B.json | Practice, A, B | 0 |

Every encounter accepted the first press, rejected an early press, then accepted a press after its deadline. In the matrix these were approximately 0.133 and 1.133 seconds after the first press. Scores followed 2 → 2 → 4 for practice, 4 → 4 → 8 for A, and 7 → 7 → 14 for B. Each result records the three engine times and deadlines, the inventory hashes, and the binary hash. The same module hash appeared in all launches. The [initial UBT build excerpt](Evidence/baseline-build.txt) records compilation and linking. The [extension UBT excerpt](Evidence/extension-build.txt) records that the target was up to date. The [hash comparison](Evidence/matrix/extension.json) identifies `Content/Encounters/B.json` as the sole added project input. Six [altered-log controls](Evidence/oracle-controls.json) confirmed that the verifier rejects wrong world identity, wrong directory, missing registration, false acceptance, fabricated scores, and a press time forced inside cooldown.

The repo retains selected build and runtime observations. Unreal's first launch used its default user-profile Zen cache before the scoped baseline was recorded, and installed UBT wrote its default diagnostic trace under Local AppData. An intermediate cache-redirection attempt hit Unreal's 119-character cache path limit. The final launch command uses the shorter fixture-local path and avoids starting Zen.

## OneStep in this example

The fixture's project instructions resolved its checkout link and led to Scout, Create, Code, and Code Design. This was a staged creation because the A baseline needed to pass in a real game world before B existed. Design review tied each pack's independence to a separate physical directory inventory and a launch that would reveal a missing dependency. The baseline manifest and extension diff check that the second pack adds data through the same registration path.

The game, code, and incident catalogs were consulted. `K-CODE-UE-PIE-VERIFICATION` distinguished a standalone Game world from PIE and led to a Game-world identity check. The lab's `Run-Lockstep.ps1` provided the existing Entry-map launch pattern, and the installed `World.h`, `InputKeyEventArgs.h`, and `TimerManager.h` supplied the actual engine contracts. `K-GAME-TECH-TIMESTEP` was informative about time domains. This interaction uses elapsed world time without a fixed-step integrator. `R-CODE-UE-EVIDENCE-PROXY` led to the independent world-time, score, identity, and inventory assertions, followed by the altered-log checks. The [document trace](doc_reads.jsonl) records the linked Markdown read during the work. Prototype-specific findings and evidence stay in the example.

**AI verification complete; awaiting vagabond testing or review.**
