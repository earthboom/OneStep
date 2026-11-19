---
id: R-CODE-UE-EVIDENCE-PROXY
title: Self-consistent evidence can hide an incorrect native result
summary: A transition validator accepted compressed wall time and equal incorrect event values. Follow-up checks
  independently bind RNG execution, PCM output, transforms and save files to their expected conditions.
kind: error
scope: Native Unreal Engine 5.8.3 Win64 validation of transitions and scoped follow-up experiments
keywords:
- test oracle
- monotonic clock
- std::chrono::steady_clock
- simulation time
- negative control
- easing
- transition
- wall age
- event continuity
- 검증
- Unreal
- evidence
- wall-age
- elapsedSeconds
- fabricated-event
- mutation-test
- per-flight
- endpoint
- 검증누락
- 실제시간
- RNG
- session-role
- PIE
- packaged
- chronology
- overlap
- audio
- PCM
- channel leakage
- source owner
- GetAzimuth
- mixed output
- Gerstner
- finite difference
- GetSafeNormal
- squared tolerance
- UE_DOUBLE_PI
- SaveGame
- CRC32
- saved bytes
- restart PID
- stable ID
- game-state provenance
- mutation baseline
- setUpClass
- failed fixture
- negative test precondition
- music PCM
status: resolved
checked_at: '2026-11-14'
trigger: Accepting transition output from its own reported time, counters or neighboring event samples
symptom: Shortening wall time, zeroing elapsed duration or substituting equal but incorrect before/after values
  left the original check green
cause_status: confirmed
prevention: Derive expected event values independently, use the clock that governs the contract and verify
  that the final runtime and artifacts match the intended test conditions.
prevention_status: verified
---

## Expected and observed

The samples agreed with each other even when the transition ran at the wrong speed or both sides of an event were changed to the same wrong value.

## Cause and resolution

A test oracle supplies the expected outcome independently of the output it evaluates. Derive event values from the schedule and curve. For a real-time contract, compare the elapsed interval with a monotonic clock and account for sampling uncertainty. For a fixed-step simulation, compare with simulation time. In portable C++, `std::chrono::steady_clock` supplies monotonic intervals. It is an implementation option, not an assertion about the historical timer.

## Recheck and prevention

The historical negative controls shortened the observed interval, discarded duration and fabricated both event values. Each change exposed the original blind spot and was rejected after repair. Keep those failure classes separate. Measurement correctness alone does not establish a frame-rate budget or perceptual quality.

### Original Unreal easing run — 2026-11-12

The native easing fixture had eight scenarios and four curves. Correct-looking states alone did not establish real transition duration or event continuity. A fresh read-only review reproduced three accepted substitutions: each case's wall-time span halved, total elapsedSeconds set to zero, and before/after event values both changed to 999999. Equality and ordering checks still passed.

The checker compared cursor/value with reported age without connecting age to the actual monotonic clock. It compared event values only with each other. Native policy semantics were not found defective. The repaired checker independently derives each event value from the original case schedule and curve; both before and after must match it. Real-time ages match monotonic wall time within an explicit 5ms Tick-entry-to-log uncertainty. A clamped terminal sample allows one recorded frame interval. Total duration is separately bounded. Fixed30 simulation capture is validated against its own clock, not real recording time.

The same verification class appeared in earlier experiments: missing per-method frame data and a global jump peak concealed a per-flight failure; billboard overlap/alpha/shadow checks accepted absent or wrong pixels. These are related prevention examples, not proof that one generic validator covers every technology.

The three easing sensitivity tests failed before the repair and passed afterward: test_twice_speed_wall_clock, test_elapsed_duration_zero and test_event_both_values_fabricated. The final easing suite passed30tests. The earlier timestep suite passed19tests after two reproduced gaps; billboard passed26feature checks and4review checks after three reproduced gaps. Preserve independent expectations and negative controls when modifying these bounded checks.

This is historical local verification, not global CI enforcement or protection against rewriting every evidence file. Passing evidence integrity does not imply a requested FPS was reached: easing observed23.21/45.66/110.32frame-updateFPS under30/60/144caps;the missed rendering bands remain unverified. Scope excludes production physics, arbitrary animation blending and universal clock guarantees.

## Evidence

The original measurements and recordings are held with the historical experiment records.

