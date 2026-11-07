---
id: K-CODE-PRINCIPLE-REUSE
title: Apply coding principles through concrete contracts and change risks
summary: Before applying a coding philosophy, retrieve the references matching the actual maintenance, interface, dependency, configuration, performance or lifetime question. Resolve tensions against project contracts and evidence rather than enforcing slogans or a universal style score.
kind: convention
scope: OneStep code design, implementation review and refactoring; other projects use this store only when configured or authorized, and their own contracts and conventions prevail
keywords: [coding-philosophy, maintainability, readability, modularity, dependency, hardcoding, memory, principle-selection, 코딩철학, 프로그래밍철학, 유지보수, 가독성, 모듈화, 의존성, 하드코딩, 메모리, 지식조회]
status: active
checked_at: '2026-11-07'
context:
  authority: User request to collect programming philosophy knowledge in the ongoing reusable knowledge workflow
  evidence_check: Routing convention; reference-specific original sources and limits remain in their Evidence sections
  application_status: Knowledge retrieval and proposed review checks; no repository code refactor, compiler test or runtime experiment
---

# Apply coding principles through concrete contracts and change risks

## Guidance

Before design, review or refactoring, identify the changed behavior, intended maintainers, likely change, language/runtime/version, callers and constraints. Search the [code catalog](index.md) by that question; start with up to three matching details and expand for a concrete dependency. Preserve the project's established contracts and useful conventions.

- For understanding and modification, combine [readability](K-CODE-READABILITY.md), [maintenance evidence](K-CODE-MAINTAINABILITY-EVIDENCE.md), and [behavior-preserving change checks](K-CODE-CHANGE-TESTS.md) as needed.
- For structure, distinguish [information hiding](K-CODE-INFORMATION-HIDING.md), [dependency direction](K-CODE-DEPENDENCY-DIRECTION.md), [external dependency choice](K-CODE-DEPENDENCY-SELECTION.md), and [abstraction cost](K-CODE-ABSTRACTION-COST.md).
- For values and state, consult [configuration policy](K-CODE-CONFIGURATION-POLICY.md), [data invariants](K-CODE-DATA-INVARIANTS.md), and [API contracts](K-CODE-API-CONTRACTS.md).
- For lifetimes and cost, distinguish [resource ownership](K-CODE-RESOURCE-OWNERSHIP.md), [GC retention and cleanup](K-CODE-GC-LIFETIMES.md), [concurrent/asynchronous lifetimes](K-CODE-CONCURRENCY-LIFETIMES.md), and [performance evidence](K-CODE-PERFORMANCE-MEASUREMENT.md).

Carry the applicable action, source/locator, conditions, tradeoff and proposed check into the existing work brief. A code example, guideline, empirical association and locally reproduced result support different claims. Read the original when the summary cannot substantiate a consequential detail. Record a hypothesis as uncertain rather than converting repeated advice into a demonstrated safeguard.

## Applicability and exceptions

These references support judgment across contexts; they do not impose one language's semantics or one author's style everywhere. Fewer imports do not by themselves prove lower coupling; more interfaces do not prove modularity; moving every constant into configuration does not prove flexibility; GC and smart pointers do not establish all cleanup or concurrency guarantees.

When principles conflict, identify the concrete contract and cost. Compare the smallest viable options under the actual change and lifetime risks. Small local work need not acquire new abstractions, configuration files, experiments or a large review template. A temporary prototype and a long-lived shared API can justify different choices without silently weakening required correctness.

## Checks

- Does the selected advice match the actual language, engine, resource owner, deployment and team context?
- What observable change, misunderstanding or failure would the proposal prevent, and at what cost?
- Which callers, states, build inputs, configuration paths and cleanup obligations are affected?
- Are empirical study limits, untested assumptions, and evidence invalidated by the change visible?
- Do verification steps challenge actual behavior rather than count lines, interfaces or assertions as success?

Use the [code method](../../skills/vegabond-code/SKILL.md) and [design method](../../skills/vegabond-code-design/SKILL.md) for execution and verification. Knowledge validation establishes storage and retrieval, not program correctness, race freedom, memory safety, performance or developer productivity.

## Evidence

- User request in the current chat on 2026-11-07 to collect programming philosophy covering maintainability, readability, dependency minimization, modularity, hardcoding and memory management, within the ongoing knowledge-capture work.
- The [knowledge procedure](../../skills/vegabond-knowledge/SKILL.md) governs scoped retrieval, source boundaries and authorized maintenance. Individual references retain inspected original sources, publication context and proposed-check limits.
- This is a retrieval convention and synthesis, not a new software study, a completed refactor or evidence that a safeguard is enforced.
