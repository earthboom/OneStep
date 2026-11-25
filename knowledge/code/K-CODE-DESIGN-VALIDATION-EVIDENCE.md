---
id: K-CODE-DESIGN-VALIDATION-EVIDENCE
title: "Choose evidence for a risky design assumption before committing dependent work"
summary: "Choose a scenario, caller measurement, state model, recovery exercise or playtest according to the claim that would change a design decision. Record the conditions and what remains untested."
kind: method
scope: "Software and game architecture decisions under uncertain quality goals, capacity, state transitions or recovery assumptions"
keywords: ["architecture evaluation","ATAM","design validation","state model","model checking","recovery exercise","capacity planning","설계 검증","검증 방법","가정 검증","위험 분석","모델 검사","복구 검증","성능 추정","설계 반례","상태 전이"]
status: active
checked_at: 2026-11-25
---

# Choose evidence for a risky design assumption before committing dependent work

## Guidance

Start with the decision and a plausible observation that would reverse it. For competing quality goals, vary one architectural parameter and identify which goal improves and which degrades. For capacity, estimate resources under a stated workload and measure a representative case at the caller. For recovery, interrupt on each side of acknowledgement and follow state through restart, reconciliation and resumption. A small state model can explore interleavings that a walkthrough misses.

## Applicability and exceptions

Invest in the experiment when a wrong assumption is costly and the result can still change a decision. Model coverage depends on the states and faults represented. A capacity estimate needs workload measurements. For a claim about player comprehension, use [the existing playtest method](../game/K-GAME-PROTOTYPE-PLAYTEST.md). A design review alone cannot establish any of these runtime outcomes.

## Checks

For autosave, identify the saved version promised after acknowledgement. Trace a crash just before and just after acknowledgement. If the result depends on platform file replacement semantics, check the target runtime before committing work that relies on it. Replay the counterexample after revision. Record the predicted or observed outcome, conditions, remaining check and owner.

## Evidence

ATAM identifies tradeoffs, Google's SRE workbook ch. 12 develops resource estimates, AWS gives an example of a model exposing an interleaving defect, and GitHub's incident shows why restored connectivity can precede service recovery. These are method and case sources, not measurements for the working project. [ATAM](https://sei.cmu.edu/documents/629/2000_005_001_13706.pdf) · [SRE workbook](https://sre.google/workbook/non-abstract-design/) · [AWS paper](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods) · [GitHub recovery timeline](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/) · [Research and source notes](../../docs/research/2026-11-25-design-review-and-cross-check.md)

For concurrent state, Lamport's lecture introduces writing down the property to preserve. For game experience, Ambinder's GDC presentation uses direct observation and player reports to interpret play. [Microsoft Research lecture](https://www.microsoft.com/en-us/research/video/thinking-above-the-code/) · [Valve slides](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf)