Transition-validator behavior was historically checked under UE 5.8.3. The clock reference establishes the C++ contract only. [C++ working draft, time.clock.steady](https://eel.is/c++draft/time.clock.steady) · [Historical transition evidence](../../knowledge/sources.md#src-ue-lab-easing-results-md) · [Fixed-step checks](../../knowledge/game/K-GAME-TECH-TIMESTEP.md)

- Measured summaries and source fingerprints in Git history (`ffb221a:records/code/evidence/unreal-validation-2026-11-12.json`): Easing, Timestep and Billboard; includes review failure/success counts and historical input digests, not implementation code.
- [Easing conditions](../../knowledge/game/K-GAME-TECH-EASING.md), [timestep conditions](../../knowledge/game/K-GAME-TECH-TIMESTEP.md), [billboard conditions](../../knowledge/game/K-GAME-TECH-BILLBOARD.md).
- Original local evidence locators: `Results/Easing/review-red.txt`, `review-green.txt`, `feature-tests.txt`; `Results/Timestep/review-red.txt`; `Results/Billboard/review-red-all.txt`. These refer to the excluded local Unreal lab and are not published artifact links.

## RNG follow-up — 2026-11-13

ONE fresh read-only review of the bounded V55 implementation found2Important final-gate gaps,not an RNG algorithm defect. A real Game pilot relabeled final-pie was accepted because consumer/world/profile were internally consistent but not bound to the intended final matrix. Recorded UTC intervals were unused,so alternating names did not establish actual sequential/non-overlapping performance execution. Cause is confirmed by the read-only substitution and local controlled records.

Nine regressions first failed:Game substituted for PIE/package,swapped performance profile,media missing capture/wrongmode/wrongFPS,overlap,reversed order and capped60launch paired with reported0FPS. The repaired final matrix binds each required session name to consumer/mode/profile/FPS/capture;launch checks require corresponding arguments/viewport/fixed-time flags. UTC start/end intervals enforce the six expected cost runs' actual order/non-overlap. Final suite38passes. This safeguard is verified locally for this task,not global CI enforcement or a proof against forged/replaced complete histories.

A separate contract correction makes final costs EXACT512warmup+4096measured ticks,65536game+65536cosmetic calls/tick:536,870,912measured calls in EACH run. Preliminary2s+8s pilot is excluded. First/continuous/final counters,all states and raw-result checksums are independently checked. Fixed count implies elapsed time differs;record scoped RNG and whole-frame/cadence separately. No save-file,renderer or general validation-framework extension was made.

Local excluded-lab evidence locators:Results/Rng/review-red.txt(9failures),feature-tests.txt(38passes),review.json;finalize_rng.py check_matrix and rng_results.py check_launch/check_cost. [RNG application conditions](../../knowledge/game/K-GAME-TECH-RNG.md) distinguish ordered outcome isolation from statistical independence,network determinism or persistent recovery. Final actual native runs/media are required separately;these regression checks alone do not certify them.

## Spatial-audio follow-up — 2026-11-13

The first real output revealed two distinct implementation conditions: native5.8exact-left panning mapped to right (installed GetAzimuth zero-forward quadrant branch matches),and the lab's obstacles shared the source owner that native occlusion intentionally ignores. The prototype implements bounded explicit source-stereo panning and separates obstacle ownership;the engine is not patched. Starting master recording before active sources omitted dormant-submix startup silence;waiting for actual active/generated audio fixed the original.065s sample-clock check without fitting or weakening it. The first final PIE matrix also failed actual PCM because Editor focus loss set the global application volume0. The test enables/restores background audio only in its process,never persists it,and observes minimum application volume1 plus unmuted device;all v2 native evidence is rerun. These are scoped corrections,not stock-engine/global resolution.

Independent verification also needed stronger expectations: a20%incorrect occluded gain passed a broad qualitative bound,so measured440/4400Hz amplitudes now match installed one-pole analytic transfer×0.25gain within3%. ONE fresh review then reproduced43.6%opposite-channel amplitude accepted at an exact hard-pan axis and behavior/media players overlapping cost runs. Three controlled records first failed;actual normalized channel coefficients are now checked within.003raw/.015decodedAAC,and all finalnativeplayers require ordered UTCnon-overlap. The tolerances distinguish int16source quantization from lossy video audio;actual AAC is fullydecoded and compared with actual masterPCM. Final suite47passes;no rereview or general framework extension.

The archived measurements retain final identity,outputs,all6repeats,review/media checks;excluded local locators Results/Sound/review-red.txt,filter-gain-red.txt,feature-tests.txt,pilot-diagnosis.txt preserve the failure trail. [SOUND conditions](../../knowledge/game/K-GAME-TECH-SOUND.md) distinguish native attenuation/occlusion from explicit panning and bounded recording/media. This is local verified prevention,not globalCI,subjective headphone certification,physicalSPL or protection against replacing entire evidence histories.

## Water derivative probe and double constant — 2026-11-14

At h=.001cm,the raw finite-difference cross has squared length below GetSafeNormal default tolerance;all60normal observations incorrectly returned zero despite correct analytic normals. Installed Vector.h confirms squared-length comparison. Divide differences by2h to measure derivative vectors before normalization;do not relax1e-6normal tolerance. This was an observation defect. Separately,using float PI in double wavenumber/phase was an actual implementation defect. Literal-double wavenumber and one-wave/budget checks reproduced220checks/7failures before UE_DOUBLE_PI,then passed;final222checks include worst-crest and nonunit direction. Independent Python native-section replay and deliberate sine-only-normal/geometry mutations detect wrong output. These scoped prevention checks are demonstrated for the bounded water component;not a global numeric-precision guarantee.

## Game-state file/world provenance — 2026-11-14

Reported load success alone does not establish game restoration. Independently decode the raw envelope and canonical byte-array,verify pre-deserialization CRC rejection,selected generation,actual stable-ID prop visibility/rotation/avatar fields,and all-or-nothing missing-ID refusal. Actual restart requires distinct producer/consumer PIDs,matching produced file hashes and preserved parent files;reverse spawn order checks binding independence. Seven evidence tests deliberately substitute world/file/status/generation/false-success/role/chronology values and are rejected. These are demonstrated scoped prevention checks,not a new observed data-loss incident or complete UE serializer/security/power-loss proof.

## Negative mutation tests require an accepted baseline — 2026-11-14

A literal session-name replacement missed longer native.json/process.json/output.f32 fixture paths. Negative assertRaises tests used preserved failed PIE (passedfalse/minAppVolume0/semanticExit2),so they failed before exercising mutations and appeared green. Fresh review reproduced rejection of the unchanged fixture. Require verify_data(unmodified fixture) in setUpClass before any negative tests. This guard reproduced RED(error1/0tests);switching to accepted v2 fixture then passes8tests,including silence/omission,1600sample layer-boundary shift,5000sample unreported delay,stereo and consumer substitutions. Full746suite rerun after repair. Retained prereview green logs are invalidated prevention evidence. No native source change was needed;actual11player PCM validation remained valid. This demonstrates the scoped positive-precondition safeguard,not universal mutation-test quality.

## Native speed evidence semantics and measurement assumptions — 2026-11-14

Independent projection rejected interpreting WorldToPixel success as front/visible:the implementation usesabsW. Record projected plus signedclipW/front separately. Native blur does not guarantee a10%tonemapped finite-bar peak drop;retain failed pilots,report peak only,and verify spatial spread with matched native view/camera/flags,cut reset and off-as-on negative control. Final114movingframes/twocuts pass;zero-spread substitution fails. A green-target pixel mask excluded actualG240/B162 pixels;inspect actual RGB and fix segmentation while retaining geometry tolerance. A blur mutation selected a stationaryzero frame;its expected rejection failed,so select verified positive-blur movement before mutation. Allnegative fixtures first pass unchanged. These are scoped evidence checks,not renderer defects or universal metric guarantees.

## Bounded contact scans need censored outcomes — 2026-11-14

The LOW/excessive-bias scan found no ON/OFF ratio below.5 in199cm after the ideal contact edge. An offline fallback incorrectly stored200cm as a measured gap. An actual-pixel precondition confirmed no dark sample;asserting a null gap reproduced RED(200notNone). Store null plus noDarkSampleInScan/scannedAfterEdgeCm/threshold instead of false precision. Eight feature tests and full762 checks pass after correction. This is right-censored threshold sampling,not a measured200cm gap or proof that no shadow exists anywhere.
