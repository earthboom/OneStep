---
id: K-GAME-TECH-HITSCAN
title: "Resolve hitscan from aiming intent and muzzle constraints"
summary: "Use hitscan for effectively instantaneous weapon travel. A camera-only trace can permit head-glitch shots; a muzzle-only trace can disagree with the crosshair at close range."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["hitscan","muzzle","crosshair","head","glitch","히트스캔"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Static-box cover and origin guards validated with native Unity 6000.0.77f1 physics in Windows Mono prototype; network authority and moving poses untested"
---
# Resolve hitscan from aiming intent and muzzle constraints

## Guidance

Use hitscan for effectively instantaneous weapon travel. Find the camera aim point, then validate a muzzle-to-aim trace with consistent collision filtering and authoritative rules. Keep the rendered tracer cosmetic if it does not simulate a projectile. Choose projectile simulation when travel time/drop matters.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Local engine evidence — 2026-11-07

[Technique Lab](../../prototypes/TechniqueLab/RESULTS.md) reproduced a camera-only hit through offset muzzle cover, then rejected it using actual Unity colliders. It also passed open-path, inside-muzzle, root-to-muzzle wall, layer and trigger checks in final PlayMode and three Windows Mono players. An origin inside a collider needs explicit handling: Unity's 3D raycast does not detect that containing collider. This fixture uses small world-layer sphere overlaps at muzzle/root, a root-to-muzzle obstruction ray, then a first-hit muzzle ray toward camera intent. Adapt overlap size, collision ownership and authoritative pose rules to the actual weapon; the fixture's 0.025 radius is not a general setting.

For 1,024 repeated shot resolutions at a static pose, safe closed/open medians were 0.932–1.104 ms across three players, versus 0.274–0.349 ms for camera-only. Safe open/closed uses five native queries (camera ray, two overlaps, root path and muzzle ray); inside-muzzle rejection uses two. The cheaper camera-only rule is deliberately incorrect behind this cover. Include the additional queries in the budget; these CPU batch-throughput values do not measure individual-shot latency, an entire frame, complex moving scenes or server performance.

## Applicability and exceptions

A camera-only trace can permit head-glitch shots; a muzzle-only trace can disagree with the crosshair at close range. The cited sources support trace/authority mechanisms, not every named shooter's current implementation.

## Checks

Proposed: muzzle against a wall, close targets, animation pose changes and asymmetric latency; compare server and client hit logs.

Executed subset: static box fixtures for wall/open/inside/beyond-wall origins, explicit layer/trigger filtering and scene control transitions. Close-range aiming policy, animated meshes, self-collision exclusions, moving collider synchronization, latency and server/client logs remain project checks.

## Evidence

- [Epic — EQS Node Reference: Tests](https://dev.epicgames.com/documentation/unreal-engine/eqs-node-reference-tests-in-unreal-engine?lang=en-US) — Official documentation; Distance, Dot and Trace. Checked 2026-11-07, except items explicitly marked further reading.
- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode) — 2020 developer account; server authority, prediction and server combat resolution; historical implementation. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V39 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.
- [Unity 6000.0 — Physics.Raycast](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/physics/raycast), Remarks: containing-collider origin limitation and explicit layer/trigger filtering; inspected 2026-11-07. This is the Unity 3D contract, not a blanket claim about other engines or Physics2D.
- Local experiment: [results and conditions](../../prototypes/TechniqueLab/RESULTS.md), [resolver](../../prototypes/TechniqueLab/Assets/TechniqueLab/ShotResolver.cs), [checks](../../prototypes/TechniqueLab/Assets/TechniqueLab/LabChecks.cs), [raw player example](../../prototypes/TechniqueLab/Results/player-run-1.json) (`shot.*`, `consumer.*` and native query counts).

