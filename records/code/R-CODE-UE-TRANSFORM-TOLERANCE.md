---
id: R-CODE-UE-TRANSFORM-TOLERANCE
title: "An exact easing endpoint can yield a tolerance-limited component position"
summary: "A scalar easing calculation finished at its target while a scene component retained a slightly different position. Compare mathematical convergence and the published transform independently."
kind: error
scope: "UE 5.8.3, collisionless single-axis translation with a scene component"
keywords: ["USceneComponent::SetWorldLocation","SetWorldLocation","USceneComponent::InternalSetWorldLocationAndRotation","TVector::Equals","UE_KINDA_SMALL_NUMBER","easing","floating-point tolerance","endpoint","정밀도"]
status: resolved
checked_at: '2026-11-12'
trigger: "Asserting the same endpoint tolerance for the scalar curve and the observed scene transform"
symptom: "The curve reached its endpoint while the remaining native displacement fell below the setter's comparison threshold"
cause_status: confirmed
prevention: "Check the engine version and compare policy value, time and published component position separately"
prevention_status: verified
---

## Expected and observed

A strict comparison of the scalar curve confirmed completion, yet the world-space position read back from the component still differed from the target. Repeating the identical setter call did not guarantee a bit-exact endpoint.

## Cause and resolution

`USceneComponent::SetWorldLocation` requests world-space translation. In the historically inspected UE 5.8.3 path, `USceneComponent::InternalSetWorldLocationAndRotation` compared relative location using `TVector::Equals`, a per-component tolerance comparison. The default vector tolerance there was `UE_KINDA_SMALL_NUMBER`. A sufficiently small change could therefore leave the stored transform alone even after the scalar reached its target.

## Recheck and prevention

Historical negative controls rejected a wrong scalar value inside the native tolerance and independently rejected an incorrect published position. Retain a strict curve check, a time check and a native position check with a bound justified for the selected axes and parent transform. Reassess swept movement, scaled parents and other engine versions separately.

## Evidence

The API references identify the public types. The setter's internal comparison and the two rejected substitutions are historical UE 5.8.3 observations. The source experiment was not rerun in this review. [Epic, USceneComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/Components/USceneComponent?application_version=5.5) · [Epic, TVector](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Core/TVector) · [Easing evidence history](../../knowledge/sources.md#src-ue-lab-easing-results-md)
