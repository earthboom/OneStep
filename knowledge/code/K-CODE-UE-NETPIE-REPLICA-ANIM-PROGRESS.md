---
id: K-CODE-UE-NETPIE-REPLICA-ANIM-PROGRESS
title: Why a simulated proxy's montage position can look frozen in a headless network PIE test
summary: A simulated proxy whose mesh is not rendered may have animation update rate optimization (URO) skip its animation update for several frames, so Montage_GetPosition stays unchanged between updates; at low test frame rates the gap exceeds a fixed wall-clock stall threshold. Count only frames where FAnimUpdateRateParameters::ShouldSkipUpdate() is false before calling the montage stalled.
kind: reference
scope: Unreal Engine 5 automation tests that observe animation progress (montage position, section, notifies) on simulated proxies in network PIE, especially headless or offscreen runs
keywords: [URO, update rate optimization, bEnableUpdateRateOptimizations, FAnimUpdateRateParameters, ShouldSkipUpdate, BaseNonRenderedUpdateRate, AnimUpdateRateParams, simulated proxy, Montage_GetPosition, RenderOffscreen, network PIE, stall check, flaky test]
status: active
checked_at: "2026-11-23"
context:
  engine: Unreal Engine 5.8 source
---

## Guidance

- With `bEnableUpdateRateOptimizations` on, a skinned mesh's update rate tracker decides per frame whether to skip the animation update. A non-rendered mesh that is not human-controlled uses `BaseNonRenderedUpdateRate`: it updates once every that many frames. On skipped frames the anim instance does not advance montages, so `Montage_GetPosition` returns the same value.
- In headless runs (`-RenderOffscreen`) other players' characters are usually not rendered, so every simulated proxy runs at the non-rendered rate. Projects often raise that rate for simulated proxies. At a slow test frame rate (high-latency network emulation, several PIE worlds in one process) a handful of skipped frames lasts longer than a few hundred milliseconds of wall time.
- A stall check based only on elapsed time therefore fails on a healthy proxy. Track how many frames since the last position change actually updated animation (`AnimUpdateRateParams->ShouldSkipUpdate()` false, or URO disabled) and require both an update count of at least two and the time threshold before reporting a stall. With a nonzero play rate, a single real update changes the position.
- Keep the rate and section assertions as they are; only progress checks need the update-aware gate.

## Applicability and exceptions

- Human-controlled (locally controlled) characters use update rate 1 and are unaffected.
- If a test needs every frame on a proxy, force it through the project's URO override or `VisibilityBasedAnimTickOption` rather than loosening the time threshold; restore the setting afterwards.
- A dedicated server may not advance player montages at all; check server state through replicated values such as play rate instead of position.

## Checks

- When a progress check fails only in the slow profile and by a margin close to (update rate) x (frame time), read the proxy mesh's `bEnableUpdateRateOptimizations` and `AnimUpdateRateParams->BaseNonRenderedUpdateRate` before suspecting gameplay.
- Confirm discrimination: with the play rate forced to zero, the update-aware check must still fail after two real updates.

## Evidence

Read in the UE 5.8 source on 2026-11-23, `Engine/Source/Runtime/Engine`:

- `Private/Components/SkinnedMeshComponent.cpp`: the update rate tracker uses rate 1 when human-controlled and `BaseNonRenderedUpdateRate` otherwise when not rendered (around line 295). `bSkipUpdate = ((Counter % UpdateRate) > 0)` is set around line 6081.
- `Classes/Engine/EngineTypes.h`: `FAnimUpdateRateParameters::ShouldSkipUpdate()` returns `bSkipUpdate` (around line 2858). `BaseNonRenderedUpdateRate` is declared around line 2768.

Runtime, one studio project, 2026-11-23: a headless network PIE test checked that a spectator's copy of a looping montage advanced. Its 0.25 second wall-clock stall threshold failed only in the high-latency profile ("position stayed for 0.26 seconds"). The project sets `BaseNonRenderedUpdateRate = 8` for simulated proxies. After the check counted only updated frames, the same suite passed in both baseline and high-latency profiles. The zero-rate discrimination was traced in code, not executed.
