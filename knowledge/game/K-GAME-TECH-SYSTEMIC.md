---
id: K-GAME-TECH-SYSTEMIC
title: "Model elemental interactions as explicit state rules"
summary: "Nintendo original slides support the element/material state-change model. Use explicit directed transition rules while treating engine implementation details as project-specific synthesis."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["systemic","chemistry","engine","elements","material","emergent","화학엔진"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Model elemental interactions as explicit state rules

## Guidance

Proposed implementation pattern: represent material properties and elemental effects as data, specify transition conditions and precedence, and send resulting events to physics, audio and rendering. Prototype a small interaction matrix before expanding combinations. The original conceptual model is confirmed by the follow-up below; the proposed data architecture is not Nintendo source code.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

The original Nintendo/GDC slides distinguish movement simulation from state transitions. At 40:23 the model separates elemental effects from material objects; at 40:53 effects may alter material state, at 41:08 effects may alter other effects, and at 41:23 material-to-material contact alone does not cause a chemical state transition. This restriction belongs to that game's model, not physical chemistry. Implementation synthesis: collect contacts/exposures, evaluate a directed effect-to-state rule table, resolve simultaneous changes with explicit precedence, commit state, then emit physics/VFX/audio events. For burning wood, a material can emit an elemental fire effect; this preserves the separation instead of declaring that every material directly transforms another.

## Applicability and exceptions

The three conceptual rules are verified from original slides; data structures, scheduling and propagation algorithms below are proposed engineering synthesis. Exact Nintendo source code, update order and simulation coefficients are not public evidence here.

## Checks

Proposed: test simultaneous fire/water/electric effects, event order, cycles, save/load and replicated authority; record unresolved combinations.

## Evidence

- [Nintendo — Breath of the Wild: Breaking Conventions](https://www.youtube.com/watch?v=niIVdlavc7I) — Earlier pass: excerpt description only. The original full talk slides were subsequently checked at the timestamps below. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V51 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [Nintendo/GDC — original technical presentation](https://www.youtube.com/watch?v=QyMsF31NdNc&t=2423s) — Original slides visually inspected at 40:23, 40:53, 41:08 and 41:23; transcript export unavailable; not a full-video viewing or source-code inspection. Checked 2026-11-07.
