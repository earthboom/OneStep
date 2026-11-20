# Feedback: The read-only default prevents saving reusable lessons even with standing store authorization

- Date: 2026-11-20
- OneStep version used: commits up to 0d0053a (2026-11-20); exact commit per session unknown
- Relevant skills/instructions: skills/vegabond-knowledge/SKILL.md (Save and maintain), skills/vegabond-research/SKILL.md (Refine the inquiry), CLAUDE.md (Cross-project knowledge, "Write only when allowed")
- Kind: problem
- Status: received
- Task context: research and audit tasks in a game project that are read-only for the working repository, with the owner's standing permission to write generalized entries to the OneStep store

## Expected and observed

Expected: generalized lessons from read-only research are saved, because the owner allowed writes to the personal cross-project store. Observed: sessions listed candidate entries as proposals and saved nothing. The owner noticed the missing entries. Saving happened only after the local instructions stated the standing authorization explicitly and said that read-only work for the repository still saves.

## Evidence and suspected cause

The knowledge skill, the research skill and the local-override section all say that read-only or analysis-only work returns proposed entries. The agent read "read-only" as the whole task's write scope, including the store. Suspected cause: the guidance does not distinguish the working repository's write scope from the store's write scope.

## Suggested improvement

State that the store's write authorization is separate from the task's write scope. When a standing store authorization is configured, read-only work for the working project still saves generalized entries; proposals remain the default only when no store authorization exists. Check: a read-only research session under that wording writes a store entry and passes the catalog check.

## Review and verification

Maintainer fills during processing.
