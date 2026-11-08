---
id: K-GAME-TECH-DUNGEON
title: "Generate levels from a traversability contract"
summary: "Choose a room graph, spatial partition, random walk or grammar according to the desired topology. Graph connectivity does not prove platformer reachability, key availability or acceptable difficulty."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["procedural","dungeon","BSP","random","walk","grammar","절차적생성"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Generate levels from a traversability contract

## Guidance

Choose a room graph, spatial partition, random walk or grammar according to the desired topology. Establish start-to-goal connectivity, then instantiate compatible rooms, doors and encounters. Separate seeded topology generation from decoration so cosmetic changes do not unexpectedly change routes.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Graph connectivity does not prove platformer reachability, key availability or acceptable difficulty. Different Spelunky, Rogue, Isaac and Dead Cells versions should not be assigned one universal algorithm.

## Checks

Proposed: generate a large reproducible seed set, validate movement-aware reachability and key ordering, retain failing seeds.

## Evidence

- [Shaker et al. — Constructive Generation Methods for Dungeons and Levels](https://www.pcgbook.com/chapter03.pdf) — 2016 author chapter; representation, BSP, agents and platform levels. Checked 2026-11-07, except items explicitly marked further reading.
- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — Author interactive article; graph representation and heuristic search. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V40, V56 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

