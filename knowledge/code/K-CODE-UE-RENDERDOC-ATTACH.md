---
id: K-CODE-UE-RENDERDOC-ATTACH
title: Attach RenderDoc to an Unreal editor and get past the startup blockers
summary: The engine RenderDoc plugin loads only with -AttachRenderDoc or renderdoc.AutoAttach; with DLSS in the project, NGX init fails under RenderDoc and a modal dialog stalls editor startup until someone answers it.
kind: method
scope: Unreal Engine 5 editors on Windows D3D12 where a frame must be captured with RenderDoc, especially projects that ship the NVIDIA DLSS plugin
keywords: [Unreal Engine, RenderDoc, RenderDocPlugin, AttachRenderDoc, renderdoc.CaptureFrame, renderdoc.CapturePIE, DLSS, NGX, frame capture, editor startup hang, D3D12]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5.8 source build
  platform: Windows desktop, D3D12
  tool: RenderDoc 1.47
---

## Guidance

1. Install RenderDoc to its default path. The plugin looks for `renderdoc.dll` there.
2. Start the editor with `-AttachRenderDoc`. Without it, the log shows `RenderDoc plugin will not be loaded`. A ready plugin logs `RenderDoc plugin is ready!`.
3. If the project has the NVIDIA DLSS plugin, NGX init fails with `NVSDK_NGX_Result_FAIL_PlatformError`, and in the editor the plugin opens a modal Yes/No/Cancel warning titled `Warning -- DLSS incompatible with plugins and/or API capture tools`. Startup stops until it is answered. Yes continues and changes nothing. No continues and hides the warning. Cancel exits the editor. DLSS stays off for that run, so captures show the engine upscaler path instead of DLSS. Capture DLSS passes with NVIDIA Nsight Graphics instead.
4. Capture with `renderdoc.CaptureFrame` or the viewport toolbar button, or with `renderdoc.CapturePIE` for a game frame. Files go to `<Project>/Saved/RenderDocCaptures/`. On first launch RenderDoc asks about anonymous analytics. Choose no submission when work must stay local.

5. To list the pass tree without driving the UI, run `qrenderdoc.exe --python <script.py>`. The script runs in the embedded Python 3.8 with the `renderdoc` module. `__file__` is not defined there, so hard-code paths. End with `os._exit(0)`. An uncaught error leaves the UI open and the process waiting. Walk `controller.GetRootActions()` recursively, and name each action with `action.GetName(controller.GetStructuredFile())`.

## Applicability and exceptions

Applies to editor builds. The DLSS dialog is compiled only `WITH_EDITOR`, and it is skipped when unattended or when the project or local DLSS setting disables it. Other capture tools that NGX reports as incompatible behave the same way.

## Checks

- Editor log stops growing for minutes while the process still responds: check the main window title for a modal dialog before calling it a hang.
- When waiting for a line in the editor log after a restart, first confirm that the log header shows the new start time. The old log stays in place until the new process rotates it, so a wait loop can match stale lines.
- `Total Editor Startup Time` includes the time a modal dialog waited for the user.
- Do not split cost by marker range alone. Unreal GPU markers can nest wrongly in a capture, so one marker may span most of the frame. Count draws and dispatches per leaf pass instead.
- If `FetchCounters([EventGPUDuration])` returns an empty list in a scripted replay, measure pass times in the engine (`ProfileGPU`) instead.

## Evidence

Observed once in a UE 5.8 game project on Windows with D3D12 and the DLSS plugin (2026-11-06). The first editor run had no `-AttachRenderDoc` and logged that the plugin would not load. The second run loaded RenderDoc API v1.7.0, failed NGX init with PlatformError, and sat at the DLSS modal for about an hour. During that time the log was silent and the process reported Responding. After Yes, the viewport capture produced a 390 MB `.rdc` of about 8,000 events, which RenderDoc 1.47 opened with no problems. One wait loop matched the previous run's log before rotation and reported too early.

The same day, a scripted run of `qrenderdoc.exe --python` on a 554 MB PIE capture with 11,542 events extracted 843 marker rows in under ten minutes. The first attempt used `__file__`, failed before writing its log, and hung until the timeout. `EnumerateCounters` listed 16 counters, but `FetchCounters` for GPU duration returned no results. In the extracted tree, `FXSystemPreRender` spanned most of the frame, and a TSR marker contained 17 draws.
