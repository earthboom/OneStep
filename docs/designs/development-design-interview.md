# Design proposal: turn a critical question into a testable development decision

2026-11-24 · Proposed revision to OneStep's software and game design workflow

## What the video contributes

Tech Bridge's 13:37 Korean video summarizes a longer NetworkChuck interview with Matt Pocock. This analysis uses the publishers' descriptions and chapter markers and Pocock's published skills. The Korean caption endpoint returned an empty response. Times below locate the publisher's topics; the design recommendations are our interpretation. [Korean video](https://www.youtube.com/watch?v=T8ccKI9Wn2E) · [Original interview](https://www.youtube.com/watch?v=mU8WKII1gpk)

| Korean chapter | What to take into OneStep |
| --- | --- |
| 0:31 strategy and tactics; 2:31 questions, vocabulary and decisions | Humans own priorities and acceptable losses. Test an ambiguous term against two concrete outcomes. Retain an agreed meaning where later work will use it. The original interview's 12:35 chapter applies the interview to Pocock's own video editor. [Original demonstration](https://www.youtube.com/watch?v=mU8WKII1gpk&t=755s) · [Domain modeling instructions](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md) |
| 4:48 reasoning effort and context; 6:17 specification, tickets and subagents | Hand the next unit the decided behavior, counterexample, source and open dependency. Ticketing and parallel workers are options once units have independent inputs and checks. Model-specific reasoning settings and context-size thresholds are not established for OneStep by the video. [Korean chapter](https://www.youtube.com/watch?v=T8ccKI9Wn2E&t=288s) · [Pocock's ticketing instructions](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md) |
| 7:08 merge risk; 8:33 feedback; 9:59 tests and deep modules | Review the change where it can do harm. For a consequential state transition, inspect its implementation and test the public behavior under failure. A deep module lets a caller use a small interface while the owning code handles meaningful complexity. Useful signals include real callers, old fixtures and player observations. [Korean review chapter](https://www.youtube.com/watch?v=T8ccKI9Wn2E&t=428s) · [Module design instructions](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md) |

## Proposed change to the existing route

[Scout](../../skills/vegabond-scout/SKILL.md) already distinguishes simple work from material ambiguity. [The design guide](../../skills/vegabond-code-design/references/scope-and-delivery.md) already identifies costly decisions and checks between units. The missing connection is what happens to a consequential question after the user answers it.

1. **Before asking, identify a real fork.** Separate the desired outcome, proposed mechanism and preserved behavior. Check the project term, actual caller, prior decision or incident when available. Current code can establish what happens today. A person's choice establishes whether it ought to change. If both interpretations produce the same behavior and check, proceed directly.
2. **Ask one question whose answer changes the work.** Describe a situation the user recognizes, the observable consequences of the plausible choices and which decision hinges on the answer. Offer a recommendation with its cost when the evidence warrants one. Leave room for a third outcome. Resolve prerequisite decisions first. Technical unknowns that a cheap experiment can settle go to that experiment.
3. **Make the answer usable.** In the existing brief, record the term or rule, the guarantee, a case that would violate it, and where to check it. Distinguish a confirmed decision from a reversible assumption or a user decision still open. Promote a recurring term to the project's existing vocabulary and a long-lived tradeoff to its decision history only when appropriate. A disagreement between the code and the answer becomes an explicit proposed change.
4. **Choose the work boundary.** Keep tightly coupled updates and their rejection path in one coherent unit. Split when a compatibility check, player observation or other result can redirect later work. Each handoff carries its behavior, preservation condition, relevant evidence, and actual blocking dependency. Independent checks and shared-state ownership determine whether parallel execution is feasible. Delegation also requires authorization.
5. **Stop asking and check independently.** The interview ends when the next unit has an outcome and an observable failure, and remaining uncertainty is reversible, isolated or assigned to a specific probe. Advance independent work while a user decision is pending. At integration, check the original user path and the highest-cost failure through the normal entry point. A failed check goes back to the implicated assumption. Record a reusable incident when there is an observed failure and a verified lesson.

**Suggested placement.** Scout keeps the ambiguity trigger. The code-design guide owns steps 1–4 and the stopping rule. Code verification consumes the failure example and inspects the affected implementation. Planning reuses the same decision for a player-facing or production commitment. Use the existing brief as the handoff. A short request needs no new file, ticket, glossary or review meeting.

## A worked design conversation

**Request:** “Add autosave after a boss.” Suppose the project currently restores location at checkpoints. The unresolved product term is “saved.” Ask: “The player collects the boss reward, quits before reaching the next checkpoint and reopens the game. Which reward, boss and location should they see?” The question allows different persistence rules for all three.

**Illustrative answer:** “Keep the reward. The boss stays defeated. Start at the previous checkpoint.” Record that reward ownership and boss defeat must agree after restart, while location follows the existing checkpoint. Test an interruption between recording defeat and granting the reward, followed by a reload and retry. Expect one reward, no respawn and the previous checkpoint location. A single operation can own the first two changes. The caller can request a completed encounter without knowing the order of individual writes. If old releases must open the new record, a real cross-version round trip becomes a prerequisite to enabling the writer. This example defines behavior and a proposed check; it does not assume a particular storage transaction exists.

## How to evaluate the revision

Compare the current and proposed instructions on the same briefs in fresh contexts. Give both evaluators the same materials and scripted user answers. Review behavior, the resulting decision and its test.

| Trial | Expected evidence |
| --- | --- |
| Plain label typo, plus a case already covered by an existing design decision | No unnecessary question or extra document. The existing decision is reused when applicable. |
| Ambiguous reward with the answer above | A concrete interruption question. The answer changes the persistence rule, handoff and expected reload result. Asking repeatedly without incorporating the answer fails. |
| An existing client rejects new saves; a supplied old fixture settles the technical question | Inspect the fixture or propose the compatibility check. Ask the human only about an unresolved support commitment. Keep the writer conditional. |
| Twelve planned rooms and an unfamiliar navigation cue | Keep twelve rooms in scope. Test the cue at one junction first. Automated playback establishes rendering; an unprompted player's choice and explanation address discoverability. |

Track missed decisions that change behavior, questions already answered by the project, and handoffs that lose an agreed preservation condition. These are proposed acceptance tests. No new skill implementation or comparative trial was performed in preparing this design.

## Development-only pilot, 2026-11-25

Two independent evaluators received the same three hypothetical software requests and fixtures. One used the pre-change code and code-design instructions and one used the pilot. Each asked one question about a relic collected before the next checkpoint. Both then received the same two alternative answers in separate scenarios. For immediate retention, both handoffs expected exactly one owned relic and no pickup after Continue. For rollback, both expected the pickup to reappear. Both preserved the checkpoint position. Both reused the supplied feedback inbox rule and handled a plain label typo without a question.

The trial exercised the proposed questions and implementation handoffs. It found no improvement over the baseline on these cases. The explicit rule is a pilot in the two development skills. Actual implementation behavior and rework remain unmeasured.
