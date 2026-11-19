---
id: K-CODE-UE-PIE-VERIFICATION
title: Verify actual Unreal PIE through the native Editor automation API
summary: Use the installed engine's Editor automation API for authorized PIE tests,
  then independently check WorldType, the requested consumer, rendering, runtime results
  and build identity. Standalone game execution and a successful process exit do not
  establish PIE.
kind: method
scope: Unreal Engine 5.8.3 installed Windows C++ Editor and Development Game verification;
  adapt and recheck APIs for other versions or projects
keywords: ["Play In Editor","PIE","UnrealEd","FEditorLoadMap","FStartPIECommand","FEndPlayMapCommand","UWorld::WorldType","EWorldType::PIE","Target.bBuildEditor","latent automation command","rendered viewport","orthographic camera","snapshot lifetime","backpressure","에디터 자동화","플레이 월드"]
status: active
checked_at: '2026-11-11'
context:
  engine: "UE 5.8.3 Windows D3D11, Editor automation and separately cooked Development Game"
  verification: "Historical world, rendering, runtime-policy and owned-output checks; other projects and engine releases require rechecking"
---

## Guidance

Use the Editor automation commands in the installed engine's `AutomationEditorCommon.h`. In UE 5.8.3, `FEditorLoadMap` loads the test map, `FStartPIECommand(false)` requests Play In Editor (PIE) and `FEndPlayMapCommand` requests its end. Latent commands can span frames. Wait until the play world exists and the tested consumer finishes before teardown. Gate the `UnrealEd` module dependency on `Target.bBuildEditor` and use the Editor/automation compile guards appropriate to the target.

Inspect the test world's `UWorld::WorldType` against `EWorldType::PIE`. A standalone `-game` launch has a game world and exercises a separate contract. Match the launched Editor module and its source, configuration and test driver to the intended build. Require both the automation result and the consumer's runtime result. Rendering claims require a rendering backend, the expected viewport, and actual captured content. Fixed-time video and ordinary packaged frame timing answer different questions.

## Applicability and exceptions

Historical checks exercised native C++ Editor automation and separately cooked Development Game builds on UE 5.8.3, Windows/D3D11. Verify the latent command signatures, play-world creation, camera path, teardown and assets for each receiving project. Networked PIE, other graphics backends and live autosave during simulation need independent checks.

## Checks

- Reject a standalone world, wrong consumer, stale result, unfinished activity, nested failure, missing viewport or unexpected dimensions. Check rendering flags and test mode against the running implementation. Deliberately altering a label, policy or trace launcher must invalidate its evidence.
- Inspect pixels at the relevant screen position and the visual mesh component's world transform alongside the collision component. In an orthographic camera, automatic view-origin or near/far-plane adjustment can shift intended framing. Compare actual pixels and projected positions, including HUD occlusion. Test the first, intermediate and terminal states before despawn.
- Reconstruct original request IDs, arrivals, admissions, refusals, completions and oldest waiting request from individual records when checking service. Compare implementations at identical simulation times and validate the observed settings and results of both runs.
- For snapshot verification, compare value types, escaping, precision, member/array order when contractual, and omitted/duplicate members. Mutate and destroy source data before writing. Detach all inputs before background work, including metadata and strings, keeping live `UObject` and world access on the game thread. Exercise bounded input ownership, refusal and retry, FIFO completion, write failure, and pending work at exit. Normal polling can be nonblocking while shutdown drains. A temporary-file rename does not establish crash durability.

## Evidence

The historical reports below recorded actual PIE and packaged results, including a standalone-world rejection, detection of displaced visual geometry and incorrect runtime settings, output parity, and draining an accepted save during shutdown. A partially owned snapshot still read live world data. A later path deep-owned all writer inputs and tested them after source destruction. The original reports establish these observations within their tested conditions. No new Editor, performance or gameplay run was performed in this review.

- [Epic, EWorldType::Type](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/EWorldType__Type?application_version=5.8) · `UnrealEd/Public/Tests/AutomationEditorCommon.h` (UE 5.8.3)
- [PIE automation](../sources.md#src-ue-lab-editor-gate-results-md) · [Orthographic framing](../sources.md#src-ue-lab-traffic-results-md) · [Mesh transforms](../sources.md#src-ue-lab-stream-results-md) · [Queue and policy identity](../sources.md#src-ue-lab-admission-results-md)
- [Viewport and trace settings](../sources.md#src-ue-lab-hitch-results-md) · [Planner comparison](../sources.md#src-ue-lab-planner-results-md) · [Snapshot parity](../sources.md#src-ue-lab-snapshot-results-md) · [Worker completion](../sources.md#src-ue-lab-async-save-results-md)
