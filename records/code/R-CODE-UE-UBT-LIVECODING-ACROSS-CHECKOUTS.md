---
id: R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS
title: An Unreal build was refused for Live Coding although no editor had the project being built open
summary: UnrealBuildTool checks a named mutex that is derived from the editor executable path, not from the project, so an editor with Live Coding in another checkout that uses the same engine blocks builds of every project on that engine. Close that editor or build with -NoHotReloadFromIDE when the build is meant to be independent.
kind: error
scope: UnrealBuildTool on Windows when several project checkouts share one engine installation or source build
keywords: [UnrealBuildTool, UBT, Live Coding, LiveCoding, "Unable to build while Live Coding is active", named mutex, "Global\\LiveCoding_", HotReload.cs, "-NoHotReloadFromIDE", bAllowHotReloadFromIDE, shared engine, multiple checkouts, Build.bat]
status: resolved
checked_at: 2026-11-24
context:
  engine: "Unreal Engine 5.8 source build"
  platform: Windows 11
trigger: Building an editor target from the command line while an editor from another project checkout on the same engine is running with Live Coding enabled
symptom: "UBT stops with \"Unable to build while Live Coding is active\" although no editor has the target checkout open"
cause_status: confirmed
prevention: Before a command-line build, check for any running editor that uses the same engine executable, not just the same project; close it, or pass -NoHotReloadFromIDE only when the build must not affect that editor
prevention_status: proposed
---

## Expected and observed

A code-only editor build was started in one checkout. No editor had that checkout open. Expected: a normal build. Observed: UBT refused with `Unable to build while Live Coding is active`. An editor process from a second checkout of the same game, using the same engine build, was running.

## Cause and resolution

Confirmed in UBT source: the Live Coding check opens a mutex named `Global\LiveCoding_` followed by the editor executable path. The name contains no project path, so any Live Coding session of that engine executable matches. Closing the other checkout's editor released the mutex and the same build then succeeded.

The UBT source also shows that the check is skipped when hot reload from the IDE is disabled (`bAllowHotReloadFromIDE`, command-line `-NoHotReloadFromIDE`). That bypass was read but not run here; using it while the other editor is live leaves that editor's loaded modules out of date if both share output binaries.

## Recheck and prevention

On 2026-11-24 the build succeeded after the other editor closed. The proposed check (look for any editor process started from the same engine executable before building) was not run as a separate safeguard, so it stays proposed.

Separate engine installations have different executable paths and do not share the mutex. Behavior on other platforms was not examined.

## Evidence

- Engine source, Unreal Engine 5.8: `Engine/Source/Programs/UnrealBuildTool/System/HotReload.cs` (Live Coding mutex name `Global\LiveCoding_` built from the editor executable path, checked only when `bAllowHotReloadFromIDE` is true); `Engine/Source/Programs/UnrealBuildTool/Configuration/BuildConfiguration.cs` (`[CommandLine("-NoHotReloadFromIDE", Value = "false")]` on `bAllowHotReloadFromIDE`).
- Session observation, 2026-11-24: the refused build, the other checkout's editor process, and the successful rebuild after it closed.
