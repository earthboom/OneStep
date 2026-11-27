---
id: K-CODE-UE-TAGQUERY-EMPTY-MATCH
title: What an empty FGameplayTagQuery or tag container matches in Unreal, and why an unset allowlist needs its own check
summary: FGameplayTagQuery::Matches returns false for an empty query, HasAny returns false and HasAll returns true for an empty container, and project wrappers often turn an empty query into match-all. When a query selects what an action may touch, check emptiness at configuration time instead of relying on the match call.
kind: reference
scope: Unreal Engine 5 GameplayTags runtime module; code that filters or selects actors by a designer-authored tag query or tag container
keywords: [FGameplayTagQuery, FGameplayTagContainer, MatchesQuery, Matches, IsEmpty, HasAny, HasAll, empty query, allowlist, optional filter, match-all, gameplay tag, designer-authored condition, unset property]
status: active
checked_at: "2026-11-24"
context:
  engine: Unreal Engine 5.8 (5.8.0 source tree)
---

## Guidance

A gameplay tag query (`FGameplayTagQuery`) is a designer-authored boolean expression over gameplay tags. A tag container (`FGameplayTagContainer`) is a set of tags. Each has a fixed answer when the condition side is empty, and the answers differ:

| Call | Empty condition gives | Reading |
| --- | --- | --- |
| `FGameplayTagQuery::Matches(Tags)` | false | An unset query matches nothing |
| `FGameplayTagContainer::MatchesQuery(Query)` | false | Forwards to `Query.Matches(*this)` |
| `FGameplayTagContainer::HasAny(Other)` with empty `Other` | false | Nothing to find |
| `FGameplayTagContainer::HasAll(Other)` with empty `Other` | true | No check failed |

Decide what an empty condition should mean from the role the condition plays, then confirm the call path gives that meaning:

- **Optional filter** (a restriction on something that is allowed by default, such as "only apply when the target has these tags"): empty means no restriction, so the wanted answer is true. The engine query call does not give that, which is why projects commonly wrap it as `Query.IsEmpty() ? true : Tags.MatchesQuery(Query)`.
- **Allowlist or selection** (the condition names what an action may touch, and everything else is left alone): empty means nothing is selected, so the wanted answer is false. Passing such a condition through a match-all wrapper makes an unset property select every candidate.

For an allowlist, do not let the match call carry the empty case. Check `IsEmpty()` (and a null asset, when the query lives in a data asset) once when the owner is configured or activated, report it as a visible error naming the owner, and turn that selection path off. The per-candidate match then never sees an empty condition, and either wrapper semantic is safe.

## Applicability and exceptions

- The table is the engine behavior. A project helper with the same name as an engine function can differ; read the helper before assuming either semantic.
- An empty condition is not the same as a condition that matches nothing by content (for example a query on a tag no object has). The configuration check catches only the unset case; a regression test or data check is needed for the other.
- `HasAll` on an empty container returning true is the same hazard in container form: a "must have all of these" list that is left empty passes every candidate.
- This entry does not cover `FGameplayTagRequirements` or gameplay effect application requirements; their empty-case behavior was not read.

## Checks

- For each designer-authored tag condition, write down whether it restricts or selects, and what an unset value should do.
- Open the function the code actually calls (engine call or project wrapper) and read its empty branch.
- For a selecting condition, find the place that rejects an empty or missing condition before the first candidate is tested, and confirm it logs with the owner's name.
- Add a test that runs the owner with the condition unset and asserts that no candidate is selected and the error is reported.

## Evidence

Read in a UE 5.8.0 source tree on 2026-11-24, module `Engine/Source/Runtime/GameplayTags`:

- `Private/GameplayTagContainer.cpp`: `FGameplayTagQuery::Matches` returns false when `IsEmpty()`; `FGameplayTagQuery::IsEmpty` tests for an empty token stream; `FGameplayTagContainer::MatchesQuery` returns `Query.Matches(*this)`.
- `Classes/GameplayTagContainer.h`: the `HasAny` comment and body return false for an empty `ContainerToCheck`; the `HasAll` comment and body return true for an empty `ContainerToCheck`, "because there were no failed checks".

The wrapper form and the allowlist hazard were found by reading one studio project's helper during a design review; nothing was run. The project's classes and data stay in that project's documents.
