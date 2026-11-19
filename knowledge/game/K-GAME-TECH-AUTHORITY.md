---
id: K-GAME-TECH-AUTHORITY
title: Combine server authority with bounded client prediction
summary: Keep input intent, server acknowledgement and visual prediction distinct.
  Local Unreal RPC tests verify ordered pending replay and final convergence under
  emulated delay and loss.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- server
- authority
- prediction
- reconciliation
- netcode
- 서버권한
- client-side prediction
- server reconciliation
- authoritative server
- acknowledged input
- unacknowledged input replay
- movement correction
- packet simulation
- 서버 보정
- 서버 확정 대기
- 미확인 입력 재적용
- 네트워크 에뮬레이션
status: active
checked_at: '2026-11-20'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V04 UE 5.8.3 listen server plus separate local client. Wait/predict
    over Unreal UDP and a bounded 20 Hz motion model. Native outgoing 60 ms and 10%
    loss, six frame-cost runs with exact suffix and final-state evidence.
---
# Combine server authority with bounded client prediction

## Guidance

Send player intent to an authoritative simulation; validate it rather than trusting claimed outcomes. Predict latency-sensitive local actions, reconcile against acknowledged server state, then reapply unacknowledged inputs where the movement model supports it. Keep cosmetic smoothing separate from authoritative collision.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Authority reduces some cheats; it does not prevent all cheating. Never grant rewards because a predicted animation played. Current Riot service rates are not adopted as general requirements.

With **client-side prediction**, the player sees a locally simulated input before the authoritative server confirms its result. **Server reconciliation** corrects the local simulation at the acknowledged input and replays newer pending inputs. In a movement system that can replay inputs, force a correction while newer inputs are still pending and check that each pending input affects the resulting state exactly once. [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode)

## Checks

Proposed: inject loss, jitter and invalid inputs; log input sequence, acknowledgement, correction magnitude and authoritative rewards.

## Evidence

- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode) — 2020 developer account; server authority, prediction and server combat resolution; historical implementation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V04 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Unreal listen-server prediction and reconciliation — 2026-11-20

The local V04 experiment compared waiting and prediction with a separate client and listen server on loopback, sending a shared 20 Hz input sequence via Unreal UDP. Each peer uses 60 ms outgoing lag and 10% loss. The server commits each of the 180 steps once. Both server changes produce the prescribed 48 cm and 64 cm corrections. The replay list is exactly the pending suffix after the acknowledgement. Each run drains to 0 cm final position error.

Input-response median ranges were 145.236–153.142 ms for waiting and 0.498–0.644 ms for prediction across three runs. Client whole-frame p95 was 10.362–11.322 and 10.556–10.673 ms. Use the engine-visible response definition, watch queue depth and measure final convergence independently of transient pose error. This fixture establishes the owned movement contract for one local link with bounded loss and a simple planar motion model.
