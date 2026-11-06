---
name: vegabond-code
description: Use when implementing software, repairing defects, refactoring, or investigating code and runtime behavior in any language or engine, coordinating design when needed.
---

# Vegabond Code

Execute software work within the active operation. Reuse its brief and profile; follow the [agent instructions](../../agents/vegabond-agent.md) for common boundaries and completion. If invoked directly, use [scout's shared setup](../vegabond-scout/SKILL.md#frame-and-classify) and its linked operation without restarting classification.

## Identify the working environment

Use repository guidance, source and relevant callers, project/dependency configuration, tests, scripts, and CI to establish the changed component's language, engine/framework and versions, toolchain/platform/target, and actual build, test, launch and inspection paths. For new work, distinguish a proposed toolchain from an observed one. Resolve conflicting evidence narrowly; reuse scout's readiness check rather than treating configuration as proof that tools run.

Classify the actual component, not its extension or the repository's main technology. Unreal C++ and independent C++ need their own toolchains; Unity uses its project/package contracts. A Python tool inside an Unreal repository follows its own runtime, adding engine checks when its effects reach assets or engine behavior. For mixed work, identify affected components and boundary checks. Keep source locations and the result in the existing brief, not a separate environment report.

Request relevant contracts, version-specific sources, and prior failure/prevention checks through [vegabond-knowledge](../vegabond-knowledge/SKILL.md), reusing the existing information brief. Select available environment skills or direct tools through scout's mapping.

## Choose the design depth

Use [vegabond-code-design](../vegabond-code-design/SKILL.md) when a meaningful choice about state ownership, lifecycle, interfaces used by other callers, concurrency, persistence, external integration, or migration must be settled before implementation. A local edit following an established pattern can state its relevant contract and preservation conditions inline and proceed. File count alone does not decide; reuse a valid existing design and revisit only decisions changed by evidence.

Pass the current brief, environment, affected source/contracts, constraints, and unanswered decisions. Design returns a bounded implementation direction and checks within this workflow; it does not restart scout or create another execution loop. A design-only request ends with that result rather than an unsolicited implementation.

## Implement or investigate

Read [verification and handoff](references/verification.md) before changing code or judging the result. It owns the detailed preparation, build/test/runtime/real-use checks, review-and-repair loop, verification-change scrutiny, long-work state, and demonstrated safeguards. Apply it to each coherent change and the final integrated artifact; do not defer reading it until completion.

- **Create:** Follow the selected design or existing local pattern and implement a complete usable path. Resolve a load-bearing assumption with a small integration slice before dependent implementation, using scout's existing scale decision.
- **Revise:** Reproduce a defect and trace its cause before repair. For intentional restructuring, preserve the established behavior and public contracts while changing coherent units. Keep unrelated cleanup outside scope.
- **Research:** Trace code, data flow, and runtime evidence; compare options against the question and cite files, symbols, logs, and applicable sources. Leave investigated code unchanged; use an isolated harness for experiments.

If implementation evidence refutes the design, return the affected decision and evidence to code-design, then update the existing brief and checks. A changed goal or premise follows the common return-point rules; do not silently redefine acceptance to fit the implementation.

## Hand back

Return the patch or investigation, acceptance evidence for the actual final code, review results, and explicit unresolved conditions to the active operation. Send confirmed corrections and useful methods or demonstrated safeguards to knowledge for authorized storage; the verification reference defines the software evidence to supply. Distinguish completed AI checks from vagabond's independent acceptance under the common instructions.
