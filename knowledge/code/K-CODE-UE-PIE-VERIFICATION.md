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
keywords:
- Unreal
- UE5.8.3
- PIE
- UnrealEditor
- Automation
- FStartPIECommand
- WorldType
- runtime-verification
- rendered-viewport
- 언리얼
- 에디터
- 실제월드
- 자동화
- 검증
- admission
- queue-cap
- token-bucket
- rejection
- goodput
- 거부율
- 입장
- 제공량
- Unreal Insights
- occlusion query
- horizon pruning
- same-binary
- frame alignment
- 프레임 지연
- packed priority
- heap sift
- PriorityKey
- plannerPeak
- per-request equivalence
- 계획 처리
- owned snapshot
- record DOM
- saveTail
- private commit
- PagefileUsage
- snapshot lifetime
- 스냅샷 저장
- owned async save
- publicationToAck
- pending exit drain
- writer backpressure
- full input lifetime
- 비동기 저장
status: active
checked_at: '2026-11-11'
context:
  engine: UE5.8.3 installed Windows D3D11
  verification: Three actual PIE consumers and final full-cook Game consumers executed;
    no OS permission action
  admission_evidence: UE5.8.3 paired six-policy overload comparison; accepted latency/all-offered
    goodput/rejection and full frames; finite static graph scope
  hitch_evidence: UE5.8.3 same-binary3paired admission profiles; named frame traces;
    scene-local query suppression and cardinal reservation proof limits
  planner_evidence: UE5.8.3 equivalent packed-priority heap; scoped bit-domain/path/order/native/profile
    and3paired frame evidence
  snapshot_evidence: UE5.8.3 owned records/direct JSON; exact byte/value/order/lifetime/native
    safety,3paired transition/save/process-memory observations
  async_save_evidence: UE5.8.3 detached full input; same-binary owned-sync/async3pairs,
    exact records, queue/failure/pending-exit controls; finished-fixture rendering
    only
---
# Verify actual Unreal PIE through the native Editor automation API

## Guidance

For legitimate engine test work, inspect the installed `UnrealEd/Public/Tests/AutomationEditorCommon.h` and implementation rather than assuming manual toolbar input is the only route. In the checked engine, `FEditorLoadMap`, `FStartPIECommand(false)` and `FEndPlayMapCommand` are latent commands that load a map, request actual play and end it. Wait for the actual play world and consumer completion; a queued start request alone is not success.

Keep `UnrealEd` dependencies conditional on `Target.bBuildEditor` and Editor tests inside appropriate Editor/automation compile guards. Run the Editor with a targeted Automation command and exported results. Do not use NullRHI as proof of rendered play. A `-game` process is a standalone Game world and must not substitute for PIE.

Independently require actual `EWorldType::PIE`, the expected mode/consumer, meaningful runtime checks, nonzero rendered viewport and scenario completion. Compare the Editor DLL, project/config/source identity with the built artifact. Reject failed/missing/stale/unfinished test and native reports even if the process exits0. Preserve captures in new session directories and distinguish fixed-time readback from unbiased performance observations.

## Applicability and exceptions

This method executes authorized engine operations; it does not answer security permission requests or change OS security/privacy settings. A manual UI restriction is not itself proof that the native engine capability is unavailable. If the engine API is blocked or the actual world/render check fails, retain that specific blocker rather than substitute another world type or manufacture a pass.

The demonstrated fixture used Engine Entry/Cube assets and a custom native GameMode/Actor. It does not establish all project assets, plugins, networking or rendering backends. When DLL locks require ending an Editor, identify only the owned disposable test instance and its work state; do not terminate unrelated or unsaved user work.

## Checks

The [local gate](../../prototypes/UnrealTechniqueLab/EDITOR-GATE-RESULTS.md) ran camera/hitscan/path in actual WorldType3 with two Automation tests and73 runtime checks per process,270 gameplay ticks and native viewport videos. The expected-mode test caught an intentionally hardcoded path assumption under a camera launch. A missing runtime save bridge failed before correction.

