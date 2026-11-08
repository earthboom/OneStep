---
id: K-GAME-TECH-DDA
title: "Distinguish adaptive pacing from hidden outcome control"
summary: "Use observable performance proxies to choose bounded adjustments: spawn cadence, resources, recovery windows or opponent pace. Left 4 Dead's Director changes pacing and does not justify arbitrary enemy stat changes."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["DDA","rubber","banding","director","pacing","난이도"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Distinguish adaptive pacing from hidden outcome control

## Guidance

Use observable performance proxies to choose bounded adjustments: spawn cadence, resources, recovery windows or opponent pace. Separate player-selectable difficulty from dynamic pressure and from competition catch-up. Use hysteresis and cooldowns to avoid rapid oscillation.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Left 4 Dead's Director changes pacing and does not justify arbitrary enemy stat changes. Secretly changing competitive outcomes can undermine trust; no universal tuning coefficients are established.

## Checks

Proposed: log proxy, state, adjustment and reason; compare fixed/adaptive schedules and test manipulation and failure loops.

## Evidence

- [Mike Booth — The AI Systems of Left 4 Dead](https://cdn.fastly.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf) — 2009 developer slides; adaptive pacing, especially pp.79–92. Pacing is not equivalent to arbitrary difficulty scaling. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V41 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

