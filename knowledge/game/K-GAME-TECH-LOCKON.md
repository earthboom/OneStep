---
id: K-GAME-TECH-LOCKON
title: Select stable lock-on targets before changing movement framing
summary: Score eligible targets by distance, screen direction, angle and line of sight.
  Engineering synthesis from target filtering/framing.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- lock-on
- target
- scoring
- Z
- targeting
- 락온
- hysteresis
- sticky target
- retention band
- weak actor identity
- same ID replacement
- opposite held keys
- target switching
- 대상 전환
- 타깃 유지
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 known5candidate lock-on only:37policy,198actual
    PIE cases observed30/60/144,3paired packaged costs and native1x media; no combat/camera/input-feel
    validation
---
# Select stable lock-on targets before changing movement framing

## Guidance

Score eligible targets by distance, screen direction, angle and line of sight. Use hysteresis so nearly equal candidates do not flicker, and explicit rules for target switching or loss. Orient camera and character independently; map strafe movement relative to the selected target when appropriate.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Nintendo's original staff interview connects Z-targeting to making a selected opponent legible and describes replacing the prototype marker with Navi. This supports target-selection feedback, not a claim of worldwide invention priority. A practical implementation should retain the current target until loss rules fire, score new candidates only on acquisition/switch, and separate character orientation, orbit movement and camera framing. Introduce target-loss grace only if occlusion policy allows it.

## Applicability and exceptions

The original staff account supports Z-targeting's marker/Navi feedback design. It does not establish worldwide first-invention priority or prescribe an exact scoring formula.

## Checks

Proposed: overlapping enemies, occlusion, targets crossing behind the camera and controller target-switch inputs.

## Evidence

- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US) — Official worked example; dot, distance and line-of-sight target filtering. Checked 2026-11-07, except items explicitly marked further reading.
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 2015 creator-authored article; camera-window, framing and smoothing. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V53 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [Nintendo — Where the Name Navi Came From](https://iwataasks.nintendo.com/interviews/3ds/zelda-ocarina-of-time/1/3/) — Original staff interview text retrieved by search; direct fetch timed out. Supports marker/Navi design account, not first-ever priority. Checked 2026-11-07.

### Local Unreal lock-on selection — 2026-11-11

[Native LOCKON results](../../prototypes/UnrealTechniqueLab/LOCKON-RESULTS.md) add actual UE5.8.3 selection/retention/switching for five known actors and one fixed perspective camera. Reuse TRACE center-point3D range/cone and first-hit simple Visibility with entire observer ignored. Prototype score4*(1-dot)+.1*distance/1000 and exact smallerID tie are authored choices, not Nintendo parameters; angular centering is not pixel distance. Acquire1000cm/45deg half-angle, retain1100cm/50deg; valid current remains despite improved competing score. Current outside acquisition can remain in retention and act as horizontal atan2(Y,X)/ID switching reference; no alternative keeps it. Explicit left/right chooses next/previous eligible with wrap. No automatic score-driven switch.

Rising-edge acquire/switch/release prevents held repeats and held reacquisition after loss; release wins and both raw direction levels held cancel even with staggered presses. Immediate occlusion/range/cone loss has no grace or fallback. Stable ID is not lifetime identity: invalidate current weak actor before candidate lookup so a replacement with the sameID cannot inherit selection. Missing/no-hit target is not visible. Scripted public API commands exercise the same policy, not physical keyboard/gamepad routing or player comfort.

Compiled37policy checks and six actual PIE worlds×33scenarios=198 at observed30/60/144 verify score ties, jitter retention, left/right wrap/held/repress/opposing keys, no candidates, inclusive entry/exit boundaries, wall/behind camera, overlapping projected targets, real Destroy/replacement, channel and self-ignore controls. Independent review's opposite-held defect was demonstrated RED then fixed GREEN; independent evidence mutation tests require the final33case positive fixture first. Historical32case pilot and wrong generic legacy test invocation are preserved but not final proof.

Three identical1280x720 packaged comparisons retain input sequence and selected IDs; one second switch pulses,2s warmup+10s measured, static5candidates with3eligible. Reference5rays/evaluation versus gated3 means40%fewer only for this workload. Report selection and full-frame p95/max, raw denominators and surrounding waits separately; query reduction is not an overall frame-speedup or production scalability claim. Native1x screenshots/videos are separate from performance. Physical input, moving camera/strafe, combat AI, skeletal exposure, broad candidate discovery, network authority and general multi-NPC budgets remain untested. Renderer/Present/save/framework/tools were not optimized. Installed5.8.3 headers and actual native runs establish the local API; rolling web API pages were empty/inaccessible on this pass.
