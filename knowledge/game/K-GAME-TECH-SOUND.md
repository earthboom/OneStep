---
id: K-GAME-TECH-SOUND
title: "Model distance, occlusion and room response separately"
summary: "Use attenuation curves for level, air-absorption filtering for timbre, spatialization for direction, and occlusion/reverb for obstruction and room response. One ray is only an occlusion approximation; full propagation/diffraction is another system."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["spatial", "audio", "Doppler", "reverb", "occlusion", "attenuation", "음향", "sound attenuation", "air absorption", "spatialization", "occlusion low-pass filter"]
status: active
checked_at: '2026-11-19'
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

**Sound attenuation** sets level by source–listener distance. **Air absorption** varies spectral filtering with distance, while spatialization supplies directional cues. Under Unreal's occlusion settings, a blocking trace can control both attenuation and low-pass filtering. Vary distance with line of sight unchanged, then add a wall at fixed distance to isolate the two effects. [Epic — Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)

## Checks

Proposed: compare headphones/speakers, open/closed doors, listener/source motion, room transitions and many simultaneous voices.

## Evidence

- [Epic — Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine) — Official documentation; attenuation, air absorption, occlusion and reverb sends. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V22 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

