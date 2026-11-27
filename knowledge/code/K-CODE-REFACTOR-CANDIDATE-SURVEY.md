---
id: K-CODE-REFACTOR-CANDIDATE-SURVEY
title: How to find small, high-value refactoring candidates in a large game codebase
summary: Split the source tree by area, search each area for a fixed set of concrete signals (diverged copies, unused hot-path copies, by-value large parameters, debug-only ticks, process-lifetime statics holding session state, bypassed helpers), verify every hit in code and rank by payoff per effort; style-only sweeps and length-only findings rank low.
kind: method
scope: Read-only discovery of refactoring candidates in large C++ game projects, especially Unreal Engine; the signals locate questions and do not replace behavior tests for the chosen change
keywords: [refactoring candidates, code survey, duplication, copy divergence, dead code, hot path, pass by value, TFunctionRef, FGameplayEventData, bAllowTickOnDedicatedServer, bCanEverTick, AActor::Tick, RegisterTickFunction, NM_DedicatedServer, empty tick, function-local static, static storage duration, PIE, 리팩터링 후보, 중복 코드, 복사본 불일치, 핫패스]
status: active
checked_at: "2026-11-27"
context:
  engine: Unreal Engine 5.8
  language: C++20
relations:
  requires: [K-CODE-ABSTRACTION-COST, K-CODE-MAINTAINABILITY-EVIDENCE]
---

# How to find small, high-value refactoring candidates in a large game codebase

## Guidance

Split the source tree into a few independent areas (for example ability system, AI and spawning, UI and data, items and services) and survey them in parallel. Give each survey the project's coding conventions and the same signal list. Require a file and line for every claim and a list of checked-and-rejected items.

Signals that most often produced a small change with a concrete payoff:

- **Diverged copies.** When the same block exists in several places, compare the copies line by line. A copy that reads the wrong configuration variable, misses a zero guard or uses a different build guard is both a duplication and a latent defect, so it ranks above plain duplication.
- **Unused copies on a hot path.** A local that copies a large struct (an effect spec, a user record, a quest array) and is never read, or a by-value parameter of a large struct in a per-hit or per-frame function. In Unreal, `FGameplayEventData` and `FGameplayTagContainer` passed by value allocate on copy; a synchronous callback parameter can be `TFunctionRef` instead of a by-value `TFunction`.
- **Debug-only ticks.** A component that sets `bCanEverTick` only to draw a debug overlay when a console variable is set still costs one tick per instance wherever it is allowed to tick. Gate the tick on the debug build flag and set `bAllowTickOnDedicatedServer` to false where the work is client-only. `PrimaryComponentTick` settings are written by every constructor in the class chain, so read the base class constructors before claiming which machines tick: a project base component may already set `bAllowTickOnDedicatedServer` to false, which removes the server half of the payoff. The engine applies `bAllowTickOnDedicatedServer` when the tick function registers, by testing the world's net mode, so a play-in-editor dedicated server world honors it too.
- **Empty actor ticks.** On a native C++ actor class, `AActor::Tick` runs Blueprint `ReceiveTick` and latent actions only for Blueprint-generated or non-native classes. An override that only calls `Super::Tick` therefore does nothing on the native class but still registers a tick function when `bCanEverTick` is true. Removing the override and the tick flags is safe once no Blueprint subclass is spawned and nothing enables the tick.
- **Process-lifetime state.** A function-local `static` has static storage duration, so it lives for the whole process and is shared by every instance of the class. Two cases make it a real defect: an editor runs several play sessions one after another in one process, and the end path does not terminate the process (a `static bool bEnded` then makes the second session skip its end path); or several instances live at once in one process, such as several clients in a multi-client play-in-editor session (a static timer or sample history is then advanced or overwritten by all of them). Move the value into the instance whose lifetime matches the state: a game-instance subsystem for state that must survive map travel, the game mode or controller for state that should reset with the level.
- **Bypassed helpers and repeated linear lookups.** Callers that repeat an existing helper's body, or a per-item linear search inside a loop over the same container.

Rank by payoff per effort and by risk. Length alone, table-shaped functions and project-wide style sweeps rank low. Changes to when a shared widget refreshes rank as higher risk even when small.

## Applicability and exceptions

