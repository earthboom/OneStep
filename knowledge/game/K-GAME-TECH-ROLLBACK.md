---
id: K-GAME-TECH-ROLLBACK
title: "Restore and re-simulate state for rollback networking"
summary: "Predict missing remote inputs, save simulation snapshots, and compare actual inputs when received. Rollback is not merely skipping an animation's beginning."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["rollback","GGPO","delay","input","prediction","롤백","롤백넷코드","재시뮬레이션"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Restore and re-simulate state for rollback networking

## Guidance

Predict missing remote inputs, save simulation snapshots, and compare actual inputs when received. On mismatch restore the earlier snapshot and simulate forward without rendering every intermediate frame. Deduplicate audio, particles and achievements across replay. Input delay can be combined with rollback to bound corrections.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Rollback is not merely skipping an animation's beginning. It needs restorable deterministic state, replay CPU budget and a maximum rollback policy.

## Checks

Proposed: force wrong predictions, out-of-order inputs and long gaps; verify final state hashes and exactly-once side effects.

## Evidence

- [GGPO — Rollback Networking SDK](https://www.ggpo.net/) — Project explanation; prediction, save/load state and re-simulation. Checked 2026-11-07, except items explicitly marked further reading.
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) — 2014 author article; exact determinism and input synchronization. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V31 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

