---
id: K-GAME-TECH-SOUND
title: Model distance, occlusion and room response separately
summary: Verify attenuation, stereo direction, obstruction and room reverb separately in the mixed output.
  UE5.8.3 V22 covers listener axes, door occlusion, outdoor and indoor reverb, priority,
  boundary conditions and reversal during a fade.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["spatial", "audio", "Doppler", "reverb", "occlusion", "attenuation", "음향", "sound attenuation", "air absorption", "spatialization", "occlusion low-pass filter", "stereo", "equal-power", "listener", "GetAzimuth", "source owner", "master PCM", "submix", "recording", "door", "WASAPI", "NonRealtime", "좌우", "청취자", "문", "가림", "녹음", "V22", "Audio Volume", "room response", "early reflections", "late reflections", "reverb zone", "fade reversal", "잔향", "리버브", "실내", "실외", "구역 우선순위", "직접음"]
status: active
checked_at: "2026-11-22"
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE 5.8.3 guidance for attenuation, stereo direction, solid occlusion and native reverb transitions.
  panning_limit: Native5.8exactleftaxis failed;explicit source-stereo equal-power
    implemented,no enginepatch or cross-version guarantee
---
# Model distance, occlusion and room response separately

## Guidance

Use attenuation curves for level, air-absorption filtering for timbre, spatialization for direction, and occlusion/reverb for obstruction and room response. Relative radial motion can drive Doppler pitch when appropriate. Author parameters around listener position, not necessarily the camera.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

One ray is only an occlusion approximation; full propagation/diffraction is another system. Pitch and filtering should preserve gameplay cue recognition. Doppler is a proposed physical transfer, not a verified setting in every cited game.

**Sound attenuation** sets level by source–listener distance. **Air absorption** varies spectral filtering with distance, while spatialization supplies directional cues. Under Unreal's occlusion settings, a blocking trace can control both attenuation and low-pass filtering. Vary distance with line of sight unchanged, then add a wall at fixed distance to isolate the two effects. [Epic — Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)

### Room reverb at listener boundaries

For authored indoor and outdoor transitions, send the source to the native reverb path and keep its direct path active. Give overlapping Audio Volumes different priorities. The higher priority wins and the volume's fade setting controls the reverb parameter transition. Set the outdoor response and exit fade explicitly when return to a dry baseline matters. Use actual mixed output to check both the short transient and its tail after entry, exit, reentry and changes of direction. [Epic — Audio Volume Actor](https://dev.epicgames.com/documentation/en-us/unreal-engine/audio-volume-actor-in-unreal-engine) · [Epic — AAudioVolume, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/AAudioVolume?application_version=5.8)

## Checks

The first Unreal experiment checks scripted poses, listener rotation and wall and door output. The room reverb experiment checks listener boundary entry and exit, overlapping presets and reversal. Continuous traversal, subjective quality, Doppler and HRTF still need their own evidence.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Epic — Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine) — Official documentation; attenuation, air absorption, occlusion and reverb sends. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V22 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Native Unreal validation — 2026-11-13

The historical Unreal run and archived measurements:83policy/47evidence,PIE OFF/ON+packaged OFF/ON each17cases,6matched realtime costs,and native normal1xvideoWITHactualsound. Inner100cm/falloff900cm/outer1000cm,coincident/boundary/reentry,same live source/door,listener rotation and physical obstruction are checked using actual master float PCM,not parameters alone. 440/4400Hz magnitude and channel-energy projections independently bind output to native source/listener/box observations.

Use explicit equal-power source-stereo gains in this prototype;native attenuation and gain0.25/LPF1000Hz occlusion remain active,native spatializer/airfilter/focus/reverb disabled. The installed5.8.3 default panner actually mapped exactX0,Ynegative to right;GetAzimuth zero-forward quadrant handling matches. No coordinate nudging/enginepatch. Explicit panning uses listener-right dot normalized source direction,zero distance centered,and squared gains sum1. This validates left/right,not front/back/elevation localization or stock-panner correctness on everyversion.

Native occlusion ignores the source's owning Actor:own the physical walls/door appropriately,not under that ignored owner. Same door component physically moves open/closes/reopens. For background PIE,temporarily enable and then restore background audio in process;observe actual application volume/device muting,not merely component IsPlaying. v1 final PCM failed and v2 was fully rerun. PlayWhenSilent keeps the source active beyond audible range,so zero PCM is not a culling-cost result. Start master recording after real active/generated audio;the dormant initial submix can omit startup silence. Preserve sample-clock checks rather than fitting away missing data. Settled one-pole LPF expectations use b=exp(-2pi cutoff/rate);at1000Hz/48k,440/4400magnitudes=0.91544145/0.22471156. Check0.25gain×transfer,actual stereo coefficients (.003raw/.015decodedAAC tolerance) and finite/nonclipped output;do not infer filter response from a cutoff setting alone.

Six actual realtime players use16voices,same input/layout/closeddoor/device/1280x720/cap0,2swarmup+8smeasure;OFF/ON three each,UTCordered/nonoverlapping. Pre/post actual PCM calibration is outside measured interval;no capture/recording/readback during measurement. Whole wall/cadence and delayedGPU are not isolated audioCPU. See all repeats in archived measurements. Media-only builtin NonRealtime audio at30sim/30play is separate;encoded audio is decoded and checked,not a substituted input tone.

Scope excludes reverb,Doppler,HRTF,full propagation/diffraction,externalplugins,engine/renderer/framework improvements andpublication. No microphone/SPL,subjective hardware quality,hotplug,maxvoice or cross-version guarantee. Previous unrelated actualFPSgaps remain unverified. Latest22limited sheets/21without dedicated prototypes.

### Measured costs and retained limits

Measured whole-wall p95(ms),OFF:[8.743,8.803,8.698],ON:[8.716,8.612,8.677],on the fixed16voice workload above. These small whole-frame differences do not isolate occlusion CPU cost or establish a benefit from enabling it. Cadence-derived loopFPS is not physical monitor refresh. Use recorded conditions and all repeats,not a universal voice-capacity or frame-budget guarantee. The prototype uses PlayWhenSilent for input continuity;outside-range silence does not mean voice/DSP work was culled. Actual background PIE playback was enabled only in the testprocess and restored;v1silent/intermittent runs were rejected and the whole v2matrix remeasured.

## Native Unreal V22 room reverb validation

Set early and late reflection bypass flags explicitly when constructing a native preset. The UE 5.8.3 runtime default in this setup bypassed early reflections. Register a runtime-created sound class on the active device before playback and verify a nonzero source probe in the mixed output. Keep source gain and the dry path stable while changing the wet response. Give overlapping volumes distinct priorities and define the outdoor response and fade.

Exercise boundaries, entry, exit, reentry and reversal during a fade. Use an impulse or short tone to verify direct amplitude and residual decay in actual master PCM. Different authored decay settings can produce the same measured envelope. Measure zone selection, parameter interpolation and the remaining tail separately. Test the chosen presets and playback hardware in the production setup. [Epic — AAudioVolume, UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/AAudioVolume?application_version=5.8)
