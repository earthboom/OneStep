---
id: K-CODE-CPP-GAMEPLAY-FRAMEWORK
title: "Choose C++ gameplay composition by ownership and change impact"
summary: "Trace a gameplay request through its state owner, build dependencies, registrations and lifetimes. Validate the boundary by adding a second ability and removing an optional feature."
kind: method
scope: "Standalone C++ and Unreal gameplay. Engine contracts depend on installed version, authority and runtime configuration."
keywords: ["C++","Unreal","gameplay framework","ability cooldown","component composition","ECS","Game Features","게임플레이 프레임워크","능력 재사용 대기시간","컴포넌트 조합","상태 소유권","게임 피처"]
status: active
checked_at: "2026-11-21"
---
# Choose C++ gameplay composition by ownership and change impact

## Guidance

Put the state and transitions that enforce an invariant together. An inventory can expose grant/query results while retaining control over slot layout, ordering, capacity and persistence. For an ability, let the owner answer a request with acceptance or rejection and apply cost and cooldown exactly as its public contract specifies. Notify UI after resolution.

Use values, policies or member components for independently varying behavior. Use virtual dispatch or an engine hook when callers share meaningful guarantees about initialization, failure and cancellation. Trace the methods and overrides needed to understand one request. Keep compile/link dependencies, asset references and runtime activation distinct. An ordinary Unreal module may suffice for a build boundary. Game Features introduce registration, readiness and deactivation obligations for independently activated content.

For frequent bulk updates, identify reads, writes, structural-change visibility and ordering before trying ECS. Compare with the existing layout on the target workload. In Unreal, server GameMode and replicated GameState have different audiences. Match state to Pawn, world or Game Instance lifetime. Disconnect timers, subscriptions and input on the boundary that owns them. Delay activation until prerequisites arrive.

## Applicability and exceptions

Dungeon Siege and Overwatch illustrate their own composition and networking pressures. Lyra and Action Roguelike are examples with specific engine and initialization assumptions. The inheritance experiments varied by task, SyDRA mapped includes in ten engines and tested comprehension with sixteen participants, and Core ECS determinism concerns a formal model. None prescribes a hierarchy depth, engine-wide ECS migration or cross-platform simulation result. Verify toolchain support for WG21 proposals.

## Checks

Start with one cooldown ability. Test accepted, failed, canceled and duplicate requests, late initialization, respawn and map travel. Add a second policy without changing callers. Remove the HUD and compare authoritative results. For optional features, run base, A, B, both, deactivate and reactivate, including the build without A. For saves, read prior data and inject an interrupted write. For replication, observe actual server and client roles. For performance, use identical inputs, entity counts, builds and frame-time distributions.

## Evidence

The November 21 review inspected named paper sections, documented contracts and public-code symbols. Video references include official descriptions and slides. The executed C++ and Unreal examples support the optional-content paths they exercised; the Unreal sample declares EngineAssociation 5.8.

[Executed gameplay examples](../../docs/examples/cpp-gameplay-workflow/README.md) · [Information hiding](K-CODE-INFORMATION-HIDING.md) · [Dependency direction](K-CODE-DEPENDENCY-DIRECTION.md) · [Abstraction costs](K-CODE-ABSTRACTION-COST.md)

- [ACM](https://doi.org/10.1145/361598.361623) · [Full paper](https://ckrybus.com/static/papers/decomposing_systems_into_modules_1972.pdf) · [Liskov and Wing, 1994 — Authors' copy](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf) · [Daly paper](https://strathprints.strath.ac.uk/2676/1/strathprints002676.pdf) · [Replication](https://page.mi.fu-berlin.de/prechelt/Biblio/inheritTR.pdf)
- [Ullmann et al., 2025 — Paper](https://espace2.etsmtl.ca/id/eprint/29117/1/Petrillo-F-2024-29117.pdf) · [Redmond et al., 2025 — Paper](https://arxiv.org/abs/2508.15264) · [OOPSLA talk](https://www.youtube.com/watch?v=z2vqiVtmsuY) · [Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c-hier-class-hierarchies-oop) · [WG21 proposal](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3019r14.pdf)
- [Dungeon Siege — Slides and speaker notes](https://this.scottbilas.com/files/pubs/2002/gdc-san-jose/GameObjects.pdf) · [Developer retrospective](https://this.scottbilas.com/) · [GDC Vault](https://gdcvault.com/play/1024001/-Overwatch-Gameplay-Architecture-and) · [Official GDC video](https://www.youtube.com/watch?v=W3aieHjyNvw) · [Tech Talk](https://dev.epicgames.com/community/learning/talks-and-demos/yrrn/lyra-starter-game-overview)
- [Sample](https://dev.epicgames.com/documentation/unreal-engine/lyra-sample-game-in-unreal-engine) · [Init State implementation](https://dev.epicgames.com/documentation/unreal-engine/game-framework-component-manager-in-unreal-engine?lang=en-US) · [Inside Unreal video](https://www.youtube.com/watch?v=YKhcN8NkIYY) · [Action component implementation](https://github.com/tomlooman/ActionRoguelike/blob/master/Source/ActionRoguelike/ActionSystem/RogueActionComponent.cpp) · [Action header](https://github.com/tomlooman/ActionRoguelike/blob/master/Source/ActionRoguelike/ActionSystem/RogueAction.h)
- [Component chapter](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/component.markdown) · [Event Queue chapter](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/event-queue.markdown) · [Parent, GoingNative 2013](https://learn.microsoft.com/en-us/shows/goingnative-2013/inheritance-base-class-of-evil) · [Acton, CppCon 2014](https://www.youtube.com/watch?v=rX0ItVEVjHc) · [Godot Node documentation](https://docs.godotengine.org/en/stable/classes/class_node.html)
- [Node C++ implementation](https://github.com/godotengine/godot/blob/master/scene/main/node.cpp) · [O3DE component contract](https://docs.o3de.org/docs/user-guide/programming/components/create-component/)
- [Unreal Modules](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules) · [CMake target linking contract](https://cmake.org/cmake/help/latest/command/target_link_libraries.html) · [Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine) · [Game Features](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine) · [Game Feature Action lifecycle](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/GameFeatures/UGameFeatureAction)
- [Flecs Quickstart](https://www.flecs.dev/flecs/Quickstart.html) · [EnTT developer talk](https://skypjack.github.io/pdf/the_cpp_of_entt.pdf) · [MassEntity documentation](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine?lang=en-US) · [Gameplay Framework Quick Reference](https://dev.epicgames.com/documentation/unreal-engine/gameplay-framework-quick-reference-in-unreal-engine?lang=en-US) · [Lyra ability initialization](https://dev.epicgames.com/documentation/unreal-engine/abilities-in-lyra-in-unreal-engine?lang=en-US#how-are-lyra-characters-initialized)
- [Subsystems](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine?lang=en-US) · [Object Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine?lang=en-US) · [Actor Lifecycle](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-actor-lifecycle)
- [Unreal Automation Test Framework](https://dev.epicgames.com/documentation/unreal-engine/automation-test-framework-in-unreal-engine?lang=en-US) · [Testing networked games](https://dev.epicgames.com/documentation/en-us/unreal-engine/testing-and-debugging-networked-games-in-unreal-engine)
