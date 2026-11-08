---
id: K-GAME-TECH-RNG
title: "Separate reproducible randomness from security-sensitive randomness"
summary: "A deterministic PRNG advances internal state into a reproducible sequence. Predictability is implementation-dependent; not every modern game prevents RNG manipulation."
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["PRNG","PCG","seed","stream","deterministic","난수"]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: "External source text checked; source-specific limits appear in Evidence"
  application_status: "Reference research and proposed checks only; no engine implementation or performance validation"
---
# Separate reproducible randomness from security-sensitive randomness

## Guidance

A deterministic PRNG advances internal state into a reproducible sequence. Persist state or use stable independent streams for replay, generation and loot; cosmetic draws must not unexpectedly consume gameplay randomness. Choose a generator by period, quality, speed and reproducibility requirements.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

In pret's Emerald reconstruction, Random advances a 32-bit state by multiplication and addition, then returns its upper 16 bits; SeedRng assigns the state. The header identifies the recurrence s'=(1103515245*s+24691) mod 2^32. Thus an identical seed and identical count/order of calls reproduce this stream, not merely an identical elapsed wall-clock time. Instrument seed initialization and every caller before diagnosing a version-specific manipulation. Keep gameplay and cosmetic streams separate for new games.

## Applicability and exceptions

Predictability is implementation-dependent; not every modern game prevents RNG manipulation. General-purpose PCG is not a substitute for a cryptographically secure generator where secrecy matters.

## Checks

Proposed: replay from stored state, change cosmetic activity, check distribution and ensure independent streams remain independent in actual use.

## Evidence

- [Melissa O'Neill — PCG Random Number Generators](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf) — 2014 technical report; abstract, generator state and stream design. Not cryptographic certification. Checked 2026-11-07, except items explicitly marked further reading.
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) — 2014 author article; exact determinism and input synchronization. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V55 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [pret/pokeemerald — random.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/random.c) — Random and SeedRng inspected; community reconstruction, not a vendor patch history. Checked 2026-11-07.
- [pret/pokeemerald — random.h](https://github.com/pret/pokeemerald/blob/master/include/random.h) — ISO_RANDOMIZE1 and declarations inspected; formula transcribed, no game build. Checked 2026-11-07.
