---
id: K-GAME-TECH-CONTROLLER
title: "Implement forgiving platformer input as explicit state windows"
summary: "Timestamp jump requests and last grounded state. Celeste values and integer-AABB rules are a particular game solution."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["coyote","jump","buffering","corner","correction","acceleration","조작감","코요테타임","점프버퍼링","착지","입력씹힘","코너보정"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Implement forgiving platformer input as explicit state windows

## Guidance

Timestamp jump requests and last grounded state. Permit a jump while its input buffer and ground-grace conditions overlap, then consume the request once. Add bounded corner correction after collision tests, and specify moving-platform momentum ownership. Tune acceleration, release deceleration and air control against intended challenge reach.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Celeste values and integer-AABB rules are a particular game solution. Do not permit infinite buffered jumps, correction through walls, or accidental momentum duplication.

## Checks

Proposed: test inputs just before/after ledges and landings, corner approaches, reversals and moving-platform stops at several frame rates.

## Evidence

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html) — Creator text; coyote time, buffering, corner correction and momentum storage. Checked 2026-11-07, except items explicitly marked further reading.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — Creator implementation; integer AABBs and fractional remainder. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V29, V30, V46 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

