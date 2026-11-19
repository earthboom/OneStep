---
id: K-CODE-UE-RENDERDOC-ATTACH
title: Attach RenderDoc to an Unreal editor and get past the startup blockers
summary: "Attach the engine's RenderDoc plugin, verify readiness in the current Editor log and inspect modal warnings when startup stalls. NGX initialization and DLSS availability depend on the plugin and capture environment."
kind: method
scope: Unreal Engine 5 editors on Windows D3D12 where a frame must be captured with RenderDoc, especially projects that ship the NVIDIA DLSS plugin
keywords: [Unreal Engine, RenderDoc, RenderDocPlugin, AttachRenderDoc, renderdoc.CaptureFrame, renderdoc.CapturePIE, DLSS, NGX, frame capture, editor startup hang, D3D12, "renderdoc.AutoAttach", "Render Hardware Interface", "EventGPUDuration", "ProfileGPU", "GetRootActions"]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5.8 source build
  platform: Windows desktop, D3D12
  tool: RenderDoc 1.47
---

## Guidance

1. Configure the RenderDocPlugin to locate `renderdoc.dll`, using its installation path or the plugin settings supported by that engine version.
2. Start the editor with `-AttachRenderDoc`. Without it, the log shows `RenderDoc plugin will not be loaded`. A ready plugin logs `RenderDoc plugin is ready!`.
3. In the observed combination of NVIDIA DLSS (Deep Learning Super Sampling) and RenderDoc, initialization of the NVIDIA NGX SDK failed with `NVSDK_NGX_Result_FAIL_PlatformError`, and in the editor the plugin opens a modal Yes/No/Cancel warning titled `Warning -- DLSS incompatible with plugins and/or API capture tools`. Startup stops until it is answered. Yes continues and changes nothing. No continues and hides the warning. Cancel exits the editor. DLSS stays off for that run, so captures show the engine upscaler path instead of DLSS. Verify support separately when the requested capture must include DLSS.
4. Capture with `renderdoc.CaptureFrame` or the viewport toolbar button, or with `renderdoc.CapturePIE` for a game frame. Files go to `<Project>/Saved/RenderDocCaptures/`. On first launch RenderDoc asks about anonymous analytics. Choose no submission when work must stay local.

5. To list the pass tree without driving the UI, run `qrenderdoc.exe --python <script.py>`. The script runs in the embedded Python 3.8 with the `renderdoc` module. `__file__` is not defined there, in the observed context, so pass explicit input and output paths. Arrange orderly closure and an explicit failure exit. An uncaught error leaves the UI open and the process waiting. Walk `controller.GetRootActions()` recursively, and name each action with `action.GetName(controller.GetStructuredFile())`.

## Applicability and exceptions

Applies to editor builds. The DLSS dialog is compiled only `WITH_EDITOR`, and it is skipped when unattended or when the project or local DLSS setting disables it. Other capture tools that NGX reports as incompatible behave the same way.

## Checks

- Editor log stops growing for minutes while the process still responds: check the main window title for a modal dialog before calling it a hang.
- When waiting for a line in the editor log after a restart, first confirm that the log header shows the new start time. The old log stays in place until the new process rotates it, so a wait loop can match stale lines.
- `Total Editor Startup Time` includes the time a modal dialog waited for the user.
- Do not split cost by marker range alone. Unreal GPU markers can nest wrongly in a capture, so one marker may span most of the frame. Count draws and dispatches per leaf pass instead.
- If `FetchCounters([EventGPUDuration])` returns an empty list in a scripted replay, measure pass times in the engine (`ProfileGPU`) instead.

## Evidence

In a UE 5.8 source-build Editor on Windows D3D12 (2026-11-06), RenderDoc API 1.7.0 attached, NGX initialization failed, and an Editor modal held startup. Acknowledging it allowed an .rdc capture to open in RenderDoc 1.47 with DLSS inactive. A stale log caused a false readiness result. Scripted replay enumerated actions; a missing script-path variable stalled one run, and GPU-duration queries yielded no usable timings. Other plugin versions and DLSS-enabled capture were not tested. [Epic, Using RenderDoc with Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-renderdoc-with-unreal-engine?application_version=5.8)
