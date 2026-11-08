---
id: K-GAME-TECH-TRACE
title: "Combine distance, angle and collision queries for perception"
summary: "For unit forward f and direction d, the cone test is dot(f,d)>=cos(halfFOV). The [-1,1] dot-product range requires normalized vectors."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["dot","product","raycast","FOV","Lambert","perception","내적","시야"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
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

