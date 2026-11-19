---
id: R-CODE-UE-EVIDENCE-PROXY
title: "Self-consistent event values can hide an incorrect transition"
summary: "A transition validator accepted compressed wall time and mutually consistent fabricated event values. Bind elapsed time and the values on both sides of an event to independent expectations."
kind: error
scope: "Native real-time or fixed-step transition validation, historically UE 5.8.3 on Win64"
keywords: ["test oracle","monotonic clock","std::chrono::steady_clock","simulation time","negative control","easing","transition","wall age","event continuity","검증"]
status: resolved
checked_at: '2026-11-12'
trigger: "Accepting transition output from its own reported time, counters or neighboring event samples"
symptom: "Shortening wall time, zeroing elapsed duration or substituting equal but incorrect before/after values left the original check green"
cause_status: confirmed
prevention: "Compute expected event values independently and check elapsed time against the clock governing the contract"
prevention_status: verified
---

## Expected and observed

The samples agreed with each other even when the transition ran at the wrong speed or both sides of an event were changed to the same wrong value.

## Cause and resolution

A test oracle supplies the expected outcome independently of the output it evaluates. Derive event values from the schedule and curve. For a real-time contract, compare the elapsed interval with a monotonic clock and account for sampling uncertainty. For a fixed-step simulation, compare with simulation time. In portable C++, `std::chrono::steady_clock` supplies monotonic intervals. It is an implementation option, not an assertion about the historical timer.

## Recheck and prevention

The historical negative controls shortened the observed interval, discarded duration and fabricated both event values. Each change exposed the original blind spot and was rejected after repair. Keep those failure classes separate. Measurement correctness alone does not establish a frame-rate budget or perceptual quality.

## Evidence

Transition-validator behavior was historically checked under UE 5.8.3. The clock reference establishes the C++ contract only. [C++ working draft, time.clock.steady](https://eel.is/c++draft/time.clock.steady) · [Historical transition evidence](../../knowledge/sources.md#src-ue-lab-easing-results-md) · [Fixed-step checks](../../knowledge/game/K-GAME-TECH-TIMESTEP.md)
