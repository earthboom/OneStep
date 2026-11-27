# Feedback: Regenerating a translation conflicts with a write tool that requires reading the file first

- Date: 2026-11-20
- OneStep version used: fd3b1bb (2026-11-20)
- Relevant skills/instructions: skills/vegabond-knowledge/references/storage.md (catalog save order; generate translations without reopening them), user-level rule that AI never reads OneStep `*.kr.md`
- Kind: problem
- Status: received
- Task context: Claude Code sessions saving knowledge entries and rebuilding a domain catalog, under an instruction never to read or search OneStep `*.kr.md` files

## Expected and observed

Expected: after `build`, the agent regenerates each changed catalog translation from its English file and writes it, without opening the existing translation. Observed: the Claude Code `Write` tool refuses to overwrite an existing file that has not been read in the session ("File has not been read yet"). Reading it would break the `*.kr.md` rule. Agents then improvise: one retest wrote the regenerated translation to a scratch path and copied it over with a shell `cp`; this audit session deleted the stale translation first and then wrote a new one; an earlier retest patched rows into the translation by script, which loaded the old file. The first two keep the rule; the third did not. None of these paths is described anywhere, and the retest that hit the refusal still reported "none" as strategy feedback.

## Evidence and suspected cause

Transcript inspection on 2026-11-20: a `Write` to `knowledge/code/index.kr.md` returned the refusal above; the session then wrote the same content to its scratchpad, compared catalog row IDs with the English catalog, copied the file into place and passed `catalog.py check`. In a separate session, a `Write` to an entry translation failed with "File has been modified since read"; deleting the file and writing it again succeeded. Suspected cause: the storage guide's rule "generate every changed translation from English without reopening it" assumes a write path that does not require a prior read, which this harness's write tool does not provide for existing files. Whether other harnesses share the constraint was not checked.

## Suggested improvement

In the storage guide, name a permitted way to replace an existing translation without reading it, for example: write the regenerated file to a temporary path, check it (row IDs match the English catalog, linked translations exist), then move it into place; or delete the stale translation and create it again. Say that a script that edits rows inside the existing translation is not permitted, because it loads the old text. Check: a later session that regenerates a catalog translation uses the named path and its transcript shows no read of the `*.kr.md` file.

## Review and verification

Maintainer fills during processing.
