# Software verification and handoff

Use this procedure from [vegabond-code](../SKILL.md) before changing code or judging a software result. The [agent instructions](../../../agents/vegabond-agent.md) own common completion, acceptance, and failure routing; this reference owns software-specific checks.

## Prepare checks

Before implementation, map the acceptance conditions and preserved contracts to executable checks, including relevant safeguards from the information brief. Establish the baseline for the affected path and distinguish existing failures. For a bug with a practical local test path, capture a regression check failing for the intended reason before the fix. Otherwise retain the closest observable reproduction and state its limits.

Use the project's existing verification commands and harness first. Confirm that the command actually discovers the intended tests and reaches the changed behavior; an exit-zero run with no relevant assertions is not proof. Retain the command, target/configuration, code revision or relevant diff, and observed results in existing task evidence. When a missing repeatable path would otherwise leave required behavior unchecked, add the smallest reusable check within scope and demonstrate it end to end.

## Verify

Retain these four stages where applicable:

1. **Build/preparation:** Run the project's actual build, compile, or equivalent preparation for the affected target and configuration.
2. **Automated tests:** Run relevant existing tests. Add regression or behavior coverage when it provides meaningful protection, using expected results independent of the implementation. Include affected boundary and error paths.
3. **Runtime readiness:** Launch the application or required environment and confirm the changed path can be reached without initialization failures.
4. **Real use:** Exercise the changed behavior through its public interface. For Unreal or Unity games, launch the editor and perform actual play, including relevant multiplayer roles. For a CLI, invoke real commands; for a library, exercise a real consumer or harness.

For a defect, rerun the original reproduction as well as affected surrounding behavior. Record commands, target/configuration, outcomes, and observed runtime behavior. Apply the agent instructions' blocked-versus-inapplicable distinction to each stage. A code investigation without an implementation change uses the checks needed to substantiate its claims rather than requiring an unrelated full build.

## Review and repeat

After each coherent change, run the affected build/preparation and automated checks, then inspect the diff and relevant callers against the requirements. Look for omitted behavior, broken contracts, state/lifecycle errors, and risks specific to the change. Review whether the tests would detect incorrect behavior rather than merely repeat the implementation. Use available review or test skills when they add relevant capability; a review finding needs a concrete mechanism or evidence before it motivates a change.

Review changes to tests and verification configuration as part of the patch: deleted assertions, skips, exclusions, relaxed expected values, lint/type suppressions, and disabled checks need a contract-based reason. Do not use them to hide a valid failure. If a check is wrong, identify the conflicting requirement or evidence, explain the correction, and verify the preserved contract. Keep blocked or skipped required checks visible in the handoff rather than counting them as passes. For a practical regression or consequential safeguard, demonstrate that the check detects the original failure or a controlled broken case; keep expected results independent of the implementation.

Inspect exception swallowing, success-shaped defaults, unconditional retries, arbitrary waits, and compatibility paths for evidence that they handle legitimate states. A fallback is valid only when the contract calls for it and its failure behavior is checked; for example, a permitted missing configuration must not silently turn malformed configuration into success. Unsupported workarounds are hypotheses to investigate, not completed fixes. Remove speculative changes that the evidence rules out without discarding unrelated work.

For a confirmed failure or defect, use the command, assertion, log, or interaction to localize its cause. Correct it, repeat the original failure check and affected surrounding checks, and review the repaired diff. Repeat until required checks pass and no confirmed in-scope defect remains. Do not weaken a valid check to accept incorrect behavior; correct a mistaken check against the requirement with an explicit reason.

Use the agent instructions' [shared failure and feedback rules](../../../agents/vegabond-agent.md#respond-to-failures-and-feedback) when diagnosis, evidence, scope, or capability needs reassessment.

After the local loop, run the required integrated and real-use checks on the final artifact. A failure returns to diagnosis and repair; later edits invalidate affected evidence. Separate reproducible pre-existing failures from introduced ones, and do not treat a pre-existing failure as proof of acceptance.

## Continue long or staged work

At phase boundaries and before a handoff or context reset, update the existing brief with the goal and preservation conditions, completed and pending acceptance items, current code state, evidence pointers, decisions that constrain the next step, and next action. Record decisions and checks, not private reasoning or every tool call. On resumption, reconcile that state with the current diff and valid evidence before continuing. Recheck evidence invalidated by intervening changes; do not silently drop pending conditions or rerun all completed work by default.

## Retain useful safeguards

For repeated consequential mistakes, use the existing knowledge/record flow to identify the pattern, then prefer a scoped structural fix, type constraint, lint/CI check, or behavior test over another prose warning. Reuse the project's enforcement path and demonstrate detection of the actual mistake or a controlled equivalent. Report what is automatically enforced versus merely documented, and any remaining limits. Do not claim a rule is enforced just because it appears in this skill, or impose new infrastructure on every small task.
