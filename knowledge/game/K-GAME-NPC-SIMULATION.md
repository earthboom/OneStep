---
id: K-GAME-NPC-SIMULATION
title: "Select NPC decision models and preserve state beyond camera view"
summary: "Define what the player must observe, then choose a decision model and independent update levels for AI, collision, animation, rendering and replication. Transfer authority once when changing fidelity."
kind: method
scope: "Game NPC behavior, encounter coordination and simulation level of detail, including multiple observers."
keywords: ["NPC AI","Behavior Tree","FSM","GOAP","HTN","utility AI","simulation LOD","offscreen","blackboard","몬스터 AI","행동 트리","화면 밖 NPC","오프스크린","시뮬레이션 LOD","군중","상태 복원"]
status: active
checked_at: "2026-11-22"
---
# Select NPC decision models and preserve state beyond camera view

## Guidance

Trace sensing → remembered observation (time and expiry) → decision → action → result. Give a state machine entry, exit and interruption rules for explicit phases. Use a behavior tree for prioritized reusable paths, with defined running/success/failure results, Blackboard writers and abort cleanup. Utility selection needs comparable scores, tie-breaking and a retention threshold to avoid switching. Bound GOAP/HTN planning time, node count and replans. Provide fallback when a plan fails in the actual world.

Group decisions own scarce attack slots, spawns and seats. Navigation chooses a traversable route, local avoidance reacts to neighbors, and admission/yield rules resolve bottlenecks. Log candidate scores, plan failure or denied slots as appropriate so designers can explain what players saw.

Choose full update, reduced-frequency update, summary simulation or suspension according to threat, objective, last interaction and every relevant observer. Keep rendering, AI, collision, shadows, audio, animation, network relevance and residency independently adjustable. Use hysteresis or residence time to avoid thrashing. Transfer event/timer ownership once and bound catch-up work. Preserve stable ID, area, goal, arrival time, health, defeat and quest state where required.

## Applicability and exceptions

An offscreen pursuer can still collide, emit sound and affect combat. A door can remain part of navigation with drawing disabled. An incidental crowd may retain only density, while a named companion requires individual continuity. Mass LOD and Unity CullingGroup expose inputs or mechanisms. The game defines the promised outcomes.

## Checks

Interrupt an attack, expire a sound observation, block a path and contend for one slot. Leave during combat, return after a long absence, then repeat with a second observer still present. Compare full and summarized runs for promised quest/defeat outcomes, reaction latency, valid placement, duplicate attacks/spawns and catch-up hitches.

## Evidence

The November 22 development practices review drew on Halo 2, F.E.A.R., Left 4 Dead and S.T.A.L.K.E.R. developer accounts, planning and simulation research, and engine documentation. The cited team examples have different persistence needs. No local AI or offscreen route was run in that review.

[Crowd admission and avoidance](K-GAME-TECH-CROWD.md) · [Cooperative encounter direction](K-GAME-COOP-DIRECTOR.md)

- [Halo 2 behavior design](https://www.gamedeveloper.com/programming/gdc-2005-proceeding-handling-complexity-in-the-i-halo-2-i-ai) · [Analysis of planning in games](https://cdn.aaai.org/ojs/12728/12728-52-16245-1-2-20201228.pdf) · [Unreal StateTree](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-state-tree-in-unreal-engine) · [Iovino et al. literature review](https://arxiv.org/abs/2005.05842) · [Unreal BT](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview)
- [Unity Behavior graphs](https://docs.unity.cn/Packages/com.unity.behavior%401.0/manual/behavior-graph.html) · [Dave Mark and Kevin Dill, GDC 2010](https://media.gdcvault.com/gdc10/slides/MarkDill_ImprovingAIUtilityTheory.pdf) · [Orkin talk](https://gdcvault.com/play/1013459/Three-States-and-a-Plan) · [Valve talk video](https://www.gdcvault.com/play/1422/) · [Group control and encounter direction — Original presentation](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ReplayableCooperativeGameDesign_Left4Dead.pdf)
- [Recast and Detour source](https://github.com/recastnavigation/recastnavigation) · [ORCA paper and code](https://gamma-web.iacs.umd.edu/ORCA/) · [Unity AI Navigation](https://docs.unity.com/en-us/engine/6000.3/manual/packages-list/packages-all/pack-safe/com-unity-ai-navigation) · [Unreal AI Perception](https://dev.epicgames.com/documentation/en-us/unreal-engine/ai-perception-in-unreal-engine)
- [Carlson and Hodgins, 1997](https://graphicsinterface.org/proceedings/gi1997/gi1997-1/) · [Unreal Mass Gameplay](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-gameplay-in-unreal-engine) · [Chenney, GDC 2001](https://pages.cs.wisc.edu/~schenney/research/culling/chenney-gdc2001.pdf) · [Epic Significance Manager](https://dev.epicgames.com/documentation/unreal-engine/significance-manager-in-unreal-engine) · [S.T.A.L.K.E.R. developer interview](https://www.gamedeveloper.com/game-platforms/interview-inside-the-ai-of-i-s-t-a-l-k-e-r-i-)
- [O’Sullivan et al., 2002 — Paper](https://secom.ru.is/publications/CGF2002.pdf) · [Assassin’s Creed Unity — GDC session](https://www.gdcvault.com/play/1022411/massive-crowd-on-assassin-s) · [Assassin’s Creed Unity — Video](https://www.youtube.com/watch?v=Rz2cNWVLncI) · [Animation Budget Allocator](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-budget-allocator-in-unreal-engine) · [Unity CullingGroup](https://docs.unity.com/en-us/engine/6000.5/manual/cameras/occlusion-culling/culling-group-api/api)
- [AnimatorCullingMode](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/animatorcullingmode)
