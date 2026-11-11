---
id: K-GAME-TECH-TRACE
title: Combine distance, angle and collision queries for perception
summary: For unit forward f and direction d, the cone test is dot(f,d)>=cos(halfFOV).
  The [-1,1] dot-product range requires normalized vectors.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
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
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 center-point vision:24model,132actual PIE cases30/60/144,3paired
    package query/frame observations and normal-speed native media; no broader AI/Lambert
    validation
---
# Combine distance, angle and collision queries for perception

## Guidance

For unit forward f and direction d, the cone test is dot(f,d)>=cos(halfFOV). Reject by distance first, then angle, then trace for occlusion. Handle zero-length directions and decide whether to project onto the ground plane. Trace channels, ignored actors, simple/complex collision and multi-point targets determine what visible means.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

The [-1,1] dot-product range requires normalized vectors. Angle inclusion alone does not prove visibility. Lambert diffuse max(0,n dot l) is a separate shading use of the same operation.

## Checks

Proposed: targets behind thin cover, at cone edges and at identical positions; draw traces and normals.

## Evidence

- [Epic — EQS Node Reference: Tests](https://dev.epicgames.com/documentation/unreal-engine/eqs-node-reference-tests-in-unreal-engine?lang=en-US) — Official documentation; Distance, Dot and Trace. Checked 2026-11-07, except items explicitly marked further reading.
- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US) — Official worked example; dot, distance and line-of-sight target filtering. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V18, V38 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Local Unreal center-point perception — 2026-11-11

[Native vision results](../../prototypes/UnrealTechniqueLab/VISION-RESULTS.md) implement a known-candidate3D cone/range plus simple Visibility first-hit target rule. One observer/target/wall, range1000cm/full90° are experiment settings. Normalize vectors; reject coincidence/zero/nonfinite input; numerical guards1e-8cm and dot1e-12 are not gameplay forgiveness. Skip distance failures before computing angle (dotComputed=false is unavailable). Ignore the observer actor including its forward test component. A no-hit query is not target detection. This is center-point line of sight, not whole-body exposure, brightness, target selection or memory.

Model24 and six actual UE5.8.3 PIE worlds (reference/gated × observed30/60/144,132cases) verify exact range/cone policy boundaries, rear/elevation, wall/near-corner blocked/tangent/clear, configured.1cm thin wall, wall beyond target, channel filters, self-ignore and an owner-block sensitivity control. The exact tangent's first-hit coordinates are retained; contact results near edges remain backend/precision-sensitive. Pilot and final-source evidence are distinct. Observed rate and actual PIE viewport are checked; standalone1280x720 performance is a separate consumer.

Three same-source package pairs use one target and identical scripted candidate poses,2s warmup+10s measured. Reference issues one ray per valid candidate; early gating issues rays only for eligible candidates (about25%in this workload), with identical detection rules. Report phase/evaluation/query counts and denominators. This supports early rejection, not a general frame-rate speedup, multi-NPC budget or production scalability. Geometry/query microtimers exclude earlier scripted transform changes and later rendering; whole-frame/cadence records retain those costs. Normal-speed native video and screenshots are separate from measurement. No patrol,pursuit,combat,EQS,renderer,Present,save or framework optimization.

EQS documentation is a conceptual source; its rolling page returned5.9 on this check. Installed5.8.3 World.h/CollisionQueryParams and actual5.8.3 execution establish this local API contract. Lambert lighting, skeletal/complex collision, other origin-overlap policies, multiplayer authority and multi-point visibility remain untested.
