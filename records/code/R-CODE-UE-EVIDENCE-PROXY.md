---
id: R-CODE-UE-EVIDENCE-PROXY
title: Independent native-result checks accepted self-consistent wrong evidence
summary: Easing checks accepted a halved wall-time span and fabricated equal event values; independent clock and event-time expectations rejected them after three failing sensitivity tests.
kind: error
scope: OneStep Unreal technique experiments; UE5.8.3 Win64/DX11; bounded result validation
keywords: [Unreal, evidence, transition, wall-age, elapsedSeconds, fabricated-event, mutation-test, per-flight, endpoint, 검증누락, 실제시간]
status: resolved
checked_at: '2026-11-12'
trigger: Validating native transition or rendering results from reported state, counters and passed flags
symptom: Halving wall-time spans, setting elapsedSeconds to zero or replacing both event values with 999999 still passed the original easing validator
cause_status: confirmed
prevention: Derive state and event values independently from authored times and bind runtime age to wall time; demonstrate rejection of missing and substituted evidence
prevention_status: verified
---

## Expected and observed

The native easing fixture had eight scenarios and four curves. Correct-looking states alone did not establish real transition duration or event continuity. A fresh read-only review reproduced three accepted substitutions: each case's wall-time span halved, total elapsedSeconds set to zero, and before/after event values both changed to 999999. Equality and ordering checks still passed.

## Cause and resolution

The checker compared cursor/value with reported age without connecting age to the actual monotonic clock. It compared event values only with each other. Native policy semantics were not found defective. The repaired checker independently derives each event value from the original case schedule and curve; both before and after must match it. Real-time ages match monotonic wall time within an explicit 5ms Tick-entry-to-log uncertainty. A clamped terminal sample allows one recorded frame interval. Total duration is separately bounded. Fixed30 simulation capture is validated against its own clock, not real recording time.

The same verification class appeared in earlier experiments: missing per-method frame data and a global jump peak concealed a per-flight failure; billboard overlap/alpha/shadow checks accepted absent or wrong pixels. These are related prevention examples, not proof that one generic validator covers every technology.

## Recheck and prevention

The three easing sensitivity tests failed before the repair and passed afterward: test_twice_speed_wall_clock, test_elapsed_duration_zero and test_event_both_values_fabricated. The final easing suite passed30tests. The earlier timestep suite passed19tests after two reproduced gaps; billboard passed26feature checks and4review checks after three reproduced gaps. Preserve independent expectations and negative controls when modifying these bounded checks.

This is historical local verification, not global CI enforcement or protection against rewriting every evidence file. Passing evidence integrity does not imply a requested FPS was reached: easing observed23.21/45.66/110.32frame-updateFPS under30/60/144caps;the missed rendering bands remain unverified. Scope excludes production physics, arbitrary animation blending and universal clock guarantees.

## Evidence

- [Committed measured summaries and source fingerprints](evidence/unreal-validation-2026-11-12.json): Easing, Timestep and Billboard; includes review failure/success counts and historical input digests, not implementation code.
- [Easing conditions](../../knowledge/game/K-GAME-TECH-EASING.md), [timestep conditions](../../knowledge/game/K-GAME-TECH-TIMESTEP.md), [billboard conditions](../../knowledge/game/K-GAME-TECH-BILLBOARD.md).
- Original local evidence locators: `Results/Easing/review-red.txt`, `review-green.txt`, `feature-tests.txt`; `Results/Timestep/review-red.txt`; `Results/Billboard/review-red-all.txt`. These refer to the excluded local Unreal lab and are not published artifact links.
