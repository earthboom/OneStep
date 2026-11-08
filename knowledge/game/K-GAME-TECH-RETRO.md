---
id: K-GAME-TECH-RETRO
title: "Distinguish affine texture transforms from perspective projection"
summary: "Mathematical derivation: an affine 2D transform is p'=A*p+b and preserves parallelism. An affine transform alone is not perspective projection."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["affine","perspective","Mode7","scanline","아핀"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Distinguish affine texture transforms from perspective projection

## Guidance

Mathematical derivation: an affine 2D transform is p'=A*p+b and preserves parallelism. Perspective ground rendering needs scale varying with depth; changing affine parameters per scanline can approximate that view. Use for stylized flat-ground effects or historical rendering study.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

The bsnes renderer's renderMode7 loads signed matrix coefficients and centers/offsets, computes a scanline origin with fixed-point clipping/truncation, advances source coordinates by matrix increments, then resolves tile and palette samples plus out-of-range rules. This confirms a concrete raster implementation beyond the earlier README. Perspective-like ground requires the game to vary parameters across scanlines; a single affine mapping is insufficient. For faithful emulation, retain signed widths, intermediate truncation, wrap/clamp behavior and register-latch timing instead of substituting unrestricted floats.

## Applicability and exceptions

Source-level affine sampling is now checked in bsnes. Hardware bus timing, register-latch fidelity and original Mario Kart per-scanline code are not verified by reading this renderer alone.

## Checks

Proposed: verify the general transform using a checkerboard, then consult emulator/hardware source before implementing authentic Mode 7.

## Evidence

- [Godot — Matrices and transforms](https://docs.godotengine.org/en/latest/tutorials/math/matrices_and_transforms.html) — Official tutorial; 2D translation/rotation/scale math; latest documentation, API version not pinned. Checked 2026-11-07, except items explicitly marked further reading.
- [DerKoun — bsnes-hd README](https://github.com/DerKoun/bsnes-hd/blob/master/README.md) — Emulator author's implementation description; HD Mode 7 and integer-math limits; no emulator run. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V57 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [bsnes — renderMode7 source](https://github.com/bsnes-emu/bsnes/blob/master/bsnes/sfc/ppu-fast/mode7.cpp) — renderMode7; public master source read 2026-11-07, no emulator/hardware run; original Mario Kart code and cycle-exact timing not established. Checked 2026-11-07.
