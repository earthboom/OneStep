---
id: K-GAME-TECH-RETRO
title: Distinguish affine texture transforms from perspective projection
summary: Use affine UV mapping for flat texture motion and row-dependent depth for
  a stylized horizontal floor. Unreal 5.8.3 evidence covers pixel alignment, signed
  UV addressing, scale zero and the horizon guard.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["affine", "perspective", "Mode7", "scanline", "아핀", "Mode 7", "affine transformation", "fixed-point arithmetic", "affine UV", "horizon guard", "negative UV", "wrap clamp", "주사선", "지평선", "반복 클램프"]
status: active
checked_at: '2026-11-18'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V57 native basic/affine/scanline floor with actual sampled pixels,
    nine packaged costs and normal 1x capture. Flat-plane effect and explicit point-sampling
    limits.
---
# Distinguish affine texture transforms from perspective projection

## Guidance

Mathematical derivation: an affine 2D transform is p'=A*p+b and preserves parallelism. Perspective ground rendering needs scale varying with depth; changing affine parameters per scanline can approximate that view. Use for stylized flat-ground effects or historical rendering study.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

The bsnes renderer's renderMode7 loads signed matrix coefficients and centers/offsets, computes a scanline origin with fixed-point clipping/truncation, advances source coordinates by matrix increments, then resolves tile and palette samples plus out-of-range rules. This confirms a concrete raster implementation beyond the earlier README. Perspective-like ground requires the game to vary parameters across scanlines; a single affine mapping is insufficient. For faithful emulation, retain signed widths, intermediate truncation, wrap/clamp behavior and register-latch timing instead of substituting unrestricted floats.

### Mode 7

Mode 7 applies an affine transformation to a background. Per-scanline changes can suggest a horizon. Fixed-point arithmetic quantizes the coordinates, which matters when matching an emulator reference. Compare integer sampling at scanline boundaries before attributing a discrepancy to the projection model.

## Applicability and exceptions

Source-level affine sampling is now checked in bsnes. Hardware bus timing, register-latch fidelity and original Mario Kart per-scanline code are not verified by reading this renderer alone.

## Checks

Proposed: verify the general transform using a checkerboard, then consult emulator/hardware source before implementing authentic Mode 7.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Godot — Matrices and transforms](https://docs.godotengine.org/en/latest/tutorials/math/matrices_and_transforms.html) — Official tutorial; 2D translation/rotation/scale math; latest documentation, API version not pinned. Checked 2026-11-07, except items explicitly marked further reading.
- [DerKoun — bsnes-hd README](https://github.com/DerKoun/bsnes-hd/blob/master/README.md) — Emulator author's implementation description; HD Mode 7 and integer-math limits; no emulator run. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V57 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

### Follow-up evidence

- [bsnes — renderMode7 source](https://github.com/bsnes-emu/bsnes/blob/master/bsnes/sfc/ppu-fast/mode7.cpp) — renderMode7; public master source read 2026-11-07, no emulator/hardware run; original Mario Kart code and cycle-exact timing not established. Checked 2026-11-07.

## Native Unreal V57 follow-up — 2026-11-18

At the same screen rectangle, rotate/scale about a UV pivot and then translate. Fractional parts repeat negative UV, clamp uses the edge texel, and a zero scale collapses the sampled coordinate to the transformed pivot. The horizontal floor shares a depth along each row, with reciprocal depth controlled by the horizon. Return sky before division within the guard. Verify explicit camera axis registration, actual texture palette and expected texel classes independently. The point sampler leaves visible near-horizon aliasing. When choosing a resolution or filter, repeat the screen-space guard and boundary checks. Whole-frame/GPU observations apply to the measured 1280×720 fixture.
