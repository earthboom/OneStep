---
name: vegabond-code-design
description: Use when software work needs decisions about architecture, data ownership, lifecycle, interfaces, concurrency, persistence, or migration before implementation, or when a software design is the requested deliverable.
---

# Vegabond Code Design

Settle software design decisions for the calling operation or [vegabond-code](../vegabond-code/SKILL.md). Reuse its brief, environment, sources, and information brief. The caller owns execution and verification; design does not start a second workflow or certify working software. Follow the [agent instructions](../../agents/vegabond-agent.md) for document boundaries and common acceptance. Reading this skill does not spawn an agent.

If invoked directly, fill only missing context through [scout's shared setup](../vegabond-scout/SKILL.md#frame-and-classify) and [code's environment assessment](../vegabond-code/SKILL.md#identify-the-working-environment). For a design-only request, deliver the design and its supporting evidence without changing production code. Use isolated experiments only when authorized and needed to settle a decision.

## Resolve the design

1. **Ground the decision.** Identify the decision to settle, required outcome, preservation conditions, and affected boundaries from the existing brief. Inspect relevant entry points, callers, data, tests, and project conventions. Refine source or prior-lesson questions through [knowledge](../vegabond-knowledge/SKILL.md) only when the information brief has a concrete gap. Keep required guarantees distinct from proposed tradeoffs; expose conflicting requirements or unavailable capabilities instead of silently weakening the goal.
2. **Define the shape.** State the relevant data model, state owner, invariants, lifecycle and interfaces before specifying implementation steps. Include failure behavior and, where material, concurrent access, retries, persistence, cleanup and integration boundaries. Use the language/framework's actual contracts. Resolve only what the task needs; a pure function need not acquire an artificial state machine.
3. **Choose with evidence.** Compare alternatives when there is a real tradeoff; do not invent several designs for an obvious local pattern. Explain the selected structure's fit, costs, and material rejected option. When an empirical uncertainty could overturn the choice, inspect evidence or run the smallest scoped prototype before dependent work. Mark an inaccessible required check blocked and an untested assumption uncertain; a plausible sketch is not runtime proof.
4. **Make it implementable and checkable.** Identify affected interfaces/callers, migration order and compatibility obligations when relevant. Link each load-bearing invariant or assumption to a concrete check, expected observation, and required environment. Set measurable budgets for performance/resource claims when those claims matter. Before returning a design or advancing dependent implementation, read and apply [design review](references/review.md): trace requirements to mechanisms and evidence, challenge relevant failure sequences, and repair contradictions. The review owns these detailed checks; the caller's software verification still applies to implementation.

## Return the decision

Put the outcome in the existing brief or requested design artifact: chosen shape and ownership, interfaces and failure behavior, key reason/tradeoff, affected implementation or migration units, checks, and open assumptions or blockers. Use a small table or diagram only when it clarifies the relationships. No mandatory new file, approval checkpoint, or fixed template is needed.

State which guarantees the design supports, which implementation checks remain, and which unresolved premises block named dependent work. A useful partial proposal is not a satisfied guarantee. The caller applies [code's verification procedure](../vegabond-code/references/verification.md) to the actual implementation and returns here only when evidence changes a design decision. Preserve valid context rather than redesigning everything after each failure.
