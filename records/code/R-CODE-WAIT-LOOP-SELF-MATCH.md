---
id: R-CODE-WAIT-LOOP-SELF-MATCH
title: A wait-until-process-exits loop never ended because its command-line pattern matched the waiting shell itself
summary: A polling loop that waits while any process command line matches a text pattern also matches its own shell and helper processes, whose command lines contain that pattern, so it never exits. Match on the process image name first and confirm once, before waiting, that the matched processes are the intended ones.
kind: error
scope: Shell polling loops on Windows that wait for other processes by searching process command lines (Get-CimInstance Win32_Process, wmic, ps/pgrep -f style matching)
keywords: [polling, wait loop, process wait, self-match, command line match, Get-CimInstance, Win32_Process, CommandLine, "pgrep -f", background task, UnrealBuildTool, dotnet.exe, build mutex wait]
status: resolved
checked_at: 2026-11-26
context:
  platform: Windows 11
  shell: "Git Bash launching Windows PowerShell 5.1 per poll"
trigger: Starting a background loop that sleeps while Get-CimInstance Win32_Process finds any process whose CommandLine matches a tool name, to wait for another build before starting one's own
symptom: The wait never reports completion after the awaited build is gone; a one-off listing with the same filter shows the loop's own bash.exe and powershell.exe processes, plus an unrelated helper whose path contains the tool name, as matches
cause_status: confirmed
prevention: Filter by process Name (for example Name -eq 'dotnet.exe') before matching a CommandLine pattern, and run the filter once as a listing before starting the loop to confirm no match is the waiter itself or an unrelated helper
prevention_status: verified
---

## Expected and observed

Before starting a build, a background loop was meant to wait until another checkout's build tool and any editor process had exited. Each poll ran `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'UnrealBuildTool' -or $_.Name -match '^UnrealEditor' }` and slept while anything matched. Expected: the loop prints a completion line once the other build ends. Observed: it was still waiting long after; a listing with the same filter returned the intended `dotnet.exe ... UnrealBuildTool.dll` process and also several `bash.exe` and `powershell.exe` processes belonging to the loop itself, plus `UbaVisualizer.exe`, whose executable path contained the tool name.

## Cause and resolution

Confirmed from the listing. The loop's own shell command line contained the literal pattern text, and the per-poll PowerShell process carried it as well, so the condition was true for as long as the loop ran. A long-lived helper whose install path contained the tool name would also have kept it true after the build ended.

Resolution: the loop was stopped and restarted with `($_.Name -eq 'dotnet.exe' -and $_.CommandLine -match 'UnrealBuildTool\.dll') -or $_.Name -match '^UnrealEditor'`. The image-name filter excludes the waiter's shells, and the narrower pattern excludes the helper. The restarted loop printed its completion line once the other build finished, and the dependent build then ran.

## Recheck and prevention

On 2026-11-26 the one-off listing with the original filter showed the waiter's own processes among the matches, which is the check that exposes this failure; with the corrected filter, the loop ended when the awaited build ended. Applies to any command-line text match, including `pgrep -f` and `ps | grep`, where the waiting command carries the searched text. Not examined: processes whose image name is shared by unrelated tools, such as other `dotnet.exe` programs whose command lines happen to mention the same assembly.

## Evidence

- Session observation, 2026-11-26, Windows 11 with Git Bash and Windows PowerShell 5.1: the stalled loop, the process listing that showed the self-matches, and the corrected loop's completion line.
