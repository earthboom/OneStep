---
id: K-GAME-TECH-IK
title: Fit animation contacts with constrained inverse kinematics
summary: Trace the intended foot contact, place an effector and constrain knee direction
  with a pole/joint target. IK does not create a complete gait or correct unreachable
  targets automatically.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- IK
- FABRIK
- foot
- placement
- heel
- retargeting
- 역운동학
- static support
- sole anchor
- pelvis budget
- half blend
- previous bone buffer
- PoseableMesh
- three point support
- swing release
- 발 고정
- 골반 보정
- 계단
- 접지
status: active
checked_at: '2026-11-11'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 V37 real68bone skin/static support only:47policy,108actual
    PIE observed30/60/144,3paired package costs and native1x media; V08/broaderIK
    untested
---
# Fit animation contacts with constrained inverse kinematics

## Guidance

Trace the intended foot contact, place an effector and constrain knee direction with a pole/joint target. Transform all inputs into compatible coordinate spaces; offset pelvis if necessary and blend IK by gait phase. Use two-bone analytic solvers for limbs and iterative chains such as FABRIK where needed.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Implementation synthesis from Two Bone IK: query the support plane, construct the desired foot transform including shoe sole/heel offset, solve the leg with a stable knee target, and compensate pelvis/root only within allowed limits. Blend contact constraints by gait state so a swinging foot is not permanently pinned. If art uses shortened bones to preserve character height, separately validate reach, seated contacts and the unchanged gameplay capsule. A visual bone adjustment must not silently alter competitive hit geometry.

## Applicability and exceptions

IK does not create a complete gait or correct unreachable targets automatically. Heel height, skeleton proportions, interaction sockets and gameplay collision need an explicit contract; particular commercial games' shin-shortening claims remain unverified.

## Checks

Proposed: stairs, slopes, moving surfaces, sitting, hand contacts and extreme footwear; inspect foot sliding and knee flips.

## Evidence

- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine) — Official documentation; effector, joint target and coordinate spaces. Checked 2026-11-07, except items explicitly marked further reading.
- [Epic — FABRIK AnimBP Node](https://dev.epicgames.com/documentation/unreal-engine/fabrik-animation-blueprint-in-unreal-engine?lang=en-US) — Official documentation text; arbitrary-length chain and effector. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V08, V37 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine) — Effector, joint-target and coordinate-space contract; high-heel procedure is proposed transfer, not confirmation of specific commercial games. Checked 2026-11-07.

### Local Unreal static-foot placement — 2026-11-11

[Native V37 results](../../prototypes/UnrealTechniqueLab/FOOTIK-RESULTS.md) add real UE5.8.3 skin evidence: installed UE4Mannequin68bones/ThirdPersonWalk1s, hidden source animation→visible PoseableMesh→native AnimationCore TwoBoneIK without stretch.32installed assets retain exact bytes/original package paths. Sole model uses bind-foot frame,6cm forward center and imported-bounds minimumZ; probe center/heel-8/toe+12,100up/120down, ignore character. Require3hits,≤35deg, normal dot≥.999 and plane distance≤.25cm. This is a calibrated three-point model, not every skinned vertex or an arbitrary shoe/foot polygon.

Authored half-cycle stance/.06cycle ramps latch a world anchor and release swing; use actual animation contact curves when transferring. Blend from ORIGINAL source ankle to contact and compute pelvis against that exact endpoint. Do not multiply full-contact pelvis by alpha and blend again from a shifted ankle: that rejected the pilot's valid half-blend. Shared pelvis≤20cm downward is validated for compatible legs before commit; monotonic candidate removal leaves0shift if none survive. Preserve limb shell[|upper-lower|+.1,upper+lower-.1]cm; stable pole prevents tested knee flips. Rejected leg retains local source pose, although another solved leg's pelvis may move its ancestors.

The real static skin exposed duplicate pose publication: source and corrected visible pose were both finalized in one frame, leaving15.6–38.1cm previous/current bone-buffer differences and visible blur. Read component-space source bones from the hidden source, copy local pose, then publish only the final visible pose once. A native static-history assertion caught the original failure and verifies<.05cm after first3case samples; no renderer/AA/motion-blur setting was changed. This is a scoped skeletal integration correction, not global engine enforcement.

Policy47 and six actual PIE worlds×18cases=108 at observed30/60/144 check support edges, stairs, slopes, unknown ground, reach/pelvis limits, translated/yaw spaces, stance drift, swing release, half-blend, actual3D sole-anchor error/normal/limb length/knee sign and unchanged capsule transforms/dimensions/sweep outcomes. Disabled IK is a real source-pose sensitivity control. Full-contact error0with full=0 is unavailable; blending deliberately allows partial contact error. Capsule fixture is scripted, not CharacterMovement clearance/walkability proof.

Adoption limits remain explicit: lower-flat-12cm right leg needs23.778cm pelvis;35deg support accepts geometrically but this authored pose needs21.000/33.019cm. These legs fall back at20cm, not successfully reach the ground.35.001deg rejects support. Three matched1280x720 off/on package pairs,2s warmup+10measured retain common animation/copy/final skin/camera/lighting; on6support rays/evaluation, off0. Foot-stage timing includes common final pose publication, not pure solver overhead. Full-frame p95/max/raw denominators and actual FPS remain separate from normal1x capture. One character does not establish a multi-character budget or general frame speedup.

External Two Bone IK documentation is conceptual/rolling5.9; installed5.8.3 headers/runtime establish local API use. This covers V37 only. Footwear/V08, FABRIK, moving surfaces, whole-body/hand/seated IK, retargeting, new locomotion/networking and player-rated animation feel remain untested. No generic validation-tool/renderer/Present/save optimization or implementation publication was added.
