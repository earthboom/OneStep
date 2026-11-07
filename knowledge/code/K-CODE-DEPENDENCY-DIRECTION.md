---
id: K-CODE-DEPENDENCY-DIRECTION
title: Direct dependencies toward contracts that protect policy
summary: Protect important policy from volatile implementation details with a suitable contract, while avoiding interfaces that merely duplicate stable concrete APIs.
kind: reference
scope: Dependency design across software policy and implementation boundaries; C++ historical DIP and Go interface examples require language-specific adaptation
keywords: [dependency inversion, DIP, dependency direction, coupling, policy, interface ownership, dependency injection, 의존성 역전, 의존 방향, 결합도, 정책, 인터페이스]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Martin original DIP article and official Go and Google guidance inspected on 2026-11-07
  application_status: Reference only; no dependency graph or runtime behavior verified in a target implementation
---

# Direct dependencies toward contracts that protect policy

## Guidance

Source observation: Martin's 1996 DIP article argues that policy and implementation should depend on abstractions, and abstractions should avoid implementation details. Effective Go shows behavior-based interfaces; Google's build chapter distinguishes explicit direct dependencies from accidental transitive ones. These discuss different dependency mechanisms.

Synthesis: identify the policy worth preserving and the detail likely to vary, then choose a contract expressing the policy's needs. Avoid defining it through vendor types, database rows, transport failures, or configuration unless intentionally required. Centralize construction and concrete selection where composition is understood.

Draw source, build, and runtime relationships separately. Calling an adapter at runtime does not require policy source to import its concrete implementation. Conversely, passing an interface does not remove dependence on its semantics, lifetime, ordering, or shared state. Evaluate change propagation and knowledge requirements as well as import counts. One import of a volatile shared schema can matter more than several stable library imports.

## Applicability and exceptions

Use inversion for a substitution boundary, external integration, expensive side effect, or independently evolving policy. A useful seam may have one production implementation. Several implementations need not share an abstraction when their contracts differ.

Do not require an interface for every class, a dependency injection container, or two adapters at every boundary. Stable concrete types or internal helpers may need no indirection. Parameters, callbacks, protocols, traits, or standard contracts may suffice. Martin's C++ examples are historical arguments; Go's implicit interface satisfaction is language-specific. Framework ownership and generated interfaces can constrain placement.

## Checks

Proposed checks for the chosen implementation:

- Write the policy's required operations and guarantees before selecting an adapter API.
- Inspect source and build graphs for forbidden concrete imports, cycles, and undeclared direct dependencies.
- Try one credible detail change on paper; locate policy edits, including leaked data and error types.
- Exercise contract behavior with the actual adapter where applicable; a test double alone cannot establish integration compatibility.
- Remove an interface mentally: if no volatility, knowledge, or testing cost returns, reconsider its value.

## Evidence

- [Martin, The Dependency Inversion Principle](https://www.cs.utexas.edu/users/downing/papers/DIP-1996.pdf), pp. 5–7 and 10–11: Copy, layers, and adapter discussion; original article inspected through a university mirror.
- [Effective Go](https://go.dev/doc/effective_go#interfaces), “Interfaces and other types”; behavior contracts inspected. Page warns its 2009 guidance is not actively updated.
- [Software Engineering at Google, chapter 18](https://abseil.io/resources/swe-book/html/ch18.html), “Internal dependencies”; build-specific advice inspected. No local architecture or performance result was established.
