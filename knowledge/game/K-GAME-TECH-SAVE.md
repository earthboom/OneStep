---
id: K-GAME-TECH-SAVE
title: "Design versioned durable saves and compact password states"
summary: "Serialize persistent state, stable object identifiers and schema version rather than raw runtime pointers. A checksum detects some corruption; it is not tamper-proof authentication."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["save","serialization","checksum","password","bitflags","저장","세이브","백업","저장손상"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Design versioned durable saves and compact password states

## Guidance

Serialize persistent state, stable object identifiers and schema version rather than raw runtime pointers. Pack independent flags into bits when useful. Password saves encode a small reconstructible state into a restricted alphabet with error detection. Proposed durability design: validate a new save before replacing the known-good slot and retain a recoverable generation.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Emerald's public reconstruction writes sector groups using a save counter to select a slot and tracks the last known good write state; loading validates sector data and selects a valid generation. This is a historical reconstruction, not Nintendo-authored source or a tested local save system. For a new implementation, use generation IDs, payload validation and a documented commit/recovery order; do not assume two files alone are atomic. The original Simon's Quest reverse-engineering FAQ describes seven state bytes, a two-byte additive check and a scrambling byte, encoded into a 16-character password. Item/experience/day state is reconstructed, not an exact paused-world snapshot.

## Applicability and exceptions

A checksum detects some corruption; it is not tamper-proof authentication. Eight bits store eight independent yes/no flags, not hundreds of millions of independent events. Two slots alone do not prove atomic filesystem behavior.

## Checks

Proposed: interrupt each write stage, corrupt payloads, load older schemas, and verify backups and object references; test on the target platform.

## Evidence

- [Epic — Saving and Loading Your Game](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine) — Official documentation; custom SaveGame and asynchronous saving. Checked 2026-11-07, except items explicitly marked further reading.
- [pret/pokered — save.asm](https://github.com/pret/pokered/blob/master/engine/menus/save.asm) — Community disassembly artifact, not Nintendo-authored source; inspected as historical implementation evidence, no ROM built. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V20, V54 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [pret/pokeemerald — save.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/save.c) — HandleWriteSector, save generation selection and validation text inspected; community reconstruction; no ROM build or fault injection. Checked 2026-11-07.
- [kingshriek — Simon's Quest Password System FAQ](https://gamefaqs.gamespot.com/nes/587179-castlevania-ii-simons-quest/faqs/38582) — Original reverse-engineering account, generation/decoding sections; exact ROM behavior not independently executed; do not copy apparent transcription errors as a tested decoder. Checked 2026-11-07.
