---
id: K-CODE-UE-TIMER-MANAGER
title: What Unreal FTimerManager does when a running handle is set again, how SetTimerForNextTick differs, and which timers survive their owner
summary: SetTimer on a handle that still names a live timer clears that timer and creates a new one with a new handle value, and a rate of 0 or less only clears; SetTimerForNextTick takes no handle and runs at the next timer manager tick, which can be later in the same frame; no engine code clears an actor's timers on EndPlay or destruction, so cleanup depends on the delegate type.
kind: reference
scope: Unreal Engine 5 FTimerManager used through UWorld::GetTimerManager or AActor::GetWorldTimerManager on the game thread; native C++ timers and Blueprint timer-by-event or by-function nodes
keywords: [FTimerManager, FTimerHandle, SetTimer, SetTimerForNextTick, ClearTimer, ClearAllTimersForObject, FTimerDelegate, CreateUObject, CreateWeakLambda, CreateLambda, TFunction, bRequiresDelegate, ETimerStatus, ActivePendingRemoval, TimerManager.GuaranteeEngineTickDelay, UGameInstance::GetTimerManager, AbilitySystem.ClearAbilityTimers, UUserWidget::CancelLatentActions, timer restart, debounce, dangling capture]
status: active
checked_at: "2026-11-20"
context:
  engine: Unreal Engine 5.8 (release/5.8.0p5 source)
---

## Guidance

**Setting a handle that is already running.** `SetTimer(Handle, ...)` first looks the handle up. If it still names a live timer, that timer is cleared, then a new timer is added and the handle is overwritten with a new index and serial. Nothing is kept: the countdown restarts from the new rate, the old delegate and its payload are dropped, and copies of the old handle value stop matching anything. This makes "call SetTimer again with the same member handle" the standard restart or debounce pattern. A rate of 0 or less only clears and invalidates the handle; it never calls the delegate. Timers set through a different handle variable are independent, so a discarded local `FTimerHandle` cannot be cancelled and repeated calls stack.

Re-arming from inside the timer's own callback is safe: the executing timer is removed, the loop for that timer stops, and the new timer is scheduled normally.

**Cleared timers.** `ClearTimer` on an active timer only marks it `ActivePendingRemoval`; the entry is removed later in the tick. Lookup functions already treat it as gone, so `IsTimerActive` is false immediately.

**SetTimerForNextTick.** It returns a new handle every call and has no handle argument, so it never replaces an earlier request; two calls run twice unless the caller clears the stored previous handle. With the default `TimerManager.GuaranteeEngineTickDelay=0`, the timer is made active at the current timer clock and fires at the next `FTimerManager::Tick` that advances time. `UWorld::Tick` runs the timer tick after `TG_PostPhysics` and before `TG_PostUpdateWork`. So a request made before that point in a frame (network receive, tick groups up to post physics) runs later in the same frame, while a request made inside a timer callback or after the timer tick runs in the next frame. Setting the CVar to 1 guarantees an engine frame boundary for requests made before the timer tick. A normal `SetTimer` made before the timer tick is held as pending and never fires in the frame it was set.

**Owner destruction.** In this engine version, `AActor::EndPlay` and actor destruction do not call `ClearAllTimersForObject`. What happens depends on the delegate:

| Delegate | Weak check before running | Keyed for `ClearAllTimersForObject(Object)` |
| --- | --- | --- |
| Method on a UObject (`SetTimer(Handle, this, &Method)`, `CreateUObject`, `BindUObject`) | Yes. A destroyed or garbage object makes it a no-op; a looping timer is removed at its next fire. | Yes, by that object |
| Dynamic delegate (Blueprint timers, `CreateUFunction`) | Yes | Yes, by that object |
| `CreateWeakLambda(Context, ...)` | Yes, on the context object only | Yes, by the context object, not by the class that set it |
| `CreateLambda`, raw `TFunction` lambda, `CreateRaw` | No. It runs whenever it expires. | No. `ClearAllTimersForObject` never sees it. |

