---
id: K-GAME-STRATEGY-RTS
title: Design RTS pressure through economy, information, and counterplay
summary: For competitive RTS planning, connect economic pacing and unit roles to readable opportunities for response, then evaluate outcomes across maps and skill levels.
kind: reference
scope: Asymmetric competitive 1v1 RTS; StarCraft II beta and Legacy of the Void developer accounts
keywords: [RTS, real-time strategy, economy, micro, macro, counterplay, scouting, balance, 실시간전략, 정찰, 견제, 자원, 대응, 밸런스]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Two original Blizzard developer articles opened and relevant text read
  application_status: Planning synthesis only; no RTS prototype, replay dataset, or balance test executed
---

# Design RTS pressure through economy, information, and counterplay

## Guidance

**Source observations.** Dustin Browder described initial spreadsheets followed by extensive playtesting, professional input, replays, community feedback, and statistics by race and map. The team removed needless ability steps and retained some defendable rushes. Blizzard's 2015 recap connected starting workers, economy, and diverse micro to pacing; it also described revising the Disruptor's overly binary outcomes.

**Proposed reusable method.** Map the loop as scout → interpret → allocate workers/production → commit → contest → recover. For every aggressive option, write its preparation cost, visible warning, defender response, and recovery opportunity. Specify whether the defender loses through missing information, misinterpreting it, choosing a counter too late, or failing execution. These imply different remedies.

Build a unit-role matrix containing target, effective range, movement, positional dependency, production commitment, and attention demand. Check overlaps before adding units; a new activated ability should create a decision rather than a mandatory click. Attach economy milestones to opportunities for interaction: first scouting, first attack, expansion defense, and composition transition. Changing worker counts or travel distance therefore requires revisiting attack windows and defensive production.

Prototype the smallest two-sided contest with production and a representative map. Keep desired play patterns explicit so equal win rates cannot conceal repetitive openings or unanswerable attacks. Budget unit readability, effects, AI, animation, and map support alongside the number of factions.

## Applicability and exceptions

These sources concern a demanding competitive mode. Campaigns, co-op, controller interfaces, and slower strategic games may prioritize accessibility differently. Asymmetric factions need meaningful options, not identical mechanics or equal clicks. Historical StarCraft values are examples, not transferable constants. The articles describe the developers' process; they do not establish causal proof that a particular change improves every audience's experience.

## Checks

- Replay rush, defensive, and expansion openings on several map geometries; mark warning-to-impact time and available responses.
- Segment outcomes by matchup, map, and skill; inspect replays before diagnosing an aggregate win-rate difference.
- Observe whether players understand a loss and can attempt a different response next match.
- Audit repeated inputs and ability failures for decisions, clarity, and attention overload; separately inspect professional execution limits and newcomer comprehension.

## Evidence

- [StarCraft II Beta Retrospective](https://news.blizzard.com/en-us/article/39345/starcraft-ii-beta-retrospective): Browder's answers on Frenzy, balancing techniques, and rush strategies. Original interview text read; beta-era account.
- [Competitive Multiplayer—Panel Recap](https://news.blizzard.com/en-gb/article/19955452/starcraft-ii-competitive-multiplayer-panel-recap): “Five Goals for the Future,” “Harnessing Player Feedback,” and “More Communication Helps.” Official written 2015 recap read; not a transcript or present-day balance guide.
