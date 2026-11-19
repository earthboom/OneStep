---
id: K-GAME-TECH-IK
title: Fit animation contacts with constrained inverse kinematics
summary: Solve a visual leg toward a calibrated sole contact, respecting reach, joint direction, coordinate
  spaces and gait phase before applying pelvis compensation.
kind: reference
scope: Game development. For static supports, latch a stance contact and release it during swing.
keywords:
- IK
- FABRIK
- foot
- placement
- heel
- retargeting
- 역운동학
- static support
- sole anchor
- pelvis budget
- half blend
- previous bone buffer
- PoseableMesh
- three point support
- swing release
- 발 고정
- 골반 보정
- 계단
- 접지
- Two Bone IK
- Joint Target Location
- UPoseableMeshComponent
- effector
status: active
checked_at: '2026-11-19'
---
# Fit animation contacts with constrained inverse kinematics

## Guidance

Inverse kinematics (IK) solves joint transforms for a desired endpoint or effector. Unreal's Two Bone IK uses a three-joint limb and a Joint Target Location to guide the bend. FABRIK iteratively reaches backward and forward through a chain, with a precision goal and iteration budget. Express the effector, pole and support plane in the solver's declared spaces. Offset the ankle by the calibrated sole or shoe geometry.

## Applicability and exceptions

For static supports, latch a stance contact and release it during swing. Blend from the source pose, then solve pelvis displacement against that blended endpoint and both legs' reach. Fall back if a compatible pelvis shift does not exist. `UPoseableMeshComponent` allows bone-space or component/world pose operations according to the API used. Specify the supported space for each operation. Keep visual contact independent of the gameplay capsule.

## Checks

Compare source and final skinned poses on flat ground, stairs, conflicting contacts, mid-blend, unreachable supports and swing release. Verify heel/toe penetration, knee continuity, previous-frame pose history and unchanged gameplay collision.

## Evidence

Epic documents the solve controls and poseable mesh APIs. Prior Unreal observations covered a static support, calibrated sampling and reach rejection for a skinned biped. Commercial footwear rigs, moving supports, retargeting and a production animation graph were outside that observation.

- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine)
- [Epic — FABRIK AnimBP Node](https://dev.epicgames.com/documentation/unreal-engine/fabrik-animation-blueprint-in-unreal-engine?lang=en-US)
- [Epic — UPoseableMeshComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UPoseableMeshComponent?application_version=5.8)
