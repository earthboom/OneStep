---
id: K-GAME-ACTION-COMBAT
title: Design combat around readable threats and meaningful responses
summary: Specify what players can perceive and do against each threat, then teach those responses through enemy behavior. Transfer the method conditionally rather than copying reaction timings.
kind: reference
scope: Action combat; enemy and ability design; PvE and conditional PvP transfer
keywords: [action, combat, enemy design, counterplay, telegraph, encounter, prototype, playtest, 액션, 전투, 적 설계, 대응, 전조, 전투 기획, 플레이테스트]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Official developer articles read; no gameplay experiment performed
  application_status: Transferable synthesis and proposed checks; untested in a target game
---
# Design combat around readable threats and meaningful responses

## Guidance

**Source claims.** Riot describes counterplay as a player's available response to an enemy threat; intelligible responses support agency and back-and-forth depth. PlatinumGames explains that NINJA GAIDEN 4 increased enemy mobility alongside player mobility while preserving reaction opportunities. Early soldiers allow experimentation, while officers encourage using the new stagger system. These are two different combat contexts, not a shared timing formula.

**Transferable synthesis.** For each enemy action, specify the cue, threatened space, player response, cost, and consequence. Build the repeated loop as perceive → choose → commit → read outcome → reposition. A dodge that always cancels every commitment may erase the decision; an attack with no observable cue may turn learning into guessing. Decide which effect is intended before adjusting damage.

Use enemy combinations to test interactions between spacing, camera, animation, stamina, target selection, and recovery. Introduce a response where players can discover its value, then combine it with another pressure. Keep alternatives visible: a specialist response can be efficient without making every other action useless. This sequencing is a proposed planning method, not a reported result from either developer.

## Applicability and exceptions

Useful for real-time melee, character action, boss fights, and abilities that invite reactions. Strategic preparation or positional avoidance can provide counterplay when an individual hit is deliberately unreactable. Horror, ambushes, and attrition may intentionally limit immediate agency; state that experience target and inspect the larger recovery loop. PvP advice needs separate latency and skill-bracket checks.

## Checks

**Proposed checks, not executed:** Prototype one threat and two responses before a full encounter. Ask unfamiliar players to identify the cue and explain their loss before explaining the rule. Record whether failure came from recognition, decision, execution, or missing information. Repeat with multiple enemies and the production camera; verify that effects and off-screen attacks preserve the intended response. Compare costly and cheap responses for dominant repetition.

## Evidence

- [Riot, Champion Counterplay](https://www.leagueoflegends.com/en-us/news/dev/quick-gameplay-thoughts-may-14/), “Champion Counterplay,” opening definition and fairness/depth discussion; official article text opened on 2026-11-07. Supports the stated design rationale, not universal player outcomes.
- [PlatinumGames, NG4 Enemy Battle Design](https://www.platinumgames.com/official-blog/article/14074), opening mobility discussion and D.D.O. soldiers/officers paragraphs; official text opened on 2026-11-07. Videos and in-game behavior were not tested; numerical timings are not generalized.
