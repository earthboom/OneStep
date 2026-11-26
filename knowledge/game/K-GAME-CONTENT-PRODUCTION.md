---
id: K-GAME-CONTENT-PRODUCTION
title: "Choose who authors game content and how it reaches a release"
summary: "Choose an authoring workflow around a real edit, trace a shipped value back to its approved source, and prove clean builds, repeat visits and release rollback preserve the intended result."
kind: method
scope: "Game balancing sheets, level editors, content DSLs, PCG, live state and independently released packs."
keywords: ["content production","spreadsheet import","typed data generation","DSL","procedural generation","event sourcing","content pack","data management","게임 데이터 관리","제작 도구","스프레드시트","데이터 임포트","절차적 생성","콘텐츠 팩","이벤트 소싱","버전 배포"]
status: active
checked_at: "2026-11-22"
---
# Choose who authors game content and how it reaches a release

## Guidance

For balance and localization, import an approved sheet revision. Validate typed columns, units, copied formulas, IDs, ranges and foreign keys. Use child rows or assets for variable-length waves. Trace a shipped attack value to row, column and revision. Separate exploratory simulation sheets from approved export. For placement, graph, collision or lighting work, prefer a previewable asset or level editor. Track Unity assets with .meta. Unreal One File Per Actor changes editor collaboration units while cooking actors into their level.

Start behavior authoring with named conditions and actions. Introduce a DSL or bounded scripts when repeated combinations justify maintaining types, permitted operations, ordering, diagnostics, budgets and compatibility. Wesnoth WML ties scenarios to maps and successors, OpenTTD NML compiles to GRF, and Factorio separates prototype stages from runtime events and migrations.

For PCG choose when a layout becomes final. An author can approve generated output, a build can regenerate on tracked changes, or a runtime generator can reconstruct a world. For persistent revisits retain the generator version, input pack, random order and player edits or the resulting layout. Test reachability and the distribution of generated challenges separately.

## Applicability and exceptions

Use relational constraints and transactions when multiple writes must succeed together. Verify foreign keys actually run. Use versioned snapshots and write locks for conflicting devices. Add event history for audit or duplicate detection. Rebuilding authoritative state from events adds ordering, schema evolution, replay side effects and projection rebuild costs. Roblox's session locks and purchase IDs address a specific concurrent update problem. An event-sourcing study covered 25 engineers and 19 systems. Runtime entity handles are local to a session; persist reconstruction IDs instead.

## Checks

Choose a representative edit: move a puzzle piece, change checkpoint order, add a facility recipe or extend a co-op chapter. Open published content through the normal game. For optional packs define ID ownership, dependencies, overrides, missing-pack behavior and compatible releases. Test a base-only build, pack alone, conflicting ID, interrupted download and rollback reading a save written after the update. Compare clean/incremental artifacts and time from author edit to play. Measure whether a custom editor actually reduces repeated corrections.

## Evidence

The November 22 review compared Epic Tavern and Darkwater sheet workflows, Unpacking tools, industry DSLs, PCG research, relational and event-sourced systems and versioned EVE data distribution. Their toolchains and production constraints differ. The checks above were proposed, not executed in a new game.

[Format and schema contracts](K-GAME-CONTENT-FORMATS.md) · [Stage registration and progression](K-GAME-STAGE-AUTHORING.md) · [Random stream ownership](K-GAME-TECH-RNG.md)

- [Luban features, validation, and target-specific exports](https://www.datable.cn/en/docs/reference/features) · [Unreal Data Tables and Curve Tables](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine) · [Epic Tavern, Tomo Moriwaki, GDC 2026 — Developer talk](https://gdcvault.com/play/1035719/Spreadsheets) · [Engels and Erwig, ClassSheets, ASE 2005 — Authors' paper](https://web.engr.oregonstate.edu/~erwig/papers/ClassSheets_ASE05.pdf) · [TU Delft research](https://repository.tudelft.nl/record/uuid%3A47944256-3559-4c30-a5d2-a795f4bf8e3a)
- [Unity production guide](https://unity.com/how-to/architect-game-code-scriptable-objects) · [Unreal Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine) · [Unreal Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine) · [Unreal OFPA](https://dev.epicgames.com/documentation/en-us/unreal-engine/one-file-per-actor-in-unreal-engine) · [Unity asset metadata](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html)
- [Unreal Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Unite talk](https://www.youtube.com/watch?v=raQ3iHhE_Kk) · [Unpacking developer talk](https://youtu.be/2j7AJj1oRSQ)
- [GDC talk on gameplay scripting design](https://www.gdcvault.com/play/1023204/Sculpting-a-Gameplay-Scripting) · [ScenarioWML](https://wiki.wesnoth.org/ScenarioWML) · [WML campaign authoring guide](https://wiki.wesnoth.org/MakingCampaignInWML) · [Official NML source and compiler](https://github.com/OpenTTD/nml) · [NewGRF usage guide](https://wiki.openttd.org/en/Manual/NewGRF)
- [Data lifecycle](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) · [Migrations](https://lua-api.factorio.com/latest/auxiliary/migrations.html)
- [Goals and design challenges in PCG research](https://drops.dagstuhl.de/entities/document/10.4230/DFU.Vol6.12191.61) · [Insomniac's Marvel’s Spider-Man production paper](https://history.siggraph.org/wp-content/uploads/2022/09/2019-Talks-Santiago_Procedural-System-Assisted-Authoring.pdf) · [Tanagra paper](https://cdn.aaai.org/ojs/12379/12379-52-15907-1-2-20201228.pdf) · [Bungie asset pipeline talk](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Build Systems à la Carte paper](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf)
- [No Man’s Sky continuous world generation talk](https://www.gdcvault.com/play/1024265/Continuous-World-Generation-in-Noby) · [Horizon Zero Dawn GPU runtime placement talk](https://www.gdcvault.com/play/1024700/) · [Paper on measuring the expressive range of procedural generation](https://cdn.aaai.org/ojs/13012/13012-52-16529-1-2-20201228.pdf)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html) · [Roblox player data example](https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing) · [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html) · [Wube development article on Factorio saving and loading](https://www.factorio.com/blog/post/fff-270) · [Unity Cloud Save write locks](https://docs.unity.com/en-us/cloud-save/concepts/write-locks)
- [Martin Fowler on Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) · [Industry study by Overeem et al.](https://arxiv.org/abs/2104.01146) · [Archetypes in Unity Entities](https://docs.unity3d.com/Packages/com.unity.entities%401.0/manual/concepts-archetypes.html) · [Unreal MassEntity](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine)
- [Unreal Data Registries](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-registries-in-unreal-engine) · [Unreal Game Features](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine) · [Unity CCD releases and badges](https://docs.unity.com/en-us/ccd/dashboard) · [CCP's EVE static data transformation pipeline](https://developers.eveonline.com/blog/reworking-the-sde-a-fresh-start-for-static-data) · [CCP's versioned distribution API](https://developers.eveonline.com/blog/the-sde-over-http-static-data-dynamically)
