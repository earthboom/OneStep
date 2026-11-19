---
id: K-GAME-TECH-HITSCAN
title: Resolve hitscan from aiming intent and muzzle constraints
summary: Resolve an instantaneous game hit against the selected aiming point and the actual origin's
  unobstructed path. Define starting overlaps and ownership filtering.
kind: reference
scope: Game development. For Unreal object-type queries, `UWorld::LineTraceSingleByObjectType` casts
  a segment against selected object types.
keywords:
- hitscan
- muzzle
- crosshair
- head
- glitch
- 히트스캔
- Unreal
- 언리얼
- UWorld::LineTraceSingleByObjectType
- UWorld::OverlapAnyTestByObjectType
- Physics.Raycast
status: active
checked_at: '2026-11-19'
---
# Resolve hitscan from aiming intent and muzzle constraints

## Guidance

In a game with an offset third-person camera, the camera ray chooses aim intent. Query the path from the in-game emitter to that point against the gameplay collision world. A camera peeking past cover can see a target while the emitter remains obstructed. Define whether a blocked or initially embedded origin cancels the action. Cosmetic tracers can display the resolved result.

## Applicability and exceptions

For Unreal object-type queries, `UWorld::LineTraceSingleByObjectType` casts a segment against selected object types. `UWorld::OverlapAnyTestByObjectType` checks whether a shape already overlaps a selected type at a pose. Configure ownership, object filters and the authoritative pose consistently. In Unity 3D, `Physics.Raycast` misses the collider containing its origin, so an overlap test can be needed there.

## Checks

Compare unobstructed and occluded poses, an emitter inside geometry, a body-to-emitter path crossing cover, ignored owner and obstacles beyond the intended endpoint. Exercise actual collision responses and authoritative animation timing in the target game.

## Evidence

Epic and Unity document the respective query APIs. Riot describes server-side decisions in VALORANT. Earlier simple static collider checks in Unity and Unreal exposed camera-only false positives. Animated targets, latency and server reconciliation were outside those checks.

- [Unity 6000.0 — Physics.Raycast](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/physics/raycast)
- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode)
- [Epic — UWorld object-type queries](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UWorld?application_version=5.8)
