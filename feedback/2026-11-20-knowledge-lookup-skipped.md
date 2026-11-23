# Feedback: Knowledge lookup is skipped unless the entry instructions name the exact search command

- Date: 2026-11-20
- OneStep version used: commits up to 0d0053a (2026-11-20); exact commit per session unknown
- Relevant skills/instructions: skills/vegabond-scout/SKILL.md (Frame and classify, knowledge request), skills/vegabond-knowledge/SKILL.md (Find and synthesize)
- Kind: problem
- Status: verifying
- Task context: four checkouts of one game repository, each with its own local instructions that layer OneStep on team instructions; design, implementation, merge and research tasks

## Expected and observed

Expected: substantive tasks request a focused knowledge brief and search problem records by the planned action. Observed: where the local instructions named only the scout and knowledge skills, eight audited sessions (from about one hundred to over two thousand tool calls each) ran no search helper and accessed no knowledge path. Scout was read in most of them. Where the local instructions gave the exact helper command with `--store records`, every procedure session ran it and reported the consulted IDs.

## Evidence and suspected cause

Counts of main-thread tool inputs naming the helper or store paths (method: knowledge/code/K-CODE-AGENT-INSTRUCTION-AUDIT.md). Suspected cause: scout's "Request a focused brief from knowledge" reads as optional context gathering, and documents routed by the working project satisfy the agent's sense of an information step. Not confirmed by a controlled comparison in the same checkout.

## Suggested improvement

Give the concrete retrieval command in scout's information step or in the linked-project instruction block, including the records search by planned action, and ask for consulted IDs with adoption decisions in the report. Check: in a checkout with the revised block, a substantive task shows a helper call in the transcript and IDs in the report.

## Review and verification

2026-11-23: Scout now gives an executable records query, shows how to turn a scoped incident into a verification decision, and gives a spacing-only example where the input suffices.

Six fresh contexts ran the existing [request-to-application cases](../skills/vegabond-knowledge/tests/information-needs/evaluation.md) against the revised Scout. Their answers met the original [case criteria](../skills/vegabond-knowledge/tests/information-needs/rubric.json). In the provider swap, the performer consulted R-EVAL-BUSY and its incident source, withheld the earlier provider's retry rule, and proposed checking for duplicate charges after a lost response. In the spacing case, the performer returned the requested one-space change and reported comparing it with the supplied sentence. The other cases covered a queued callback, narrative disclosure, combat pacing and a retention claim.

These were synthetic tasks reviewed for the decisions in their answers. No before/after measurement in the original game checkouts or maintainer acceptance has been recorded.

A seventh fresh context used the current checkout for a fixed-forward camera test plan. It searched problem records by the planned reversal, opened R-CODE-UE-SPEED-REVERSE, and used the earlier failure to select a per-frame check of the actual camera position after lag relative to the capsule. This verifies selection of a relevant check. No Unreal runtime was run for this planning task.
