---
id: K-CODE-UE-ENGINE-CHECKOUT
title: Confirm which engine source checkout is current before reading a custom Unreal engine
summary: An engine path environment variable can point at a stale checkout whose active source lives in a git worktree; check worktrees, branch and Build.version before drawing conclusions from engine source or history.
kind: lesson
scope: Projects built on a source-built or forked Unreal Engine located through an environment variable or registry association
keywords: [Unreal Engine, custom engine, engine fork, git worktree, Build.version, EngineAssociation, engine source, stale checkout]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5 source build
  vcs: git with worktrees
---

## Guidance

Before reading engine source, engine history or engine modification markers, confirm which checkout holds the engine version the project actually uses:

1. Run `git worktree list` in the path the environment variable names. Another worktree may hold the release branch.
2. Check that `Engine/Build/Build.version` exists and that its major and minor version match the version the project documents.
3. Check `git status` and the branch. A default branch with a very short history or a mass of staged deletions is not the engine source.
4. When the project names the engine by a registry GUID (`EngineAssociation` in the `.uproject`), resolve the GUID to a path before assuming the environment variable is the build input.

Only then search the engine for modification markers or renderer changes.

## Applicability and exceptions

Applies to any project that resolves a custom engine by path or by registry association. It does not apply to a launcher-installed engine, which has no git history to misread. A worktree layout is one cause; other causes include several engine clones for different releases side by side.

## Checks

- `git worktree list` lists more than one path: decide which one is the release branch before reading.
- `Engine/Build/Build.version` is missing: the checkout is not a usable engine tree.
- The editor executable that the project's run scripts build from the environment variable does not exist: fix the variable before the first run.
- The `.uproject` `EngineAssociation` GUID is missing from `HKCU\Software\Epic Games\Unreal Engine\Builds`: the engine registration step was skipped for the current checkout.
- Before running a registration script that removes other GUIDs pointing at the same engine path, list the `EngineAssociation` of every local `.uproject`. A checkout whose `.uproject` was locally rewritten to an auto-generated GUID loses its engine association when that GUID is removed. A lower-impact alternative is to add the project GUID without removing others and to set the engine variable at user scope; both are reversible without administrator rights.
- The commit count of the current branch is implausibly small for an engine (tens rather than hundreds of thousands): the wrong branch.
- Restrict marker searches (for example a `*_ENGINE_MODIFIED` macro) to specific module directories or use `git log -- <paths>`; a recursive grep over all of `Engine/Source` took longer than five minutes on Windows.

## Evidence

Observed once in a UE 5.8 game project on Windows (2026-11-05, rechecked 2026-11-06). The engine environment variable pointed at a checkout on its default branch: 22 commits, about 148,000 staged deletions, no `Build.version`. `git worktree list` showed the release branch in a sibling worktree with `Build.version` 5.8 and the studio's engine modifications. The first reading of engine history came from the stale checkout and was corrected after the worktree check.

A follow-up check on 2026-11-06 found that the project's run scripts launch `%<engine env var>%\Engine\Binaries\Win64\UnrealEditor.exe`, and the stale checkout had no `Engine` directory at all. The scripts therefore could not start from that path, while the worktree held a built `UnrealEditor.exe`. Check that the executable the scripts name exists before the first run.

The registry check on the same day found the project's `EngineAssociation` GUID unregistered; the only registered build was an auto-generated GUID pointing at the worktree. The new engine worktree shipped a registration script that writes the project GUID, the engine environment variable and the shared DDC variable together, and it had not been run. When a new engine checkout or worktree replaces an old one, run its registration script (or equivalent) so the GUID and the environment variable move together.

Not verified: that running the registration script alone makes the run scripts and the `.uproject` association work end to end.
