---
id: K-CODE-INFORMATION-HIDING
title: Place module boundaries around hidden design decisions
summary: Group responsibilities around decisions that should change privately, and evaluate a boundary by what callers must know rather than by file or class size.
kind: reference
scope: Software module design and refactoring; historical information-hiding arguments adapted to current language and performance constraints
keywords: [information hiding, encapsulation, modularity, cohesion, temporal decomposition, change propagation, 정보 은닉, 캡슐화, 모듈성, 응집도, 변경 전파]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Primary texts and official C++ guidance inspected on 2026-11-07; source observations separated from design synthesis
  application_status: Reference only; no project refactoring or runtime verification performed
---

# Place module boundaries around hidden design decisions

## Guidance

Source observation: Parnas contrasts processing-stage decomposition with boundaries that conceal changeable decisions. His module is a responsibility assignment, not necessarily a procedure. Abseil gives a narrower C++ example: file-local helpers can restrict visibility and make inputs clearer, with exceptions for object-state interactions.

Synthesis: identify a decision whose change would otherwise spread: representation, persistence format, ordering policy, resource ownership, or a protocol rule. Put its interpretation and mutation behind one coherent contract. State what callers may rely on and what remains private. A module can span several files; several tiny classes can still expose one shared implementation decision.

Trace knowledge crossing the boundary. Returning an internal container, requiring initialization in a special order, or exposing storage-specific errors can couple clients even when fields are private. Prefer operations expressing the caller's purpose when they eliminate that knowledge. Keep necessary behavior visible: ownership, failure, lifetime, concurrency, and ordering guarantees belong in the contract when callers need them.

## Applicability and exceptions

Use this when changes repeatedly cross module boundaries or reviewers must understand many internals together. Processing stages describe execution, streaming, or scheduling; they become useful maintenance boundaries when their shared contract is stable and independently useful.

Do not hide every implementation fact through another layer. A public data format may be the intended contract. Performance-sensitive boundaries may need batching, value types, or inlining; Parnas explicitly discusses implementation overhead. Neither his historical examples nor Abseil's C++ default establishes a universal module size or language-independent helper rule.

## Checks

Proposed review checks, not demonstrated safeguards:

- Name the decision hidden by each candidate module and the clients that currently know it.
- Walk through a plausible representation or policy change; list required client edits and explain each contractual dependency.
- Review exposed types, mutable aliases, call order, errors, and shared state for knowledge leaks.
- Confirm clients can perform normal work without reconstructing internals; measure actual hot paths before accepting performance claims.

## Evidence

- [Parnas, 1972 primary text](https://www.cs.lafayette.edu/~gexia/cs301/resources/parnas.html), “Changeability,” “The Criteria,” and “Efficiency and Implementation”; university transcription inspected, with its explicit accuracy warning. ACM publisher PDF returned 403.
- [Original 1971 CMU report scan](https://prl.khoury.northeastern.edu/img/p-tr-1971.pdf), title and “The Criteria,” printed pp. 17–21; repository cover, university mirror. Earlier report cross-check, not the 1972 edition.
- [Abseil Tip 186](https://abseil.io/tips/186), “Benefits” and “Reasons to Look Elsewhere”; C++ advice inspected. These sources supply design reasoning, not measured results for this repository.
