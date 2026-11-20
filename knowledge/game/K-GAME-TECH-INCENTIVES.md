---
id: K-GAME-TECH-INCENTIVES
title: Evaluate rewards by the behavior they make worthwhile
summary: Evaluate rewards by the repeated choices they make worthwhile. Timed counterattack
  recovery trades temporary health recovery against exposure.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- risk
- reward
- grind
- automation
- aggression
- incentives
- 보상
- Regain System
- recoverable health
- push-forward combat
- recoverable health gauge
- counterattack heal
- expiry boundary
- 회복 가능 체력
- 반격 회복
- 만료 경계
- 연속 피격
status: active
checked_at: '2026-11-21'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped local Unreal evidence for timed counterattack recovery
    with authored damage and hit inputs.
---
# Evaluate rewards by the behavior they make worthwhile

## Guidance

Proposed design synthesis: define the intended repeated choice, its time/resource cost, failure consequence and alternative. Efficiency upgrades or automation can change the work rather than only increasing numbers. Attack-to-heal and time pressure can reward engagement, but compare them against safe policies and different skill levels. Consult the existing economy and combat entries before tuning.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Bloodborne producer Masaaki Yamagiwa explicitly describes a short post-hit window in which counterattacks restore part of the lost health, with recoverable health visible in the gauge. A transferable implementation tracks a bounded recoverable-damage pool and expiry, then applies eligible hits without exceeding it; renewal/stacking rules must be authored rather than inferred. This differs from ordinary kill-to-heal. DOOM's GDC presentation is an authoritative discovery lead for push-forward combat, but its description alone does not establish exact resource/drop formulas.

## Applicability and exceptions

Bloodborne's short recovery window is supported by a producer account; exact damage percentages/timing and DOOM drop algorithms remain separate questions. Rewards are not proof of enjoyment or a reason to ban cautious play.

Bloodborne's **Regain System** makes a portion of newly lost health recoverable for a limited time through eligible counterattacks. When adapting this as a risk/reward mechanic, check whether players can read the recoverable portion and whether repeated hits can restore more than the recorded loss. Retain the expiry and recovery cap as game-specific choices. [Masaaki Yamagiwa — Bloodborne combat details](https://blog.playstation.com/2014/08/13/bloodborne-on-ps4-new-combat-details/)

## Checks

Proposed: compare passive/aggressive/efficient policies, record time-to-upgrade and recovery opportunities, then test perceived agency.

## Evidence

- Reuse [resource-flow analysis](K-GAME-ECONOMY.md) for upgrade/automation costs and [combat response design](K-GAME-ACTION-COMBAT.md) for offensive incentives. These existing references retain their source-specific conditions; no new playtest is implied.

- [Ian Schreiber — Probability and Randomness](https://gamebalanceconcepts.wordpress.com/2010/07/28/level-4-probability-and-randomness/) — 2010 designer course; probability distributions and expected values. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V05, V17, V34 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.


### Follow-up evidence

- [Masaaki Yamagiwa — Bloodborne combat details](https://blog.playstation.com/2014/08/13/bloodborne-on-ps4-new-combat-details/) — Producer-authored Regain System discussion; historical 2014 design account, not exact frame/percentage data. Checked 2026-11-07.
- [id Software/GDC — Embracing Push Forward Combat](https://www.youtube.com/watch?v=2KQNpQD8Ayo) — 2018 official talk description only; detailed formulas not verified. Checked 2026-11-07.

## Designing timed counterattack recovery

Define recoverable health from actual applied damage. Use separate expiry times when later damage should leave the earlier deadline in place. If the deadline is exclusive, expire the affected amounts before resolving hits at that tick. Limit recovery by the live health deficit, remaining recoverable amount and a per-hit cap. Count a confirmed hit only once.

Show current and recoverable health as distinct gauge segments. Compare immediate engagement, delayed engagement and retreat under representative exposure. The health advantage depends on how much the counterattack recovers and how much extra damage it exposes the player to.
