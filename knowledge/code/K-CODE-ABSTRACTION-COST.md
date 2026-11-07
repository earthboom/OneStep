---
id: K-CODE-ABSTRACTION-COST
title: Introduce abstractions when they reduce total reasoning cost
summary: Evaluate an abstraction by complexity hidden and changes simplified relative to its interface, indirection, and maintenance costs; similar code alone is insufficient evidence.
kind: reference
scope: Choosing helpers, shared modules, generalization, and refactoring in maintained software; design heuristics rather than universal size or timing rules
keywords: [abstraction cost, deep module, YAGNI, DRY, premature generalization, semantic duplication, refactoring, 추상화 비용, 깊은 모듈, 중복, 성급한 일반화, 리팩터링]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Ousterhout author-hosted course notes and Fowler original essays inspected on 2026-11-07
  application_status: Reference synthesis only; proposed review checks have no demonstrated local productivity or runtime result
---

# Introduce abstractions when they reduce total reasoning cost

## Guidance

Source observation: Ousterhout favors rich functionality behind a simple interface and flags pass-through layers; his generality advice remains tied to present capabilities. Fowler's YAGNI rejects speculative features while allowing refactoring. His Design Stamina essay explicitly labels the productivity payoff a hypothesis without objective proof.

Synthesis: compare what callers must understand before and after extraction. Weigh a stable concept, owned rule, or hidden decision against added contracts, navigation, configuration, indirect control flow, debugging, and compatibility. Moving lines can simply relocate complexity.

Distinguish semantic duplication from coincidental resemblance. Sharing one rule that must change together can prevent divergence; merging independently evolving rules because their syntax resembles each other can couple unrelated changes. This is a proposed criterion, not an empirical finding from these sources. Temporary duplication can preserve freedom while the domain becomes clearer.

Choose the smallest useful generalization of current needs: perhaps a local helper, concrete module, or standard interface. A deep module can contain substantial implementation work if its contract simplifies clients. Depth does not justify unrelated responsibilities or opaque behavior.

## Applicability and exceptions

Apply when extracting repeated code, introducing layers, or designing reusable APIs. Repetition count is a clue, not a universal threshold: neither two implementations nor three copies automatically establishes the right boundary. A single complex integration may warrant abstraction immediately; several similar calculations may deserve separate ownership.

Public APIs, compatibility commitments, expensive migrations, and known variation can justify earlier design. YAGNI allows maintaining changeability. Anticipated reuse alone cannot establish value. These authors emphasize generality differently and provide judgment, not universal size targets, investment formulas, or measured payoff dates.

## Checks

Proposed design review checks:

- Show current callers before and after; list decisions and guarantees each must understand.
- Name the shared rule and why its clients should change together; separate merely similar operations.
- Count introduced concepts and configuration branches as well as deleted lines.
- Walk through a plausible new case and a divergent case; check whether the abstraction stays coherent.
- Reconsider pass-through layers that provide no policy, isolation, or meaningful contract; verify real behavior after refactoring.

## Evidence

- [Ousterhout, Modular Design](https://web.stanford.edu/~ouster/cgi-bin/cs190-winter18/lecture.php?topic=modularDesign), “Classes Should be Deep,” “Generic Classes are Deeper,” and “New Layer, New Abstraction”; author-hosted 2018 notes inspected, not the complete book.
- [Fowler, Yagni](https://martinfowler.com/bliki/Yagni.html), speculative-feature costs and refactoring clarification; 2015 essay inspected.
- [Fowler, Design Stamina Hypothesis](https://martinfowler.com/bliki/DesignStaminaHypothesis.html), pseudo-graph, hypothesis limitation, and design-payoff discussion; 2007 essay inspected. No local implementation was evaluated.
