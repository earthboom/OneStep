# Engine-saved fixture checks

This test-only project creates real uncooked assets with Unreal Editor, then reloads them in a **second process without saving** to produce `oracle.json`. The standalone parser is compared with that independent observation by `../verify_engine_assets.py`. It does not link into or add a runtime dependency to the parser.

The fixture set contains a nonempty tutorial animation (188 source frames in the checked engine), a montage referencing it, a compiled widget with a canvas and text child, a PrimaryAssetLabel with three soft references and nondefault rules, and a two-row DataTable. These are controlled engine-authored samples, not production-project coverage.

Use a **fresh isolated directory** and an authorized UE 5.8 Windows editor installation with development headers/libraries and the built-in tutorial animation content. The helper accesses properties that Python correctly refuses as protected. It only changes the isolated `/Game/ReaderChecks/` widget and exports native property text; it never edits engine source or assets. First compilation may populate large engine development caches. The fixture recipe is scoped to the checked UE 5.8 source build; other builds may require API adaptation. Missing source content or build capabilities must fail explicitly.

Example PowerShell from the OneStep root (replace the engine placeholder):

```powershell
$taskEngine = '<engine directory>'
$taskFixture = Join-Path (Get-Location) '.cache/onestep/native-reader-check'
if (Test-Path -LiteralPath $taskFixture) { throw 'Use a new empty fixture directory' }
Copy-Item -LiteralPath 'tools/unreal-assets/tests/engine' -Destination $taskFixture -Recurse
$taskEditor = Join-Path $taskEngine 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
$taskBuilder = Join-Path $taskEngine 'Engine/Build/BatchFiles/Build.bat'
& $taskBuilder AssetCheckEditor Win64 Development "-Project=$taskFixture/AssetCheck.uproject" -WaitMutex -UsePrecompiled -NoHotReloadFromIDE -NoUBA -NoXGE -NoFASTBuild -NoSNDBS -MaxParallelActions=4
if ($LASTEXITCODE -ne 0) { throw 'Fixture helper build failed' }
[Environment]::SetEnvironmentVariable('UE-LocalDataCachePath', "$taskFixture/DDC")
& $taskEditor "$taskFixture/AssetCheck.uproject" -run=pythonscript "-script=$taskFixture/create_assets.py" -unattended -nullrhi -nosound -nop4 -ddc=NoShared "-abslog=$taskFixture/create.log"
if ($LASTEXITCODE -ne 0) { throw 'Fixture creation failed' }
& $taskEditor "$taskFixture/AssetCheck.uproject" -run=pythonscript "-script=$taskFixture/read_assets.py" -unattended -nullrhi -nosound -nop4 -ddc=NoShared "-abslog=$taskFixture/read.log"
if ($LASTEXITCODE -ne 0) { throw 'Independent native observation failed' }
python -B tools/unreal-assets/tests/verify_engine_assets.py --project $taskFixture --output "$taskFixture/evidence"
```

Build the parser's Release CLI first using the main README. Treat any nonzero verifier exit as a failed check. Inspect `creation.json`, `oracle.json` and `evidence/results.json`, including preserved input hashes and partial decoding, rather than relying on a successful editor exit alone. No network is used to obtain project assets. The animation is duplicated from installed engine content, which remains untouched; generated binary fixtures are locally ignored and are not distributed in this repository.

Generation refuses to run after `oracle.json` freezes the samples. Repeat only the native **read** and parser verification against those files, or start a new directory to generate different samples. Report output must be outside source `Content`. The native read script and CLI verifier both compare before/after package hashes. These checks concern serialized structure, properties and references; they do not test animation playback, compressed-track decompression, montage runtime state or rendered widget appearance.
