---
id: K-CODE-GIT-ISOLATED-MERGE
title: Resolve a large branch merge in a sparse linked worktree without touching the main checkout
summary: Dry-run the merge with git merge-tree to get the conflict list and stage blobs, then do the real merge in a linked worktree with a cone sparse checkout of only the conflicting directories and LFS smudge disabled; decide binary and generated conflicts from history and regeneration, and keep EOL-only regeneration drift out of the index.
kind: method
scope: Git repositories with large binary or LFS content where the main working copy must stay untouched (open editors, locked files, no checkout rule) while a merge with many conflicts is resolved
keywords: [git merge, git merge-tree, git worktree, sparse-checkout, GIT_LFS_SKIP_SMUDGE, LFS pointer conflict, binary conflict, generated code, protoc, core.autocrlf, EOL drift, MERGE_MSG, cleanup=verbatim, merge commit]
status: active
checked_at: "2026-11-06"
context:
  vcs: git 2.x with git-lfs
  platform: Windows (core.autocrlf=true)
---

## Guidance

1. Dry run first: `git merge-tree --write-tree --name-only <ours> <theirs>` lists the conflicted paths without updating the index or working tree, and the full output gives the base, ours and theirs blob ids per path. Save both; they are the ground truth for the rest of the work.
2. Create the merge branch in a linked worktree: `git worktree add -b <merge-branch> <dir> <ours>`, then `git sparse-checkout set --cone <conflict dirs>` so only the directories holding conflicts (plus what regeneration tools need) are materialized. Export `GIT_LFS_SKIP_SMUDGE=1` for every git command there so LFS files stay pointers.
3. Run `git merge --no-ff --no-commit <theirs>` in the worktree. The conflict set must equal the dry run; stop if it does not.
4. Decide each binary or LFS conflict from history, never by default to a side: compare the two sides' blob ids at the commits that changed the path (`git log <base>..<side> -- <path>`, `git rev-parse <commit>:<path>`). If a side's blob is identical to a known historical version, inspect the later history and intended changes before choosing the staged version. Two unrelated changes to one asset stay a human decision; list them with both sides' tickets, authors and dates.
5. Regenerate generated outputs (protobuf code, compiled data) from the auto-merged source instead of merging them. Before trusting the generator, regenerate each side's committed outputs from that side's own sources and require equality ignoring line endings.
6. With `core.autocrlf=true`, a generator that writes LF makes every output look modified while the normalized diff is empty. Classify with `git diff --quiet -- <file>` (normalized) per file and restore the EOL-only files with `git checkout -- <file>`; stage only files whose normalized content changed. A generator that enumerates inputs with an unordered directory listing can also reorder whole blocks: compare added and removed lines to locate a pure reorder, then establish that the language and generator contract allow it before discarding the difference.
7. Write the merge commit message into `.git/worktrees/<name>/MERGE_MSG` (or `.git/MERGE_MSG`): keep git's subject and the `# Conflicts:` block verbatim and append per-path resolution notes; commit with `git commit --cleanup=verbatim` so the block survives. Keep human decisions visibly unresolved in the index and finish them before making the merge commit.
8. Before the commit: no unmerged paths, `git status` shows no unstaged drift in the worktree, and every regenerated or semantically merged artifact has an independent check recorded.

## Applicability and exceptions

Applies to merges where the number or size of conflicts makes an in-place merge in the main checkout unsafe. Sparse checkout must include every directory a regeneration tool reads or writes, otherwise the tool runs on a partial tree; extend the sparse set before running it. An LFS conflict appears as a text conflict on the pointer lines when no `merge.lfs` driver is configured; the pointer is resolved by `git checkout --ours|--theirs -- <path>` followed by `git add`, not by editing it. Semantic merges of data files have their own methods (see K-CODE-UE-LOC-MERGE for Unreal localization files).

## Checks

- Dry-run conflict list == real merge conflict list.
- For every binary path resolved to a side, the index blob equals that side's blob (`git ls-files -s`).
- For every regenerated output, regeneration from the staged sources reproduces the staged blob ignoring CR.
- `git status --short` in the worktree shows only `UU` for the deliberately deferred paths and `M `/`A ` for staged entries; nothing in ` M`, `MM` or `??` after regeneration.
- The main checkout's `git status` is unchanged by the whole procedure.

## Evidence

In a UE5 game repository on Windows on 2026-11-06 the preview and real merge identified the same paths. Binary history and independent regeneration distinguished genuine differences from line-ending and order-only changes. Unrelated edits to the same binary were left for human resolution. Custom LFS merge drivers and Git versions predating `merge-tree --write-tree` (2.38) were not tested. [Git, merge-tree](https://git-scm.com/docs/git-merge-tree/2.45.0.html) · [Git, worktree](https://git-scm.com/docs/git-worktree)
