---
id: K-GAME-TECH-BLEND
title: "Choose blend operations in the correct colour space"
summary: "Straight alpha: C=alpha*S+(1-alpha)*D. Blend mode affects sorting, depth writes and supported lighting."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["alpha","additive","modulate","blending","블렌딩"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Choose blend operations in the correct colour space

## Guidance

Straight alpha: C=alpha*S+(1-alpha)*D. Additive commonly accumulates S over D; modulate multiplies them. Use linear-light calculations and distinguish premultiplied from straight-alpha assets. Masked materials discard pixels rather than continuously blending them.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Blend mode affects sorting, depth writes and supported lighting. Adding colour does not make effects readable on all backgrounds.

## Checks

Proposed: inspect bright/dark backgrounds, overlapping particles and sprite edges; compare blend equations with imported texture data.

## Evidence

- [Epic — Material Blend Modes](https://dev.epicgames.com/documentation/en-us/unreal-engine/material-blend-modes-in-unreal-engine) — Official documentation; masked, translucent, additive and modulate modes. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V45 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

