---
id: K-GAME-GAMEPLAY-REGRESSION
title: "Verify gameplay regressions through the affected player journey"
summary: "Exercise a supported entry point with fixed initial state, independent expected outcomes and an interruption. Select neighboring paths from rule, asset, progression and deployment dependencies."
kind: method
scope: "Unity and Unreal game rules, scenes, packages, multiplayer, visual review and performance checks."
keywords: ["gameplay regression","test oracle","replay","Play Mode","Functional Testing","Gauntlet","flaky test","게임플레이 회귀","회귀 테스트","플레이 검증","리플레이","기존 동작","플레이테스트","테스트 오라클","재접속"]
status: active
checked_at: "2026-11-22"
---
# Verify gameplay regressions through the affected player journey

## Guidance

Choose a representative success path, an interruption and entry to new content. Record baseline build/content IDs, options, save, random seed, role, initial state, actions, visible results and authoritative state at checkpoints. Derive expectations from approved rules, fixed examples, an independent calculation or agreed invariant. Record how many paths ran and isolate pre-existing failures. Use the first divergent command and fields to diagnose a changed replay.

Follow callers, serialized references, subscriptions, pack registration, unlocks and shipping configurations. A new board needs a menu entry, solution replay, retry and a neighboring board sharing the rule. A changed racing checkpoint needs normal, skipped, wrong-way and respawn paths and a ghost policy. For tactics compare action points, turn order, invalid commands and simultaneous win/loss. For co-op reconnect around reward commitment and inspect both server state and client presentation. For streaming return to the same NPC and record quest continuity and cold/warm costs.

In Unity exercise rules/data in Edit Mode, input and assembly in Play Mode, and relevant bundles, backend and settings in a Player. In Unreal use low-level or Automation tests for rules, Data Validation for assets, Functional Testing for world readiness and a package for cooking and menu paths. Gauntlet can coordinate the required server and clients. Test actual device input and networking when the contract depends on them.

## Applicability and exceptions

For deterministic turns compare exact state. For real-time physics define tolerances and supported scheduling conditions. A bot finishing a mission shows reachability, while the rule still needs an independent oracle. Select visual baselines by device, settings, camera and capture time. Human play assesses intent, readability and feel. Budget performance by repeated route, distribution and variation; defer judgment when a difference is within the variation.

## Checks

Wait for readiness or authoritative acknowledgment with a timeout. Reset saves, time, seeds, subscriptions and world objects. Keep first-failure logs even after a passing rerun. Give quarantined tests an owner and reinstatement condition. Review changes to assertions, fixtures, image tolerances and filters. Prove a representative check rejects a known bad candidate. For migration read, resave and reread older data, including repeat conversion or missing packs.

## Evidence

The November 22 review distinguished test-oracle and property research, game-specific selection studies and their subjects, proof-of-concept automation, Rare/Mojang/Ubisoft production reports and Riot's server determinism work. The proposed genre cases are designs for tests, not local execution results.

[Stage authoring](K-GAME-STAGE-AUTHORING.md) · [Save recovery](K-GAME-TECH-SAVE.md) · [Playtest selection](K-GAME-PROTOTYPE-PLAYTEST.md)

- [Barr et al., test oracle research, IEEE TSE — Paper](https://web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf) · [Claessen and Hughes, QuickCheck, ICFP 2000 — Paper](https://www.cs.tufts.edu/comp/150FP/archive/john-hughes/quick.pdf) · [Regression test selection paper](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/p173-rothermel.pdf) · [GameRTS paper](https://ttfish.cc/content/Papers/icse23.pdf) · [Luo et al., flaky tests, FSE 2014 — Paper](https://mir.cs.illinois.edu/~marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf)
- [Record and replay research](https://link.springer.com/article/10.7603/s40601-013-0010-4) · [Planning and learning research](https://arxiv.org/abs/2402.12393) · [Rare talk video](https://www.gdcvault.com/play/1026366/Automated-Testing-of-Gameplay-Features) · [Rare presentation materials](https://media.gdcvault.com/gdc2019/presentations/Masella_Robert_AutomatedTestingOf.pdf) · [Minecraft talk video](https://gdcvault.com/play/1027345/Lessons-Learned-in-Adapting-the)
- [Ubisoft, The Division, GDC 2019 — Talk video](https://www.gdcvault.com/play/1026382/Automated-Testing-Using-AI-Controlled) · [Presentation materials](https://media.gdcvault.com/gdc2019/presentations/Paredes_Jose_AutomatedTestingUsing.pdf) · [Implementation account](https://www.riotgames.com/en/news/determinism-league-legends-implementation) · [Tracing state divergences](https://www.riotgames.com/en/news/determinism-league-legends-fixing-divergences) · [Kalibera and Jones, performance changes and measurement uncertainty — Paper](https://arxiv.org/abs/2007.10899)
- [Unity Test Framework modes](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/edit-mode-vs-play-mode-tests.html) · [Low-Level Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/write-low-level-tests-in-unreal-engine) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Input Test Fixture](https://docs.unity3d.com/Packages/com.unity.inputsystem%401.11/manual/Testing.html) · [Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine)
- [Functional Testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine) · [Player test workflow](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/workflow-run-playmode-test-standalone.html) · [Network Simulator](https://docs.unity3d.com/Packages/com.unity.multiplayer.tools%402.2/manual/network-simulator.html) · [Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine) · [Network emulation](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-network-emulation-in-unreal-engine)
- [Player profiling](https://docs.unity3d.com/6000.0/Documentation/Manual/profiler-profiling-applications.html) · [Frame measurement API](https://docs.unity3d.com/Packages/com.unity.test-framework.performance%403.0/manual/measure-frames.html) · [Unreal Insights](https://dev.epicgames.com/documentation/unreal-engine/unreal-insights-in-unreal-engine) · [Screenshot Comparison](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine)
- [Automated playtesting of game parameters](https://sites.cc.gatech.edu/fac/riedl/pubs/zook-fdg14.pdf)
