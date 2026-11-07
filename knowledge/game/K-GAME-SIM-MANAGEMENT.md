---
id: K-GAME-SIM-MANAGEMENT
title: Make production constraints discoverable before expanding recipe breadth
summary: For industrial management games, connect resource transformations, visible bottlenecks, and staged learning so expansion creates decisions rather than opaque recipe workload.
kind: reference
scope: Factory automation and industrial resource management; Factorio 2.0 and Space Age design posts from 2023–2024
keywords: [simulation, management, factory, automation, production, logistics, bottleneck, recipe, 시뮬레이션, 경영, 자동화, 생산, 물류, 병목, 제작법]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Three Wube original developer posts opened and relevant sections read
  application_status: Proposed design and prototype checks; no factory simulation or player test executed
---

# Make production constraints discoverable before expanding recipe breadth

## Guidance

**Source observations.** Wube's Factoriopedia addresses both ingredient discovery and finding uses for an item. Trigger technologies connect unlocks to encountering or producing materials. Gleba's development replaced many direct-output plants with fewer plants and deeper processing; spoilage makes throughput and waste handling consequential.

**Proposed reusable method.** Draw a material-flow graph with sources, transformations, transport limits, buffers, byproducts, upkeep, and sinks. Add the information path: how does a player discover each input, output use, unlock, and failure reason? The core loop should let players identify a constraint, change the system, and observe its effect. Expose sufficient rates and traces to distinguish missing supply, transport saturation, blocked output, and unavailable technology.

Choose one constraint that changes a planning habit, such as perishable inventory or competing uses for a seed. Connect it to existing machines and transport instead of multiplying unrelated recipes. Define startup, steady operation, shortage, shutdown, and restart behavior. If waste remains physical, provide a comprehensible removal or reuse path; if it disappears, ensure the player can still diagnose the loss.

Stage unlocks around demonstrated interactions where appropriate, then introduce optimization after the player has a working chain. Budget recipe authoring, icons, tooltips, graph navigation, and failure feedback together. A compact but interacting chain is a useful prototype before adding resources or production tiers.

## Applicability and exceptions

Applies to systemic industrial management where understanding and improving flows is the intended activity. It does not cover social simulation, city politics, financial management, or realistic industrial safety. Some players enjoy broad recipe catalogs; breadth is not inherently a defect. Discovery games may hide relationships deliberately, while an optimization game may need exact rates. Trigger unlocks can constrain player freedom and must fit the intended learning contract. Historical developer posts establish design rationale, not current numerical rules.

## Checks

- Give testers a stalled chain and ask them to locate the cause using only in-game information.
- Calculate material and energy conservation under normal production, overflow, starvation, and restart; inspect waste accumulation and deadlocks.
- Compare a new recipe's decision with existing ones; identify changes in layout, scheduling, allocation, or transport.
- Measure time spent diagnosing, redesigning, waiting, and repeating manual work; use player explanations to interpret those times.

## Evidence

- [FFF #397: Factoriopedia](https://www.factorio.com/blog/post/fff-397): “The core of the problem” and “The Factoriopedia.” Original text read; UI rationale, not usability-test results.
- [FFF #376: Research and Technology](https://www.factorio.com/blog/post/fff-376): “Discovering new materials,” “Trigger technologies,” and “We can apply this elsewhere.” Original text read; development proposal.
- [FFF #414: Spoils of Agriculture](https://www.factorio.com/blog/post/fff-414): “Spoilage” and “Design journey.” Original text read; pre-release mechanics and author judgments, not transferable balance values.
