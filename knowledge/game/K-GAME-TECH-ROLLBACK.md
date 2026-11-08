---
id: K-GAME-TECH-ROLLBACK
title: "Restore and re-simulate state for rollback networking"
summary: "Predict missing inputs, restore snapshots and re-simulate corrections. Commit external achievements and rewards only after trusted confirmation; replay deduplication alone cannot validate a predicted event."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["rollback","GGPO","delay","input","prediction","achievement","reward","confirmation","롤백","롤백넷코드","재시뮬레이션","업적","보상","확정"]
status: active
checked_at: '2026-11-08'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Restore and re-simulate state for rollback networking

## Guidance

Predict missing remote inputs, save simulation snapshots, and compare actual inputs when received. On mismatch restore the earlier snapshot and simulate forward without rendering every intermediate frame. Input delay can be combined with rollback to bound corrections.

Separate rollback-owned state, reversible presentation and irreversible external effects. Restore simulation state; deduplicate or cancel speculative audio, particles and UI. Do not grant platform achievements, currency or external rewards from a predicted event, even if it is emitted only once. Commit only after the event and its eligibility are confirmed by the protocol's trusted boundary: agreed final inputs/verified state in a peer protocol, or the responsible authority in an authoritative design. Elapsed time or a full animation is not confirmation. See [authority and prediction](K-GAME-TECH-AUTHORITY.md) when that architecture applies.

Give each confirmed effect a stable idempotency key, including session/match, event identity and recipient, that survives replay and retries without merging distinct events. Confirmation prevents false awards; idempotency prevents duplicates. An in-memory seen-set is not crash-safe delivery: external rewards also need a durable commit/retry contract and compatible receiver deduplication or transactions.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Rollback is not merely skipping an animation's beginning. It needs restorable deterministic state, replay CPU budget and a maximum rollback policy.

## Checks

Proposed engine/protocol checks: force wrong predictions, out-of-order inputs and long gaps; verify final state hashes. A predicted KO corrected to a block must grant zero external awards. Pending/untrusted events must grant zero; a confirmed eligible event replayed or retried must grant one. Distinct events in the same tick, recipients and matches must remain distinct. Test restart/acknowledgment loss against the actual durable delivery and receiver contract before claiming reliable external delivery.

[Controlled event traces](../../skills/vegabond-knowledge/tests/game-application/check_rollback_rewards.py) compare a dedup-only negative control with a confirmation gate and stable keys. These exercise a toy contract, not GGPO/Photon, a game, a network or a reward service; they do not validate determinism, trust, persistence or performance.

## Evidence

- [GGPO — Rollback Networking SDK](https://www.ggpo.net/) — Project explanation; prediction, save/load state and re-simulation. Checked 2026-11-07, except items explicitly marked further reading.
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) — 2014 author article; exact determinism and input synchronization. Checked 2026-11-07, except items explicitly marked further reading.
- [Photon Quantum 3 — Frames, “Which Frame To Read In The View”](https://doc.photonengine.com/quantum/v3/manual/frames) — Predicted view state can change on rollback; use verified state for non-reverting decisions. Product-specific confirmation terminology, not a requirement for a server. Checked 2026-11-08.
- [Photon Quantum 2.1.9 — CallbackEventCanceled](https://doc-api.photonengine.com/en/quantum/v2/class_quantum_1_1_callback_event_canceled.html) — Predicted events can be canceled; synchronized events are raised on verified frames. Separating confirmation from external award delivery is engineering synthesis; the API does not promise durable reward transactions. Checked 2026-11-08.
- Originating channel shorts: V31 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

