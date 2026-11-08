---
id: K-GAME-TECH-WATER
title: "Use summed waves for water surfaces with explicit limits"
summary: "Represent height as a sum of waves with amplitude, wavelength, direction and phase. Steepness must be bounded to avoid folding."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["Gerstner","sine","waves","water","물","파도"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Use summed waves for water surfaces with explicit limits

## Guidance

Represent height as a sum of waves with amplitude, wavelength, direction and phase. Gerstner waves also move surface points horizontally, producing sharper crests. Compute normals from the same displacement field and share a compatible surface query with buoyancy gameplay.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Steepness must be bounded to avoid folding. Wave sums are not full fluid simulation and do not automatically handle breaking waves, shore interaction or flow around obstacles.

## Checks

Proposed: inspect overhead repetition, shallow coastlines, floating objects and different simulation rates.

## Evidence

- [Mark Finch — Effective Water Simulation from Physical Models](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-1-effective-water-simulation-physical-models) — GPU Gems ch.1; sum of sines and Gerstner waves. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V32 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

