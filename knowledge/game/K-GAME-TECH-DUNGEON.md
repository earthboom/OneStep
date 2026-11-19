---
id: K-GAME-TECH-DUNGEON
title: Generate levels from a traversability contract
summary: Use binary space partitioning to lay out rooms, then test both graph connectivity and clearance
  for the intended moving body.
kind: reference
scope: Game development. For seeded grid generation, Unreal Engine's `FRandomStream` produces a repeatable
  sequence from an explicit seed.
keywords:
- procedural
- dungeon
- BSP
- random
- walk
- grammar
- 절차적생성
- seed
- room corridor
- capsule clearance
- connectivity
- farthest exit
- 던전
- 시드
- 방 통로
- 연결성
- binary space partitioning
- breadth-first search
- flood fill
- FRandomStream
status: active
checked_at: '2026-11-19'
---
# Generate levels from a traversability contract

## Guidance

Binary space partitioning (BSP) recursively splits a region. Place rooms within leaf regions and connect rooms on opposite sides of each internal split. A grid flood fill from the entrance measures reachable floor cells. With unit movement costs, breadth-first search also supplies shortest path lengths for choosing a distant exit. Random walks and authored grammars offer different control over structure.

## Applicability and exceptions

For seeded grid generation, Unreal Engine's `FRandomStream` produces a repeatable sequence from an explicit seed. Reproduction also requires the same draw order, generator and input settings. Epic warns about weak low bits, so use its range functions instead of taking a remainder for bounded choices. A cell connection may still be too narrow for a capsule or impassable under gravity.

## Checks

Repeat a seed, independently flood-fill the final map and sweep the intended capsule along connecting turns and doorways. Test minimum leaf size, narrow corridors, unreachable goals and changes in draw order. Playtest pacing separately.

## Evidence

The PCG chapter describes constructive methods, and Epic documents the seeded stream. Prior Unreal observations covered generated static flat grids and upright capsule clearance. They establish neither full character traversal nor level quality.

- [Shaker et al. — Constructive Generation Methods for Dungeons and Levels](https://www.pcgbook.com/chapter03.pdf)
- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Epic — FRandomStream](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Core/FRandomStream)
- [Epic — Random Streams](https://dev.epicgames.com/documentation/en-us/unreal-engine/random-streams-in-unreal-engine)
