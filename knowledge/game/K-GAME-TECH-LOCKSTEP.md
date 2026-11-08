---
id: K-GAME-TECH-LOCKSTEP
title: "Use lockstep only with an exact determinism contract"
summary: "Exchange tick-indexed inputs instead of every object's state. Sharing a random seed alone does not guarantee determinism; floating-point and threading differences can diverge."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["deterministic","lockstep","RTS","hash","결정론"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Use lockstep only with an exact determinism contract

## Guidance

Exchange tick-indexed inputs instead of every object's state. Start from identical state and make random streams, processing order, arithmetic and simulation steps reproducible. Use state hashes to locate divergence. A playout buffer absorbs arrival jitter but adds delay.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Sharing a random seed alone does not guarantee determinism; floating-point and threading differences can diverge. Shared simulation can expose information clients should not know.

## Checks

Proposed: compare per-tick hashes across supported platforms/builds and long runs with the same recorded inputs.

## Evidence

- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) — 2014 author article; exact determinism and input synchronization. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V04 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

