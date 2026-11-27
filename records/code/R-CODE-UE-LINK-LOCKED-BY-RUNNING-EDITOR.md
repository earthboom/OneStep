---
id: R-CODE-UE-LINK-LOCKED-BY-RUNNING-EDITOR
title: An Unreal editor build compiled cleanly but failed to link because a headless editor instance of the same project still held the module DLL
summary: A command-line editor build compiled every file but stopped at link with UBA error 9001 and LNK1104, because an editor process started in server mode by another workflow had the project's editor module DLL loaded. A report that the editor was closed did not mean the process had exited. List every process whose command line names the project file before building, and confirm each one has exited.
kind: error
scope: Command-line UnrealBuildTool builds of an editor target on Windows while another editor process of the same project, in any mode, is running
keywords: [UnrealBuildTool, UBT, Build.bat, LNK1104, "cannot open file", "UbaSessionServer", "error code 9001", "Unreal Build Accelerator", UBA, "being used by another process", UnrealEditor.exe, "-server", "-NoLiveCoding", CrashReportClientEditor, module DLL lock, headless editor, Win32_Process, CommandLine]
status: resolved
checked_at: '2026-11-26'
context:
  engine: "Unreal Engine 5.8 source build"
  platform: Windows 11
  build_executor: "Unreal Build Accelerator with remote workers, then local NoUba retry"
trigger: Building an editor target from the command line while an editor process of the same project, started in server or other headless mode by a different workflow, is still alive
symptom: "All compile actions succeed, then UbaSessionServer cannot open the project's UnrealEditor-<Module>.dll for write (error code 9001), the NoUba retry fails with LINK fatal error LNK1104, and the result is Failed (OtherCompilationError)"
cause_status: confirmed
prevention: Before an editor build, list processes whose command line contains the project's .uproject path (any mode, including -server and headless runs, plus their CrashReportClientEditor), and confirm by process ID that each has exited instead of relying on a report that the editor was closed
prevention_status: verified
---

## Expected and observed

A code-only change was built with the engine's `Build.bat` for the editor target, Development configuration. Expected: a normal compile and link. Observed: all compile actions finished without errors, including the changed file. The link of the project's game module DLL then failed. `UbaSessionServer` reported that it could not open `Binaries/Win64/UnrealEditor-<Module>.dll` for write after retrying for 20 seconds, naming `UnrealEditor.exe` and `CrashReportClientEditor-Win64-Development.exe` as the holders (UBA exit code 9001). The local `[NoUba]` retry failed with `LINK : fatal error LNK1104: cannot open file`.

No interactive editor was open. The holder was an `UnrealEditor.exe` started about 40 minutes earlier by a separate measurement workflow, with the same project file and `-server -nullrhi -NoLiveCoding -NoCompile -unattended`. The `CrashReportClientEditor` process had started in the same second, which is its normal companion launch, not a crash. After the user said the editor had been closed, the same process IDs were still alive with unchanged memory.

## Cause and resolution

Cause confirmed. Windows refuses write access to a DLL that a running process has loaded. An editor started in server or other headless mode loads the same editor module binaries as an interactive editor. `-NoLiveCoding` only avoids the Live Coding mutex described in [R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS](R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS.md). It does not release the output files, so this failure appears at link time rather than as an up-front refusal.

Resolution: with the user's approval, the editor, its `CrashReportClientEditor` and its `UnrealTraceServer` were stopped by process ID. The same build command was rerun and succeeded, relinking only the remaining actions.

## Recheck and prevention

Correction check, 2026-11-26: the rerun after the processes exited ended with `Result: Succeeded`.

Prevention check, 2026-11-26: before the first build, a process listing filtered on the project file path (`Get-CimInstance Win32_Process`, selecting `CommandLine`) found the server-mode editor. The listing was repeated after the user reported it closed and still showed the same process IDs. The build failure then confirmed that exactly these processes held the DLL, and the build succeeded once they exited. The check detected the actual blocker, so its state is verified for this condition.

Applicability: the check covers any editor process of the same project. Processes of other projects on the same engine do not lock this project's binaries, but they can still trigger the Live Coding refusal in the related record. A compile-only success is partial evidence: it shows the changed source compiles but not that the target links. Report the link as blocked until it succeeds.

## Evidence

- Session observation, 2026-11-26: the build log lines quoted above (UBA 9001, LNK1104, `Result: Failed (OtherCompilationError)`), the process listing with command lines and start times, the user-approved stop by process ID, and the successful rebuild.
- Windows file-sharing behavior for loaded images: [Microsoft, LNK1104](https://learn.microsoft.com/en-us/cpp/error-messages/tool-errors/linker-tools-error-lnk1104) (lists a file in use by another process as a cause).
