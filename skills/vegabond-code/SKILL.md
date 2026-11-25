---
name: vegabond-code
description: Use when implementing software or gameplay content, repairing defects, refactoring, or investigating code and runtime behavior in any language or engine, coordinating design when needed.
---

# Vegabond Code

Execute software work within the active operation. Reuse its brief and profile; follow the [agent instructions](../../agents/vegabond-agent.md) for common boundaries and completion. If invoked directly, use [scout's shared setup](../vegabond-scout/SKILL.md#frame-and-classify) and its linked operation without restarting classification.

Proceed directly when the requested behavior and its pass condition are clear. Consult the working project's glossary only if two plausible readings of a term would give the same test case opposite verdicts. Before changing the code or test, read just the matching entry and check the linked contract. In OneStep's `docs/development-glossary.md`, locate the term in the first column and read that row only. Reuse a definition and boundary case already verified in the design handoff. If the entry is missing or conflicts with the caller or test, use the governing project evidence to settle the boundary before reporting a pass.

## Identify the working environment

Use repository guidance, source and relevant callers, project/dependency configuration, tests, scripts, and CI to establish the changed component's language, engine/framework and versions, toolchain/platform/target, and actual build, test, launch and inspection paths. For new work, distinguish a proposed toolchain from an observed one. Resolve conflicting evidence narrowly; reuse scout's readiness check rather than treating configuration as proof that tools run.

Classify the actual component, not its extension or the repository's main technology. Unreal C++ and independent C++ need their own toolchains; Unity uses its project/package contracts. A Python tool inside an Unreal repository follows its own runtime, adding engine checks when its effects reach assets or engine behavior. For mixed work, identify affected components and boundary checks. Keep source locations and the result in the existing brief, not a separate environment report.

For C++ components, read the [C++ project guidelines](references/cpp-project-guidelines.md) before implementation. Apply the common rules to C++ and the additional rules to Unreal C++. The working project's instructions and conventions take precedence. When introducing a language feature or ownership model, designing a public API, choosing a design pattern, or tuning performance, consult only the relevant section of the [C++ implementation guide](references/cpp-implementation.md). Reuse guidance already loaded for the task.

Request relevant contracts, version-specific sources, and prior failure/prevention checks through [vegabond-knowledge](../vegabond-knowledge/SKILL.md), reusing the existing information brief. Select available environment skills or direct tools through scout's mapping.

Apply the shared [information-needs judgment](../vegabond-scout/references/information-needs.md) after inspecting the component and callers: refine questions about affected state, ownership, lifecycle, failure and verification as relevant. Check actual version and mechanism before applying a retrieved API guarantee or incident fix.

For game implementation, debugging or optimization, apply the [game evidence reuse convention](../../knowledge/game/K-GAME-RESEARCH-USE.md), reusing scout's lookup when valid. Retrieve from the concrete feature or reproduced symptom, check engine/platform and state-authority conditions, and connect the selected technique to a code change and observable check. Preserve rejection reasons and feed measured outcomes back through knowledge; a source-game example is not proof of this implementation.

## Choose the design depth

When deciding how to carry a design into implementation, use the [scope and delivery criteria](../vegabond-code-design/references/scope-and-delivery.md). Keep a single shared invariant and its callers together, or identify the intermediate evidence that would change the next unit. Carry that choice into verification of the integrated behavior.

Use [vegabond-code-design](../vegabond-code-design/SKILL.md) when a meaningful choice about state ownership, lifecycle, interfaces used by other callers, concurrency, persistence, external integration, or migration must be settled before implementation. A local edit following an established pattern can state its relevant contract and preservation conditions inline and proceed. File count alone does not decide; reuse a valid existing design and revisit only decisions changed by evidence.

For a new game, route the [foundation decisions](../vegabond-code-design/references/gameplay-framework.md#plan-a-new-game-foundation) through code design before selecting or creating gameplay scaffolding. The brief needs a framework suited to representative play, named state owners and lifetimes, and an authoring and registration path for the first content and its next variant. Reuse settled decisions from the project brief.

For an existing game, route changes to the gameplay framework, shared content contracts, or dependencies between features through code design. When adding content through an existing extension point, use the existing contract and check the new content alongside the supported baseline. An independently optional feature also requires the applicable [dependency and independence checks](../vegabond-code-design/references/gameplay-framework.md#make-feature-dependencies-explicit), even when it uses an existing extension point. Use code design if these checks reveal a new dependency or a needed contract change.

Pass the current brief, environment, affected source/contracts, constraints, and unanswered decisions. Design returns a bounded implementation direction and checks within this workflow; it does not restart scout or create another execution loop. A design-only request ends with that result rather than an unsolicited implementation.

## Implement or investigate

When a user decision changed the design, exercise the distinguishing case from the handoff through the normal entry point. Compare the observation with the outcome the user chose, including any promised preservation or failure behavior. If the environment is unavailable, carry the concrete expected result forward as pending.

Read [verification and handoff](references/verification.md) before changing code or judging the result. It owns the detailed preparation, build/test/runtime/real-use checks, review-and-repair loop, verification-change scrutiny, long-work state, and demonstrated safeguards. Before editing shared gameplay code, changing a shared rule, or adding a stage, use its [gameplay regression checks](references/verification.md#gameplay-regression-checks) to record preserved behavior and the check scope in the existing brief. Apply verification to each coherent change and the final integrated artifact.

For a gameplay framework or content boundary change, carry the representative extension, affected dependency checks, and supported content configurations from the design into software verification. Apply the relevant dependency and configuration checks to an independently optional feature added through an existing extension point as well. Exercise the production registration and play path. Record the actual changes needed to add the variant and the behavior of the applicable configurations in the verification evidence.

When changing input response, impact feedback, or the presentation of a gameplay outcome, use the [gameplay feedback checks](references/verification.md#gameplay-feedback-checks), including for asset-only changes that affect those behaviors.

For game data changes, streamed, cached or pooled content, rendering budgets, or NPC behavior across lifetime and visibility changes, apply the relevant [game runtime checks](references/world-lifecycle-verification.md) alongside the general verification procedure. Use the actual integration boundary for each claim, including existing data bytes, engine residency, and observable state where applicable.

- **Create:** Follow the selected design or existing local pattern and implement a complete usable path. Resolve a load-bearing assumption with a small integration slice before dependent implementation, using scout's existing scale decision.
- **Revise:** Reproduce a defect and trace its cause before repair. For intentional restructuring, preserve the established behavior and public contracts while changing coherent units. Keep unrelated cleanup outside scope.
- **Research:** Trace code, data flow, and runtime evidence; compare options against the question and cite files, symbols, logs, and applicable sources. Leave investigated code unchanged; use an isolated harness for experiments.

If implementation evidence refutes the design, return the affected decision and evidence to code-design, then update the existing brief and checks. A changed goal or premise follows the common return-point rules; do not silently redefine acceptance to fit the implementation.

## Hand back

Return the patch or investigation, acceptance evidence for the actual final code, review results, and explicit unresolved conditions to the active operation. Send confirmed corrections and useful methods or demonstrated safeguards to knowledge for authorized storage; the verification reference defines the software evidence to supply. Distinguish completed AI checks from vagabond's independent acceptance under the common instructions.
