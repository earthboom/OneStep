---
id: K-GAME-TECH-SPEED
title: "Use speed effects without hiding actionable information"
summary: "Coordinate FOV changes, camera offset/lag and velocity-based blur with acceleration events. Motion blur does not restore lost input responsiveness or actual frames."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["FOV","motion","blur","speed","camera","속도감"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Use speed effects without hiding actionable information

## Guidance

Coordinate FOV changes, camera offset/lag and velocity-based blur with acceleration events. Separate base framing from effects so changing visual intensity does not alter aiming or movement rules. Depth-based camera-motion blur reconstructs pixel motion from view transforms; moving objects need additional motion information.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Motion blur does not restore lost input responsiveness or actual frames. Large FOV shifts and forced camera motion may impair comfort and target reading.

## Checks

Proposed: compare disabled/reduced/full effects in actual driving or traversal tasks, including accessibility preferences.

## Evidence

- [Gilberto Rosado — Motion Blur as a Post-Processing Effect](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-27-motion-blur-post-processing-effect) — GPU Gems 3 ch.27; depth reconstruction and velocity sampling. Checked 2026-11-07, except items explicitly marked further reading.
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 2015 creator-authored article; camera-window, framing and smoothing. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V06 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

