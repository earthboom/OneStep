---
id: R-CODE-GIT-INDEX-LOCK-RENAME
title: "Verify index and refs after an interrupted Windows checkout"
summary: "An interrupted Git for Windows switch can leave updated files and a pending index while HEAD still names the old branch. Inspect the actual state before deciding how to recover."
kind: error
scope: "Git for Windows, interrupted checkout in a clean linked worktree with Git LFS filters"
keywords: ["Git for Windows","index.lock","GIT_INDEX_FILE","reflog","symbolic-ref","HEAD","git worktree","Git LFS","인덱스"]
status: resolved
checked_at: '2026-11-18'
trigger: "An index replacement prompts for retry during checkout and the terminal cannot accept input"
symptom: "The new worktree files existed, the temporary index remained and the expected branch reference and HEAD update were absent"
cause_status: suspected
prevention: "Use an input-capable terminal and minimize concurrent status polling for the duration of large checkouts"
prevention_status: proposed
---

## Expected and observed

The checkout reached its index replacement step but the retry prompt could not receive input. The worktree, index, branch ref and symbolic HEAD had reached different stages. A transient open handle was suspected. Its owner was never identified.

## Cause and resolution

Git's index stages paths and objects. `index.lock` may hold its pending replacement. `GIT_INDEX_FILE` selects an alternate index and permits read-only comparison on a **copy**. The reflog records local ref movements, so it can disambiguate the commit intended before a remote-tracking ref moved. `HEAD` normally refers to the checked-out branch. Identify the owning worktree, any live writer, local changes and intended commit before interpreting any lock as stale.

## Recheck and prevention

In the recorded clean-worktree recovery, both index files were backed up, the copy of the pending index matched the intended commit, the writer was stopped and the checked index and branch/HEAD were finalized. The resulting status, branch, materialized LFS content and lock state were verified. When the retry prompt is usable, allow the original operation to finish. A manual completion can omit checkout hooks, and matching a commit tree is insufficient when local changes must be carried. Reduced polling remains a proposed precaution.

## Evidence

One historical Windows worktree observation, 2026-11-18. Public references establish Git terminology, not the transient handle's identity. [Git glossary](https://git-scm.com/docs/gitglossary) · [git-reflog](https://git-scm.com/docs/git-reflog) · [Worktree isolation](../../knowledge/code/K-CODE-GIT-ISOLATED-MERGE.md)
