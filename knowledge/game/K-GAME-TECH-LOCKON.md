---
id: K-GAME-TECH-LOCKON
title: "Select stable lock-on targets before changing movement framing"
summary: "Score eligible targets by distance, screen direction, angle and line of sight. Engineering synthesis from target filtering/framing."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["lock-on","target","scoring","Z","targeting","락온"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Select stable lock-on targets before changing movement framing

## Guidance

Score eligible targets by distance, screen direction, angle and line of sight. Use hysteresis so nearly equal candidates do not flicker, and explicit rules for target switching or loss. Orient camera and character independently; map strafe movement relative to the selected target when appropriate.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Nintendo's original staff interview connects Z-targeting to making a selected opponent legible and describes replacing the prototype marker with Navi. This supports target-selection feedback, not a claim of worldwide invention priority. A practical implementation should retain the current target until loss rules fire, score new candidates only on acquisition/switch, and separate character orientation, orbit movement and camera framing. Introduce target-loss grace only if occlusion policy allows it.

## Applicability and exceptions

The original staff account supports Z-targeting's marker/Navi feedback design. It does not establish worldwide first-invention priority or prescribe an exact scoring formula.

## Checks

Proposed: overlapping enemies, occlusion, targets crossing behind the camera and controller target-switch inputs.

## Evidence

- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US) — Official worked example; dot, distance and line-of-sight target filtering. Checked 2026-11-07, except items explicitly marked further reading.
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 2015 creator-authored article; camera-window, framing and smoothing. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V53 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [Nintendo — Where the Name Navi Came From](https://iwataasks.nintendo.com/interviews/3ds/zelda-ocarina-of-time/1/3/) — Original staff interview text retrieved by search; direct fetch timed out. Supports marker/Navi design account, not first-ever priority. Checked 2026-11-07.
