---
id: K-GAME-TECH-DDA
title: Distinguish adaptive pacing from hidden outcome control
summary: Choose bounded adjustments from observable pressure signals. A native two-threshold
  fixture verifies timed spawn recovery and resumption while preserving the active
  cap and unit stats.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- DDA
- rubber
- banding
- director
- pacing
- 난이도
- dynamic difficulty adjustment
- adaptive dramatic pacing
- hysteresis
- enemy spawn cadence
- recovery window
- spawn resumption
- 적 출현 간격
- 회복 구간
- 히스테리시스
- 출현 재개
status: active
checked_at: '2026-11-20'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V41 UE 5.8.3 fixed/adaptive spawn cadence in a single scripted
    arena. Native threshold/recovery/resume checks and three uncaptured runs per policy.
    Human experience and other adjustment parameters remain untested.
---
# Distinguish adaptive pacing from hidden outcome control

## Guidance

Use observable performance proxies to choose bounded adjustments: spawn cadence, resources, recovery windows or opponent pace. Separate player-selectable difficulty from dynamic pressure and from competition catch-up. Use hysteresis and cooldowns to avoid rapid oscillation.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Left 4 Dead's Director changes pacing and does not justify arbitrary enemy stat changes. Secretly changing competitive outcomes can undermine trust; no universal tuning coefficients are established.

Dynamic difficulty adjustment (DDA) changes a challenge parameter in response to player performance. **Adaptive dramatic pacing** changes the timing or population of threats to alternate pressure and recovery. Booth describes the latter for Left 4 Dead. For a new design, log the input signal and changed parameter separately. A hysteresis band uses different entry and exit thresholds to prevent rapid reversals near one threshold. [Mike Booth — The AI Systems of Left 4 Dead](https://cdn.fastly.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf)

## Checks

Proposed: log proxy, state, adjustment and reason; compare fixed/adaptive schedules and test manipulation and failure loops.

## Evidence

- [Mike Booth — The AI Systems of Left 4 Dead](https://cdn.fastly.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf) — 2009 developer slides; adaptive pacing, especially pp.79–92. Pacing is not equivalent to arbitrary difficulty scaling. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V41 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Unreal fixed and adaptive spawn cadence — 2026-11-20

The local V41 experiment compared fixed eligibility and two-threshold recovery using the same 12-second pressure trace. Cap and stats are held at three concurrent actors, health 100 and attack 10. Recovery enters at pressure 70 and exits at 45 after a minimum of 2.0 seconds. The two windows lasted 2.0 and 2.6 seconds. Both resumed spawning on the release step with a slot available. Fixed spawns totaled 15 and adaptive spawns 12, reproducibly. Whole-frame p95 ranges across three runs were 10.783–12.219 and 10.924–12.222 ms. The actor workloads differ with the policies.

Expire old actors before admitting the next spawn. Keep separate entry and exit thresholds if noisy pressure causes chatter. Quote the measured recovery and cap separately. If queued opportunities would create a resume burst, drop them and restart from a successful spawn. Use an authored trace to verify the policy and playtest the pressure proxy independently of the scheduling logic.
