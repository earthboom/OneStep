---
id: K-GAME-TECH-ROLLBACK
title: Restore and re-simulate state for rollback networking
summary: Restore a bounded snapshot and re-simulate with corrected inputs. Publish
  confirmed contact events once. Native Unreal evidence covers both waiting and rollback
  on one reproducible delay trace.
kind: reference
scope: Game development. For a rollback simulation, restored state and input order
  must reproduce the agreed result within the replay budget.
keywords:
- rollback
- GGPO
- delay
- input
- prediction
- achievement
- reward
- confirmation
- 롤백
- 롤백넷코드
- 재시뮬레이션
- 업적
- 보상
- 확정
- idempotency key
- verified frames
- CallbackEventCanceled
- rollback contact
- snapshot restore
- contact event deduplication
- 접촉 이벤트
- 스냅샷 복원
- 입력 대기
- 롤백 재실행 틱
status: active
checked_at: '2026-11-20'
context:
  application_status: V31 Unreal 5.8.3 30 Hz two-character integer contact scene.
    Native wait/rollback comparison with authored input arrivals, exact confirmed
    state and contact proof, three frame-cost runs per method.
---
# Restore and re-simulate state for rollback networking

## Guidance

Rollback networking predicts missing input, saves restorable simulation snapshots and re-simulates when the received input differs. Cancel or reconcile speculative audio, particles and UI. An external achievement, currency award or other irreversible effect must wait for verified eligibility. Give the confirmed effect an idempotency key that distinguishes session, event and recipient across replay and delivery retries.

## Applicability and exceptions

For a rollback simulation, restored state and input order must reproduce the agreed result within the replay budget. A peer protocol can agree on final inputs and verified state. An authoritative game delegates eligibility to its responsible authority. A display animation or elapsed delay cannot establish confirmation. Reliable cross-restart delivery also requires durable state and a compatible receiver contract.

## Checks

Inject wrong and out-of-order inputs and compare final state hashes. A predicted knockout corrected to a block must produce zero external awards. Replay and retry a confirmed award and expect one delivery effect. Test distinct same-tick events, recipients, lost acknowledgments and restart recovery.

## Evidence

GGPO describes prediction and replay. Photon Quantum distinguishes predicted and verified frames and documents cancellation of predicted events. Earlier synthetic event traces exposed a false award when deduplication was the only guard. They did not exercise network determinism or a durable reward service. External delivery is an engineering design requirement.

- [GGPO — Rollback Networking SDK](https://www.ggpo.net/)
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)
- [Photon Quantum 3 — Frames, “Which Frame To Read In The View”](https://doc.photonengine.com/quantum/v3/manual/frames)
- [Photon Quantum 2.1.9 — CallbackEventCanceled](https://doc-api.photonengine.com/en/quantum/v2/class_quantum_1_1_callback_event_canceled.html)

## Unreal contact rollback — 2026-11-20

The local V31 experiment used the same 30 Hz two-character input sequence and the same delayed, reordered and duplicate arrivals for waiting and rollback. Every 240-tick confirmed trajectory matches the independent oracle. The two real contact starts publish once. Two predicted contacts are cancelled when the late avoidance inputs arrive. Snapshot restore and replay regenerate genuine contact calculations, so the confirmation frontier matters for stable event delivery.

Prediction replayed 181 ticks over 34 batches with a depth of at most 8; waiting replayed none. Response medians were 167.209–167.926 and 0.515–0.558 ms respectively across three repeats. The full rollback-frame p95 band was 10.529–11.572 ms. Size history for the accepted delivery delay and measure both the inner replay work and the affected whole frames. This evidence covers a local scripted delivery schedule and one deterministic contact model.
