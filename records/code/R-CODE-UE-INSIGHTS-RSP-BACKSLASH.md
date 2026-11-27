---
id: R-CODE-UE-INSIGHTS-RSP-BACKSLASH
title: Headless Unreal Insights export wrote no files because backslashes in response-file paths were stripped
summary: TimingInsights export commands read their output path as an escaped token, so a quoted Windows path in an -ExecOnAnalysisCompleteCmd response file lost every backslash and no CSV appeared. Write the paths with forward slashes and check the export log's resolved Filename line.
kind: error
scope: UnrealInsights.exe headless analysis on Windows; TimingInsights.ExportThreads, ExportTimers and ExportTimingEvents run from a response file
keywords: [Unreal Insights, Timing Insights, UnrealInsights.exe, "-ExecOnAnalysisCompleteCmd", "@=", response file, "-NoUI", "-AutoQuit", "-OpenTraceFile", TimingInsights.ExportTimingEvents, TimingInsights.ExportTimers, TimingInsights.ExportThreads, FParse::Token, bUseEscape, backslash, escape, headless export, utrace, CSV]
status: resolved
checked_at: 2026-11-24
context:
  engine: "Unreal Engine 5.8 (UnrealInsights program and TraceInsights module)"
  platform: Windows 11
trigger: Running UnrealInsights.exe -NoUI -AutoQuit with -ExecOnAnalysisCompleteCmd="@=<response file>" whose export commands name quoted Windows paths with backslashes
symptom: Analysis completes and the process exits 0, but no export file exists; the export log shows the output path with its backslashes removed, for example D:Projectfolder...
cause_status: confirmed
prevention: Write every path inside the response file with forward slashes, then confirm the log's resolved Filename line and the file's existence instead of the exit code
prevention_status: verified
---

## Expected and observed

A response file passed through `-ExecOnAnalysisCompleteCmd="@=<file>"` held `TimingInsights.ExportThreads`, `ExportTimers` and `ExportTimingEvents` commands with quoted output paths such as `"D:\dir\exports\threads.csv"`. Expected: one CSV per command. Observed: the process exited 0 after analysis and no CSV existed in the target folder or anywhere else searched. The export log printed the path as `D:direxportsthreads.csv`.

## Cause and resolution

Confirmed in engine source. `FInsightsManager::Exec` sends a command that starts with `@=` to `HandleResponseFileCmd`, which runs the file line by line. Each export handler parses its filename with `FParse::Token(Cmd, bUseEscape)` where `bUseEscape` is true, so a backslash inside the quoted token is treated as an escape character and removed. The resulting relative-looking path was not the intended folder.

Resolution: the script that writes the response file converts the export folder to forward slashes. With the same trace and commands, all four exports were written.

## Recheck and prevention

On 2026-11-24 the forward-slash response file produced `threads.csv`, `timers.csv` and two timing-event CSVs from a 162 MB trace, and later runs added further filtered exports (`-threads=`, `-timers=` with `*` wildcards, `-startTime=`, `-endTime=`, `-columns=`). The log line `Filename: "<path>"` showed the full path each time. The earlier backslash run is the failing case this check detects.

Do not treat the exit code as success: also check the resolved Filename line and that the output file exists. Paths given directly on the command line are parsed by different code and were not tested here. GPU timer names in the export can be format strings such as `SceneRender- %s`, so per-view GPU work may not be separable from the CSV alone.

## Evidence

- Engine source, Unreal Engine 5.8: `Engine/Source/Developer/TraceInsights/Private/Insights/InsightsManager.cpp` (`FInsightsManager::Exec`, `HandleResponseFileCmd`); `Engine/Source/Developer/TraceInsights/Private/Insights/TimingProfiler/TimingProfilerManager.cpp` (`TimingInsights.ExportTimingEvents` handler, `const bool bUseEscape = true; FString Filename = FParse::Token(Cmd, bUseEscape);`); `Engine/Source/Runtime/Core/Private/Misc/Parse.cpp` (`FParse::Token` escape handling). Engine functional tests in `Insights/Tests/FunctionalTests/ExportCommandsTests.cpp` use the same `-ExecOnAnalysisCompleteCmd="@=%s"` form.
- Session observation, 2026-11-24: the failing backslash run, its export log, and the passing forward-slash runs described above.
- Related measurement guidance: [K-CODE-PERFORMANCE-MEASUREMENT](../../knowledge/code/K-CODE-PERFORMANCE-MEASUREMENT.md).
