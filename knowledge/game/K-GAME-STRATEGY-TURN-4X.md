---
id: K-GAME-STRATEGY-TURN-4X
title: Connect turn budgets, empire growth, and campaign endings
summary: In empire-scale turn strategy, inspect which actions compete for resources and how victory resolves a campaign after strategic uncertainty disappears.
kind: reference
scope: Turn-based empire and 4X design; Old World designer accounts of Orders and victory conditions
keywords: [4X, turn-based strategy, action economy, opportunity cost, victory, snowball, empire, 턴제전략, 행동경제, 기회비용, 승리조건, 문명, 제국]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Soren Johnson original designer notes opened; body and relevant author comment read
  application_status: Proposed campaign planning method; no simulation, AI evaluation, or full campaign played
---

# Connect turn budgets, empire growth, and campaign endings

## Guidance

**Source observations.** Johnson describes Old World's shared Orders pool as making military and economic actions compete; unlimited movement exposed comprehension problems and led to fatigue. His ending notes connect evolving ambitions to player direction, while victory points provide competitive pressure and a dominance finish. These are his design judgments for Old World, not universal genre findings.

**Proposed reusable method.** For a representative turn, list useful actions, what each consumes, and what must be postponed. Separate genuine allocation decisions from maintenance that is always correct. If introducing a shared action pool, examine empire scale, movement visibility, roads, retreat, and worker tasks together; changing only the command limit can accidentally favor a small mobile force or suppress economic recovery.

Model early, contested middle, dominant, and losing campaign states before expanding the technology tree. For each state, write a plausible goal, a way to change direction, an observable threat, and an end condition. Decide whether victory is a fixed race, a portfolio of objectives, or self-directed simulation. Do not silently switch contracts. For a score finish, check how settlement limits and map size affect score supply. For dynamic objectives, define eligibility, feasibility, replacement, and AI visibility rules.

Treat the ending as a pacing system with production consequences: objective variants, diplomacy explanations, AI behavior, and campaign testing all need authoring time. Prototype a compressed campaign before committing to many eras or factions.

## Applicability and exceptions

Use for empire management with turns and interacting military/economic systems. Small squad tactics, simultaneous turns, and open-ended simulations require different assumptions. Orders are one option; per-unit actions can be appropriate when their local choices remain interesting. Single-player AI may intentionally differ from human victory behavior, but players still need dependable rules for direct interactions. No source establishes a universally correct action cap, campaign length, or victory threshold.

## Checks

- Record meaningful choices and unavoidable maintenance per turn as the empire grows.
- Compare a concentrated offensive, split fronts, and economic investment under the same budget; inspect visibility and recovery.
- Run objective generation against disadvantaged and unusual empire states; flag impossible or repetitive tasks.
- Measure turns between a tester becoming confident of the outcome and the actual ending; inspect surprise losses and dominant-player cleanup separately.

## Evidence

- [Old World Designer Notes #1: Orders](https://www.designer-notes.com/old-world-designer-notes-1-orders/): shared-pool rationale, multiplayer prototypes, visibility, and fatigue; author's July 27 comment on escalating costs. Relevant original text read, not independently replicated.
- [Old World Designer Notes #11: The End](https://www.designer-notes.com/old-world-designer-notes-11-the-end/): victory points, ambitions, AI asymmetry, and double victory. Original designer account read; its genre-wide opinions remain attributed judgments.
