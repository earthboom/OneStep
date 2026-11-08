---
id: K-GAME-TECH-CAMERA
title: "Combine dead zones, prediction and time-consistent damping"
summary: "Choose a framing target before smoothing: player, look-ahead point, room anchor or multiple subjects. The formula is derived engineering synthesis; moving targets and collision still need explicit handling."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["camera","deadzone","lookahead","damping","spring","카메라","데드존","룩어헤드","카메라흔들림"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Stationary-target damping validated in Unity 6000.0.77f1 Windows Mono prototype; framing, moving-target behavior and collision remain untested"
---
# Combine dead zones, prediction and time-consistent damping

## Guidance

Choose a framing target before smoothing: player, look-ahead point, room anchor or multiple subjects. Use a dead zone to suppress unnecessary tracking. For a stationary target, exponential damping x+=(target-x)*(1-exp(-lambda*dt)) has a time-consistent decay; use a damped spring if velocity and overshoot matter.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Local engine evidence — 2026-11-07

[Technique Lab](../../prototypes/TechniqueLab/RESULTS.md) implemented the damping kernel and a rendered moving-target illustration. Final PlayMode and three Windows Mono player runs passed the synthetic stationary 30/60/144-step, hitch and zero-dt checks. Actual Update sequences integrated exactly two seconds (rate 4, start 0, target 10); maximum player error against `10*(1-exp(-8))` was 0.000001907, below the declared 0.0001 tolerance. Actual achieved rates were recorded rather than inferred from caps.

In CPU batches of 100,000 scalar followers, per-item exponentials had per-process median costs of 2.429–2.813 ms; sharing alpha for identical rate/dt took 1.711–1.755 ms. This is repeated scalar math/checksum throughput on one host, not whole-frame or camera-system cost. Share alpha only for genuinely identical inputs; preserve separate values otherwise. Do not extrapolate this result to a single camera, GPU work or another backend.

## Applicability and exceptions

The formula is derived engineering synthesis; moving targets and collision still need explicit handling. A fixed 10% per rendered frame changes feel with FPS. Do not let smoothing hide incoming hazards.

## Checks

Proposed: compare 30/60/144 FPS, fast reversals, room boundaries, teleports and different aspect ratios.

Executed subset: stationary elapsed-time, hitch and zero-dt response in the local Unity prototype. Fast reversals, boundaries, teleports, aspect ratios, dead-zone/prediction design, camera collision and player comfort remain proposed checks. A moving target sampled per frame does not have the stationary target's exact invariance.

## Evidence

- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 2015 creator-authored article; camera-window, framing and smoothing. Checked 2026-11-07, except items explicitly marked further reading.
- [Ryan Juckett — Damped Springs](https://www.ryanjuckett.com/damped-springs/) — 2012 author derivation; damping cases and time-step handling. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V23, V48 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.
- Local experiment: [results, conditions and reproduction](../../prototypes/TechniqueLab/RESULTS.md), [kernel](../../prototypes/TechniqueLab/Assets/TechniqueLab/CameraDamping.cs), [independent checks](../../prototypes/TechniqueLab/Assets/TechniqueLab/LabChecks.cs), [raw player example](../../prototypes/TechniqueLab/Results/player-run-1.json) (`frameResponses`, camera benchmark rows). Actual execution is limited to the documented Unity/Windows/Mono setup.