A reference count of zero does not prove dead code when reflection or visual scripting can call the function; report such a function as unverified. Engine-generated or protocol-generated code, wire formats and anti-cheat paths are poor candidates. A diverged copy may be intentional; confirm with the owner before unifying it. A process-lifetime static is harmless on a dedicated server that runs one session per process, so the payoff is in editor and automation runs. Before claiming a second-session failure, trace what the end path does: if finishing the session exits the process, the flag never survives into another session and the fix is a cleanup, not a defect fix. A static used to de-duplicate a request (send only when the value changes) keeps its effect as a member when the owning instance lives as long as the request target.

## Checks

- Re-read each cited line before reporting; one survey in this task had stopped an unused-function scan partway, and it said so, which kept an incomplete claim out of the ranking.
- For a hot-path claim, name the caller that makes it hot.
- For a diverged copy, state which variant is the intended rule.
- For each candidate, list the behavior to test after the change.
- For a tick claim, trace `PrimaryComponentTick` (or `PrimaryActorTick`) assignments through every base class constructor, and check who still depends on the tick: subclasses, Blueprint subclasses with an Event Tick, `SetComponentTickEnabled` calls and tick prerequisites.
- For a process-lifetime static, name the owner's lifetime (process, game instance, level, controller), whether several owners coexist in one process, and whether the end path exits the process.
- For a build-flag gate, read how the flag is defined per target and per build pipeline. A flag that defaults to off outside the editor can still be turned on by the build server for internal builds, which decides where the debug feature survives.

## Evidence

- Task check 2026-11-26: four parallel read-only surveys of a roughly 1M-line Unreal Engine 5 game source tree produced 32 candidates; 12 were re-verified directly against the cited lines (diverged water-exit configuration variable, mismatched build guards between two spell cast classes, unused effect-spec copy per health change, debug-only equipment tick, empty pool-manager tick, process-lifetime end-game flag, quest array copy per damage event, per-item linear slot lookup, unreferenced utility functions, seven copies of a cursor-recenter block). No change was implemented or measured.
- Task check 2026-11-26 (follow-up implementation of the debug-only equipment tick): the survey had claimed the tick also ran on the dedicated server. The project's base component constructor already set `bAllowTickOnDedicatedServer` to false, so only client ticks remained to remove. The gated change built for the editor target (flag on) and a game Development target (flag off). The survey missed this because it read only the derived constructor.
- Task check 2026-11-27 (second follow-up, an empty pool-manager actor tick and a debug-only loot component tick): the same survey miss recurred for the component, whose base constructor also disabled dedicated server ticks; the server-side payoff claim was dropped before the change was made. The pool-manager actor, spawned by the game mode on every dungeon server, did tick there. Both changes built for the editor target (flag on) and the game Development target (flag off), and the existing looting automation (eight network play-in-editor cases, baseline and high latency) passed. A whole-content name scan plus a Blueprint text render found no Blueprint subclass or tick override for either class. No frame cost was measured.
- Task check 2026-11-27 (third follow-up, moving seven function-local statics into members): the survey's "second session skips its end path" claim for the end-game flag did not hold as stated, because that project's finished end path requests a process exit; the move was kept as a cleanup. A client-side fog sampling timer was the case that several instances share in one multi-client play-in-editor process. The change touched only timers and flags; build and regression results are in the project's task record.
- Registration check: Unreal Engine 5.8 `Engine/Source/Runtime/Engine/Private/TickTaskManager.cpp` line 2412, `FTickFunction::RegisterTickFunction` tests `bAllowTickOnDedicatedServer || !(World && World->IsNetMode(NM_DedicatedServer))`.
- Native actor tick: Unreal Engine 5.8 `Engine/Source/Runtime/Engine/Private/Actor.cpp` lines 2006-2028, `AActor::Tick` calls `ReceiveTick` and processes latent actions only when the class is compiled from Blueprint or is not native.
- `TFunctionRef` declaration: Unreal Engine 5.8 `Engine/Source/Runtime/Core/Public/Templates/Function.h` line 556.
- `bAllowTickOnDedicatedServer` declaration: Unreal Engine 5.8 `Engine/Source/Runtime/Engine/Classes/Engine/EngineBaseTypes.h` line 221 (`FTickFunction`).
- Static storage duration of a block-scope `static` variable: C++ standard draft [basic.stc.static] and [stmt.dcl], https://eel.is/c++draft/basic.stc.static.
