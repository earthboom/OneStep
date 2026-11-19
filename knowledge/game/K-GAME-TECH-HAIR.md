---
id: K-GAME-TECH-HAIR
title: Choose hair representation and simulation independently
summary: Choose hair cards or Groom strands against silhouette, backdrop coverage
  and GPU budget. A native fixed-LOD rig verifies rigid root attachment and near/far
  performance.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- groom
- strands
- hair
- cards
- 머리카락
- Groom Asset
- simulation guides
- strand interpolation
- hair cards
- hair silhouette
- background see-through
- rigid root attachment
- 헤어 카드
- 헤어 스트랜드
- 두피 부착
- 배경 비침
- 헤어 GPU 비용
status: active
checked_at: '2026-11-20'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V13 UE 5.8.3 Win64 DX11 original masked hair cards and native
    Groom strands. Rigid attach, fixed LOD, physics off. Head turn and near/far pixels,
    three whole-frame and GPU measurements per arm.
---
# Choose hair representation and simulation independently

## Guidance

Use cards for authored silhouette and lower representation budgets; consider strands for close detailed characters. Separate render representation, simulation guides, collision and LOD. Establish platform support before selecting a groom pipeline.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Epic documents separate guide simulation, interpolation onto render strands, hair-density voxelization, visibility, lighting and composition passes. Lower render-curve count and lower guide count target different costs; even invisible hair can require updates for shadows. Use per-pass profiling before choosing cards/strands or decimation. Capcom's CEDEC 2026 session confirms a PRAGMATA long-hair/strand workflow in Maya and RE ENGINE, but its accessible description does not verify exact strand/point counts.

### Groom Asset

A Groom Asset can carry guide curves and render strands. With strand interpolation, simulated guides drive the motion of render strands. A guide-count change and a render-curve change affect different work. Profile the relevant passes at the intended LOD before selecting a reduction.

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

## Unreal masked cards and Groom strands — 2026-11-20

The local V13 experiment used one 19-lock style with 722 card triangles and 3,192 Groom curves. Rigid scalp attachment, fixed LOD and simulation off isolate the two representations under common lights and camera poses. A matched no-hair render provides silhouette and background gap evidence. Both have visible gaps in the tested checker backdrop. Near-side strand coverage was 3.68 times card coverage for these assets. Read the pose-level overlap and backdrop samples for this hairstyle.

Three runs yielded whole-frame p95 of 12.456–14.736 ms (cards) and 9.925–12.799 ms (strands), and whole-GPU p95 of 13.708–14.826 and 9.808–13.885 ms respectively. Use the screen footprint at actual camera distances and keep the light and material setup comparable. GPU totals cover the complete selected representation. Add separate skinning, collision and LOD evidence when those systems are active.
