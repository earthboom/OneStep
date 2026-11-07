---
id: "K-GAME-ECONOMY"
title: "Model game-resource flows before tuning individual rewards"
summary: "For resource-based games, trace creation, storage, transfer, conversion and removal over a defined play horizon. Compare player policies, caps and feedback loops before interpreting a spreadsheet or a single reward rate as evidence of balance."
kind: "reference"
scope: "In-game resource systems, RPG progression, strategy, management and trading; scenario models rather than financial advice or a monetization requirement"
keywords: ["economy", "sources", "sinks", "resource-flow", "feedback-loop", "simulation", "currency", "inflation", "게임경제", "보상", "재화", "수급", "소모처", "성장", "밸런스"]
status: "active"
checked_at: "2026-11-07"
context: {"evidence_check": "Named primary source text or slides inspected; source-specific access limits in Evidence", "application_status": "Source-based reference and proposed synthesis; no project gameplay trial"}
---

# Model game-resource flows before tuning individual rewards

## Guidance

Source observations: Dormans models interacting resource flows and feedback structures, then tests a simplified strategy game with scripted policies [S1]. Schreiber discusses resource generation, destruction, exchange and the different conditions of open economies [S2]. Unity maps progression-relevant resources to earning and spending activities in an F2P-oriented guide [S3].

Proposed method: define the resource and accounting boundary. For each source and sink, record amount, rate, trigger, cap, recipient and prerequisite. Track transfers separately from creation or destruction: a player trade does not itself remove currency from the whole economy. Start with a balance identity: ending stock = starting stock + created + transferred in - consumed - transferred out.

Compare plausible strategies and periods, including novice, efficient, returning and capped players where relevant. Trace a timing or reward change into progression, purchasing choices, scarce inputs, and content demand. Label model assumptions and compare predictions with authorized playtest or live observations before committing a tuning change.

## Applicability and exceptions

The account boundary may be one player, a faction, a server, or one run; conclusions change with it. Resource models omit information, execution skill and social behavior unless represented. A closed single-player economy and player-traded persistent economy have different goals. Source/sink equality is not universally desirable during growth or depletion. F2P examples do not require premium currencies, energy gates or paid acceleration in another game.

## Checks

Proposed checks: reconcile units and accounting totals; test caps and loops under alternate policies; identify runaway accumulation, starvation and dominant conversions. Report sensitivity and excluded behavior. A simulation result holds for that model and policy, not for all players or a proven stable market.

## Evidence

- [S1] Joris Dormans, [Simulating Mechanics to Study Emergence in Games](https://pure.hva.nl/ws/portalfiles/portal/141880/556168_dormans_simulating_mechanics.pdf), 2011, university repository original paper; Resource Flow / Simulating SimWar / Discussion, PDF pp. 3-7 including repository cover.
- [S2] Ian Schreiber, [Level 10: Final Boss](https://gamebalanceconcepts.wordpress.com/2010/09/08/level-10-final-boss/), 2010, Economic Systems / Open and closed economies / negative-sum discussion. Author original opened.
- [S3] Unity, [Building an in-game economy](https://unity.com/how-to/building-game-economy-guide-part-2), Understanding resources / Mapping your sources and sinks. Official guide opened; F2P framing retained.
- All checked 2026-11-07. No game economy simulation or actual player test was run here. Current Machinations documentation returned incomplete shells and was not used as inspected original evidence.
