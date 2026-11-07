---
id: K-CODE-API-CONTRACTS
title: Make interface obligations and guarantees explicit before replacing a dependency
summary: Compare an interface's accepted inputs, observable results, failures and resource lifetime before changing its implementation or provider. A matching method signature alone does not establish substitutability.
kind: reference
scope: Internal and external software interfaces; concrete guarantees depend on language, library and deployed version
keywords: [API contract, precondition, postcondition, invariant, error semantics, resource lifetime, compatibility, 인터페이스, 계약, 사전조건, 사후조건, 수명]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Official Python 3.14 io and Rust std Vec documentation inspected online
  application_status: Proposed contract review; no dependency substitution or runtime check performed
---

# Make interface obligations and guarantees explicit before replacing a dependency

## Guidance

Before using or replacing an interface, write down what callers must provide and what they may rely on. Proposed contract dimensions are valid inputs and state, result meaning and units, state changes, failure behavior, ownership and lifetime, and relevant ordering or concurrency constraints. Mark unspecified behavior explicitly; an implementation's current habit is not automatically a promise.

Separate preconditions from postconditions. A precondition states what must hold before a call, such as a usable resource or an allowed range. A postcondition describes the result and state after successful completion. Error semantics must also say what remains valid after failure: whether work was partial, state changed, cleanup is required, or retry is safe. An invariant describes a condition that must remain true at the stated observation boundary.

Document the caller's obligations and the provider's guarantees where users encounter the interface. Types can encode some distinctions; validation, documentation and examples cover others. Prefer the smallest useful contract over a duplicate account of implementation internals.

## Applicability and exceptions

Use this comparison for wrappers, library upgrades, mocks, alternate providers and internal refactoring across a module boundary. A shared signature cannot settle semantic compatibility. Resource ownership matters even with automatic memory management: files, locks, subscriptions and asynchronous tasks have useful lifetimes distinct from object reachability.

Not every interface needs every dimension. A pure calculation may have no cleanup obligation. Timing or allocation details belong in the contract only when callers legitimately depend on them. Version-specific examples below illustrate the method; they do not impose Python or Rust semantics on another language.

## Checks

Proposed checks, requiring local application:

- List one normal case, one boundary case and each consequential failure or lifetime transition. State caller obligations and observable guarantees separately.
- Compare old and new providers against those cases, including partial completion and cleanup. Resolve ambiguous guarantees before migration.
- Choose targeted type checks, contract tests or inspection for the identified risk. Record the dependency version and any unverified dimensions.

## Evidence

Source observations, checked 2026-11-07:

- [Python io documentation](https://docs.python.org/3.14/library/io.html), “Overview,” “IOBase,” and “Raw File I/O”: documents data-type errors, context-manager closure and possible partial raw writes. Official English Python 3.14 reference; relevant sections accessible. No Python execution was performed.
- [Rust Vec documentation](https://doc.rust-lang.org/std/vec/struct.Vec.html#guarantees), “Guarantees” and `with_capacity`: distinguishes guaranteed capacity behavior from an unspecified growth strategy. Official English std reference, served as 1.99.1; relevant sections accessible. No Rust build or compatibility test was performed.
