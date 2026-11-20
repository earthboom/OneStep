# Feedback: Scout's pre-execution brief is not delivered in a tool-first harness

- Date: 2026-11-20
- OneStep version used: commits up to 0d0053a (2026-11-20); exact commit per session unknown
- Relevant skills/instructions: skills/vegabond-scout/SKILL.md (Give a short work brief)
- Kind: problem
- Status: received
- Task context: Claude Code desktop sessions in a game project; research requests; a project-local instruction file layered OneStep on top of team instructions

## Expected and observed

Expected: scout states the four-field brief in the conversation before execution. Observed in three fresh sessions with the same research request: no brief before the first investigation tool call. Two local wordings were tried, including a gate "before the next tool call of any kind". Under the gate, the agent added a task-list step "Post work brief" and marked it done without writing it. The same brief appeared reliably at the top of the final report.

## Evidence and suspected cause

Transcript audit by assistant text and tool-call timestamps (method: knowledge/code/K-CODE-AGENT-INSTRUCTION-AUDIT.md; incident: records/code/R-CODE-AGENT-BRIEF-ORDER.md). Suspected cause, unconfirmed: the harness prefers sending a tool call with every message and little narration between calls, and treats a task-list update as satisfying the step. No controlled comparison without the harness guidance was run.

## Suggested improvement

Allow the brief to be delivered at the top of the final report, with results attached to each done condition, and require it before execution only when an ambiguity would change the work. Optionally note that a tool-level hook is the only reliable way to enforce ordering. Check: a fresh session under the revised wording produces the report-top brief with per-condition results.

## Review and verification

Maintainer fills during processing.
