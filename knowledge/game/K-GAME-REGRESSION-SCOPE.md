---
id: "K-GAME-REGRESSION-SCOPE"
title: "Choose gameplay regression checks from the affected play paths"
summary: "Select checks for shared rules, content registration, compatibility and runtime assembly. Record an independent expectation and compare visible results with committed game state."
kind: "method"
scope: "Unity and Unreal gameplay changes, new content, shipped saves, multiplayer and performance-sensitive play"
keywords: ["gameplay regression","test oracle","Unity Play Mode","Unreal Functional Testing","packaged build","replay","snapshot comparison","게임플레이 회귀","패키지 검증","회귀 테스트","스테이지 검증"]
status: "active"
checked_at: "2026-11-26"
---

# Choose gameplay regression checks from the affected play paths

## Guidance

Record stage and build versions, initial state, input, player-visible result and committed state. Derive the expected outcome from an approved rule, accepted fixture or small independent calculation. Capture baseline failures and explain changes to assertions, tolerances, fixtures, disabled checks and reference images.

- **Shared rules or lifetimes.** Exercise valid, invalid and boundary inputs plus retry and second entry in representative existing stages. Find affected callers through code, scenes/maps, prefabs/Blueprints, catalogs, subscriptions and deployment settings.
- **New or changed content.** Validate IDs, references and genre rules. Follow the actual list → unlock → enter → retry or exit → finish path in the shipping build. Check an existing stage that shares the preset or progression table. Where relevant, replay old solutions or ghosts and confirm the policy for changed records.
- **Compatibility and authority.** Load and resave a supported old save, reread it and repeat migration. Try a missing pack, canceled load or unsupported save. For networked rewards, disconnect before completion and after acknowledgement and compare authoritative state and client views for missed or duplicate outcomes.

## Applicability and exceptions

Choose the lowest execution layer that can show the claim. Add target-build evidence when the claim depends on content delivery, platform input, networking or performance.

| Claim | Unity | Unreal |
| --- | --- | --- |
| Rules, converters and asset validity | Edit Mode and editor asset checks | Low-Level Tests or module automation, plus Data Validation in the editor or a commandlet |
| Scene, world and input assembly | Play Mode with readiness signals and the actual input/command route. Use InputTestFixture for isolated inputs. | Automation or Functional Testing with level readiness and the intended authority environment |
| Delivered content, devices and networking | Standalone Player or project automation using representative shipping settings and required clients | Target packaged session for cooked assets and real launch. Use Gauntlet for coordinated clients and servers where applicable. |
| Measurement | Profile the target Player and repeat the measured route | Unreal Insights with selected traces, plus screenshot checks under fixed capture conditions |

## Checks

For a puzzle, compare piece position and move count after a legal push, blocked push and restart. For racing, exercise branching, skipped checkpoints and respawn before testing old ghosts. For tactics, compare action points, turn order and simultaneous objective outcomes. Record the first divergence and the exact evidence location. State which paths ran, their conditions and what remains to execute. [OneStep verification procedure](../../skills/vegabond-code/references/verification.md) · [Stage compatibility](K-GAME-STAGE-COMPATIBILITY.md)

### Reproduction, visual quality and performance

For deterministic rules compare exact checkpoints using the same inputs. For real-time play use supported timing/position tolerances and compare the checkpoint order, game state and first divergence. Wait for world readiness or authoritative confirmation with a timeout. Reset saves, random state, timers, subscriptions and objects, and retain the first failure for diagnosis.

For capture comparisons fix device, resolution, settings, camera and capture time. Combine automated state/layout checks with observed play for camera, feel and objective discovery. Keep baseline and candidate workloads matched, separate first entry from repeats, and compare frame-time tails, long frames, load time and peak/resident memory against the device budget and run-to-run variability. [World runtime budgets](K-GAME-WORLD-RUNTIME-BUDGET.md) · [Playtest method](K-GAME-PROTOTYPE-PLAYTEST.md)

## Evidence

Test oracle and QuickCheck papers distinguish expected results and properties from execution. Regression selection and GameRTS support choosing cases through dependencies and observable play paths. Luo et al. describe wait and order-related flakes. Rare, Mojang and Ubisoft describe production automation. Riot's reports show tracing the first gameplay-state divergence. Kalibera and Jones describe uncertainty in repeated performance measurements. These methods inform the proposed scenarios, whose results depend on the target game and configurations.

- Methods and measurement · [Test oracles](https://web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf) · [QuickCheck](https://www.cs.tufts.edu/comp/150FP/archive/john-hughes/quick.pdf) · [Regression test selection](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/p173-rothermel.pdf) · [GameRTS](https://ttfish.cc/content/Papers/icse23.pdf) · [Flaky tests](https://mir.cs.illinois.edu/~marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf) · [Record and replay](https://link.springer.com/article/10.7603/s40601-013-0010-4) · [Model-based RPG proof of concept](https://arxiv.org/abs/2402.12393) · [Automated playtesting](https://sites.cc.gatech.edu/fac/riedl/pubs/zook-fdg14.pdf) · [Measurement uncertainty](https://arxiv.org/abs/2007.10899)
- Production examples · [Rare talk](https://www.gdcvault.com/play/1026366/Automated-Testing-of-Gameplay-Features) · [Rare slides](https://media.gdcvault.com/gdc2019/presentations/Masella_Robert_AutomatedTestingOf.pdf) · [Mojang talk](https://gdcvault.com/play/1027345/Lessons-Learned-in-Adapting-the) · [Ubisoft talk](https://www.gdcvault.com/play/1026382/Automated-Testing-Using-AI-Controlled) · [Ubisoft slides](https://media.gdcvault.com/gdc2019/presentations/Paredes_Jose_AutomatedTestingUsing.pdf) · [Riot implementation](https://www.riotgames.com/en/news/determinism-league-legends-implementation) · [Riot divergence tracing](https://www.riotgames.com/en/news/determinism-league-legends-fixing-divergences)
- Unity · [Edit and Play Mode](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/edit-mode-vs-play-mode-tests.html) · [InputTestFixture](https://docs.unity3d.com/Packages/com.unity.inputsystem%401.11/manual/Testing.html) · [Standalone Player tests](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/workflow-run-playmode-test-standalone.html) · [Network Simulator](https://docs.unity3d.com/Packages/com.unity.multiplayer.tools%402.2/manual/network-simulator.html) · [Player profiling](https://docs.unity3d.com/6000.0/Documentation/Manual/profiler-profiling-applications.html) · [Repeated frame measurement](https://docs.unity3d.com/Packages/com.unity.test-framework.performance%403.0/manual/measure-frames.html)
- Unreal · [Low-Level Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/write-low-level-tests-in-unreal-engine) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Automation](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine) · [Functional Testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine) · [Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine) · [Network emulation](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-network-emulation-in-unreal-engine) · [Unreal Insights](https://dev.epicgames.com/documentation/unreal-engine/unreal-insights-in-unreal-engine) · [Screenshot comparison](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine)
