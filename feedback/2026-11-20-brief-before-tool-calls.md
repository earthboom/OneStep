# Feedback: Scout's pre-execution brief is not delivered in a tool-first harness

- Date: 2026-11-20
- OneStep version used: commits up to 0d0053a (2026-11-20); exact commit per session unknown
- Relevant skills/instructions: skills/vegabond-scout/SKILL.md (Give a short work brief)
- Kind: problem
- Status: verifying
- Task context: Claude Code desktop sessions in a game project; research requests; a project-local instruction file layered OneStep on top of team instructions

## Expected and observed

Expected: scout states the four-field brief in the conversation before execution. Observed in three fresh sessions with the same research request: no brief before the first investigation tool call. Two local wordings were tried, including a gate "before the next tool call of any kind". Under the gate, the agent added a task-list step "Post work brief" and marked it done without writing it. The same brief appeared reliably at the top of the final report.

## Evidence and suspected cause

Transcript audit by assistant text and tool-call timestamps (method: knowledge/code/K-CODE-AGENT-INSTRUCTION-AUDIT.md; incident: records/code/R-CODE-AGENT-BRIEF-ORDER.md). Suspected cause, unconfirmed: the harness prefers sending a tool call with every message and little narration between calls, and treats a task-list update as satisfying the step. No controlled comparison without the harness guidance was run.

## Suggested improvement

Allow the brief to be delivered at the top of the final report, with results attached to each done condition, and require it before execution only when an ambiguity would change the work. Optionally note that a tool-level hook is the only reliable way to enforce ordering. Check: a fresh session under the revised wording produces the report-top brief with per-condition results.

## Review and verification

2026-11-23: [Scout's framing guidance](../skills/vegabond-scout/SKILL.md#frame-and-classify) now makes a visible kickoff brief conditional on ambiguity that changes the result. It retains working checks for clear multi-step tasks and delivers simple edits directly.

Fresh-context trials checked the order of the user-facing messages:

- An event notice had two possible audiences with different entrances. Before drafting, the performer stated the confirmed date, time and location, identified the single-entrance check and asked which audience would receive the notice. After the trial user selected staff, it delivered one notice with the north entrance and all confirmed event facts.
- The existing spacing fixture yielded the corrected sentence directly after setup. Both file-based trials had an initial skill-loading notice. In a separate inline trial with the Scout rule already supplied, the entire response to a one-space correction was the corrected sentence, with no preliminary message or question.

These results cover the sampled conversations. Ordering in the originally reported Claude Code desktop environment and maintainer acceptance remain unverified.
