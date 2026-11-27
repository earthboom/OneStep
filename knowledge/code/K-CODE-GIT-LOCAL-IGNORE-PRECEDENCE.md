---
id: K-CODE-GIT-LOCAL-IGNORE-PRECEDENCE
title: Keep a path out of Git locally when a nested .gitignore re-includes it with a negation
summary: A pattern in $GIT_DIR/info/exclude loses to a negation such as !dir/** in a .gitignore inside the working tree, so the path stays untracked-and-visible; put the local ignore after the negation in that same .gitignore and confirm with git check-ignore -v by reading the reported pattern, not the exit code.
kind: reference
scope: Git working trees where a committed .gitignore re-includes a directory (for example shared tool or skill folders) and one user needs a personal subfolder kept out of commits
keywords: [git, gitignore, ".git/info/exclude", info/exclude, negation, "!dir/**", precedence, check-ignore, "git check-ignore -v", local-only, untracked, personal files]
status: active
checked_at: "2026-11-25"
context:
  git: "2.45.1.windows.1"
  platform: Windows
---

## Guidance

Git reads ignore patterns from several sources with a fixed precedence. Patterns in a `.gitignore` inside the working tree beat `$GIT_DIR/info/exclude`, and `info/exclude` beats `core.excludesFile`. Within one level the last matching pattern wins, and a lower-level `.gitignore` beats a higher-level one.

So when a committed `.gitignore` says `*` then `!skills/` and `!skills/**`, adding `sub/skills/mine/` to `info/exclude` does nothing: the negation re-includes the path. To keep a personal folder local:

1. Add the ignore line to the same `.gitignore` that holds the negation, after the negation line (for example `skills/mine/`).
2. That `.gitignore` edit is itself a working-tree change. Leave it uncommitted, or ask whether the team wants the rule committed. `git update-index --skip-worktree` can hide the edit from `git status`, but it also hides later upstream changes to that file.
3. If editing that file is not acceptable, put the personal folder outside the re-included directory (for example a user-level tool directory) instead of fighting precedence.

## Applicability and exceptions

Applies to untracked paths. An already tracked file stays tracked whatever the ignore rules say; it needs `git rm --cached` or a different approach. A negation cannot re-include a file whose parent directory is excluded, so `!dir/**` works only when `dir/` itself is re-included (as with `!skills/`). Linked worktrees share `info/exclude` but each has its own copy of the in-tree `.gitignore`, so an uncommitted rule must be added in each worktree that needs it.

## Checks

- Run `git check-ignore -v <path>` and read the reported source and pattern. Exit code 0 only means a pattern matched; a match on a `!` pattern means the path is NOT ignored.
- `git status --short --untracked-files=all <dir>` no longer lists the personal files.

## Evidence

Git documentation, gitignore, section "Pattern format" and the precedence list (https://git-scm.com/docs/gitignore). Local reproduction on 2026-11-25 with git 2.45.1.windows.1 in a scratch repository: with `sub/.gitignore` containing `*`, `!.gitignore`, `!skills/`, `!skills/**` and `sub/skills/mine/` in `.git/info/exclude`, `git check-ignore -v` reported `sub/.gitignore:4:!skills/**` (exit 0) and `git status` still listed `sub/skills/mine/SKILL.md`. After appending `skills/mine/` to `sub/.gitignore`, `check-ignore` reported that line and the file disappeared from `git status`. The same result was observed in a real project's personal skill folder. Tracked files, `skip-worktree` and other Git versions were not tested.
