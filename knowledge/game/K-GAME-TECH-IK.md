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
checked_at: '2026-11-21'
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

## V08 footwear calibration on static supports — 2026-11-21

Define heel and toe outsole samples in the neutral shoe frame. Convert the ankle offset and shoe pitch to the solver's bone space. Find a compatible support plane and latch the contact during stance. Align the shoe frame to the plane and solve the leg to the resulting ankle target. Use shoe-specific calibration when the outsole position or rest pitch changes. Release the anchor when support is lost or the leg cannot reach within the pelvis limit. Keep the gameplay capsule independent of the visual correction.

The UE 5.8.3 Win64 Development trial used one 68-bone mannequin, one source walk cycle, rigid flat-shoe and high-heel test shapes, an 8-degree ramp and an 8 cm step. The heel used a 21-degree pitch calibration. Both profiles rendered the same geometry and evaluated the same authored samples. The comparison used the common flat calibration or the shoe-specific calibration in the same Two Bone IK solver. The 60 Hz sample clock controls the input sequence. Native frame cadence is measured independently.

Over 32 profile/scenario combinations, the high heel's maximum full-stance lift and penetration with the common reference were 2.104 cm and 5.896 cm. Both fell below 0.001 cm with shoe calibration. Flat-shoe full-stance errors stayed below 0.001 cm with either profile. Measured stance drift was zero. Both profiles released the planted anchors after support removal and refused the deep unreachable targets. A pre/post capsule sweep matched on all 3,072 behavior frames across the two profiles.

Evaluate walking in stance, transitions and swing separately. The tuned high heel still showed 8.322 cm maximum outsole penetration in a transition and 14.622 cm in swing. The tuned flat shoe reached 9.901 cm in swing. These peaks came from the sampled shoe contacts in the scripted walk. Stance calibration is suitable for contact fitting when the source animation and its transitions already provide the required swing clearance.

Three same-workload runs per profile measured 1,408 frames each at 1280×720 DX11. The observed p95 ranges were as follows, in milliseconds.

| Profile | IK | Pose publication and shoe transforms | Whole frame |
| --- | ---: | ---: | ---: |
| Common | 0.0405–0.0474 | 0.0138–0.0150 | 10.109–10.318 |
| Shoe-specific | 0.0441–0.0474 | 0.0142–0.0159 | 10.005–10.182 |

Use these costs for the measured single-character scene. Repeat footwear calibration, pose reach and swing clearance checks for each production rig, shoe and gait.
