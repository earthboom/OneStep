---
name: vegabond-research
description: Use when investigating a question, comparing options, or supplying evidence for a defined step of another task, using relevant sources in any domain.
---

# Vegabond Research

Deliver an evidence-based answer within the requested scope. Reuse the brief and task profile supplied by scout. If invoked directly, use [scout's shared setup](../vegabond-scout/SKILL.md#frame-and-classify) without rerouting, and follow the [agent instructions](../../agents/vegabond-agent.md) for document boundaries, verification, and acceptance.

## Refine the inquiry

Use the shared [information-needs judgment](../vegabond-scout/references/information-needs.md) to test whether the questions cover the decision and relevant counterevidence. Return source applicability and gaps without treating agreeing summaries or successful searches as independent proof or whole-task coverage.

Use [vegabond-knowledge](../vegabond-knowledge/SKILL.md) for existing sources, claims, and known gaps, reusing scout's information brief. Verify them against the question and current evidence. In read-only work, return proposed knowledge updates with the findings rather than changing stores.

Use the shared profile to refine the question or decision and its comparison criteria. Apply the relevant specialist's research method and claim-specific checks through [scout's shared mapping](../vegabond-scout/SKILL.md#connect-steps-to-skills-and-checks). Correct unsupported reasoning or the answer, not the investigated sources. Sources may be supplied material or external evidence; web search is not always required. Refine only missing inquiry details rather than repeating the shared assessment.

For supporting research, answer the calling step's question instead of taking ownership of the whole creation or revision task. Leave investigated sources unchanged; producing a requested answer or report does not authorize implementation changes.

When knowledge retrieval supplied an unanswered question, use that gap and its conditions directly; do not send it through the same lookup again. Investigate only the concepts and prerequisites needed for the decision, expanding when evidence reveals a material dependency.

## Investigate

1. Turn the question into answerable subquestions or comparison criteria. Bound the investigation to what the requested answer or decision needs.
2. Examine primary sources where available, checking dates, versions, and applicability. Link material conclusions to evidence, address contradictions, and distinguish supported facts from inference. Unavailable evidence remains a limitation.
3. Synthesize the answer or recommendation against the criteria. Stop when questions are supported or remaining evidence gaps are explicit; pursue further searches only when they could materially change the conclusion. Do not present unresolved acceptance conditions as verified.

Hand back the answer or requested report, supporting source references, reasoning, and material uncertainty. Make clear which conclusions are established and which still depend on assumptions or missing evidence.

For a knowledge-gap handoff, identify what the sources establish, what the caller must check in its environment or artifact, and any reusable candidate with its conditions. Return these to the calling step and [knowledge's gap-closing flow](../vegabond-knowledge/SKILL.md#close-a-knowledge-gap); the specialist verifies application and knowledge handles selective storage within the existing write scope. Research alone does not certify execution or require a new stored entry.
