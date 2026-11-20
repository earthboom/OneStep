---
id: R-CODE-AGENT-BRIEF-ORDER
title: Instruction text did not make an agent post its work brief before tool calls
summary: Two wordings requiring a visible brief before execution were ignored in fresh sessions; the agent planned and checked off the step without writing it. The same brief was reliably given at the top of the final report.
kind: error
scope: Claude Code desktop sessions following a project-local procedure that requires visible text before the next tool call
keywords: [work brief, instruction ordering, pre-execution output, tool call, task list, marked done, Claude Code, CLAUDE.local.md, hook, PreToolUse, final report, 브리프]
status: resolved
checked_at: "2026-11-20"
context:
  tool: Claude Code desktop app, 2026-11
trigger: An instruction requires the agent to post text before its next tool call in a tool-first harness
symptom: The agent proceeds from reading procedure files straight to searches and fetches; a task-list step for the text is marked complete without any text
cause_status: suspected
prevention: Require order-sensitive content in the final report, or enforce order with a tool-level hook; audit order from the transcript
prevention_status: proposed
relations:
  prevention: [K-CODE-AGENT-INSTRUCTION-AUDIT]
---

## Expected and observed

Expected: after reading the procedure files, the agent states a four-field work brief in the conversation before investigating. Observed in three fresh sessions with the same research prompt: no brief before execution. First wording ("first visible text of the task") produced no brief anywhere. A stricter gate ("before the next tool call of any kind, end that message with the brief") produced a task-list item "Post work brief", which was marked done together with the file-reading step while the next calls went straight to document reads, searches and web fetches. The brief appeared only at the top of the final report.

## Cause and resolution

Suspected cause: the harness and its own instructions favor sending a tool call with every message and short or no narration between calls, so a local text instruction loses to that pattern; the task-list update appears to be treated as satisfying the step. Not confirmed; no controlled comparison with the harness guidance removed. Resolution: the requirement was relocated. Briefs are now required at the top of the final report, with results attached to each done condition, and a brief is shown first only when ambiguity would change the work. Delivery before execution remains unachieved.

## Recheck and prevention

Recheck: in the retest under the stricter gate, the report-top brief, the required report lines and the verbatim handoff phrase were all present (transcript inspection, 2026-11-20). A fresh session under the relocated rule (a read-only engine API research request, same day) opened its final report with the four-field brief and a status for each done condition; as expected under the relocation, no brief preceded the first tool call. The statuses said "done" without per-condition evidence, so the evidence part of the rule held only partly. Proposed prevention: put order-sensitive outputs where the final artifact can carry them, or block investigation tools until the text exists with a PreToolUse hook; neither is verified. Audit with [K-CODE-AGENT-INSTRUCTION-AUDIT](../../knowledge/code/K-CODE-AGENT-INSTRUCTION-AUDIT.md) rather than task status.

## Evidence

Transcripts of the original sessions and two controlled retests in one game project checkout, 2026-11-19 to 2026-11-20, inspected by assistant text and tool-call timestamps. Instruction revisions were made in an untracked local instruction file; the revision history is in the originating session, not stored here.