Seven schema regressions reject standalone WorldType1, wrong mode, unfinished path, no rendered viewport, wrong elapsed response and nested failed checks. This safeguards the checked harness, not every future implementation. Recheck startup/teardown, current-world ownership, capture dimensions, build hashes and actual completion in the receiving project.

## Evidence

- [Results, raw reports, build/cook evidence and source hashes](../../prototypes/UnrealTechniqueLab/EDITOR-GATE-RESULTS.md).
- [Frozen Editor test](../../prototypes/UnrealTechniqueLab/Results/Sources/editor-gate/Source/UnrealTechniqueLab/LabTests.cpp), [native report gate](../../prototypes/UnrealTechniqueLab/Results/Sources/editor-gate/Test-PieReport.ps1), [runner](../../prototypes/UnrealTechniqueLab/Results/Sources/editor-gate/Run-Pie.ps1).
- [Actual regression results](../../prototypes/UnrealTechniqueLab/Results/pie-contract-green.txt) and [installed primary source hashes](../../prototypes/UnrealTechniqueLab/Results/editor-gate-primary-sources.json), inspected2026-11-09. Native API/source execution is local evidence; no claim of compatibility with later engine releases.

### Native viewport content follow-up — 2026-11-09

[TrafficLab final movies](../../prototypes/UnrealTechniqueLab/TRAFFIC-RESULTS.md) show why positive viewport dimensions and a passing physics report are insufficient visual acceptance: an automatic UE5.8.3 orthographic view-origin correction undid the camera XY offset and placed the narrow portal behind the HUD. Installed CameraComponent.cpp:482–486 and SceneView.cpp:589–596 identified the path; actual original PNGs confirmed failure after a position-only change. Explicit near/far planes and disabled automatic origin updates fix this static diagnostic camera, with real projected portal coordinates and corrected native media. Do not transfer these settings as a general moving-camera/render default. Inspect actual pixels and geometry framing for the feature being demonstrated; retain failed captures and exact source identity rather than relabeling an old video final.

### Native StreamLab ledger and mesh pose — 2026-11-09

[StreamLab](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.md) now verifies ten actual PIE and ten full-cook standalone scenarios with identical per-ID action records, native source/module/player/harness identity, full-map fixed-camera framing and original native media. Inspect the **mesh component world position**, not only Actor/capsule position and mesh scale: an offset child visual can otherwise pass physical audits. A displaced-mesh sensitivity test failed before this check and passes after it. Preserve full five-fraction first/interior/terminal native coverage before pooled despawn. Request epochs and oldest pending ID must reconcile with the lifecycle ledger independently of aggregate throughput. Model25 and96 focused regressions pass; this does not validate arbitrary physics/continuous NavMesh or infinite-time fairness.

### Bind policy identity and retained refusals — 2026-11-09

[AdmissionLab](../../prototypes/UnrealTechniqueLab/ADMISSION-RESULTS.md) adds actual PIE12/standalone12 paired policy cases. Corrupt the displayed policy identity and require native configuration binding to fail, as well as capsule/visual radius and mesh-world-pose/wall-query controls. Replay original offered IDs/epochs, queue-full refusals, accepted FIFO prefix and integer credits independently; aggregate throughput alone cannot establish service or bounded waiting. Keep actual camera-ready completion, five first/interior/terminal samples and approved source/project/module/player/harness dependency hashes. Native capture/15x motion is separate from no-capture real-time frame comparison; PIE viewport can differ and is not the performance input.127focused regressions pass; actual media/decode/hashes and finite geometry/queue limits remain attached.


### Bind the actual optimization and viewport — 2026-11-10

