---
id: K-GAME-TECH-NOISE
title: "Generate coherent terrain with gradients and multi-scale noise"
summary: "Use coherent noise for spatially continuous variation. A heightfield cannot represent overhangs; density fields can."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["Perlin","noise","fractal","fBm","terrain","바이옴"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Generate coherent terrain with gradients and multi-scale noise

## Guidance

Use coherent noise for spatially continuous variation. Perlin noise computes gradient-dot products at surrounding lattice corners and blends them with smooth interpolation; adding the raw dot products is insufficient. Sum octaves with controlled frequency and amplitude for multi-scale detail. Derive biome fields independently from final mesh construction.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Mojang's 1.18 development notes explicitly separate terrain shaping, biome distribution, noise caves and aquifers. Aquifers give underground regions local water levels; cave carving and noise fields can coexist. For a new generator, treat density d(x,y,z), climate/biome fields and fluid occupancy as separate inputs. Evaluate density including neighbor margins before meshing a chunk, and make cave/biome blending deterministic across boundaries. This is an implementation synthesis, not Mojang's exact density function.

## Applicability and exceptions

A heightfield cannot represent overhangs; density fields can. Exact Minecraft algorithms change by edition/version and are not established from this general reference.

## Checks

Proposed: fix seeds, inspect chunk seams and derivatives, and validate biome transitions and reachable terrain.

## Evidence

- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf) — 2002 paper; interpolation and gradients. Checked 2026-11-07, except items explicitly marked further reading.
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf) — 2016 author chapter; terrain and multi-scale noise. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V07, V50 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [Mojang — Java 1.18 experimental world generation](https://www.minecraft.net/en-us/article/new-world-generation-java-available-testing) — Official historical development notes; release scope distinguished from snapshot behavior. Checked 2026-11-07.
- [Mojang — Bedrock 1.18.0 release notes](https://feedback.minecraft.net/hc/en-us/articles/4414284658701-Minecraft-Caves-Cliffs-Part-II-1-18-0-Bedrock) — New biome/cave generation and aquifers; edition/version retained. Checked 2026-11-07.
