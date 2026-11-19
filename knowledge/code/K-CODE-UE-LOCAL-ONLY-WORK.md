---
id: K-CODE-UE-LOCAL-ONLY-WORK
title: Keep Unreal editor work local by checking the shared DDC and the distributed compile paths
summary: A local Unreal build or editor session can still reach team infrastructure through the shared DDC, UBA/Horde remote compile and Incredibuild shader compile; disable the shared DDC per checkout with a User*.ini override and confirm each path from the logs.
kind: method
scope: Unreal Engine 5 projects on a studio network with a shared DDC and distributed compile agents, when work must stay on the local machine
keywords: [Unreal Engine, DDC, Derived Data Cache, shared DDC, UserEngine.ini, UnrealBuildTool, UBA, Horde, Incredibuild, XGE, distributed compile, local only, "Unreal Build Accelerator", "LogDerivedDataCache", "BuildConfiguration.xml", "bAllowUBAExecutor"]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5.8 source build
  platform: Windows desktop
---

## Guidance

When a task must stay on the local machine, check each path by which an editor build or editor session touches team infrastructure. Do not assume that a local command stays local.

1. The Derived Data Cache (DDC) stores regenerable engine/asset data. For a filesystem-backed shared DDC, disable it for one checkout only by creating `<Project>/Config/UserEngine.ini` with `[DerivedDataCacheStores]` and `Shared=(Type=FileSystem, Path=None)`. Use the store name the project's `DefaultEngine.ini` uses. Keep the file out of version control with `.git/info/exclude` (`<Project>/Config/User*.ini`) so nothing changes for the team. On editor start, `LogDerivedDataCache` must print `Shared: Disabled because the path is configured to 'None'`.
2. C++ compile. Unreal Build Accelerator (UBA) can execute compiler actions dispatched through Horde. UnrealBuildTool reads the per-user `%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml`. A configured `<Horde>` server and enabled `bAllowUBAExecutor` can allow remote actions. Confirm actual execution using the build output. Look for `RemoteExecutor:` and `Horde URL:` in the build output.
3. Shader compile. XGE is a separate distributed execution controller used by Incredibuild. The editor log line `Using XGE Controller for shader compilation` together with an installed Incredibuild (`xgConsole.exe`) means shader jobs can go to Incredibuild agents. `LogUbaHorde: ... Not Enabled` covers only UBA, not Incredibuild.

Report every path that is still active before claiming that the work is local only.

## Applicability and exceptions

Applies to studio setups with a shared DDC, Horde/UBA or Incredibuild. Check the backend and executor actually selected; other versions and installations can use other services. The `User*.ini` layer (GameDirUser) affects only that checkout. The local DDC (engine `DerivedDataCache` folder and the local ZenServer) is still shared with other projects on the same engine on this machine. Treat host-local sharing separately if the requirement calls for per-project isolation.

## Checks

- Find the DDC proof line in the editor log by the `LogDerivedDataCache` category. Plain `Shared:` also matches `LogEOSShared:` and other categories.
- `git status` stays clean and `git check-ignore -v` names the exclude rule for the override file.
- The build output has no `RemoteExecutor:` lines when remote compile must be off.
- Check executor settings and logs before authorizing a build that must stay local. A selected remote controller and an actual remote action support different conclusions.

## Evidence

In a Windows UE 5.8 source-build session on 2026-11-06, the checkout override disabled its filesystem DDC store. The build output still identified remote C++ actions and the editor selected the XGE shader controller. Actual remote shader execution and a per-build local-only UBA configuration were not verified. Log categories and executor settings are version-dependent. [Epic, Horde and Unreal Build Accelerator](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-unreal-build-accelerator-and-remote-compilation-tutorial-for-unreal-engine?application_version=5.8)
