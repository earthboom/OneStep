---
id: K-GAME-PUZZLE
title: Build puzzle content around discoverable interactions and deductions
summary: For authored logic puzzles, prototype the interaction or deduction the player should discover, then test whether the available information supports it. Use variants and cuts to shape a learning sequence rather than targeting puzzle count alone.
kind: reference
scope: Game planning; authored systemic logic and environmental puzzles; not a complete method for trivia, hidden-object, or procedural puzzle economies
keywords: [puzzle, deduction, rule-discovery, level-design, playtesting, 퍼즐, 추론, 규칙발견, 레벨설계, 플레이테스트]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Developer articles opened; embedded talk not inspected; source claims separated from planning synthesis
  application_status: Reference research only; proposed checks not run on a game
---

# Puzzle discovery and content structure

## Guidance

**Source-supported:** Patrick Traynor's strategy collection suggests requiring a particular interaction or deduction, exploring mechanic pairs and unusual geometry, and using playtester misunderstandings or alternate solutions to generate levels. He describes iteration as producing many discarded drafts and potentially several useful variants [1]. Jonathan Blow's developer post describes deleting an unsatisfactory area containing roughly 25 puzzles; it also cautions that puzzle counts are not directly comparable when their scale differs [2]. His talk announcement frames design as exploring a system's consequences and seeking clear expression of its ideas [3].

**Reusable planning synthesis:** First define the player's initial rule model, visible goal, legal actions, and the new inference a level makes possible. Build a minimal playable arrangement that requires that inference; separately record intended solutions, alternatives, and accidental bypasses. An alternate solution may expose another worthwhile concept rather than simply being a defect.

Organize content by knowledge prerequisites: introduce an interaction, vary its context, combine it with another, then revisit it under a changed assumption. This is a candidate sequence, not a requirement to make every puzzle teach exactly one fact. Give players room to experiment and decide when to leave an optional challenge. Plan undo, reset, and feedback according to the cost of experimentation. Difficulty can come from unfamiliar reasoning, execution, memory, or search; identify which you actually intend before adding complexity.

## Applicability and exceptions

Best suited to finite authored systems whose rules can be explored. Timing puzzles, collaborative puzzles, riddles, and culturally dependent clues need additional evidence. Minimal presentation can aid focus but may remove orientation or accessibility cues. More possible states do not establish more valuable discoveries. The cited deletion is one production decision, not an optimal rejection rate.

## Checks

Proposed checks: observe a fresh player without supplying the missing rule; record what they noticed, inferred, and tried. Compare failures with information actually available. Replay after changes to confirm solvability and inspect unintended shortcuts. Distinguish productive experimentation from repeated guesses caused by unreadable feedback. These checks remain unexecuted here.

## Evidence

1. [Traynor, Puzzle Level Idea Strategies](https://cwpat.me/misc/puzzle-level-idea-strategies/), 2022-07-14: headings “Find an interaction and force it,” “Clarify a misunderstanding,” “Turn alternate solutions,” and “Other notes”; full article inspected.
2. [Blow, How many puzzles are in The Witness?](https://www.the-witness.net/news/2011/02/how-many-puzzles-are-in-the-witness/), 2011-02-08: opening paragraphs before comments; developer text inspected, reader comments excluded.
3. [Designing to Reveal the Nature of the Universe](https://the-witness.net/news/2011/11/designing-to-reveal-the-nature-of-the-universe/), 2011-11-02: author introduction/abstract only; embedded talk and comments are outside the inspected evidence.
