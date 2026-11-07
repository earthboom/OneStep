---
id: K-GAME-NARRATIVE-ADVENTURE
title: Plan narrative adventure through choices, state, and traversable content
summary: For branching narrative adventures, specify what players know, what choices change, and how story passages reconnect under accumulated state. Prototype representative routes and balance their resource and time consequences before expanding prose volume.
kind: reference
scope: Game planning; choice-based interactive fiction and narrative travel adventures; not universal prose or dramatic-writing rules
keywords: [narrative-adventure, interactive-fiction, branching, state, choice, ink, 내러티브어드벤처, 인터랙티브픽션, 분기, 선택, 상태관리]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Official ink tutorial and inkle development article inspected
  application_status: Reference research only; no script compiled or story playtested
---

# Choices, state, and narrative traversal

## Guidance

**Source-supported:** inkle's tutorial demonstrates linked passages, choices, visit-dependent content, repeatable versus once-only choices, live preview, and warnings for unintended loose ends [1]. Its 80 Days development account describes complexity from interconnected travel, resources, timing, and special cases. For balancing, the team used the original novel's approximately eighty-day itinerary as a reference route and compared other journeys against that spine [2]. These are implementation capabilities and a specific production example, not proof that every branching story needs the same structure.

**Reusable planning synthesis:** Define the player's role and recurring decision: whom to trust, where to travel, what to investigate, or what to spend. For each choice record the information visible beforehand, intended commitment, state changed, immediate response, and later content that reads that state. Distinguish expressive choices from strategic ones so the presentation does not promise an unimplemented consequence.

Sketch a passage-and-state graph before writing every variant. Use shared destinations with conditional acknowledgments when a permanent branch would add cost without an intended experiential difference. Preserve consequences that matter after reconnection. Plan content units around actions and discoveries, including how a player obtains necessary information; lore volume alone does not create agency.

Prototype one representative journey including a consequential choice, reconnection, setback, and ending. Estimate reading and decision time alongside travel, currency, or relationship pressures. A reference itinerary can reveal unreasonable costs without proving that all paths are balanced. Reserve production time for rare state combinations, unavailable choices, recovery situations, and localization.

## Applicability and exceptions

Useful when authored text and persistent state shape progression. Environmental storytelling and cinematic action need separate navigation and encounter methods. Converging branches can preserve expression but weaken strategic consequences if nothing remembers the choice. Unlimited branching increases writing, translation, and verification work. An eighty-day benchmark is specific to 80 Days, not a universal pacing target.

## Checks

Proposed checks: inspect choice labels against the resulting action; trace each knowledge-dependent response to a prior source; traverse representative state combinations and all authored endings; inspect loops and resource exhaustion for intended recovery or failure. Ask playtesters what they believed a choice would change, then compare with actual behavior. No reader or gameplay results were generated here.

## Evidence

1. [inkle, Writing web-based interactive fiction with ink](https://www.inklestudios.com/ink/web-tutorial/): “The anatomy of an ink story,” “Conditional content,” and “Advanced ink”; official tutorial text inspected, linked manual not assumed inspected.
2. [inkle, Journey's End...](https://www.inklestudios.com/2014/07/14/approaching-journeys-end), 2014-07-14: “The world, turns out, is big” and “Balancing”; full developer article inspected. Historical production account, not measured evidence for a new game.
