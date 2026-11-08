---
id: K-GAME-TECH-IK
title: "Fit animation contacts with constrained inverse kinematics"
summary: "Trace the intended foot contact, place an effector and constrain knee direction with a pole/joint target. IK does not create a complete gait or correct unreachable targets automatically."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["IK","FABRIK","foot","placement","heel","retargeting","역운동학"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Fit animation contacts with constrained inverse kinematics

## Guidance

Trace the intended foot contact, place an effector and constrain knee direction with a pole/joint target. Transform all inputs into compatible coordinate spaces; offset pelvis if necessary and blend IK by gait phase. Use two-bone analytic solvers for limbs and iterative chains such as FABRIK where needed.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Implementation synthesis from Two Bone IK: query the support plane, construct the desired foot transform including shoe sole/heel offset, solve the leg with a stable knee target, and compensate pelvis/root only within allowed limits. Blend contact constraints by gait state so a swinging foot is not permanently pinned. If art uses shortened bones to preserve character height, separately validate reach, seated contacts and the unchanged gameplay capsule. A visual bone adjustment must not silently alter competitive hit geometry.

## Applicability and exceptions

IK does not create a complete gait or correct unreachable targets automatically. Heel height, skeleton proportions, interaction sockets and gameplay collision need an explicit contract; particular commercial games' shin-shortening claims remain unverified.

## Checks

Proposed: stairs, slopes, moving surfaces, sitting, hand contacts and extreme footwear; inspect foot sliding and knee flips.

## Evidence

- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine) — Official documentation; effector, joint target and coordinate spaces. Checked 2026-11-07, except items explicitly marked further reading.
- [Epic — FABRIK AnimBP Node](https://dev.epicgames.com/documentation/unreal-engine/fabrik-animation-blueprint-in-unreal-engine?lang=en-US) — Official documentation text; arbitrary-length chain and effector. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V08, V37 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine) — Effector, joint-target and coordinate-space contract; high-heel procedure is proposed transfer, not confirmation of specific commercial games. Checked 2026-11-07.
