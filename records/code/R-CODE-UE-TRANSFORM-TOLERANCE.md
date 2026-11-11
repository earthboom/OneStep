---
id: R-CODE-UE-TRANSFORM-TOLERANCE
title: Exact easing endpoint was mistaken for an exact native component update
summary: Policy reached400cm while SetWorldLocation retained399.9999445cm because the installed engine skips sub-tolerance movement; separate strict policy-value checks from the one-axis native transform tolerance.
kind: error
scope: UE5.8.3 SceneComponent SetWorldLocation; collisionless one-axis scalar easing fixture
keywords: [Unreal, SetWorldLocation, endpoint, precision, tolerance, UE_KINDA_SMALL_NUMBER, policy-value, tiny-movement, 끝점, 정밀도]
status: resolved
checked_at: '2026-11-12'
trigger: Requiring near-bit-exact native mesh endpoints after small eased movement
symptom: Policy value and cursor completed at400cm and2s but actual component remained399.9999445cm and failed a1e-8cm publication assertion
cause_status: confirmed
prevention: Check installed setter tolerance and retain independent policy-value, time and actual-transform assertions with separately documented bounds
prevention_status: verified
---

## Expected and observed

The easing pilot expected SetWorldLocation to publish an arbitrarily small final displacement. Case4 failed with maximum native publication error0.000055478756cm while the scalar policy finished exactly at400cm. Repeating the final update did not establish bit-exact native placement.

## Cause and resolution

Installed UE5.8.3 SceneComponent.cpp InternalSetWorldLocationAndRotation compares NewLocation.Equals(GetRelativeLocation()); Vector.h supplies UE_KINDA_SMALL_NUMBER as the default vector tolerance. A sub-tolerance update can be skipped. The original1e-8cm native assertion was incompatible with this chosen public API;the engine was not modified.

The fixture now records scalar policy value separately and checks it against an independent curve within1e-7cm. Actual native x uses1e-4cm for this one-axis fixture. Time/cursor checks retain their separate bounds. No temporary offset, direct setter bypass or renderer change was used. This bound does not transfer unchanged to arbitrary parent scales, multiple moving axes, collision resolution or other engine versions.

## Recheck and prevention

The original failing pilot remains in the local evidence. The corrected pilot and all final96method-case observations passed the declared distinct checks. test_policy_endpoint_value_wrong rejects a1e-5cm scalar endpoint error even though it fits the looser native tolerance;test_native_publication_wrong rejects a changed actual component position. Final30easing evidence tests passed. This demonstrates the specific separation, not globally enforced engine precision.

## Evidence

- [Committed measured summary and source fingerprints](evidence/unreal-validation-2026-11-12.json), Easing precision finding and sensitivity checks.
- [Reusable easing conditions](../../knowledge/game/K-GAME-TECH-EASING.md).
- Historical installed source symbols: `USceneComponent::InternalSetWorldLocationAndRotation`, `TVector::Equals`; observed version5.8.3. No engine source or physical installation binding is published.
- Original local locator `Results/Easing/pilot-v2-60/native.json`; corrected `pilot-v3-60` and final runs. Source implementation, runtime artifacts and media remain excluded.
