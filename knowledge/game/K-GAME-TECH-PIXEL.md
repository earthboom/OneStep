---
id: K-GAME-TECH-PIXEL
title: Design pixel clusters and palette storage deliberately
summary: Match pixel scale and filtering to the intended look. Unreal 5.8.3 V35/V58
  checks nearest/bilinear, alpha edges and color-table swaps, with measured PNG, decoded
  BGRA8 and packaged texture bytes.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["pixel", "art", "dithering", "palette", "indexed", "colour", "픽셀", "PLTE", "indexed-colour PNG", "16색", "팔레트", "PNG", "indexed PNG", "GPU memory", "texture memory", "텍스처 메모리", "이미지 용량", "palette lookup", "premultiplied alpha", "integer scale", "nearest", "bilinear", "G8", "팔레트 교체", "정수 확대", "최근접", "알파 경계"]
status: active
checked_at: '2026-11-18'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: 96x96 V35/V58 UE5.8.3 sprite with 16 visible colors and separate
    transparency. Native pixels, 6 matched costs, 24s normal speed, decoded and RHI
    texture sizes.
---
# Design pixel clusters and palette storage deliberately

## Guidance

For readable low-resolution sprites, tune clusters, edge rhythm, palette and selective anti-aliasing at the actual display scale. Indexed colour stores palette indices; n colours need ceil(log2(n)) index bits in principle, subject to format constraints. Dithering trades spatial patterns for perceived intermediate tones.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### PLTE

An indexed-colour PNG stores palette indices in its image data. The required `PLTE` chunk holds the corresponding RGB entries. Inspect the importer’s chosen texture format to determine GPU memory use, since a small palette in the file does not require indexed GPU storage.

## Applicability and exceptions

Art conventions are stylistic choices, not universal bans. File size, decoded CPU memory and GPU texture format are different budgets. This reference does not certify a particular SNES sprite's storage layout.

## Checks

Proposed: preview integer and noninteger scaling, filtering and palette swaps; inspect runtime texture memory rather than PNG size.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [W3C, PNG Specification (PLTE)](https://www.w3.org/TR/png-3/#11PLTE) — terminology and applicability of PLTE, indexed-colour PNG. This is source evidence. The suggested target checks remain to be run.

- [Derek Yu — Pixel Art Tutorial: Basics](https://www.derekyu.com/makegames/pixelart.html) — Creator tutorial; outlines, anti-aliasing and shading. Checked 2026-11-07, except items explicitly marked further reading.
- [W3C — PNG Specification, Third Edition](https://www.w3.org/TR/png/) — 2025 recommendation; indexed colour and PLTE; storage format, not GPU residency. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V35, V58 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native pixel sampling and LUT follow-up — 2026-11-18

The historical Unreal run verifies integer/fractional scaling with nearest/bilinear, palette exchange and alpha edges over two backgrounds. A 613-byte indexed PNG and a 1,053-byte RGBA PNG both decoded as 36,864-byte BGRA8 buffers in Unreal's ImageWrapper. The explicitly retained G8 index and two palette rows total 9,472 bytes in the measured Win64 DX11 package. Record encoder palette padding, decode format and runtime format/mips as separate evidence.

When resolving a palette in the shader, sample categorical indices at texel centers. Apply bilinear to the four resolved colors and alphas. Use premultiplied color for alpha-composite interpolation. Measure source art and target workload because the tested asset is 96×96 with one mip and the timings cover the whole frame. The 720-frame native capture and six cost runs are linked above.
