---
id: K-GAME-TECH-SOUND
title: "Model distance, occlusion and room response separately"
summary: "Use attenuation curves for level, air-absorption filtering for timbre, spatialization for direction, and occlusion/reverb for obstruction and room response. One ray is only an occlusion approximation; full propagation/diffraction is another system."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["spatial","audio","Doppler","reverb","occlusion","attenuation","음향"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Model distance, occlusion and room response separately

## Guidance

Use attenuation curves for level, air-absorption filtering for timbre, spatialization for direction, and occlusion/reverb for obstruction and room response. Relative radial motion can drive Doppler pitch when appropriate. Author parameters around listener position, not necessarily the camera.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

One ray is only an occlusion approximation; full propagation/diffraction is another system. Pitch and filtering should preserve gameplay cue recognition. Doppler is a proposed physical transfer, not a verified setting in every cited game.

## Checks

Proposed: compare headphones/speakers, open/closed doors, listener/source motion, room transitions and many simultaneous voices.

## Evidence

- [Epic — Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine) — Official documentation; attenuation, air absorption, occlusion and reverb sends. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V22 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

