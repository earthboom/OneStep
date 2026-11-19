---
id: K-GAME-TECH-LOCKON
title: Select stable lock-on targets before changing movement framing
summary: Acquire a target under explicit visibility and scoring rules. Keep a valid selection until
  its release condition occurs or the player requests a switch.
kind: reference
scope: Game development. For Unreal object lifetimes, `TWeakObjectPtr` holds a non-owning object reference.
keywords:
- lock-on
- target
- scoring
- Z
- targeting
- 락온
- hysteresis
- sticky target
- retention band
- weak actor identity
- same ID replacement
- opposite held keys
- target switching
- 대상 전환
- 타깃 유지
- TWeakObjectPtr
- Z-targeting
- line of sight
status: active
checked_at: '2026-11-19'
---
# Select stable lock-on targets before changing movement framing

## Guidance

Filter candidates by range, view cone and line of sight, then score the survivors for acquisition. Hysteresis uses a wider exit band than entry band to suppress boundary jitter. Retaining the current selection avoids changing target whenever two scores cross. Define deterministic ties, switch order and whether occlusion allows grace. Distinguish angular centering from distance in projected screen pixels.

## Applicability and exceptions

For Unreal object lifetimes, `TWeakObjectPtr` holds a non-owning object reference. Test validity before use so a destroyed actor cannot pass selection to a replacement sharing a gameplay ID. Evaluate press edges separately from held directions. Character facing, camera orbit and attack decisions can then consume the selected identity independently.

## Checks

Cross two targets near the aiming center, oscillate at entry and exit boundaries, destroy and replace the selected actor, occlude it, and hold both switch directions. Log selected identity before and after each change. Check physical input and camera comfort in play.

## Evidence

Nintendo's staff interview describes Z-targeting feedback and Navi. Epic's example shows target filtering. Earlier scripted Unreal checks covered selection continuity, switching and actor replacement in a fixed view. They do not validate camera feel or Nintendo's implementation details.

- [Nintendo — Where the Name Navi Came From](https://iwataasks.nintendo.com/interviews/3ds/zelda-ocarina-of-time/1/3/)
- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US)
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers)
- [Epic — Object Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine)
