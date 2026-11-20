# Feedback: Knowledge lookup is skipped unless the entry instructions name the exact search command

- Date: 2026-11-20
- OneStep version used: commits up to 0d0053a (2026-11-20); exact commit per session unknown
- Relevant skills/instructions: skills/vegabond-scout/SKILL.md (Frame and classify, knowledge request), skills/vegabond-knowledge/SKILL.md (Find and synthesize)
- Kind: problem
- Status: received
- Task context: four checkouts of one game repository, each with its own local instructions that layer OneStep on team instructions; design, implementation, merge and research tasks

## Expected and observed

Expected: substantive tasks request a focused knowledge brief and search problem records by the planned action. Observed: where the local instructions named only the scout and knowledge skills, eight audited sessions (from about one hundred to over two thousand tool calls each) ran no search helper and accessed no knowledge path. Scout was read in most of them. Where the local instructions gave the exact helper command with `--store records`, every procedure session ran it and reported the consulted IDs.

## Evidence and suspected cause

Counts of main-thread tool inputs naming the helper or store paths (method: knowledge/code/K-CODE-AGENT-INSTRUCTION-AUDIT.md). Suspected cause: scout's "Request a focused brief from knowledge" reads as optional context gathering, and documents routed by the working project satisfy the agent's sense of an information step. Not confirmed by a controlled comparison in the same checkout.

## Suggested improvement

Give the concrete retrieval command in scout's information step or in the linked-project instruction block, including the records search by planned action, and ask for consulted IDs with adoption decisions in the report. Check: in a checkout with the revised block, a substantive task shows a helper call in the transcript and IDs in the report.

## Review and verification

Maintainer fills during processing.
