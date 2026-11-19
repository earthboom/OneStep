---
id: K-CODE-UE-RENDER-ORIENTATION
title: How to map an Unreal project's rendering setup before studying or optimizing it
summary: Classify the rendering path from renderer settings, find engine renderer changes by marker or history, and locate project render hooks by searching for view extensions, global shaders and shader files, before planning study or optimization.
kind: method
scope: Unreal Engine 5 game projects, especially ones with a custom engine and in-project rendering plugins
keywords: [Unreal Engine, rendering, renderer settings, Nanite, Lumen, Virtual Shadow Maps, distance field shadows, static lighting, SceneViewExtension, ISceneViewExtension, RDG, FRDGBuilder, IMPLEMENT_GLOBAL_SHADER, usf, vertex factory, scalability, PSO, "Render Dependency Graph", "FRDGBuilder::AddPass", "FGlobalShader", "FDeferredShadingSceneRenderer::Render", "pipeline state object"]
status: active
checked_at: "2026-11-05"
context:
  engine: Unreal Engine 5.x
  platform: Windows desktop
---

## Guidance

Map the rendering setup in this order. Each step is a short read or search.

1. **Classify the rendering path** from `Config/DefaultEngine.ini` `[/Script/Engine.RendererSettings]`: `r.Nanite`, `r.DynamicGlobalIlluminationMethod` (Lumen), `r.ReflectionMethod`, `r.Shadow.Virtual.Enable`, `r.AllowStaticLighting`, `r.GenerateMeshDistanceFields`, `r.CustomDepth`, forward or deferred shading. Nanite is virtualized geometry, Lumen provides dynamic global illumination/reflections, and Virtual Shadow Maps (VSM) provide paged high-resolution shadows. Read the forward-shading switch separately. Availability of static lighting or mesh distance fields alone does not establish their use by any particular pass.
2. **Read quality tiers**: `DefaultScalability.ini`, `DefaultDeviceProfiles.ini` and the game user settings class that applies scalability, anti-aliasing and upscalers. Settings repeated at every tier (for example `r.ForceLODShadow`) deserve a look.
3. **Measure the engine renderer delta**: in the engine checkout (see [K-CODE-UE-ENGINE-CHECKOUT](K-CODE-UE-ENGINE-CHECKOUT.md)), search the studio's modification marker under `Renderer`, `RenderCore`, `RHI`, the RHI backends and `Engine/Shaders`, or filter `git log` to those paths. Use the ownership of the measured pass to choose where to investigate; engine edits also carry a merge cost.
4. **Find project render hooks**: search project `Source/` and `Plugins/` for `SceneViewExtension`, `FGlobalShader`, `IMPLEMENT_GLOBAL_SHADER`, `FRDGBuilder`, `AddPass`, scene proxies, vertex factories, and `*.usf` and `*.ush` files. Separate first-party code from third-party upscaler plugins (DLSS, XeSS, FSR), which are useful RDG reading material but not owned code. `ISceneViewExtension` supplies callbacks in the view lifecycle. `FGlobalShader` is a shader type independent of a material and `IMPLEMENT_GLOBAL_SHADER` registers its implementation. RDG (Render Dependency Graph) describes passes and their resource dependencies; `FRDGBuilder::AddPass` adds a pass to that graph. A vertex factory supplies mesh vertex data to a shader. A pipeline state object (PSO) bundles graphics pipeline state; PSO creation or compilation is one possible source of hitches.
5. **Find existing measurement**: in-game telemetry of render views, pixels, GPU memory or PSO hitches, and any profiling workflow the team already uses. Use it to rank candidates before changing structure.

Editorial judgment, not verified as a learning outcome: for study, start with a GPU frame capture (RenderDoc, `ProfileGPU` or Unreal Insights GPU tracks) and name each pass against `FDeferredShadingSceneRenderer::Render`; then follow one primitive from component to scene proxy, mesh batch, mesh pass processor and mesh draw command, using a project plugin with its own vertex factory as the concrete example. The smallest first-party view extension is a good first read for the render thread and game thread boundary.

## Applicability and exceptions

Steps 1 to 5 apply to any UE5 project. Step 3 needs engine source; with a launcher engine, treat the renderer as stock. For a Lumen and Nanite project, step 1 points to a different study and cost set (Lumen scene, Nanite rasterization, VSM page cost).

## Checks

- Every optimization candidate taken from this mapping is a hypothesis until a capture or telemetry measures it. Do not report a setting as a cost without measurement.
- Confirm that config values are not overridden by platform ini files, device profiles or user settings before treating them as effective.
- Large counts of lights or casters noted in code comments are inputs to measure, not evidence of cost.

## Evidence

A Windows UE 5.8 source/configuration review on 2026-11-05 identified renderer settings, engine modifications and project-owned rendering hooks. Effective runtime overrides, GPU cost and the proposed study sequence were not validated. Epic's RDG and FRDGBuilder references describe graph construction and pass scheduling. [Epic, Render Dependency Graph](https://dev.epicgames.com/documentation/unreal-engine/render-dependency-graph-in-unreal-engine?application_version=5.8) · [FRDGBuilder](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/RenderCore/FRDGBuilder?application_version=5.8)
