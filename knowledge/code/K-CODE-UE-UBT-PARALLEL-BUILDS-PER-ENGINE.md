---
id: K-CODE-UE-UBT-PARALLEL-BUILDS-PER-ENGINE
title: Decide whether a second Unreal engine tree is needed to build several project checkouts in parallel
summary: UnrealBuildTool serializes every build launched from the same UBT executable through a named single-instance mutex, so project checkouts that share one engine tree queue behind each other; a separate engine tree has its own UBT path and builds independently, at the cost of disk, a full engine build and keeping both trees on the same engine revision.
kind: reference
scope: Unreal Engine source builds on Windows where several project checkouts or branches are built concurrently on one machine
keywords: [UnrealBuildTool, UBT, single instance mutex, GlobalSingleInstanceMutex, UnrealBuildTool_Mutex, "-WaitMutex", "-NoMutex", "Waiting for other instance of UBT", parallel builds, multiple checkouts, second engine tree, git worktree, BuildConfiguration.xml, MaxParallelActions, Unreal Build Accelerator, UBA]
status: active
checked_at: 2026-11-27
context:
  engine: "Unreal Engine 5.8 source build"
  platform: Windows 11
---

## Guidance

- **Mechanism.** In build modes marked single-instance, UBT acquires a global named mutex whose name is derived from the path of the running UBT assembly (`UnrealBuildTool_Mutex` plus that path). With `-WaitMutex` a second build waits; without it the second build fails immediately. The project path is not part of the name, so every build of every project on one engine tree contends for the same mutex.
- **Consequence.** Several project checkouts on one engine tree cannot compile at the same time, however much CPU or memory is free. A separate engine tree has a different UBT path and therefore a separate mutex. The Live Coding check is likewise keyed by the editor executable path (see `R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS`), so a separate tree also removes that cross-checkout block.
- **`-NoMutex` is not a substitute.** It skips the check but leaves both builds writing to the same engine `Binaries`, `Intermediate` and generated-header locations for any engine module that a shared-environment target rebuilds. Use it only when you know no engine module will be rebuilt by either build.
- **Cost of a second tree.** A built source tree is mostly build output: binaries, intermediates and plugin build products, not sources. Budget for the size of the existing built tree on the target drive, or for the targets you will actually build there. Debug symbols (`.pdb`) are usually the largest single part, so the target's `DebugInfo` mode (for example `ProjectOnly`, set in that tree's `BuildConfiguration.xml` or with `-DebugInfo=`) changes the budget far more than the choice between a clone and a worktree; it also removes engine-side symbols for debugging. If the engine is a Git repository, `git worktree add` on another drive shares the object store; check out a detached commit or a separate local branch because Git refuses the same branch in two worktrees. The new tree still needs its dependency setup and a full engine build. Copying a built tree avoids the download but absolute paths in build intermediates can still trigger large rebuilds.
- **Setup side effects.** `Setup.bat` also installs redistributables machine-wide and runs `UnrealVersionSelector /register`, which offers to repoint the `.uproject` file association to the new tree with elevation. On a machine that already has a working tree, running only `GitDependencies` and the hook registration avoids those changes; opening the editor later registers the tree under the user's engine builds without touching file associations. `Setup.bat` writes its post-checkout and post-merge dependency hooks only when `.git\hooks` is a directory, so a worktree (where `.git` is a file) gets no hooks and its dependencies must be synced by hand after each update. `GitDependencies` also finds its download cache only through a `.git` directory, so a worktree runs without a cache unless `-cache=` or `UE_GITDEPS` is given.
- **Ongoing cost.** Both trees must stay on the engine revision that the project associates, and every engine update must be applied and built in both. A tree left behind can save assets with a different engine version.
- **Throughput limit.** A second tree removes waiting, not CPU contention. Two large local compiles on the same cores take roughly as long together as in sequence; the gain is that a small incremental build no longer waits for a long one. Cap local parallelism per tree in that tree's `Engine/Saved/UnrealBuildTool/BuildConfiguration.xml` when both run at once, and prefer a distributed executor (UBA with a remote pool, or similar) when the real constraint is total compile capacity.
- **Binding a checkout to a tree.** Point each checkout at its tree explicitly: the engine path the build scripts read, the registered engine association in the project descriptor, and the IDE solution generated from that tree. A per-user environment variable shared by all checkouts silently sends every checkout to the same tree.

## Applicability and exceptions

- Checked against the UE 5.8 UBT source. Other versions may name or scope the mutex differently; recheck the source line before relying on it.
- Installed (precompiled) engines have the same per-path mutex. A team build farm that compiles on separate agents is unaffected.
- When the waiting is caused by an open editor locking module DLLs or by Live Coding, a second tree helps only if that editor runs from the other tree.

## Checks

- Before adding a tree, confirm the queue is the UBT mutex: a second build prints that it is waiting for another UBT instance, or fails to acquire the mutex without `-WaitMutex`.
- After setup, start a build in each checkout at the same time and confirm neither waits.
- After an engine update, compare the engine commit of both trees before building or saving assets.

## Evidence

- Engine source, Unreal Engine 5.8: `Engine/Source/Programs/UnrealBuildTool/UnrealBuildTool.cs`, around line 446: `GlobalSingleInstanceMutex.GetUniqueMutexForPath("UnrealBuildTool_Mutex", FileReference.FromString(Assembly.GetExecutingAssembly().Location))`, acquired with `SingleInstanceMutex.Acquire` under `-WaitMutex` and `AcquireNowOrThrow` otherwise, skipped when `NoMutex` is set. Read 2026-11-27; the parallel-build check above was not run.
- Observation, 2026-11-27: a built UE 5.8 source tree measured about 336 GiB, of which plugins (with build products) were about 144 GiB, binaries about 70 GiB, intermediates about 39 GiB and sources about 37 GiB; the shared Git object store was about 26 GiB. In the same tree `.pdb` files were about 154 GiB (about 107 GiB under engine plugins), the Development editor build was about 134 GiB of binaries and 58 GiB of intermediates, the dependencies installed by `Setup.bat` were about 85 GiB (about 30 GiB compressed download, from `Commit.gitdeps.xml`), tracked files at HEAD were about 2.7 GiB, and one branch's history occupied about 12 GiB of packed objects (`git rev-list --disk-usage --objects`). `DebugInfoMode` values (`None`, `Engine`, `EnginePlugins`, `Project`, `ProjectPlugins`, `EngineOnly`, `ProjectOnly`) are defined in `Engine/Source/Programs/UnrealBuildTool/Configuration/Rules/TargetRules.cs`; the size saved by `ProjectOnly` was not measured. A fresh single-branch clone of the same engine revision, with dependencies (31 GB downloaded) and a full-debug-info Development build of `UnrealEditor`, `ShaderCompileWorker`, `LiveCodingConsole`, `CrashReportClientEditor` and `UnrealPak`, measured 305.7 GiB including a 12.7 GiB Git store; the build took 32 minutes with a UBA remote pool. Engine plugins enabled only by a game project are built later by that project's editor target and were not included. Setup side effects: read from the 5.8 `Setup.bat`, `Engine/Source/Programs/UnrealVersionSelector/Private/UnrealVersionSelector.cpp` (`RegisterCurrentEngineDirectory`, file-association prompt and elevated `/fileassociations`) and `Engine/Source/Programs/GitDependencies/Program.cs` (cache lookup through a `.git` directory), and observed in a worktree with no registered hooks.
- Related incident: `R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS` (Live Coding mutex keyed by editor executable path).
