---
id: K-GAME-TECH-RANDOM-DESIGN
title: Control randomness by decision timing and streak distribution
summary: Choose independent fixed probability,one-success shuffle bags or hard pity
  by their rate and drought contracts. UE5.8.3 finite-seed native replay/distribution/cost
  evidence distinguishes bag-boundary streaks and changed long-run pity rates from
  subjective fairness.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["randomness", "pity", "shuffle", "bag", "probability", "agency", "확률", "천장", "input randomness", "output randomness", "shuffle bag", "conditional probability", "drought", "streak", "completed interval", "censoring", "hard guarantee", "연속 실패", "셔플 백", "천장 보장"]
status: active
checked_at: '2026-11-13'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3:122policy/24actualPIE+24packagecases/9equal-offeredcosts/native1xmedia;fixed25%,bag4one,hard8;finite
    deterministic seeds,not fairness or statistical-independence certification
---
# Control randomness by decision timing and streak distribution

## Guidance

Classify when uncertainty becomes known and how strongly it changes outcomes. A shuffle bag samples without replacement until refill; a pity system changes conditional odds after failures or guarantees an outcome. Compute P(first success=n)=p_n*product(1-p_i for i<n), then derive expected wait and tail probabilities.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Input randomness is not automatically good and output randomness not automatically bad; the cited designers disagree. Changing odds changes the process and must not be described as independent fixed-probability trials.

**Input randomness** reveals uncertain information before a player chooses an action. **Output randomness** resolves uncertainty after commitment. A new draw may therefore offer an adaptation opportunity in one decision and resolve risk in another. For a pity system, compute the chance of success conditional on all preceding misses and compare its wait-time distribution with the independent-draw baseline. Equal averages can conceal markedly different long waits. [Keith Burgun — Randomness and Game Design](https://www.gamedeveloper.com/design/randomness-and-game-design)

## Checks

Proposed: compare mean, percentiles and maximum droughts, inspect bag-boundary repeats, and playtest whether players understand their options.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Ian Schreiber — Probability and Randomness](https://gamebalanceconcepts.wordpress.com/2010/07/28/level-4-probability-and-randomness/) — 2010 designer course; probability distributions and expected values. Checked 2026-11-07, except items explicitly marked further reading.
- [Keith Burgun — Randomness and Game Design](https://www.gamedeveloper.com/design/randomness-and-game-design) — Designer argument; input/output randomness. Normative position, not consensus. Checked 2026-11-07, except items explicitly marked further reading.
- [A Defense of Randomness in Competitive Games](https://www.gamedeveloper.com/design/a-defense-of-randomness-in-competitive-games) — Original design argument disagreeing with avoidance of output randomness. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V09, V44 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Native Unreal validation — 2026-11-13

The the historical Unreal run and its archived measurements.

Fixed independent-trial model p=1/4; a four-entry bag with one success; hard guarantee on the eighth offered draw since last success. Fixed/pity consume one FRandomStream fraction on every offered draw, including forced success. Bag selects the single success position uniformly on refill, equivalent to shuffling one success and three indistinguishable failures; no general multi-item shuffle is implemented. The next offered draw refills only after cursor4. Natural and forced successes reset pity failures. Reset restores the original stream seed and all bag/counter state, including partial bags. Fraction<.25 includes zero and excludes the exact quarter. Installed UE5.8.3 GetFraction uses upper23bits of LCG196314165*s+907633515; binary-quarter/slot thresholds are exactly representable.

Ideal iid-uniform theory is distinct from finite deterministic PRNG observations. Fixed success waits are geometric,mean4,with no finite drought cap. Bag stationary inter-success wait W=4+B-A for successive uniform positions A,B in0..3;P(W=n)=(4-|n-4|)/16,n1..7,mean4. Thus a bag can have six failures across refill and consecutive successes at a boundary;three is only the within-bag maximum. Pity wait has P(W=n)=.25*.75^(n-1),n1..7,and P(W=8)=.75^7;mean(1-.75^8)/.25,rate .25/(1-.75^8). Its long-run rate is about27.7813%,not25%. It bounds failures at7. Bag/pity outcomes depend on policy state;finite PRNG observations do not establish statistical independence. The policies are not interchangeable. Subjective fairness requires playtesting.

Eight seeds [0,1,-1,12345,-12345,2147483647,-2147483648,987654321],262144draws per seed/policy (2097152per policy) in actual PIE and a packaged player. Independent Python integer replay checks all offered outcomes through order-sensitive64bit FNV checksum,first256 values,final seed/cursor/counters,success count and full completed-wait histogram. A hash is a compact equality check,not collision-proof storage of every output. First success after reset is a startup/prefix wait;trailing failures are right-censored. Neither is incorrectly counted as a completed stationary interval. All finite observations obey draw=prefix+sum(completed waits)+tail. Per-policy success-rate absolute bound.002 and wait-CDF bound.005 were fixed before measurement;actual max CDF errors are in summary. Passing does not establish PRNG statistical independence,cryptographic quality or behavior across engine versions.

Nine sequential packaged players in orders fixed/bag/pity,bag/pity/fixed,pity/fixed/bag. Same eight seeds,128warmup+1024measured ticks,4096offered draws/seed/tick:32768per measured frame,33554432per run. Streams continue through warmup;no measurement reset. Same1280x720,DX11,Development,cap0/noVsync,no capture/audio,no assets/config changes. Equal offered draws is the workload contract,not equal internal random calls:bag uses one per four offered draws,fixed/pity one each. Independent integer replay checks every measured before/after state and cumulative outcome checksum including warmup;repeats must be exactly equal in values/order. Scope timer includes Next and identical checksum consumers;not pure RNG microcost. Complete OnBeginFrame→OnEndFrame wall and cadence include engine/HUD/observations/JSON-row creation;final save/startup/exit/video are outside steady-state samples. GPU samples are delayed whole-frame values. Frame-loop FPS is not physical display refresh. Host uncontrolled;three short repeats do not establish universal speed or budgets.

Actual success rates fixed0.24987173,bag0.25000000,pity0.27771807;observed max failures47/6/7. Original fixed-rate comparison must not claim all policies retain25%long-run success. Only this finite-seed/single-thread/in-memory binary-outcome setup is supported. Native122policy/24PIE+24packagecases/9costplayers/540frames18s1x;separate media-state/pixel checks bind displayed results. No renderer/framework/economy/network expansion;existing actualFPS gaps remain unverified. Choose by required independence/count-per-bag/wait-cap semantics before measured cost;subjective fairness remains playtesting. Latest23limited sheets/20without dedicated prototypes.
