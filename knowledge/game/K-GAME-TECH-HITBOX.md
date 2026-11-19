---
id: K-GAME-TECH-HITBOX
title: Keep attack, hurt and physical collision contracts distinct
summary: Clip collision queries to the attack's active time and process eligible touches once per attack
  and target, even if the sweep encounters no blocking hit.
kind: reference
scope: Game development. In Unreal Engine, `UWorld::SweepMultiByChannel` collects touches up to the
  nearest blocker on the selected channel.
keywords:
- hitbox
- hurtbox
- hitstop
- collision
- 피격
- attack window
- sphere sweep
- active clipping
- duplicate damage
- attack identity
- hurt capsule
- blocking status
- 히트박스
- 허트박스
- 중복 피격
- 고속 통과
- 공격 활성 구간
- UWorld::SweepMultiByChannel
- FHitResult
status: active
checked_at: '2026-11-19'
---
# Keep attack, hurt and physical collision contracts distinct

## Guidance

A hitbox describes an active attack volume, a hurtbox describes a damage-receiving region, and movement collision constrains the character body. Give an attack its own identity and keep a set of already affected targets for that activation. For fast linear motion sweep the previous-to-current volume only over the part of the update interval where the attack is active. Test initial overlap explicitly where the rules permit it.

## Applicability and exceptions

In Unreal Engine, `UWorld::SweepMultiByChannel` collects touches up to the nearest blocker on the selected channel. Its Boolean return indicates a blocking hit. Inspect the `FHitResult` array even when the Boolean is false, since touch-only results can still be relevant. A straight sphere sweep approximates only a linear trajectory. Rotating limbs or moving targets may require additional sampling.

## Checks

Check a complete crossing between frames, just-before/open/close boundaries, a wall preceding a hurtbox, an owner touch and repeated hits from one activation. Verify the touch-only case independently. For hitstop, specify which clocks pause and whether input buffering continues.

## Evidence

Epic documents the query contract and collision responses. Thorson describes collision and forgiveness in specific games. Prior Unreal observations covered linear sphere paths and static upright targets. They do not establish animation-driven contact, hitstop, networking or combat feel.

- [Epic SweepMultiByChannel](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/Engine/UWorld/SweepMultiByChannel?application_version=5.5)
- [collision response reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/collision-response-reference-in-unreal-engine)
- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html)
