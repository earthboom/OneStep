---
id: K-GAME-PLATFORMER
title: Establish platformer movement contracts before composing challenges
summary: Make collision, moving-platform interactions, and state communication predictable before combining movement challenges. Treat authored stage progression as a separate design layer.
kind: reference
scope: Platformer movement and level prototyping; tile-based 2D examples with limited 3D transfer
keywords: [platformer, movement, collision, moving platform, level design, animation, prototype, 플랫포머, 이동, 충돌, 발판, 레벨 설계, 기획, 프로토타입]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Author physics article and Nintendo interview read; Celeste GDC abstract only
  application_status: Proposed movement and level checks; no controller or level tested
---
# Establish platformer movement contracts before composing challenges

## Guidance

**Source claims.** Maddy Thorson's physics article distinguishes actors, solids, carrying, pushing, and context-dependent crushing behavior; pushing has priority over carrying. Nintendo's Wonder developers describe animation as state communication and explain balancing facial expressiveness with readable travel direction. The Celeste GDC abstract identifies stage creation, area arrangement, and story integration as its topics; it does not substantiate particular teaching sequences.

**Transferable synthesis.** Define the movement contract before content production: what counts as grounded, what moving surfaces carry, what pushes, and what happens when space runs out. Write player intent → input → movement → contact → feedback → retry as the local loop. A geometry change can alter contact timing, camera visibility, hazard readability, and checkpoint cost together.

Prototype representative interactions rather than only a pleasant jump on flat ground. Include side contacts, reversals, ceilings, moving surfaces, and competing contacts. Once these outcomes are predictable, compose rooms around one readable decision, then add combinations that test the same movement vocabulary. This room progression is a proposed synthesis, not a claim about the unviewed Celeste presentation.

Choose animation, camera lead, sound, and landing feedback to expose the movement state without hiding the next action. Reserve optional routes for additional mastery only when the main route still communicates its own requirements. Revisit the movement contract whenever a new ability changes reach or contact rules.

## Applicability and exceptions

Most directly applicable to precise 2D movement. The cited integer/AABB implementation is a specific solution, not a requirement for slope physics, rotation, continuous collision, or 3D traversal. Deliberately slippery, physical, or chaotic movement can be a goal; consistency should then mean understandable system behavior rather than instant control. Accessibility options may change execution demand without changing route logic.

## Checks

**Proposed checks, not executed:** Maintain a tiny interaction course with standing, clinging, pushing, and crushing cases. Replay it after controller changes. Ask new players to predict landing and platform outcomes, then compare prediction with result. Test room comprehension separately from completion, and inspect retry distance, camera framing, and optional-route visibility after each geometry change.

## Evidence

- [Thorson, Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html), “Moving Solids Prep” and “The Heavy Lifting”; author text opened 2026-11-07. Code explained, not executed.
- [Nintendo, Wonder Chapter 2](https://www.nintendo.com/au/news-and-articles/ask-the-developer-vol-11-super-mario-bros-wonder-chapter-2/), state-animation and travel-direction discussion; official interview text opened 2026-11-07. Embedded footage not analyzed.
- [GDC, Designing Celeste](https://gdcvault.com/play/1024307/Level-Design-Workshop-Designing-Celeste), “Overview”; opened 2026-11-07. Abstract only; full talk not viewed.