Two engine owners do clear timers: `UGameplayAbility::EndAbility` calls `ClearAllTimersForObject(this)` while `AbilitySystem.ClearAbilityTimers` is 1 (the default), and `UUserWidget::CancelLatentActions` does so when called. `UWorld::GetTimerManager` returns the game instance's timer manager when there is one, so an uncleared timer can outlive the world that set it and fire after a level transition.

## Applicability and exceptions

- Checked on the default timer path. With AutoRTFM transactional timers active, set and clear calls inside a closed transaction are deferred until commit or abort.
- A weak check validates only the bound object. Other UObjects copied into a payload or lambda capture are not protected, and a lambda capturing `[this]` or locals by reference inside a weak lambda bound to `this` is safe only while every captured object lives at least as long as `this`.
- A non-looping weakly bound timer whose owner died is not removed early: it stays until it expires, then runs as a no-op.
- `SetTimerForNextTick` is not a network-send boundary: an RPC and a destruction requested in the same frame can still go out in the same send.
- The engine's own wait-delay ability task switches to `SetTimerForNextTick` for a duration of 0 or less. A wrapper that passes such a duration straight to `SetTimer` never completes.

## Checks

- For each `SetTimer`, decide whether a second call must restart, must be ignored (guard with `IsTimerActive`), or must run in parallel (separate handles). A shared member handle passed for two different purposes makes the second call silently cancel the first.
- For each rate that can come from data or a console variable, confirm the 0 or less case still calls or explicitly skips the callback.
- For each `SetTimerForNextTick`, check whether the caller needs "after this frame's tick groups" (holds before the timer tick) or "after a frame boundary" (needs the CVar, a timer made after the timer tick, or another mechanism). Store and clear the returned handle if requests can repeat.
- For each lambda or raw delegate, list the captured pointers and find the code that clears it on every end path; `ClearAllTimersForObject` and ability end will not.
- For each looping timer with a discarded handle, confirm that running until the owner is destroyed is intended.

## Evidence

Read in the UE 5.8 release source on 2026-11-20:

- `Engine/Source/Runtime/Engine/Private/TimerManager.cpp`: `InternalSetTimer` (lookup, clear, rate check, pending versus active by `HasBeenTickedThisFrame`), `InternalSetTimerForNextTick` (`GuaranteeEngineTickDelay`, `ExpireTime = InternalTime`), `InternalClearTimer` (status cases including `Executing`), `InternalClearAllTimers` (uses `ObjectToTimers`), `AddTimer` (key from `GetBoundObject`), `Tick` (strict `InternalTime > ExpireTime`, loop reschedule only while `!bRequiresDelegate || IsBound()`, pending promotion at the end), `FTimerUnifiedDelegate::IsBound`, `GetBoundObject` and `Execute`.
- `Engine/Source/Runtime/Engine/Public/TimerManager.h`: `ClearTimer`, `ClearAllTimersForObject`, `FTimerData::bRequiresDelegate`.
- `Engine/Source/Runtime/Core/Public/Delegates/DelegateInstancesImpl.h`: `GetObjectForTimerManager` returns null for the functor (lambda) instance and the context object for the weak functor instance; `IsSafeToExecute` for UObject, weak lambda and raw instances.
- `Engine/Source/Runtime/Engine/Private/LevelTick.cpp`: tick group order around `GetTimerManager().Tick`.
- `Engine/Source/Runtime/Engine/Private/Actor.cpp`: `AActor::EndPlay` has no timer cleanup. `Engine/Source/Runtime/Engine/Private/World.cpp`: `UWorld::GetTimerManager`.
- `Engine/Plugins/Runtime/GameplayAbilities/Source/GameplayAbilities/Private/Abilities/GameplayAbility.cpp`: `FAbilitySystemTweaks::ClearAbilityTimers` and the `EndAbility` call; `Private/Abilities/Tasks/AbilityTask_WaitDelay.cpp`: zero-duration branch. `Engine/Source/Runtime/UMG/Private/UserWidget.cpp`: `CancelLatentActions`.

Source reading only; no runtime test. Applied in a read-only review of one studio project, where it explained a shared-handle cancellation and a wait-delay wrapper without the zero branch; the project findings stay in that project.
