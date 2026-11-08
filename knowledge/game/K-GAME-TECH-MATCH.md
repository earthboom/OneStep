---
id: K-GAME-TECH-MATCH
title: "Separate skill estimation from matchmaking policy"
summary: "Estimate skill separately from selecting a match. Do not generalize 'the highest party member sets the match' to every game."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["Elo","TrueSkill","MMR","uncertainty","matchmaking","매칭"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Separate skill estimation from matchmaking policy

## Guidance

Estimate skill separately from selecting a match. TrueSkill represents a distribution with mean and uncertainty and updates from results; Elo uses expected outcomes for rating updates. Match search additionally chooses latency, party, queue time and acceptable skill spread constraints.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Do not generalize 'the highest party member sets the match' to every game. Ratings are estimates, not a promise of 50% win probability in every individual match.

## Checks

Proposed: evaluate new-player convergence, mixed-skill parties, queue scarcity and latency; compare predicted versus observed outcomes.

## Evidence

- [Microsoft Research — TrueSkill Ranking System](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) — Official project text; mean, uncertainty, team outcomes; distinct from complete match search. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V33 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

