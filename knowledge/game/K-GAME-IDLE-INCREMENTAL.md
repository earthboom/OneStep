---
id: K-GAME-IDLE-INCREMENTAL
title: Model incremental growth and prestige around player decisions
summary: For idle and incremental games, compare production, purchase costs, multipliers and reset gains over time before choosing progression pacing. State which decisions remain meaningful during active play, waiting, offline progress and repeat runs.
kind: reference
scope: Idle and incremental resource-growth games; historical mathematical examples, not current balance values or a mandatory monetization model
keywords: [idle, incremental, clicker, prestige, growth-curve, generator, offline, automation, 방치형, 증분형, 클리커, 환생, 성장곡선, 자동화, 오프라인]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Original Kongregate articles and relevant GDC slides inspected
  application_status: Proposed planning checks; no progression simulation or gameplay trial performed
---

# Model incremental growth and prestige around player decisions

## Guidance

Source observations: Pecorella's Part I contrasts purchase-cost growth with resource production and examines generator relevance [S1]. Part III distinguishes prestige based on lifetime, maximum, or current-run earnings and cautions against treating a simplified model as accurate player behavior [S2]. The accompanying slides discuss alternate growth structures and the intended shape of repeat cycles [S3].

Proposed method: define what is accumulated, the production unit, purchase rule, unlocks, multipliers, storage limits and what resets or persists. Choose the intended decisions: purchase order, allocation, timing, collection, or discovering a new system. Model time to the next consequential change rather than only displaying large numbers.

Compare plausible purchase and reset policies across early, middle and late progression. Include discrete production cycles, offline earning, caps and automation where present. Trace one reset into the next run: what becomes faster, what new opportunity appears, and what meaningful action remains? Treat return cadence and waiting tolerance as design hypotheses to investigate with the intended audience.

## Applicability and exceptions

The cited examples describe historical versions, not current game parameters. Exponential costs and prestige are options, not requirements for every incremental game. A relaxed toy may value expression or observation more than optimization. Do not prescribe fixed reset percentages, mandatory waiting, energy gates, ads, paid acceleration, or return schedules from another game's example. Keep active effort and elapsed time distinct.

## Checks

Proposed checks: compare resource/time units, bulk purchases, milestone discontinuities, reset gains and offline limits. Look for a dominant purchase that removes intended choices, dead periods without the intended payoff, and resets that fail to change the experience. A mathematically efficient policy need not represent actual players. Record the model's assumptions and verify interpretation and pacing in authorized tests.

## Evidence

- [S1] Anthony Pecorella, [The Math of Idle Games, Part I](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-i), terminology, production/cost formulas and generator comparisons. Original author article opened.
- [S2] Pecorella, [Part III](https://www.kongregate.com/en/pages/the-math-of-idle-games-part-iii), prestige statistics, model limitations and concluding advice. Original author article opened.
- [S3] Pecorella, [Quest for Progress: The Math and Design of Idle Games](https://media.gdcvault.com/gdceurope2016/presentations/Pecorella_Anthony_Quest%20for%20Progress.pdf), 2016, PDF pp. 23, 26-27, 46-53; text inspected and relevant slide screenshots requested. The full video was not viewed.
- Checked 2026-11-07. No numerical example here is a recommendation for a new game's balance; the workflow is a proposed transferable synthesis.
