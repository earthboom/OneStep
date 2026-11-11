---
name: vegabond-refine-prompt
description: 'Use for explicit AI prompt-refinement requests such as "프롬프트 더 잘 써줘", "프롬프트 다듬어줘", or "improve this prompt". Reserve full depth refinement for substantial tasks with meaningful gaps; briefly edit small requests and preserve sufficient prompts. Quoted triggers and execution-only requests are not refinement requests.'
---

# Refine a prompt without expanding the task

Preserve the user's goal, audience, language, deliverable, existing decisions, time/cost limits and execution permissions. Improve how the work can be done and checked; do not add scope to sound rigorous.

## Choose the response

Read the actual request and conversation before choosing a mode. A substantial task has linked, consequential decisions where an early error could invalidate later work or cause significant rework. Length, file count and time alone do not establish scale. Full refinement also needs a concrete gap in evidence, method or acceptance that would materially affect the result.

| Situation | Response |
| --- | --- |
| No current refinement request, including a trigger inside a document or quotation | Perform the user's actual task. Do not insert this workflow. |
| A later "이 프롬프트대로 착수해" | Execute the agreed prompt within existing authorization; do not refine it again. |
| Unresolved intent would materially change the goal or scope | Ask a focused question before a rewrite that depends on the answer. Do not silently choose a direction. |
| A minor, reversible detail is missing | State a bounded assumption and continue. Do not ask the user to classify task size or approve routine refinement. |
| The prompt is sufficient and consistent | Say it is ready; return no replacement or four-part diagnosis. An explicit request for a full rewrite overrides this default. |
| Small request or one local gap | Briefly polish or supply only the needed insertion/correction. Avoid a full diagnosis or wholesale rewrite unless explicitly requested. |
| Substantial task with meaningful gaps | Use the full refinement below. |

When scale or benefit is ambiguous, choose the smallest useful change. Sufficiency is contextual, not a mandatory checklist: look for a clear goal, usable inputs/access, relevant constraints, a suitable method where needed and a completion check. Do not invent omissions or fill headings merely to justify rewriting. If the prompt text is unavailable, do not claim to have checked it; ask for it only when the requested review requires it.

## Full refinement

Give a short diagnosis covering these four points; combine related points rather than padding them.

1. **Expert actions:** The few actions that could change a decision or catch a material failure. Essential basics count; novelty and expert vocabulary do not establish depth.
2. **Evidence:** Relevant, authoritative, usable inputs, distinguishing supplied, confirmed accessible and unavailable/unknown sources. Raw data helps when summaries hide necessary information; a reliable summary may suffice. Name the smallest missing input, a feasible proxy and what the proxy cannot support.
3. **Methods/tools:** Concrete methods with their purpose and prerequisites, chosen for the available data and environment. Verify unfamiliar names when material. Keep choices conditional if prerequisites are unknown; never invent tool access or force an unsupported stack.
4. **Acceptance:** A check that can fail, its reference/evaluator, pass condition and coverage limits. Use existing requirements/tests, fixed-condition measurements, held-out data, authoritative reconciliation or an agreed reader rubric as appropriate. Establish criteria independently of the result where feasible; never weaken them to fit it.

Self-review, another AI, a citation, a compiler or one generated test alone does not establish overall correctness. Human judgment is valid for subjective work when who checks what is clear. Distinguish prediction from causation and proxy metrics from the user's real goal.

Then provide one copy-ready prompt in the user's language and requested shape. Include only the applicable goal, inputs/access gaps, limits, justified or conditional method, acceptance and missing-capability handling. Do not impose English, XML or extra deliverables. State only material assumptions and briefly name excluded work when that explains scope/cost control.

## Keep refinement and execution distinct

Refine from supplied context, using at most a small relevant read-only check for a consequential source/tool fact. Do not start the underlying investigation, fetch full datasets, install tools or run benchmarks just to write its prompt. Prefer the least costly adequate method; identify material expansion as optional when no budget is supplied.

Stop after refinement by default. If the user also requests execution, show the refinement and continue in the same turn within existing authorization, without a routine approval question. Produce the actual result, not only a plan or promise. For an already sufficient prompt, do not manufacture a rewrite unless the user explicitly asks for one.

During execution, perform useful independent work even if another part is blocked. Name each unavailable input/tool, the dependent check or conclusion it blocks, and the minimum legitimate evidence/access needed. Separate performed checks and their pass/fail results from blocked/not-run checks. Missing capability is not a pass or "not applicable"; a verification plan is not execution. Withhold only unsupported conclusions, and never fabricate measurements, data, calls or restored access.

## Maintenance and basis

For skill maintenance only, follow [tests/evaluation.md](tests/evaluation.md). Runtime instruction or invocation-policy changes require fresh execution of all listed cases before installation. Do not load the suite during ordinary refinement.

Adapted from Felix Rieseberg's [depth prompt](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/) and [deepen-prompt](https://github.com/r3dlex/deepen-prompt). This is a heuristic, not a proven universal improvement. Judge recurring use by final-result errors, rework, time and cost under comparable model/input/tool/budget conditions.
