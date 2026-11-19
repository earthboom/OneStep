---
id: K-GAME-TECH-LAGCOMP
title: Bound historical hit resolution for latency compensation
summary: Resolve eligible shots against a bounded, timestamped history. Compare client-view
  agreement, cover exposure and the live collision query before and after a historical
  lookup.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- lag
- compensation
- rewind
- hit
- registration
- 렉보상
- 판정불일치
- 서버되감기
- 지연보상
- lag compensation
- server rewind
- interpolation delay
- cover entry
- history gap
- historical collision
- rewind cap
- 엄폐 진입
- 기록 누락
- 되감기 상한
status: active
checked_at: '2026-11-20'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V28 UE5.8.3 listen server plus remote local client. Current/rewind
    timing with fixed UDP emulation and matched processing ticks. Static cover, one
    historical box and an 8-tick cap.
---
# Bound historical hit resolution for latency compensation

## Guidance

Retain timestamped collision history and resolve eligible shots against a bounded reconstructed past view. Account for clock mapping and interpolation delay. Keep the authoritative current world distinct from temporary historical queries.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Rewinding benefits a shooter's historical view but can hurt a player who has reached cover. 'People always prefer this' is not established; choose fairness rules and maximum rewind explicitly.

With **server rewind**, an authoritative game evaluates an eligible input against stored historical collision poses. The target time depends on how client time maps to server time and how far the displayed remote state lagged behind. Clamp it to available history, choose a missing-history policy, and verify the live collision world is unchanged after a historical query. Riot's account supplies a game-specific example of the latency tradeoff. [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode)

## Checks

Proposed: record both client views and server history for cover transitions, fast targets and asymmetric latency.

## Evidence

- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode) — 2020 developer account; server authority, prediction and server combat resolution; historical implementation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V28 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Unreal listen-server rewind — 2026-11-20

The local V28 experiment used one moving box, fixed cover, a separate client, 60 ms outbound emulation in both directions and matched server decision ticks. Across three repetitions per profile, all-offered client-view agreement was 12/36 current and 28/36 rewind. Rewind agreed on all 28 evaluated shots, rejected the four out-of-range and four missing-sample requests, and accepted eight hits at 50 or 200 ms after entering cover. Both profiles suppressed four duplicates and preserved current collision in 40 before/after checks per session.

Active decision p95 ranged from 2.200–2.500 µs for current and 3.500–14.600 µs for rewind. Host whole-frame p95 was 29.605–29.934 ms and 29.570–29.656 ms respectively. Client whole-frame p95 was 8.551–9.017 ms and 8.602–9.134 ms.

Map requests to the exact displayed pose time, then apply an explicit age limit and missing-history disposition. For fixed occluders, cap the historical geometry query at the first static hit. Use distinct collision representations so a historical query cannot change current collisions. Count explicit refusals in the all-offered rate and record time behind cover as a separate outcome. Measure decision work along with server and client frames. The 400 ms limit, exact sample matching and one-box result belong to this workload. A game with moving occluders or skeletal collision needs its own history representation and policy.
