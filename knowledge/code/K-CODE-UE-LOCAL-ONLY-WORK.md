---
id: K-CODE-UE-LOCAL-ONLY-WORK
title: Keep Unreal editor work local by checking the shared DDC and the distributed compile paths
summary: A local Unreal build or editor session can still reach team infrastructure through the shared DDC, UBA/Horde remote compile and Incredibuild shader compile; disable the shared DDC per checkout with a User*.ini override and confirm each path from the logs.
kind: method
scope: Unreal Engine 5 projects on a studio network with a shared DDC and distributed compile agents, when work must stay on the local machine
keywords: [Unreal Engine, DDC, Derived Data Cache, shared DDC, UserEngine.ini, UnrealBuildTool, UBA, Horde, Incredibuild, XGE, distributed compile, local only]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5.8 source build
  platform: Windows desktop
---

## Guidance

When a task must stay on the local machine, check each path by which an editor build or editor session touches team infrastructure. Do not assume that a local command stays local.

1. Shared DDC. Disable it for one checkout only by creating `<Project>/Config/UserEngine.ini` with `[DerivedDataCacheStores]` and `Shared=(Type=FileSystem, Path=None)`. Use the store name the project's `DefaultEngine.ini` uses. Keep the file out of version control with `.git/info/exclude` (`<Project>/Config/User*.ini`) so nothing changes for the team. On editor start, `LogDerivedDataCache` must print `Shared: Disabled because the path is configured to 'None'`.
2. C++ compile. UnrealBuildTool reads the per-user `%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml`. A `<Horde>` server with `bAllowUBAExecutor` sends compile actions to remote agents. Look for `RemoteExecutor:` and `Horde URL:` in the build output.
3. Shader compile. The editor log line `Using XGE Controller for shader compilation` together with an installed Incredibuild (`xgConsole.exe`) means shader jobs can go to Incredibuild agents. `LogUbaHorde: ... Not Enabled` covers only UBA, not Incredibuild.

Report every path that is still active before claiming that the work is local only.

## Applicability and exceptions

Applies to studio setups with a shared DDC, Horde/UBA or Incredibuild. A machine without these has nothing to check. The `User*.ini` layer (GameDirUser) affects only that checkout. The local DDC (engine `DerivedDataCache` folder and the local ZenServer) is still shared with other projects on the same engine on this machine. That is harmless, because entries are keyed by content.

## Checks

- Find the DDC proof line in the editor log by the `LogDerivedDataCache` category. Plain `Shared:` also matches `LogEOSShared:` and other categories.
- `git status` stays clean and `git check-ignore -v` names the exclude rule for the override file.
- The build output has no `RemoteExecutor:` lines when remote compile must be off.
- Remote compile agents only lend CPU and change no shared files. If the user forbids even that, disable it before the build, not after.

## Evidence

Observed once in a UE 5.8 game project on Windows (2026-11-06). The `UserEngine.ini` override produced `Shared: Disabled because the path is configured to 'None'`, while `ZenShared` and `Cloud` were already disabled by host `None`. An editor build of 549 actions ran 336 of them on four Horde UBA agents, through the user's own `BuildConfiguration.xml`, with no flag on the command line. On editor start the shader compiler chose the XGE controller, and Incredibuild was installed. The report to the user called the build "local" before the log was read, and was corrected afterwards.

Not verified: which flag or setting turns off remote UBA execution for a single build while keeping local UBA, and whether shader jobs actually reached remote Incredibuild agents.
