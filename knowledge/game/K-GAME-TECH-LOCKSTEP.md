---
id: K-GAME-TECH-LOCKSTEP
title: Use lockstep only with an exact determinism contract
summary: Use the next complete tick as the simulation boundary and compare per-tick
  hashes over the common prefix.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- deterministic
- lockstep
- RTS
- hash
- 결정론
- deterministic lockstep
- playout delay buffer
- state hash
- 입력 버퍼
- 상태 해시
- 입력 누락
- 최초 불일치
- per-tick state hash
- stall duration
status: active
checked_at: '2026-11-21'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped local Unreal evidence for two Win64 processes and one
    deterministic integer scene.
---
# Use lockstep only with an exact determinism contract

## Guidance

Exchange tick-indexed inputs instead of every object's state. Start from identical state and make random streams, processing order, arithmetic and simulation steps reproducible. Use state hashes to locate divergence. A playout buffer absorbs arrival jitter but adds delay.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Sharing a random seed alone does not guarantee determinism; floating-point and threading differences can diverge. Shared simulation can expose information clients should not know.

In **deterministic lockstep**, peers advance tick n only when the required inputs for n are available. A **playout delay buffer** holds inputs briefly to absorb jitter. It costs latency and cannot fill an indefinitely missing tick. Compare hashes of equivalent simulation state after each tick and locate the first divergence, checking seed, update order and arithmetic on each supported build. [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

## Checks

Proposed: compare per-tick hashes across supported platforms/builds and long runs with the same recorded inputs.

## Evidence

- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) — 2014 author article; exact determinism and input synchronization. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V04 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Applying input buffering

Advance only through the next tick with all required inputs. Retain input sequence numbers across reordering, and handle repeated delivery without applying an input twice. Two peers can finish at different ticks while agreeing on their shared prefix. Compare hashes at corresponding ticks to identify the earliest divergence.

Size playout delay from observed input arrival variation, the budget for input response and the tolerance for stalls. Measure deliberate buffering separately from missing-input stalls after scheduled playback starts. Define a session policy for inputs that fail to arrive. Use a determinism contract specific to the participating builds and arithmetic.
