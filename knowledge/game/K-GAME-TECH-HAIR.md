---
id: K-GAME-TECH-HAIR
title: "Choose hair representation and simulation independently"
summary: "Use cards for authored silhouette and lower representation budgets; consider strands for close detailed characters. Not every rendered strand needs independent simulation."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["groom","strands","hair","cards","머리카락"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Choose hair representation and simulation independently

## Guidance

Use cards for authored silhouette and lower representation budgets; consider strands for close detailed characters. Separate render representation, simulation guides, collision and LOD. Establish platform support before selecting a groom pipeline.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Epic documents separate guide simulation, interpolation onto render strands, hair-density voxelization, visibility, lighting and composition passes. Lower render-curve count and lower guide count target different costs; even invisible hair can require updates for shadows. Use per-pass profiling before choosing cards/strands or decimation. Capcom's CEDEC 2026 session confirms a PRAGMATA long-hair/strand workflow in Maya and RE ENGINE, but its accessible description does not verify exact strand/point counts.

## Applicability and exceptions

Not every rendered strand needs independent simulation. Long hair difficulty depends on representation, collision and animation requirements; short hair is not a universal technical necessity.

## Checks

Proposed: test shoulders, fast turns, headgear and LOD changes; profile several characters together.

## Evidence

- [Epic — Hair Rendering and Simulation](https://dev.epicgames.com/documentation/en-us/unreal-engine/hair-rendering-and-simulation-in-unreal-engine) — Overview text only; strands and cards. No platform-specific budget verified. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V13 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.


### Follow-up evidence

- [Epic — Groom Scalability and Performance](https://dev.epicgames.com/documentation/unreal-engine/groom-scalability-and-performance-with-unreal-engine) — Geometry scalability and pipeline stages text inspected; no project performance measured. Checked 2026-11-07.
- [Capcom speakers — PRAGMATA hair and facial development](https://cedec.cesa.or.jp/2026/timetable/detail/s69f305ca68328/) — Official CEDEC 2026 description and speaker affiliations; detailed presentation assets/counts not accessed. Checked 2026-11-07.
