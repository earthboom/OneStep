# Feedback: Strategy feedback stays in session reports and never reaches the inbox

- Date: 2026-11-20
- OneStep version used: commits up to 0d0053a (2026-11-20); exact commit per session unknown
- Relevant skills/instructions: agents/vegabond-agent.md (Respond to failures and feedback), feedback/README.md (Submit from a working project)
- Kind: problem
- Status: verifying
- Task context: game project sessions whose local instructions require a "OneStep strategy feedback" line in every report and name this inbox as the destination for material feedback

## Expected and observed

Expected: material strategy findings reach this inbox as report pairs. Observed: several session reports carried concrete strategy feedback lines (for example, the brief-ordering problem), but the inbox held no report until this submission. The owner relied on reading chat reports to notice strategy problems.

## Evidence and suspected cause

An inbox listing on 2026-11-20 showed only the guide and template. The transcript audit found the feedback line in session reports. Suspected cause: the report line satisfies the agent's sense of giving feedback, and the guide's requirement of explicit authorization for the inbox makes agents hesitate to write. Whether the local wording counted as authorization was not tested. A retest the same day, under local instructions that name this inbox for material feedback, ended with a feedback line that stated explicitly that it was not submitted to the inbox.

## Suggested improvement

When a working project configures the inbox, state that a material feedback line means submitting a report pair, and that the report says "submitted" or "prepared, not submitted" with the path. Check: a session that produces material strategy feedback leaves a report pair in the inbox.

## Review and verification

2026-11-23: The Scout handoff now directs material strategy findings to the [delivery check](README.md#confirm-delivery-at-handoff). A submitted handoff links both files in the configured inbox. A prepared handoff links the verified working-project pair and gives the reason for non-delivery.

The [CLI regression tests](../tools/test_check_feedback.py) exercise an independent working directory. A complete local pair produced a negative inbox result. An English-only delivery and an empty translation also failed. After the nonempty translation arrived, the same check succeeded and returned both inbox paths. The helper also rejected a directory at a report path and attempts to check paths outside the inbox. The existing report pair was checked in the real checkout; this was a presence check on an earlier submission.

These tests cover destination and file state. Adoption of the handoff in the original game project and maintainer acceptance remain unverified.