[Native profile regression](../../prototypes/UnrealTechniqueLab/HITCH-RESULTS.md) adds exact1280x720 acceptance and actual viewport DisableOcclusionQueries/kernel-policy binding. Deliberately corrupt view flag/kernel binding; reject mislabeled evidence. Fresh review demonstrated that positive dimensions and inherited policy-only acceptance were insufficient; two RED→GREEN controls close those gaps. Trace launch defaults to profile-aware acceptance; historical old binaries use explicit legacy acceptance. Two actual PIE cases match new packaged service/safety; all12packaged fixtures match prior full behavior records. Freeze source/config/project/DLL/player/harness and retain native trace/media identities.148Python checks are executed evidence, not a universal attestation scheme.


### Bind actual planner profile and trace launcher — 2026-11-10

The [actual UE5.8.3 equivalent-heap experiment](../../prototypes/UnrealTechniqueLab/PLANNER-RESULTS.md) verifies actual packed-heap/profile/detailed-clock flags, wrong-kernel sensitivity, exact1280x720 benchmark/capture and real editor-only PIE safety dimensions. Freeze the actual trace launcher and verify its recorded hash; a self-reported digest alone is insufficient. Final coarse trace forbids per-call diagnostic clocks, with separate detailed sessions and controlled failing tests. Actual PIE2cases are safety/service evidence and never timing inputs. New model11 plus previous hitch18/policy18/stream25/traffic26/crowd13/representative73 and161Python checks are retained with native build/source/harness/media identities. Equal paths/order and raw frame conservation remain required.


### Verify frozen record values, order and lifetime — 2026-11-11

The [native owned-snapshot comparison](../../prototypes/UnrealTechniqueLab/SNAPSHOT-RESULTS.md) captures deep-owned job/path/string/ledger-ID/coverage data at the same simulation boundary and emits it with the engine JSON writer at save.12compiled checks compare full legacy bytes, including field/record order, escaping, fine doubles/sentinels, permuted IDs, empty arrays, bad coverage, source mutation and destruction. Native three pairs compare all values/types/member/array order at identical epochs; duplicate JSON members are rejected. Twelve packaged completed cases and two actual PIE compare original per-ID/action/coverage/audit/service. Actual serializer binding has deliberate corruption sensitivity, and actual normal/trace launchers/dependencies/source/binary are frozen.177Python checks plus prior model/native regressions retained.

The typed record snapshot owns primitive/container data, but the current full SaveMain also reads live world/root metadata/frame DOM and stays on the game thread. **Do not move unchanged SaveMain to a worker**. Async use needs ownership for every input, bounded queued memory, ordering/error propagation/backpressure and new target checks; no worker was implemented here. Standard encoder preserves legacy numbers/escaping; do not hand-concatenate JSON or retain mutable live references for old cases.


### Detach every save input before worker dispatch — 2026-11-11

The [native owned-sync/async verification](../../prototypes/UnrealTechniqueLab/ASYNC-SAVE-RESULTS.md) supersedes the earlier snapshot-stage statement that no worker exists. Legacy SaveMain remains a GT-only compatibility path; do not move it unchanged. The new path clones root/case metadata into a uniquely owned primitive tree, deep-owns all current/case job/path/FString/ledger-ID/coverage containers, and transfers typed frame rows. Worker input has no UObject, Actor, world or shared mutable JSON reference. Sync and async execute the same standard writer and temporary-file→rename publication. Accepted work is FIFO, single consumer, capacity2 including active, charged64MiB; overflow preserves caller ownership. Explicit completion/error and zero remaining work are required. Normal Poll checks readiness without waiting; EndPlay intentionally drains and may block. Buffered close/rename is not fsync durability, crash recovery or cancellation.

Fourteen compiled checks include full byte equality after all source metadata/world/records are changed/destroyed, actual historical39-field frame oracle, escaping/fine doubles, queue overflow/resubmission, FIFO sequence, separate worker identity, write failure, byte bound, cyclic metadata rejection and destructor drain. Strict native JSON rejects duplicate members and compares all record types/values/member+array order/no omissions at identical epochs against original outputs:3paired performance runs,12packaged cases and2actual PIE cases. A pending-exit native player starts shutdown with1accepted save, drains it, publishes the same records and ends with0outstanding. PIE is safety evidence at its recorded viewport, not1280x720 timing evidence.
