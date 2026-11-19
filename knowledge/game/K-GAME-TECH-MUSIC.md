---
id: K-GAME-TECH-MUSIC
title: "Schedule adaptive music at musical boundaries"
summary: "Use synchronized stems for vertical layering and compatible sections for horizontal resequencing. Randomly concatenating clips does not guarantee musical continuity."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["adaptive", "music", "stems", "transition", "vertical", "horizontal", "음악", "vertical layering", "horizontal resequencing", "tempo map", "beat-synchronous transition"]
status: active
checked_at: '2026-11-19'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Schedule adaptive music at musical boundaries

## Guidance

Use synchronized stems for vertical layering and compatible sections for horizontal resequencing. Map gameplay state to musical intensity, then schedule transitions on beats/bars or authored cues. Track tempo, meter, entry/exit points, transition segments and crossfade policy.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Randomly concatenating clips does not guarantee musical continuity. Composer terminology varies; describe the actual scheduling operation. A brief combat toggle should not cause constant musical restarting.

In **vertical layering**, synchronized stems share a musical timeline and the mix changes by adding or removing layers. In **horizontal resequencing**, the score moves to another compatible section at a musical boundary. A tempo map converts beat or bar positions into playback time as tempo changes. Request a transition immediately before and after a tempo change and verify the audible handoff, including any pickup or decay tail. [Kent Carter / Guy Jones — Composer interview on adaptive music](https://www.gamedeveloper.com/audio/composer-guy-jones-talks-adaptive-music-for-games)

## Checks

Proposed: trigger every state transition at multiple beat offsets, test rapid reversals and loading stalls, and listen for phase/cut artifacts.

## Evidence

- [Kent Carter / Guy Jones — Composer interview on adaptive music](https://www.gamedeveloper.com/audio/composer-guy-jones-talks-adaptive-music-for-games) — 2021 direct composer interview text; stems, sections and tempo maps. Embedded podcast not played. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V25 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

