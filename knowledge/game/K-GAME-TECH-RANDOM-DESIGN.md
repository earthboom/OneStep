---
id: K-GAME-TECH-RANDOM-DESIGN
title: "Control randomness by decision timing and streak distribution"
summary: "Classify when uncertainty becomes known and how strongly it changes outcomes. Input randomness is not automatically good and output randomness not automatically bad; the cited designers disagree."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["randomness","pity","shuffle","bag","probability","agency","확률","천장"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Control randomness by decision timing and streak distribution

## Guidance

Classify when uncertainty becomes known and how strongly it changes outcomes. A shuffle bag samples without replacement until refill; a pity system changes conditional odds after failures or guarantees an outcome. Compute P(first success=n)=p_n*product(1-p_i for i<n), then derive expected wait and tail probabilities.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Input randomness is not automatically good and output randomness not automatically bad; the cited designers disagree. Changing odds changes the process and must not be described as independent fixed-probability trials.

## Checks

Proposed: compare mean, percentiles and maximum droughts, inspect bag-boundary repeats, and playtest whether players understand their options.

## Evidence

- [Ian Schreiber — Probability and Randomness](https://gamebalanceconcepts.wordpress.com/2010/07/28/level-4-probability-and-randomness/) — 2010 designer course; probability distributions and expected values. Checked 2026-11-07, except items explicitly marked further reading.
- [Keith Burgun — Randomness and Game Design](https://www.gamedeveloper.com/design/randomness-and-game-design) — Designer argument; input/output randomness. Normative position, not consensus. Checked 2026-11-07, except items explicitly marked further reading.
- [A Defense of Randomness in Competitive Games](https://www.gamedeveloper.com/design/a-defense-of-randomness-in-competitive-games) — Original design argument disagreeing with avoidance of output randomness. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V09, V44 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

