---
id: K-GAME-TECH-LAGCOMP
title: "Bound historical hit resolution for latency compensation"
summary: "Retain timestamped collision history and resolve eligible shots against a bounded reconstructed past view. Rewinding benefits a shooter's historical view but can hurt a player who has reached cover."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["lag","compensation","rewind","hit","registration","렉보상","판정불일치","서버되감기","지연보상"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Bound historical hit resolution for latency compensation

## Guidance

Retain timestamped collision history and resolve eligible shots against a bounded reconstructed past view. Account for clock mapping and interpolation delay. Keep the authoritative current world distinct from temporary historical queries.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Rewinding benefits a shooter's historical view but can hurt a player who has reached cover. 'People always prefer this' is not established; choose fairness rules and maximum rewind explicitly.

## Checks

Proposed: record both client views and server history for cover transitions, fast targets and asymmetric latency.

## Evidence

- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode) — 2020 developer account; server authority, prediction and server combat resolution; historical implementation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V28 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

