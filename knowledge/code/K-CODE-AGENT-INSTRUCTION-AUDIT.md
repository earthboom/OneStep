---
id: K-CODE-AGENT-INSTRUCTION-AUDIT
title: Verify from the session transcript that an agent followed its project instructions
summary: Judge instruction compliance from the transcript's loaded-instruction entries, tool-call inputs and timestamped text, not from the agent's report or task-list status; a step can be marked done without the required output.
kind: method
scope: Claude Code CLI and desktop sessions that store JSONL transcripts; any agent setup whose required steps leave tool calls or visible text
keywords: [Claude Code, agent instructions, instruction compliance, session transcript, JSONL, instructions attachment, tool_use, CLAUDE.md, CLAUDE.local.md, subagents, task list, self-report, audit, retest, 지침 적용 확인]
status: active
checked_at: "2026-11-20"
context:
  tool: Claude Code desktop app and CLI, transcript format as of 2026-11
---

## Guidance

To check whether sessions applied a set of instructions (an entry procedure, required reads, searches, report fields), read the transcripts directly:

1. **Locate the transcripts.** Claude Code writes one JSONL file per conversation under `~/.claude/projects/<encoded working path>/<session-uuid>.jsonl`, with subagent transcripts under `<session-uuid>/subagents/`. A desktop session ID (`local_...`) is not the file name; match files by `cwd`, the first user message and timestamps. A rewound or forked conversation can produce a second file that repeats the early messages.
2. **Confirm the instructions were loaded.** An entry with `type: attachment` and `attachment.type: instructions` lists the instruction files placed in context. Its presence answers "was the file auto-loaded" without asking the agent.
3. **Map each required step to observable evidence.** A required read is a `tool_use` whose input names the file; a required search is a command input containing the query; a required statement is an assistant `text` block. Exclude `isSidechain` entries when judging the main conversation.
4. **Check order with timestamps.** Requirements such as "state X before execution" are judged by whether the text block precedes the first non-procedure tool call, not by whether X appears somewhere.
5. **Treat self-reports as claims.** The agent's summary, its wrap-up text and task-list statuses are not evidence that a step happened.

## Applicability and exceptions

Applies when the harness keeps full transcripts. Field names and paths are observed behavior of one tool version and can change; re-inspect a sample line before scripting. A transcript shows what the agent did, not why; skipped steps need the request wording and the instruction text to diagnose. A controlled retest started from another session may wrap the prompt with extra context, and a headless run can fail on expired authentication, so retests are close to, not identical with, a user-typed prompt.

## Checks

- The `instructions` attachment lists the expected file for each audited session.
- Every required step has a matching `tool_use` input or `text` block, with its timestamp.
- For ordering rules, the first qualifying text precedes the first non-procedure tool call.
- Any task-list item claiming a step is cross-checked against the transcript before being counted.

## Evidence

Audit of six conversations from one game project checkout on 2026-11-20, plus two controlled retests started from the desktop app. The `instructions` attachment confirmed automatic loading of a local instruction file in every session after setup. In one retest the task list showed a "post work brief" step completed while the transcript contained no such text before the following tool calls. Related incident: [R-CODE-AGENT-BRIEF-ORDER](../../records/code/R-CODE-AGENT-BRIEF-ORDER.md).
