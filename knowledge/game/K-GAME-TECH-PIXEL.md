---
id: K-GAME-TECH-PIXEL
title: "Design pixel clusters and palette storage deliberately"
summary: "For readable low-resolution sprites, tune clusters, edge rhythm, palette and selective anti-aliasing at the actual display scale. Art conventions are stylistic choices, not universal bans."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["pixel","art","dithering","palette","indexed","colour","픽셀"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Design pixel clusters and palette storage deliberately

## Guidance

For readable low-resolution sprites, tune clusters, edge rhythm, palette and selective anti-aliasing at the actual display scale. Indexed colour stores palette indices; n colours need ceil(log2(n)) index bits in principle, subject to format constraints. Dithering trades spatial patterns for perceived intermediate tones.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Art conventions are stylistic choices, not universal bans. File size, decoded CPU memory and GPU texture format are different budgets. This reference does not certify a particular SNES sprite's storage layout.

## Checks

Proposed: preview integer and noninteger scaling, filtering and palette swaps; inspect runtime texture memory rather than PNG size.

## Evidence

- [Derek Yu — Pixel Art Tutorial: Basics](https://www.derekyu.com/makegames/pixelart.html) — Creator tutorial; outlines, anti-aliasing and shading. Checked 2026-11-07, except items explicitly marked further reading.
- [W3C — PNG Specification, Third Edition](https://www.w3.org/TR/png/) — 2025 recommendation; indexed colour and PLTE; storage format, not GPU residency. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V35, V58 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

