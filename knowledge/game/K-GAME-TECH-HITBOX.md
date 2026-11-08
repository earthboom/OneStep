---
id: K-GAME-TECH-HITBOX
title: "Keep attack, hurt and physical collision contracts distinct"
summary: "Separate attack volumes, damage-receiving volumes and movement collision. This is a proposed combat engineering contract derived from collision/forgiveness principles, not a verified universal commercial hitbox recipe."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["hitbox","hurtbox","hitstop","collision","피격"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Keep attack, hurt and physical collision contracts distinct

## Guidance

Separate attack volumes, damage-receiving volumes and movement collision. Activate attacks on simulation states/frames and assign attack identities to avoid unintended repeat hits. Use grace windows or invulnerability only where the design requires them. Hit-stop should specify which clocks pause and which input buffers continue.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

This is a proposed combat engineering contract derived from collision/forgiveness principles, not a verified universal commercial hitbox recipe. Smaller hurtboxes are a choice; high-speed motion may require swept tests.

## Checks

Proposed: visualize volumes frame-by-frame, test simultaneous hits and movement through thin targets, and replay with hit-stop disabled.

## Evidence

- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html) — Creator text; coyote time, buffering, corner correction and momentum storage. Checked 2026-11-07, except items explicitly marked further reading.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — Creator implementation; integer AABBs and fractional remainder. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V42 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

