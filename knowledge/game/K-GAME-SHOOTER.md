---
id: K-GAME-SHOOTER
title: Tune shooter weapon roles together with visual recognition
summary: Preserve the intended weapon role when changing a parameter, and make combat-relevant identities readable. Balance decisions need encounter and perception tests together.
kind: reference
scope: Shooter weapon balance and combat readability; Halo 3 and TF2 historical cases
keywords: [shooter, FPS, weapon balance, role, silhouette, readability, encounter, playtest, 슈터, 총기, 무기 밸런스, 역할, 실루엣, 가독성, 기획]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Developer presentation text and Valve paper sections read
  application_status: Historical cases; proposed synthesis not validated in a target shooter
---
# Tune shooter weapon roles together with visual recognition

## Guidance

**Source claims.** Jaime Griesemer's Halo 3 presentation compares sniper-rifle changes against the problems they address and their collateral effects. It distinguishes ammunition constraints from shot spacing and considers strength outside the intended role. Valve's TF2 paper explains that distinctive class silhouettes and controlled shading support identification under varied lighting. Neither source establishes a universal weapon interval or required art style.

**Transferable synthesis.** Write a weapon's job as a situation: range, exposure, target type, movement state, and available counter-action. Then map acquire target → aim → fire → confirm → recover/reposition. A parameter can affect several steps: reload changes exposure and encounter rhythm; projectile speed changes lead prediction and available evasions; ammunition affects sustained pressure and map routes.

Compare candidate fixes by what they preserve as well as what they reduce. If a precision weapon dominates close range, test the acquisition and recovery conditions rather than automatically reducing every hit's satisfaction. Pair this with perception: opponents must recognize the threat early enough for the intended response. Evaluate character shape, weapon pose, muzzle effects, sound, background detail, and lighting as one communication system.

## Applicability and exceptions

Useful for arena, tactical, hero, and PvE shooters, with separate assumptions for aim devices, latency, enemy AI, and team size. Equal statistics do not imply equivalent roles. Deliberate identity concealment, realism, or noisy spectacle may conflict with immediate recognition; specify the tradeoff and preserve another information channel. A historical Halo adjustment is evidence about that decision, not today's optimal value.

## Checks

**Proposed checks, not executed:** Build a small map with close, medium, and long engagements. Compare candidate changes with controlled loadouts before testing pickups, economy, and teams. Log misses, second-shot opportunities, reload deaths, and role-breaking successes. Run brief identification tests at gameplay size across backgrounds; then test moving combat where attention is divided. Ask players what they saw and could have done, separating recognition failure from aiming failure.

## Evidence

- [Griesemer, Design in Detail](https://media.gdcvault.com/gdc10/slides/Griesemer_Jaime_DesignInDetail_Sniper_Halo3.pdf), “Making the Change” and “Balance by limiting strengths,” text near the final decision; official GDC-hosted developer slides and notes opened 2026-11-07. Video not viewed; case-specific timings not adopted.
- [Valve, Illustrative Rendering in TF2](https://cdn.fastly.steamstatic.com/apps/valve/2007/NPAR07_IllustrativeRenderingInTeamFortress2.pdf), abstract and §4.1 “Character Modeling,” PDF pp. 1–2; official paper text opened 2026-11-07. Design rationale checked; no current gameplay recognition study performed.
