---
id: K-CODE-UE-AUTOMATION-EXPECTED-MESSAGES
title: What happens when an Unreal automation test declares the same expected log message twice
summary: FAutomationTestBase keeps expected messages in a set keyed only by the pattern string, so a later AddExpectedError or AddExpectedMessage with the same pattern replaces the earlier declaration, including its count, verbosity and match type. When a shared harness declares an environment message, a second declaration in the test body is either overwritten or overwrites the harness.
kind: reference
scope: Unreal Engine 5 automation framework (FAutomationTestBase) expected error, warning and message declarations, including latent commands that declare during the test
keywords: [FAutomationTestBase, AddExpectedError, AddExpectedMessage, AddExpectedMessagePlain, FAutomationExpectedMessage, ExpectedMessages, EAutomationExpectedErrorFlags, EAutomationExpectedMessageFlags, Occurrences, TSet, MoveByRelocate, expected error, expected occurrences, test harness, local whitelist, 기대 오류, 예상 에러 선언]
status: active
checked_at: "2026-11-23"
context:
  engine: Unreal Engine 5.8 source (Runtime/Core Misc/AutomationTest and Containers)
---

## Guidance

`FAutomationTestBase::AddExpectedMessage` (and `AddExpectedError`, `AddExpectedMessagePlain`, which forward to it) adds an `FAutomationExpectedMessage` to `ExpectedMessages`, a `TSet<FAutomationExpectedMessage>`. The element's equality and hash use only `MessagePatternString`. The set does not allow duplicate keys, so adding an element whose pattern equals an existing one relocates the new element over the old one. Only the last declaration for a pattern survives; its occurrence count, verbosity, compare type and regex flag replace the earlier values. Declarations are not summed.

Consequences:

- A shared harness that declares an environment message (for example a headless rendering message per client) and a test body that declares the same pattern do not combine. Whichever call runs later decides the expected count. Latent commands run after `RunTest` returns, so a harness declaration made inside a latent command overrides the test body's declaration.
- A duplicate declaration with the same count looks harmless but is dead code, and it silently stops matching the real count when either side changes. Declare environment noise in one owner and let tests pass the facts that owner needs (such as client count).
- Patterns that differ by even one character are separate entries and are checked independently.

## Applicability and exceptions

Checked against the 5.8 engine source. The replacement behavior depends on `TSet` using the default key functions without duplicate keys, which holds for this member in that version. Other engine versions should be checked at the same two places before relying on it. This entry covers declaration storage only; how matched messages are counted at test end is unchanged.

## Checks

- Before adding an expected message in a test, search the shared harness and helpers it uses for the same pattern string. If one exists, remove the local declaration and supply the inputs the harness needs.
- When a count must change for one scenario, make the declaration in exactly one place and confirm with a run that the expected count is reported as met.

## Evidence

- Engine source, UE 5.8: `Runtime/Core/Public/Misc/AutomationTest.h`: `FAutomationExpectedMessage::operator==` and `GetTypeHash` compare only `MessagePatternString`; member `TSet<FAutomationExpectedMessage> ExpectedMessages`.
- `Runtime/Core/Private/Misc/AutomationTest.cpp`: `FAutomationTestBase::AddExpectedMessage` calls `ExpectedMessages.Add(...)` without a lookup.
- `Runtime/Core/Public/Containers/CompactSet.h.inl` and `SparseSet.h.inl`: when `bAllowDuplicateKeys` is false and the key exists, the new element replaces the existing one by `MoveByRelocate`.
- Task check (2026-11-23): a game test suite declared a headless cursor message per test while the shared network test harness declared the same pattern later from a latent command; the local declarations were removed and the suite was rerun under the harness declaration alone.
