# Feedback: link_project.py writes its rule block into tracked team instruction files

- Date: 2026-11-26
- OneStep version used: 99cd60c (2026-11-26)
- Relevant skills/instructions: `link_project.py`; user-level "Connect this project" instruction
- Kind: problem
- Status: received
- Task context: A shared team game repository whose `AGENTS.md` and `CLAUDE.md` are Git-tracked team instructions. The user already loads OneStep through a Git-excluded personal file (`CLAUDE.local.md`) that states OneStep setup must not be copied into `AGENTS.md`, `CLAUDE.md` or any tracked file. The user asked to connect the project.

## Expected and observed

Expected: connecting a project with personal, local-only OneStep use leaves tracked team files unchanged, or offers a local-only mode, and `--check` can confirm such a connection.

Observed (AI): `link_project.py <project>` reported "5 files updated". It appended the `onestep:checkout` block to the tracked `AGENTS.md` and `CLAUDE.md`, created an untracked `GEMINI.md`, and created `.onestep/` (with its own `.gitignore` for `checkout.local.json`). `--check` then passed. At the user's request the AI restored `AGENTS.md` and `CLAUDE.md` and added `/.onestep/` and `/GEMINI.md` to `.git/info/exclude`. After that, `--check` fails with "Connection differs from this checkout. Rerun the same command without --check.", although the pointer file is intact and OneStep still loads through the personal file.

Impact: in a shared repository the connection either leaves team instruction diffs that can be committed by accident, or, once reverted to respect the project rule, can no longer be verified by `--check`. Rerunning the command as the error suggests would reapply the unwanted edits.

## Evidence and suspected cause

- `link_project.py` line 145 fixes `entry_files = ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]`; lines 149-153 merge the rule into each, and lines 165-167 make `--check` fail when any of them lacks the block.
- There is no option for a local or Git-excluded entry file (`--help` lists only `--register` and `--check`).
- The user instruction "Connect this project" was followed as written; the conflict comes from the project's local rule, not from a deviation.
- Not checked: Codex or Gemini sessions in this project after the revert.

## Suggested improvement

Add a local-only mode (for example `--local`) that writes the rule into a Git-excluded entry file such as `CLAUDE.local.md` or `AGENTS.override.md`, adds created files to `.git/info/exclude`, and makes `--check` accept that layout. Alternatively, detect tracked entry files and ask before editing them. Check: in a repository with tracked `AGENTS.md`/`CLAUDE.md`, a local-mode link leaves `git status` showing no tracked changes and `--check` exits 0.

## Review and verification

Maintainer fills during processing.
