---
id: K-GAME-TECH-AUTHORITY
title: "Combine server authority with bounded client prediction"
summary: "Send player intent to an authoritative simulation; validate it rather than trusting claimed outcomes. Authority reduces some cheats; it does not prevent all cheating."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["server","authority","prediction","reconciliation","netcode","서버권한"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Combine server authority with bounded client prediction

## Guidance

Send player intent to an authoritative simulation; validate it rather than trusting claimed outcomes. Predict latency-sensitive local actions, reconcile against acknowledged server state, then reapply unacknowledged inputs where the movement model supports it. Keep cosmetic smoothing separate from authoritative collision.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Authority reduces some cheats; it does not prevent all cheating. Never grant rewards because a predicted animation played. Current Riot service rates are not adopted as general requirements.

## Checks

Proposed: inject loss, jitter and invalid inputs; log input sequence, acknowledgement, correction magnitude and authoritative rewards.

## Evidence

- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode) — 2020 developer account; server authority, prediction and server combat resolution; historical implementation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V04 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

