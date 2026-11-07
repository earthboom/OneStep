---
id: "K-CODE-MAINTAINABILITY-EVIDENCE"
title: "Judge maintainability through concrete changes and multiple outcomes"
summary: "Evaluate a design or refactor with representative understanding and modification tasks, preserved behavior and change impact. Treat size, complexity and coupling metrics as evidence dimensions rather than a single proof of maintainability."
kind: "reference"
scope: "Maintainability assessment and refactoring decisions; observational Windows study and a bounded student Java experiment do not establish universal design laws"
keywords: ["maintainability", "refactoring", "empirical", "change-impact", "modularity", "comprehension", "metrics", "유지보수성", "리팩터링", "실증연구", "변경영향", "이해도", "지표"]
status: "active"
checked_at: "2026-11-07"
context: {"evidence_check": "Named original author papers or official text sections inspected; specific limits in Evidence", "application_status": "Source-based reference and proposed synthesis; no local implementation or runtime validation"}
---

# Judge maintainability through concrete changes and multiple outcomes

## Guidance

Source observations: Kim, Zimmermann and Nagappan studied Microsoft refactoring through surveys, interviews and Windows history; dependency/complexity reductions coexisted with size growth, and the paper explicitly limits causal conclusions [S1]. Tempero, Blincoe and Lottridge compared two Java designs with 40 students: modification success favored higher modularity, while the lower comprehension result was a statistical trend, not an established general effect [S2].

Proposed method: identify a representative future change and the behavior that must survive. Trace which sources, decisions, dependencies and tests a maintainer must understand or modify. Compare an existing and proposed structure on correctness, effort, locality, build/runtime cost and explanation burden. Include a second kind of change when it could expose a hidden tradeoff.

Use code metrics to locate questions, then inspect actual work and evidence. Prefer a bounded experiment or change walkthrough when the structural benefit is uncertain. Distinguish a reasoned prediction, a completed modification and longer-term defect or productivity evidence.

## Applicability and exceptions

The Windows study concerns a particular large refactoring effort and reports correlation, not isolated causation. The student experiment used a limited task and comprehension questions; the understanding trend had p=.07. Neither establishes an ideal class count or a blanket preference for more indirection. Changes in team experience, tooling and task distribution can alter results.

## Checks

Proposed checks: state a falsifiable maintenance benefit and preserve the original functional contract. Inspect changed callers and integration obligations, not only local code. Can a maintainer explain why the representation exists and where the next change belongs? Report observed results and limits without claiming fewer lines, more interfaces or a score alone establishes better software.

## Evidence

- [S1] Kim, Zimmermann and Nagappan, [An Empirical Study of Refactoring Challenges and Benefits at Microsoft](https://web.cs.ucla.edu/~miryung/Publications/tse2014-refactoringpractices.pdf), IEEE TSE 2014. Author-hosted full PDF; Abstract, discussion around Tables 5-7, and section 5 Threats to Validity inspected (PDF pp. 1,12-14).
- [S2] Tempero, Blincoe and Lottridge, [An Experiment on the Effects of Modularity on Code Modification and Understanding](https://kblincoe.github.io/publications/2023_ACE_Modularity.pdf), ACE2023. Author-hosted full PDF; sections 3.3, 4, 5 and 5.1 inspected (PDF pp. 5-7).
- Checked 2026-11-07. The assessment procedure is a synthesis; no new participant study, refactoring or maintenance-task experiment was run.
