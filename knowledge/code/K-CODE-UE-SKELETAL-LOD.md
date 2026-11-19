---
id: K-CODE-UE-SKELETAL-LOD
title: How Unreal picks a skeletal mesh LOD, and why a mesh with its tick off keeps a stale LOD
summary: "The render thread computes a desired skeletal mesh LOD and the component tick applies it. When suspending ticks, check the applied level and allow any forced selection to take effect before suspension."
kind: reference
scope: Unreal Engine 5 skeletal mesh components (USkinnedMeshComponent, USkeletalMeshComponent), non-Nanite skeletal meshes
keywords: [Unreal Engine, skeletal mesh, LOD, level of detail, MinDesiredLODLevel, UpdateMinDesiredLODLevel, FSkeletalMeshObject, UpdateLODStatus, TickComponent, SetForcedLOD, ForcedLodModel, r.SkeletalMeshLODBias, LOD bias, r.SkeletalMeshLODRadiusScale, ScreenSize, LODHysteresis, ComputeBoundsScreenRadiusSquared, MaxDistanceFactor, EngineShowFlags.LOD, bThumbnailRendering, GetIsInFocus, FSceneView, FSceneViewFamily, view relevance, double buffering, one-frame latency, render thread, game thread, mutex, race condition, clamp, hysteresis, LOD popping, scalability, "FSkeletalMeshObject::UpdateMinDesiredLODLevel", "USkinnedMeshComponent::TickComponent", "USkinnedMeshComponent::SetForcedLOD", "SetComponentTickEnabled"]
status: active
checked_at: "2026-11-19"
context:
  engine: Unreal Engine 5.8 source
---

## Guidance

**Flow (who computes, who applies).**

1. **Render thread computes.** While the scene proxy gathers view relevance, `FSkeletalMeshObject::UpdateMinDesiredLODLevel` (`SkeletalRender.cpp`) runs once per view per frame.
   - It skips thumbnail views (`View->Family->bThumbnailRendering`) and view families that are not in focus (`GetIsInFocus()`; only editor viewports set this false, the default is focused).
   - It computes the screen radius squared of the bounds sphere (`ComputeBoundsScreenRadiusSquared`) and multiplies it by `LODScale` squared. `LODScale` is `r.SkeletalMeshLODRadiusScale` clamped to 0.25 to 1.0, so this cvar can only lower detail.
   - If `EngineShowFlags.LOD` is on, it walks LODs from worst to LOD1 and picks the first whose `(ScreenSize * 0.5)^2` exceeds the screen radius squared; LOD0 is the fallback. `ScreenSize` is a projected screen-size threshold.
   - Hysteresis: for LODs equal to or better than the current one, `LODHysteresis` is added to `ScreenSize`, so returning to a better LOD needs a larger on-screen size than leaving it. This prevents LOD popping at a boundary.
2. **Double buffering across views.** On the first call in a new frame number, the previous frame's working values are copied to the values the game thread reads (`MinDesiredLODLevel`, `MaxDistanceFactor`), and the working values restart. Later calls in the same frame (split screen, stereo) keep the minimum LOD and the maximum screen size. A mutex guards this only when the family has more than one view, because relevance runs in parallel.
3. **Game thread applies.** `USkinnedMeshComponent::TickComponent` calls `UpdateLODStatus` (`SkinnedMeshComponent.cpp`), which sets the LOD to `Clamp(MinDesiredLODLevel + LODBias, 0, MaxLOD)` unless a forced LOD is set. The result is one frame behind the render-thread computation.

**Pitfall.** If anything disables the mesh component tick (a custom sleep or idle optimization, `SetComponentTickEnabled(false)`), step 3 stops while step 1 keeps running for a visible mesh. The applied LOD freezes at its last value, so a frozen character seen far away stays at a coarse LOD when the camera approaches. A sufficiently negative global bias can mask stale selection at the cost of detail reduction for other meshes. `USkinnedMeshComponent::SetForcedLOD` takes a one-based selection (0 clears the override) and Epic documents application on the next tick. If a fixed LOD is appropriate, request it while ticks still run, observe it being applied, then suspend ticking. Clear it and verify automatic selection after resuming.

## Applicability and exceptions

Applies to skeletal meshes rendered through `FSkeletalMeshObject`. Nanite skeletal meshes call the same function from their own proxy path, but their geometry detail is decided by Nanite, so verify separately. Scene captures do vote like normal views. Animation update rate optimization and visibility-based anim tick are separate systems: they can change pose update frequency without the component tick being off.

## Checks

- To see the effective LOD in game, use `a.VisualizeLODs 1` and temporarily set the bias cvar to 0.
- Search the project for `SetComponentTickEnabled(false)`, `PrimaryComponentTick.bCanEverTick`, and custom freeze or sleep states on actors with skeletal meshes; for each, check whether a forced LOD is set.
- Check each asset's LOD Settings (`ScreenSize`, `LODHysteresis`) before re-enabling LOD; once a global bias is removed, also check effective bias, minimum LOD, parent/leader synchronization and forced overrides.
- Measure GPU and CPU before and after; a LOD change is a hypothesis until a capture shows the saving.

## Evidence

UE 5.8 source inspection on 2026-11-19 covered `SkeletalRender.cpp` (view filtering and accumulation), `SkinnedMeshComponent.cpp` (component update and clamp), `SceneView.h` and `EditorViewportClient.cpp` (focus). The stale selection was inferred from code. Neither the symptom nor the proposed ordering was tested in a running game, and no performance saving was measured. [Epic, FSkeletalMeshObject::UpdateMinDesiredLODLevel](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/FSkeletalMeshObject/UpdateMinDesiredLODLevel?application_version=5.8) · [USkinnedMeshComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/USkinnedMeshComponent?application_version=5.8) · [Set Forced LOD](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Components/SkinnedMesh/SetForcedLOD?application_version=5.8)
