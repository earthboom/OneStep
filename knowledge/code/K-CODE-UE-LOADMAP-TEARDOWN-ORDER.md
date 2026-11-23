---
id: K-CODE-UE-LOADMAP-TEARDOWN-ORDER
title: What still exists when actor EndPlay runs during an Unreal map load, and why UUserWidget::GetOwningPlayer is null there
summary: UEngine::LoadMap marks the old world as tearing down, then destroys each local PlayerController and its pawn and clears LocalPlayer->PlayerController, and only then calls UWorld::EndPlay; code reached from actor EndPlay (including delegates it broadcasts to widgets) sees GetOwningPlayer() return nullptr while widgets and UUserWidget::GetWorld() remain valid.
kind: reference
scope: Unreal Engine 5 client map load through UEngine::LoadMap (non-seamless travel and the travel into a new map); UMG widgets that react to manager events broadcast from actor EndPlay; seamless travel and PIE shutdown not checked
keywords: [UEngine::LoadMap, UWorld::EndPlay, EEndPlayReason::LevelTransition, UWorld::BeginTearingDown, bIsTearingDown, ULocalPlayer::PlayerController, FLocalPlayerContext::IsValid, UUserWidget::GetOwningPlayer, UUserWidget::GetWorld, AActor::EndPlay, map travel, level transition, teardown order, null PlayerController, null dereference crash, loading screen crash]
status: active
checked_at: "2026-11-23"
context:
  engine: Unreal Engine 5.8 (custom fork source checkout)
  verification: engine source reading and one client crash matched by code reading; not reproduced at runtime
---

## Guidance

**Order inside `UEngine::LoadMap` for the world being left.**

1. `UWorld::BeginTearingDown()` sets `bIsTearingDown` on the old world.
2. For every local player whose `PlayerController` belongs to that world, the engine destroys the controller's pawn, destroys the controller, and sets `LocalPlayer->PlayerController = nullptr`.
3. `UWorld::EndPlay(EEndPlayReason::LevelTransition)` runs, which calls `AActor::EndPlay` on the remaining actors (game state, managers, HUD-owning actors that are still alive).
4. `UWorld::CleanupWorld()` follows.

**Consequence for UMG.** `UUserWidget::GetOwningPlayer()` returns `PlayerContext.IsValid() ? PlayerContext.GetPlayerController() : nullptr`, and `FLocalPlayerContext::IsValid()` requires `LocalPlayer->GetPlayerController(World)` to be non-null. After step 2 that is false, so every widget's `GetOwningPlayer()` is `nullptr` for the rest of the teardown. The widget objects themselves are still alive and `UUserWidget::GetWorld()` still returns the old world. Any actor `EndPlay` that clears a list (players, party members, inventory) and broadcasts per-item removal events therefore drives widget refresh code with no owning player.

**Rules that follow.**

- In widget code that can run from a manager event, never chain `GetOwningPlayer()->...`. Calling a virtual such as `GetWorld()` on a null pointer crashes. Use the widget's own `GetWorld()` when only the world is needed, and null-check the controller when it is needed.
- To skip presentation work during the transition, test `World->bIsTearingDown`; it is already true before the controller is destroyed and before any `EndPlay` runs.
- A latent unchecked dereference can sit in a leaf widget for years and become reachable only when a new caller refreshes it from a teardown-time event. When adding such a caller, compare it with the existing callers' guards (for example, a sibling that skips the refresh when there is no controller).

## Applicability and exceptions

- Read from Unreal Engine 5.8 source. Earlier UE5 versions use the same structure, but check the line positions before citing them.
- Covers the old world in a client `LoadMap`. Seamless travel keeps the controller across the transition and was not checked. PIE shutdown follows a different path and was not checked.
- Dedicated servers have no local player, so step 2 does not apply there.
- The order can change in an engine fork; reread `UEngine::LoadMap` when the engine version changes.

## Checks

- When a widget subscribes to an event, list every place that broadcasts it, including list clears from an actor `EndPlay`, and treat "map load with no owning player" as one case.
- Search changed widget code for `GetOwningPlayer()->` and `GetOwningPlayer<...>()->` without a preceding null check.
- For a list-driven widget (one row per member), exercise a map transition whose removal order makes a remaining member move to a different row, because only a row that receives a new valid identity does a full refresh.

## Evidence

- Source check (2026-11-23, Unreal Engine 5.8 fork checkout): `Engine/Source/Runtime/Engine/Private/UnrealEngine.cpp` lines 16183 (`BeginTearingDown`), 16243-16250 (destroy pawn and controller, `Player->PlayerController = nullptr`), 16259 (`EndPlay(EEndPlayReason::LevelTransition)`), 16262 (`CleanupWorld`); `Engine/Source/Runtime/Engine/Private/LocalPlayer.cpp` lines 98-106 (`FLocalPlayerContext::IsValid`) and 147-151 (`GetPlayerController`); `Engine/Source/Runtime/UMG/Private/UserWidget.cpp` lines 1487-1490 (`GetOwningPlayer`).
- Task check (2026-11-23): a shipped client closed without a crash report while three party members loaded a dungeon map. With no callstack, the cause was matched by code reading: a party-list clear in game state `EndPlay` moved a member into another row, a newly added row widget refreshed its status cells, and a leaf cell called `GetOwningPlayer()->GetWorld()`. The fix switched the cell to its own `GetWorld()`. Runtime reproduction was not performed in this check.
