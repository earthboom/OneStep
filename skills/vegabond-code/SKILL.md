---
name: vegabond-code
description: Use when implementing software, repairing defects, refactoring, designing systems, or investigating code and runtime behavior in any language or engine.
---

# Vegabond Code

Provide software methods for the active operation. Reuse its brief and task profile; follow the [agent instructions](../../agents/vegabond-agent.md) for common boundaries and completion. If invoked directly, use [scout's shared setup](../vegabond-scout/SKILL.md#frame-and-classify) and its linked operation skill, then continue here without restarting classification.

## Identify the working environment

Refine scout's profile for the actual files, modules, and behavior being changed or investigated. Use repository guidance, project/dependency configuration, relevant callers, tests, scripts, and CI to establish:

- The target's language, engine/framework, and relevant versions.
- Its build system, compiler/runtime, platform, and target/configuration where these affect the work.
- The actual build, test, launch, and inspection paths, plus environment-specific contracts and conventions.

Do not classify from an extension or the repository's main technology alone. Unreal C++ and an independent C++ library can need different methods; a Python utility inside an Unreal repository follows its own execution path, adding engine checks when its effects reach engine assets or behavior. For mixed work, identify each affected component and the checks at their boundaries.

| Environment examples, not a closed list | Connect the identified target to |
| --- | --- |
| Unreal | Applicable engine/module contracts and project build, tests, editor, and play paths. |
| Unity | Applicable engine/package contracts and project compilation, tests, editor, and play paths. |
| Independent C++ | The actual compiler/build configuration, tests, and executable or library consumer. |
| Other languages or mixed environments | Their existing toolchains, execution paths, and affected integration checks. |

Keep the result and its source locations in the existing brief or step mapping; no separate environment report is required. Use it to select available environment-specific skills or direct tools through scout's mapping and to choose the checks below. Follow scout's readiness check rather than treating configuration as proof that tools run. Investigate missing or conflicting evidence narrowly, and ask only when unresolved intent changes the method. For new work without repository evidence, use explicit requirements and available context; distinguish a proposed toolchain from an observed one.

## Execute

Identify contracts, state ownership, lifecycle, and affected integration points at the depth the change needs, using the environment assessment above.

Request relevant contracts, version-specific references, and known failure/prevention checks through [vegabond-knowledge](../vegabond-knowledge/SKILL.md), reusing the active information brief.

- **Create:** Follow existing patterns for a small feature and implement a complete usable path. For system work, establish boundaries, interfaces, dependencies, and migration needs before implementation. Exercise a risky interface or assumption with a small integration slice before dependent work, using scout's existing scale decision.
- **Revise:** For a defect, establish a reproducible failure and trace its cause before changing code. For intentional restructuring, establish the behavior and public contracts to preserve, then change structure in coherent increments. Avoid coupling the fix to unrelated cleanup.
- **Research:** Trace the relevant code path, data flow, or runtime evidence. Compare technical options against the question's constraints, citing files, symbols, logs, and applicable documentation. Keep investigated code unchanged; experiments must use an isolated harness when needed.

## Prepare checks

Before implementation, map the acceptance conditions and preserved contracts to executable checks, including relevant safeguards from the information brief. Establish the baseline for the affected path and distinguish existing failures. For a bug with a practical local test path, capture a regression check failing for the intended reason before the fix. Otherwise retain the closest observable reproduction and state its limits.

## Verify

Retain these four stages where applicable:

1. **Build/preparation:** Run the project's actual build, compile, or equivalent preparation for the affected target and configuration.
2. **Automated tests:** Run relevant existing tests. Add regression or behavior coverage when it provides meaningful protection, using expected results independent of the implementation. Include affected boundary and error paths.
3. **Runtime readiness:** Launch the application or required environment and confirm the changed path can be reached without initialization failures.
4. **Real use:** Exercise the changed behavior through its public interface. For Unreal or Unity games, launch the editor and perform actual play, including relevant multiplayer roles. For a CLI, invoke real commands; for a library, exercise a real consumer or harness.

For a defect, rerun the original reproduction as well as affected surrounding behavior. Record commands, target/configuration, outcomes, and observed runtime behavior. Apply the agent instructions' blocked-versus-inapplicable distinction to each stage. A code investigation without an implementation change uses the checks needed to substantiate its claims rather than requiring an unrelated full build.

## Review and repeat

After each coherent change, run the affected build/preparation and automated checks, then inspect the diff and relevant callers against the requirements. Look for omitted behavior, broken contracts, state/lifecycle errors, and risks specific to the change. Review whether the tests would detect incorrect behavior rather than merely repeat the implementation. Use available review or test skills when they add relevant capability; a review finding needs a concrete mechanism or evidence before it motivates a change.

For a confirmed failure or defect, use the command, assertion, log, or interaction to localize its cause. Correct it, repeat the original failure check and affected surrounding checks, and review the repaired diff. Repeat until required checks pass and no confirmed in-scope defect remains. Do not weaken a valid check to accept incorrect behavior; correct a mistaken check against the requirement with an explicit reason.

Use the agent instructions' [shared failure and feedback rules](../../agents/vegabond-agent.md#respond-to-failures-and-feedback) when diagnosis, evidence, scope, or capability needs reassessment.

After the local loop, run the required integrated and real-use checks on the final artifact. A failure returns to diagnosis and repair; later edits invalidate affected evidence. Separate reproducible pre-existing failures from introduced ones, and do not treat a pre-existing failure as proof of acceptance.

Send confirmed corrections, technical evidence, and demonstrated safeguards or specific reusable checks to vegabond-knowledge for authorized record updates. For research or feedback-only work, correct the findings without editing investigated sources. Return the patch or investigation with review results, technical evidence, prevention references, and remaining limitations to the active operation.
