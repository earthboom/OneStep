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
3. Check `git status` and the branch. An unexpected branch or mass of staged deletions is a reason to verify the path against the build inputs.
4. When the project names the engine by a registry GUID (`EngineAssociation` in the `.uproject`), resolve the GUID to a path before assuming the environment variable is the build input.

Only then search the engine for modification markers or renderer changes.

## Applicability and exceptions

Applies to any project that resolves a custom engine by path or by registry association. It does not apply to a launcher-installed engine, which has no git history to misread. A worktree layout is one cause; other causes include several engine clones for different releases side by side.

## Checks

- `git worktree list` lists more than one path: decide which one is the release branch before reading.
- `Engine/Build/Build.version` is missing: the checkout is not a usable engine tree.
- The editor executable that the project's run scripts build from the environment variable does not exist: fix the variable before the first run.
- The `.uproject` `EngineAssociation` GUID is missing from `HKCU\Software\Epic Games\Unreal Engine\Builds`: the current user's association cannot be confirmed there.
- Before running a registration script that removes other GUIDs pointing at the same engine path, list the `EngineAssociation` of every local `.uproject`. A checkout whose `.uproject` was locally rewritten to an auto-generated GUID loses its engine association when that GUID is removed. A lower-impact alternative is to add the project GUID without removing others and to set the engine variable at user scope; both are reversible without administrator rights.
- History depth alone is inconclusive in a shallow clone. Compare the commit, branch and executable selected by the actual build or launch command.
- Restrict engine modification searches to the relevant modules or use `git log -- <paths>`, especially on large Windows checkouts.

## Evidence

A Windows UE 5.8 source-build investigation on 2026-11-05–06 found an environment variable selecting an incomplete checkout while a linked worktree contained the engine version and editor executable. The project association and per-user registration also disagreed. Inspecting those inputs corrected a source-history conclusion. Registration and launch were not retested end to end. [Git worktree manual](https://git-scm.com/docs/git-worktree)
