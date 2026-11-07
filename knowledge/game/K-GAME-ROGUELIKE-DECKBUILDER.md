---
id: K-GAME-ROGUELIKE-DECKBUILDER
title: Evaluate deckbuilder choices in run context and control content scope
summary: For single-player roguelike deckbuilders, seek contexts where each card matters, combine metrics with observed play, and budget the interactions created by new content.
kind: reference
scope: Single-player roguelike deckbuilder iteration; Slay the Spire developer slides and production account
keywords: [roguelike, roguelite, deckbuilder, cards, synergy, metrics, run, balance, 로그라이크, 로그라이트, 덱빌딩, 카드, 시너지, 회차, 밸런스]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Actual GDC slide text and Mega Crit original newsletter opened; no talk transcript used
  application_status: Proposed content and balance workflow; no card pool, telemetry, or run playtest executed
---

# Evaluate deckbuilder choices in run context and control content scope

## Guidance

**Source observations.** Giovannetti's slides aim for useful contexts for all cards while avoiding options that distort the whole game. They pair iteration and feedback with metrics, warn against treating data as a conclusion, and identify Ascension as skill stratification. Casey Yano's production account explains how visual limitations helped narrow narrative scope around deckbuilding and the core loop.

**Proposed reusable method.** Map a run as encounter information → tactical spending → reward selection → route or recovery choice → next encounter. Record both immediate survival and future deck consequences. For each card, define its intended situation, opportunity cost, enabling pieces, and a situation where declining it is reasonable. Inspect acquisition probability and encounter demands together: a coherent combo that rarely assembles may function as a trap rather than a reliable strategic branch.

Instrument offers, selections, skips, deck state, relevant upgrades, encounter, difficulty, and outcome. Compare cards within matching contexts before changing them. Use replay observation or tester explanation to decide whether a surprising metric reflects power, misunderstanding, selection bias, or experienced players rescuing difficult runs. Change one clear hypothesis and retain the previous build for comparison.

Treat card, relic, enemy, event, and route additions as interaction costs. Prototype a small complete run with several distinct decisions before multiplying content. Keep a cut criterion for mechanics that require substantial explanation, bespoke presentation, or exceptions without enriching the intended loop.

## Applicability and exceptions

Use for single-player runs with randomized offers and persistent consequences within a run. Competitive collectible card games require separate fairness and economy evidence; traditional dungeon roguelikes are not fully covered. Equal pick or win rates are not a universal goal. Rare, difficult, or situational cards may be valuable. Slides establish explicit developer takeaways, not the spoken reasoning behind every chart. The production anecdote supports a scope tradeoff, not a rule to remove narrative.

## Checks

- Trace several viable and failed runs; identify decisions that actually changed later options.
- Review unpopular cards in their intended contexts before buffing them; inspect dominant combinations for lost alternatives.
- Segment by difficulty and player experience, and report sample size and selection limitations.
- Estimate added interaction, text, localization, art, and testing work before approving a content batch.

## Evidence

- [Giovannetti: Metrics Driven Design and Balance](https://media.gdcvault.com/gdc2019/presentations/Giovannetti_Anthony_SlayTheSpire.pdf): actual 22-page GDC 2019 slides, especially PDF pp. 7, 10–16, 21. Slide text inspected; no complete video or transcript reviewed.
- [Mega Crit Neowsletter—October 2024](https://megacrit.com/news/2024-10-02-neowsletter-issue-3/): “On Aesthetics Driving Game Design,” final paragraphs on humanoid readability and narrative scope. Original developer text read; retrospective production account.
