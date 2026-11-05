---
id: K-CODE-UE-RENDER-ORIENTATION
title: How to map an Unreal project's rendering setup before studying or optimizing it
summary: Classify the rendering path from renderer settings, find engine renderer changes by marker or history, and locate project render hooks by searching for view extensions, global shaders and shader files, before planning study or optimization.
kind: method
scope: Unreal Engine 5 game projects, especially ones with a custom engine and in-project rendering plugins
keywords: [Unreal Engine, rendering, renderer settings, Nanite, Lumen, Virtual Shadow Maps, distance field shadows, static lighting, SceneViewExtension, ISceneViewExtension, RDG, FRDGBuilder, IMPLEMENT_GLOBAL_SHADER, usf, vertex factory, scalability, PSO]
status: active
checked_at: "2026-11-05"
context:
  engine: Unreal Engine 5.x
  platform: Windows desktop
---

## Guidance

Map the rendering setup in this order. Each step is a short read or search.

1. **Classify the rendering path** from `Config/DefaultEngine.ini` `[/Script/Engine.RendererSettings]`: `r.Nanite`, `r.DynamicGlobalIlluminationMethod` (Lumen), `r.ReflectionMethod`, `r.Shadow.Virtual.Enable`, `r.AllowStaticLighting`, `r.GenerateMeshDistanceFields`, `r.CustomDepth`, forward or deferred shading. With Nanite, Lumen and VSM off and static lighting on, the project runs the classic deferred path (lightmaps, shadow maps, distance field shadows). The study plan and the cost centers differ from those of a Lumen and Nanite project.
2. **Read quality tiers**: `DefaultScalability.ini`, `DefaultDeviceProfiles.ini` and the game user settings class that applies scalability, anti-aliasing and upscalers. Settings repeated at every tier (for example `r.ForceLODShadow`) deserve a look.
3. **Measure the engine renderer delta**: in the engine checkout (see [K-CODE-UE-ENGINE-CHECKOUT](K-CODE-UE-ENGINE-CHECKOUT.md)), search the studio's modification marker under `Renderer`, `RenderCore`, `RHI`, the RHI backends and `Engine/Shaders`, or filter `git log` to those paths. A small delta means improvements belong in project code and plugins; engine renderer edits carry a merge cost on every engine update.
4. **Find project render hooks**: search project `Source/` and `Plugins/` for `SceneViewExtension`, `FGlobalShader`, `IMPLEMENT_GLOBAL_SHADER`, `FRDGBuilder`, `AddPass`, scene proxies, vertex factories, and `*.usf` and `*.ush` files. Separate first-party code from third-party upscaler plugins (DLSS, XeSS, FSR), which are useful RDG reading material but not owned code.
5. **Find existing measurement**: in-game telemetry of render views, pixels, GPU memory or PSO hitches, and any profiling workflow the team already uses. Use it to rank candidates before changing structure.

Editorial judgment, not verified as a learning outcome: for study, start with a GPU frame capture (RenderDoc, `ProfileGPU` or Unreal Insights GPU tracks) and name each pass against `FDeferredShadingSceneRenderer::Render`; then follow one primitive from component to scene proxy, mesh batch, mesh pass processor and mesh draw command, using a project plugin with its own vertex factory as the concrete example. The smallest first-party view extension is a good first read for the render thread and game thread boundary.

## Applicability and exceptions

Steps 1 to 5 apply to any UE5 project. Step 3 needs engine source; with a launcher engine, treat the renderer as stock. For a Lumen and Nanite project, step 1 points to a different study and cost set (Lumen scene, Nanite rasterization, VSM page cost).

## Checks

- Every optimization candidate taken from this mapping is a hypothesis until a capture or telemetry measures it. Do not report a setting as a cost without measurement.
- Confirm that config values are not overridden by platform ini files, device profiles or user settings before treating them as effective.
- Large counts of lights or casters noted in code comments are inputs to measure, not evidence of cost.

## Evidence

Applied once to a UE 5.8 multiplayer dungeon game on Windows (2026-11-05). Steps 1 to 4 found the classic deferred setup (Nanite, Lumen and VSM off, static lighting and distance fields on), three renderer-related engine modification sites, one first-party plugin with its own vertex factory and compute shaders, one small render-thread view extension for telemetry, and third-party upscaler plugins. The study ordering is a recommendation that has not yet been followed through.

Not verified: effective values after device profile and user setting overrides; the GPU cost of any listed candidate.
