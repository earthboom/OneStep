---
name: vegabond-code-design
description: Use when software work needs architecture, ownership, lifecycle, interface, concurrency, persistence, or migration decisions, including gameplay framework design and independently extensible game content, or when a software design is the requested deliverable.
---

# Vegabond Code Design

Settle software design decisions for the calling operation or [vegabond-code](../vegabond-code/SKILL.md). Reuse its brief, environment, sources, and information brief. The caller owns execution and verification; design does not start a second workflow or certify working software. Follow the [agent instructions](../../agents/vegabond-agent.md) for document boundaries and common acceptance. Reading this skill does not spawn an agent.

If invoked directly, fill only missing context through [scout's shared setup](../vegabond-scout/SKILL.md#frame-and-classify) and [code's environment assessment](../vegabond-code/SKILL.md#identify-the-working-environment). For a design-only request, deliver the design and its supporting evidence without changing production code. Use isolated experiments only when authorized and needed to settle a decision.

Proceed directly when the requested behavior and its pass condition are clear. Consult the working project's glossary only if two plausible readings of a term would give the same test case opposite verdicts. Before defining acceptance, read just the matching entry and check the linked contract. In OneStep's `docs/development-glossary.md`, locate the term in the first column and read that row only. Hand off the distinguishing case and its expected verdict. If the entry is missing or inconsistent, check the governing source and ask only if a user decision remains.

For game architecture and technical choices, use the [game evidence reuse convention](../../knowledge/game/K-GAME-RESEARCH-USE.md), including on direct invocation. Reuse valid retrieved evidence, inspect prerequisites such as restorable state for rollback, and record adoption, conditional use or rejection against actual engine, platform and gameplay constraints. Return the selected entry IDs, implementation boundaries and proposed validation with the design.

Start a new game with the [foundation decisions](references/gameplay-framework.md#plan-a-new-game-foundation). Derive the framework, state ownership and content path from representative play before choosing project scaffolding, packages or shared base classes. For an existing game, apply the relevant parts of [gameplay framework and content design](references/gameplay-framework.md) when changing those decisions or how features compose. Carry the design and proposed checks into implementation when the request includes it.

When designing input response, impact feedback, or the camera, visual effects, audio, and haptics that communicate a gameplay outcome, use the [gameplay feedback guidance](references/gameplay-framework.md#design-gameplay-feedback).

When deciding how game data evolves, what a world loads or retains, how a renderer meets its budget, or what NPCs do offscreen, use the applicable [world runtime design guidance](references/world-lifecycle.md). Tie each chosen policy to a gameplay requirement and pass the preservation, transition and measurement conditions to implementation.

For a shared rule, public contract, or dependency that could silently break a supported path, point implementation to the caller’s expected result and the existing public-path test that asserts it. If that assertion would catch the plausible fault and allow equivalent implementations, the handoff is complete. Only when either verdict is unclear, name the unresolved behavior and the smallest comparison that would settle it. A clear local edit proceeds directly.

## Resolve the design

When the scope or implementation sequence is unsettled, use [scope, design depth and delivery units](references/scope-and-delivery.md). Return the observable outcome, the decision that warrants design and its cost if wrong, and why one coherent change or checked stages fit this particular request. Reuse Scout's brief and update its provisional scale after examining the contracts.

Use the shared [information-needs judgment](../vegabond-scout/references/information-needs.md) to test whether required guarantees, boundaries and counterexamples expose missing questions. Keep adopted contracts, conditional assumptions and rejected analogies attached to the choices they affect.

1. **Ground the decision.** Identify the decision to settle, required outcome, preservation conditions, and affected boundaries from the existing brief. Inspect relevant entry points, callers, data, tests, and project conventions. Refine source or prior-lesson questions through [knowledge](../vegabond-knowledge/SKILL.md) only when the information brief has a concrete gap. Keep required guarantees distinct from proposed tradeoffs; expose conflicting requirements or unavailable capabilities instead of silently weakening the goal.
2. **Define the shape.** State the relevant data model, state owner, invariants, lifecycle and interfaces before specifying implementation steps. Include failure behavior and, where material, concurrent access, retries, persistence, cleanup and integration boundaries. Use the language/framework's actual contracts. Resolve only what the task needs; a pure function need not acquire an artificial state machine.
3. **Choose with evidence.** Compare alternatives when there is a real tradeoff; do not invent several designs for an obvious local pattern. Explain the selected structure's fit, costs, and material rejected option. When an empirical uncertainty could overturn the choice, inspect evidence or run the smallest scoped prototype before dependent work. Mark an inaccessible required check blocked and an untested assumption uncertain; a plausible sketch is not runtime proof.
4. **Make it implementable and checkable.** Identify affected interfaces/callers, migration order and compatibility obligations when relevant. Link each load-bearing invariant or assumption to a concrete check, expected observation, and required environment. Set measurable budgets for performance/resource claims when those claims matter. Before returning a design or advancing dependent implementation, read and apply [design review](references/review.md): trace requirements to mechanisms and evidence, challenge relevant failure sequences, and repair contradictions. The review owns these detailed checks; the caller's software verification still applies to implementation.

## Return the decision

When plausible interpretations would change a user's or player's observable result, first look for the decision in the project's governing sources. If the choice still belongs to the user, ask about one concrete situation in which the outcomes diverge. Once answered, carry the agreed behavior and the expected result for that situation into the implementation handoff. A different answer should lead to a different check. Reuse settled decisions directly and leave technical unknowns to inspection or a targeted experiment.

Apply the [shared reader-facing design guidance](../../agents/references/design-communication.md) when composing and handing back the result. Explain observable behavior and important failure cases before introducing types, storage fields or transaction details. Then connect the chosen shape/ownership, interfaces, implementation or migration units, evidence and checks to the decisions they support.

State which guarantees the design supports, which implementation checks remain, and which unresolved premises block named dependent work. A useful partial proposal is not a satisfied guarantee. The caller applies [code's verification procedure](../vegabond-code/references/verification.md) to the actual implementation and returns here only when evidence changes a design decision. Preserve valid context rather than redesigning everything after each failure.
