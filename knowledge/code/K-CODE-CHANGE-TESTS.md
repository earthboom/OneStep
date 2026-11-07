---
id: K-CODE-CHANGE-TESTS
title: Verify changes at a stable behavior boundary
summary: Choose checks that detect the changed behavior's plausible failures while permitting internal restructuring. For refactoring, establish the behavior to preserve and retain meaningful assertions across the change.
kind: reference
scope: Software changes and refactoring; test selection depends on observable contracts, integration risk and execution cost
keywords: [behavior testing, regression, refactoring, test boundary, test pyramid, contract test, 회귀 테스트, 리팩터링, 동작 검증, 테스트 경계]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Original Google testing article and Martin Fowler guidance inspected online
  application_status: Proposed verification method; no project tests or controlled mutations executed
---

# Verify changes at a stable behavior boundary

## Guidance

Start from a concrete obligation: which result, failure, side effect or resource transition must a caller observe? Choose a boundary that exposes that obligation while leaving irrelevant implementation decisions free to change. A unit may contain cooperating functions or classes, beyond one private method.

Proposed method: derive expected outcomes from the requirement, contract, independently known example or invariant. Avoid reproducing the production calculation in the assertion. Control time, randomness and external responses when they would obscure the failure being checked. Use a real integration where a substitute cannot establish the relevant compatibility.

For a behavior-preserving refactoring, establish a passing baseline and identify the assertions expected to remain valid. Change in reviewable steps and rerun affected checks. A constructor or fixture adjustment may be necessary; changing an expected result deserves investigation. For an intentional behavior change, state the new expectation separately from the behavior that must remain compatible.

## Applicability and exceptions

Apply this approach to features, consequential fixes, dependency changes and restructuring. Choose focused or broad tests according to actual risk, speed, reliability and maintenance cost; no fixed test count or universal layer ratio follows.

Internal interactions merit checks when they are themselves obligations, such as avoiding a prohibited external write. Performance, concurrency and resource safety can require benchmarks, stress checks, static analysis or direct reasoning beyond ordinary output assertions.

A reversible prose-only correction may need link or reading checks rather than new executable tests. Existing adequate coverage can be rerun without adding a redundant test. This entry does not prescribe test-first development for every change or claim that passing tests prove complete correctness.

## Checks

Proposed checks, untested locally:

- Name the plausible failure and the assertion or observation that would expose it; check important boundaries and failures.
- Where consequential and practical, show that a known broken case fails before relying on a regression check.
- Review failures after restructuring: distinguish broken behavior, changed setup and unnecessary implementation coupling. Record executed checks and remaining gaps.

## Evidence

Source observations, checked 2026-11-07; linked English originals accessible:

- [Andrew Trenk, Google Testing Blog](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html), 2013-08-05, calculator example and concluding paragraphs: recommends public behavior, allowing meaningful internal checks and setup changes.
- [Martin Fowler, Refactoring](https://refactoring.com/), undated introduction: defines restructuring through behavior-preserving steps. Original author's guidance, not an empirical guarantee.
- [Fowler, Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html), 2012-05-01, main text and footnote 2: motivates focused tests through cost and brittleness, with exceptions for inexpensive reliable broad tests. No local suite was evaluated.
