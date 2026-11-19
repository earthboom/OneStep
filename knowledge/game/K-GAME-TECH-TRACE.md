---
id: K-GAME-TECH-TRACE
title: Combine distance, angle and collision queries for perception
summary: Reject distant or out-of-cone targets before querying occlusion. Define which target point,
  collision channel and hit identity constitute visibility.
kind: reference
scope: Game development. For collision-based Unreal perception, `UWorld::LineTraceSingleByChannel` reports
  the first blocking hit on a channel.
keywords:
- dot
- product
- raycast
- FOV
- Lambert
- perception
- 내적
- 시야
- occlusion
- owner ignored
- center point
- thin wall
- corner tangent
- 시야각
- 가림 판정
- 자기 자신 제외
- UWorld::LineTraceSingleByChannel
- FCollisionQueryParams::AddIgnoredActor
- EQS
status: active
checked_at: '2026-11-19'
---
# Combine distance, angle and collision queries for perception

## Guidance

For unit forward f and unit direction d to the sample, `dot(f,d) >= cos(halfFOV)` includes the cone boundary. Test squared range first and handle a coincident point before normalizing. A horizontal cone projects both vectors onto the ground plane, whereas a 3D cone also limits elevation. The Lambert cosine term in diffuse lighting uses a surface normal and light direction and answers a different question.

## Applicability and exceptions

For collision-based Unreal perception, `UWorld::LineTraceSingleByChannel` reports the first blocking hit on a channel. Configure `FCollisionQueryParams::AddIgnoredActor` to skip the observer. A trace that expects to hit the target requires its component to block that channel. A clear-to-point test instead allows a clear segment even if the endpoint has no collider.

## Checks

Place a target on the cone edge, directly above, behind a thin wall and partly exposed. Test the observer's own collider, no-hit results, target replacement and multiple sample points. Cross-check angular boundary values against known directions.

## Evidence

Epic's EQS documentation describes Distance, Dot and Trace tests. Earlier Unreal checks covered one known target point and simple first-hit visibility. Multi-point actors, animated meshes and gameplay perception remain separate questions.

- [Epic — EQS Node Reference: Tests](https://dev.epicgames.com/documentation/unreal-engine/eqs-node-reference-tests-in-unreal-engine?lang=en-US)
- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US)
- [Epic — UWorld](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorld?application_version=5.8)
- [Epic — AddIgnoredActor](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/FCollisionQueryParams/AddIgnoredActor?lang=en-US)
