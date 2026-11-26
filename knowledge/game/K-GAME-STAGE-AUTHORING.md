---
id: K-GAME-STAGE-AUTHORING
title: "Add stages through a stable catalog, runner and progression contract"
summary: "Separate stage identity, mutable play state, campaign order and permanent results. Use one runner for editor preview and shipped menu entry, then validate the stage in a target build."
kind: method
scope: "Authored puzzle boards, platform rooms, wave encounters, tactical missions and race courses."
keywords: ["stage authoring","stage catalog","StageId","progression","checkpoint","content extension","스테이지 추가","스테이지 제작","레벨 에디터","스테이지 프레임워크","해금","진행 순서","체크포인트"]
status: active
checked_at: "2026-11-22"
---
# Add stages through a stable catalog, runner and progression contract

## Guidance

Follow selection → entry → fail/retry or complete → next stage. A definition owns the stable StageId, board or map, rule references and authored settings. A catalog resolves IDs for the distribution target. Progression chooses order, chapters and prerequisites from confirmed results. A runner owns loading, initialization, retry, exit and release. A session owns the mutable board, waves and timers. Saves own confirmed IDs and scores. These can share a module in a small game.

Start preview and normal menu play with the same input validation, initialization and outcome logic. Preview may bypass unlocks and save into a test profile. When replacing an asynchronous load, release late results and prevent writes into the new session. Let content reference shared rules. Campaign ordering belongs in progression and creates no asset dependency between otherwise independent stages.

Issue an ID, author from a template, diagnose missing markers in place, register and validate the shipping catalog, then enter the stage through the real build. Board/rule variation can use a shared Scene/Map plus definitions. Spatial variation in lighting, collision and placements often belongs to a scene or map. In Unity inspect serialized dependencies and shipped Addressables. In Unreal inspect map/asset dependencies and cooking. Add a rule only when existing rules cannot express the feature.

## Applicability and exceptions

A structural check proves neither solvability nor the intended learning sequence. A known solution witnesses one route. Fair record comparison, alternate puzzle solutions, readable objectives and appropriate retry pacing need their own checks. Cooperative outcomes require the game's designated authority. Retain stage/rule revision or hash for mid-stage saves and ghosts when compatibility depends on content.

## Checks

Replay warehouse-03 through the real push rules, then reorder it and read old completion history. For a platform room reach the exit and respawn at the correct checkpoint. Interrupt a wave and re-enter without stale enemies or timers. On a tactical map swap objectives without sharing mission state. Finish quarry-loop in the target vehicle, then skip checkpoints and drive backward. Test optional packs independently, missing references, duplicate IDs and old records after revision. Measure time and shared-file edits for two representative stages and one new rule.

## Evidence

The November 22 stage framework survey drew on Tanagra and puzzle-generation/learning research, Pig Eat Ball, Celeste, Unpacking, Bethesda modular kits, Trackmania validation, Bungie builds and Factorio migrations. Creator presentations describe each production. The named boards and routes illustrate proposed tests.

[Content formats](K-GAME-CONTENT-FORMATS.md) · [Gameplay regression](K-GAME-GAMEPLAY-REGRESSION.md) · [Level design](K-GAME-TECH-LEVEL.md)

- [FDG paper](https://pcgworkshop.com/archive/dormans2010adventures.pdf) · [IEEE author manuscript](https://sander.landofsand.com/publications/Dormans_Bakkes_-_Generating_Missions_and_Spaces_for_Adaptable_Play_Experiences.pdf) · [AAAI paper](https://cdn.aaai.org/ojs/12379/12379-52-15907-1-2-20201228.pdf) · [Taylor and Parberry paper](https://ianparberry.com/techreports/LARC-2011-01.pdf) · [Kartal et al. paper](https://cdn.aaai.org/ojs/12859/12859-52-16375-1-2-20201228.pdf)
- [Butler et al., CHI 2015 — Authors' paper](https://www.ericbutler.net/assets/papers/chi2015_progression.pdf) · [GDC video](https://gdcvault.com/play/1025182/Level-Design-Workshop-Set-this) · [Nathan Fouts, Pig Eat Ball, GDC 2018 — Talk slides](https://media.gdcvault.com/gdc2018/presentations/Fouts_Nathan_SetThisGame.pdf) · [GDC video](https://www.gdcvault.com/play/1024307/The-Gamer-s-Brain-How) · [Witch Beam, Unpacking, GCAP 2023 — Developer talk](https://youtu.be/2j7AJj1oRSQ)
- [Session and video segments](https://confpad.io/conferences/gcap-2023-empower/empowering-design-the-tools-and-pipelines-of-unpacking) · [Text of the developers' GDC talk](https://www.gamedeveloper.com/design/skyrim-s-modular-approach-to-level-design) · [Fallout 4 GDC video](https://www.gdcvault.com/play/1022930/-Fallout-4-s-Modular) · [Map submission documentation](https://doc.trackmania.com/create/map-review/submit-your-map-to-map-review/) · [Validation runs and review guidelines](https://doc.trackmania.com/create/map-review/weekly-grands-guidelines/)
- [Bungie talk](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Official Factorio migration documentation](https://lua-api.factorio.com/latest/auxiliary/migrations.html)
- [Tiled templates](https://doc.mapeditor.org/en/latest/manual/using-templates/) · [Tiled JSON format](https://doc.mapeditor.org/en/stable/reference/json-map-format/) · [LDtk typed entities](https://ldtk.io/docs/general/editor-components/entities/) · [LDtk JSON documentation](https://ldtk.io/docs/game-dev/json-overview/)
- [ScriptableObject documentation](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/scriptableobject) · [Data Assets documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine) · [Scene List](https://docs.unity.com/en-us/engine/6000.0/manual/building-and-publishing/build-settings/build-profile-scene-list) · [Unity Chop Chop scene authoring example](https://github.com/UnityTechnologies/open-project-1/wiki/Scene-structure-of-locations) · [Level Instancing](https://dev.epicgames.com/documentation/en-us/unreal-engine/level-instancing-in-unreal-engine)
- [Cooking Content](https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-in-unreal-engine) · [GetDependencies](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/AssetDatabase.GetDependencies.html) · [Build Layout](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/BuildLayoutReport.html) · [Content updates](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/content-update-builds-overview.html) · [Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine)
- [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Asset Management](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine)
