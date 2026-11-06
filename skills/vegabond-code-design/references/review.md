# Design review

Apply this before handing off a software design or advancing implementation that relies on it. Use the existing brief or design artifact; no separate checklist file is required. The [design skill](../SKILL.md) owns choices, the [common instructions](../../../agents/vegabond-agent.md) own completion and failure routing, and [software verification](../../vegabond-code/references/verification.md) owns execution checks on implemented code.

## Preserve the contract and evidence boundary

Trace each material requirement and preservation condition to its mechanism, evidence or explicit assumption, and acceptance check. Use a compact mapping when prose would hide a gap. Derive the expected behavior from the request and governing contracts, not from what the chosen architecture happens to support. A successful example cannot replace the required failure or concurrency behavior.

Separate observed source/API contracts, reasoned design conclusions, proposed choices, and untested assumptions. Attach source/version and prototype conditions to claims that need them. A framework name, type, lock, queue or transaction is not evidence that a guarantee holds across every boundary. An isolated model/prototype supports only what it represents; record omitted actors, failures and environment limits. Proposed budgets are not measured performance.

Do not turn a required guarantee into a preference, remove a caller, failure case or compatibility obligation, or add an unstated environmental restriction to make the design appear complete. When constraints conflict or a capability is missing, name the incompatible requirement and the evidence, show a bounded alternative with its changed guarantee, and leave the original condition unresolved. Clarify material product choices under the common rules; independent work may continue without pretending the blocked guarantee is met.

## Challenge the mechanism

For each relevant boundary, identify who owns authoritative state, valid/invalid states, permitted transitions, and the point at which ownership, durability, or acknowledgement changes. Include error propagation and resource release. Describe the mechanism that enforces an invariant rather than repeating the invariant as a promise.

Attempt a concrete counterexample at the important transitions. Choose cases from the design's actual risks; a local pure function does not need an invented distributed-system audit. For example:

- Concurrent or delayed actors: duplicate claim, stale owner, cancellation or object destruction while work continues; distinguish protecting a local record from controlling an external side effect.
- Partial failure: crash before/after persistence or acknowledgement, timeout after remote acceptance, retry after unknown outcome, partial migration and mixed old/new callers.
- Progress and capacity: hung owner, lock held across external work, retry backlog, starvation, bounded memory/storage and cleanup. A safety mechanism must disclose the progress or availability it can sacrifice.

Write the shortest relevant event sequence, expected state/effect, and where the mechanism prevents a violation. If it does not, revise the design or mark the guarantee unresolved. Do not dismiss a reachable failure merely as unlikely. Review fallback success, blanket retry, fixed waits, global serialization and compatibility layers against their explicit contract and costs; do not ban a justified mechanism by style alone.

## Check the checks and handoff

For a load-bearing claim, name the trigger/initial state, observable result and failure predicate, plus the environment and evidence needed. Check that the proposed test could reject a broken design, rather than merely observe an internal flag set by that design. Where authorized and useful, use a minimal counterexample, model or prototype to resolve an empirical uncertainty; distinguish a prediction from an executed result. Do not claim tests, formal proof, performance, or compatibility that was not checked.

Separate a premise needed to choose or safely begin the design from an implementation check that can only run after code exists. An unresolved premise blocks the named dependent decision/work; it cannot be buried in a future-test list while declaring that work ready. Implementation checks can remain pending when the structural reasoning is supported and their gates are explicit. State the supported scope, pending checks, and blocked guarantees without a blanket readiness verdict that conceals a limitation.

Reconcile interfaces, state transitions and migration steps across the final artifact; fix contradictions and revisit only decisions affected by the new evidence. A revised design must identify changed guarantees/assumptions and affected implementation/checks in the existing brief, preserving valid decisions and evidence. A document review establishes design consistency within those bounds, not a working implementation or an automatically enforced rule.
