---
id: K-GAME-TECH-VOLUME
title: "Separate volumetric appearance from simulated smoke gameplay"
summary: "Render participating media using a density field with scattering/extinction; use noise to shape clouds or smoke, then sample light and transmittance. Volumetric rendering is not fluid dynamics."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["volumetric","smoke","clouds","Worley","연막","구름","연막","구름","경계누출","잔상"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Separate volumetric appearance from simulated smoke gameplay

## Guidance

Render participating media using a density field with scattering/extinction; use noise to shape clouds or smoke, then sample light and transmittance. Low-resolution evaluation with temporal reconstruction is a quality/performance tradeoff. For competitive smoke, share authoritative density/visibility rules rather than relying on each client's final image.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Valve's 2023 CS2 patch notes explicitly mention smoke-volume expansion near walls, changes to the stepping function on AMD hardware, and shotgun-created holes. These support an evolving spatial smoke volume, not a published complete solver. Implementation synthesis: separate authoritative smoke occupancy and temporary bullet/grenade perturbations from per-view lighting, then render the shared state with platform-appropriate sampling. Geometry intersection and reconstruction must preserve gameplay visibility across quality levels.

## Applicability and exceptions

Valve's dated patch notes confirm smoke-volume behavior; its complete density solver, replication and ray-marching code remain undisclosed. Volumetric appearance is distinct from fluid simulation and equal competitive visibility still needs target-game tests.

## Checks

Proposed: test moving lights, camera cuts, inside-volume views, depth edges and visibility agreement under different quality settings.

## Evidence

- [Epic — Volumetric Fog](https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine) — Density, scattering, temporal reprojection and performance sections. Checked 2026-11-07, except items explicitly marked further reading.
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf) — 2016 author chapter; terrain and multi-scale noise. Checked 2026-11-07, except items explicitly marked further reading.
- [u/smilefr — Optimized volumetric clouds](https://www.reddit.com/r/Unity3D/comments/1u8g138/i_finally_have_optimzied_volumetric_clouds/) — Original implementation account; quarter-resolution compute rendering and depth-edge upsample. Self-reported, no benchmark reproduced. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V10, V27 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.


### Follow-up evidence

- [Valve — Counter-Strike 2 June 2023 update notes](https://store.steampowered.com/news/posts/?appids=730&enddate=1689630041&feed=steam_announce%2F1000) — Official dated notes, VOLUMETRIC SMOKE sections; source code and cross-client determinism not disclosed. Checked 2026-11-07.
