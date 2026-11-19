---
id: K-GAME-TECH-RNG
title: Separate reproducible randomness from security-sensitive randomness
summary: Own explicit seeded gameplay and cosmetic streams to isolate ordered outcomes;
  restore complete stream and consumer state for in-memory replay. UE5.8.3 bounded
  Actor/PIE/package checks and equal-call shared/split costs are measured; no statistical-independence
  or cross-version guarantee.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["PRNG", "PCG", "seed", "stream", "deterministic", "난수", "linear congruential generator", "LCG", "Permuted Congruential Generator", "independent streams", "FRandomStream", "cosmetic", "gameplay", "reset", "memory checkpoint", "state restore", "장식", "복원", "독립 스트림"]
status: active
checked_at: "2026-11-19"
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 Win64/DX11:57policy/38evidence/8actualPIE+8packagedcases/6equal-callcosts/normal1xmedia;single-thread/in-memory
    only
---
# Separate reproducible randomness from security-sensitive randomness

## Guidance

A deterministic PRNG advances internal state into a reproducible sequence. Persist state or use stable independent streams for replay, generation and loot; cosmetic draws must not unexpectedly consume gameplay randomness. Choose a generator by period, quality, speed and reproducibility requirements.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

In pret's Emerald reconstruction, Random advances a 32-bit state by multiplication and addition, then returns its upper 16 bits; SeedRng assigns the state. The header identifies the recurrence s'=(1103515245*s+24691) mod 2^32. Thus an identical seed and identical count/order of calls reproduce this stream, not merely an identical elapsed wall-clock time. Instrument seed initialization and every caller before diagnosing a version-specific manipulation. Keep gameplay and cosmetic streams separate for new games.

## Applicability and exceptions

Predictability is implementation-dependent; not every modern game prevents RNG manipulation. General-purpose PCG is not a substitute for a cryptographically secure generator where secrecy matters.

A **linear congruential generator** (LCG) updates state by a multiply, add and reduction modulo the state range. The PCG family (Permuted Congruential Generator) applies an output transformation to a congruential state generator. For repeatable game simulation compare complete draw sequences under the same algorithm and stream parameters. If visual effects use their own streams, adding a cosmetic draw should leave gameplay draws unchanged. [O'Neill — The PCG Paper](https://www.pcg-random.org/paper.html)

## Checks

Verified native subset below: seeded replay, cosmetic state isolation, reset and whole-memory restoration. Statistical distribution quality remains a proposed, unperformed check.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Melissa O'Neill — PCG Random Number Generators](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf) — 2014 technical report; abstract, generator state and stream design. Not cryptographic certification. Checked 2026-11-07, except items explicitly marked further reading.
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) — 2014 author article; exact determinism and input synchronization. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V55 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

### Follow-up evidence

- [pret/pokeemerald — random.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/random.c) — Random and SeedRng inspected; community reconstruction, not a vendor patch history. Checked 2026-11-07.
- [pret/pokeemerald — random.h](https://github.com/pret/pokeemerald/blob/master/include/random.h) — ISO_RANDOMIZE1 and declarations inspected; formula transcribed, no game build. Checked 2026-11-07.

## Native Unreal validation — 2026-11-13

The historical Unreal run add57policy/38evidence checks,actualPIE/package8cases,shared/separate three costs each and native1xmedia. Explicit game/cosmetic FRandomStream values isolate state;do not use global/time-seeded draws or assume different seeds prove statistical independence. Keep the same ordered game events;changing game draw order/count remains a different sequence. Cosmetic calls and frame batches can change without changing split game raw values/outcomes/score. Shared negative control visibly diverges.

Whole in-memory value copies preserve initial/current seeds,both states/counters and event cursor/results. Current-seed-only Initialize changes Reset semantics;memory restoration must include consumer progress too. Checked inclusive int32 wrapper accepts width1..2^23 viaint64,rejects inverted/wider atomically;singleton advances once. Native fraction[0,1),poor low bits warning:avoid raw%range. Exact zero/max-fraction endpoints and seeds0/negative/int32extremes are covered. One game-thread owner;no cross-version/platform/thread-security guarantee.

Every final cost run is512warmup+4096measured ticks,65536rawgame+65536rawdecor/tick,exact536,870,912measured calls. Report scoped RNG and whole-frame/cadence separately;whole wall includes HUD/per-frame observation,excludes final saving/capture. Delayed GPU is whole-frame,not RNG work. Performance is workload-specific;choose separation for isolation,not an assumed whole-frame speedup. Native archived measurements retains all3repeats. Installed5.8header/runtime are authoritative for recurrence/endpoints;rolling docs only support seeded-repeatability concept.

Measured scoped RNG p95 (ms), split:[0.1532,0.1423,0.1439], shared:[0.1938,0.1919,0.1941]. Whole-frame wall p95 (ms), split:[7.345,7.226,7.272], shared:[7.496,7.354,7.267]. The split RNG interval was faster in all three runs, but no consistent whole-frame benefit was established. These values apply to the exact raw-draw/counter/checksum workload and observation overhead above, not arbitrary gameplay random APIs.

Retrieve RNG for cosmetic activity changing loot/generation/replay outcomes;NOISE/DUNGEON for generation algorithm and SAVE for durable recovery. No save-file/network/rollback/cryptography or renderer/framework expansion. Distribution quality,statistical independence and source-game patch history remain unverified. Previously missed actualFPSbands are unchanged.

## Result-policy boundary — 2026-11-13

[RANDOM-DESIGN](K-GAME-TECH-RANDOM-DESIGN.md) now implements fixed25%,one-success bag4 and hard8 on explicit seeded streams. Retrieve it for success/streak distributions and guarantees. Its finite-seed distribution observations do not establish statistical independence or change RNG replay/security limits.
