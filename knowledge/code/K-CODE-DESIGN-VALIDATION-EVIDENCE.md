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

Lengthen a cache expiry interval to identify the latency/freshness tradeoff. For throughput bound request rate times payload size, then identify which doubled input could reverse the choice. Observe the workload before treating an estimate as a measured result. For a tutorial, agree on the intended action, verify event emission, then observe a first-time player without coaching and ask which cue informed the choice. An individual playthrough can expose a counterexample but cannot estimate a population success rate. [Review and handoff](K-CODE-ACTIVE-DESIGN-REVIEW.md)

## Evidence

ATAM identifies tradeoffs and Google's SRE workbook ch. 12 develops resource estimates. In the DynamoDB design an AWS model exposed a potential data-loss trace whose shortest path had 35 high-level steps. State which faults the model covers and verify the implementation separately. A 43-second network interruption preceded 24 hours and 11 minutes of degraded service at GitHub in 2018. Include backlog clearance and reconciliation before declaring recovery. These figures belong to their original systems. [ATAM](https://sei.cmu.edu/documents/629/2000_005_001_13706.pdf) · [SRE workbook](https://sre.google/workbook/non-abstract-design/) · [AWS paper](https://www.amazon.science/publications/how-amazon-web-services-uses-formal-methods) · [DynamoDB case excerpt](https://lamport.azurewebsites.net/tla/amazon-excerpt.html) · [GitHub recovery timeline](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/)

For concurrent state, Lamport's lecture introduces writing down the property to preserve. For game experience, Ambinder's GDC presentation uses direct observation and player reports alongside instrumentation such as death-location heatmaps. The lecture description and the available Valve slides support these method summaries. [Microsoft Research lecture](https://www.microsoft.com/en-us/research/video/thinking-above-the-code/) · [Valve GDC session](https://gdcvault.com/play/1566/Valve-s-Approach-to-Playtesting) · [Valve slides](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf)
