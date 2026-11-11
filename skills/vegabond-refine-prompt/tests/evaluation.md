# Prompt-refinement regression tests

Use this procedure only when maintaining the skill. [rubric.json](rubric.json) is the authoritative catalog of fixed inputs and semantic acceptance criteria; ordinary prompt refinement does not load it. Each case has five criteria. Judge behavior and meaning, not exact wording or output similarity.

| Case | Boundary checked |
| --- | --- |
| RP-01 | Ambiguous scale: insert a local verification check only. |
| RP-02 | Sufficient prompt: return no replacement. |
| RP-03 | Substantial gaps: fully refine without executing. |
| RP-04 | No refinement request: perform the actual analysis. |
| RP-05 | Quoted trigger: summarize the source instead of refining. |
| RP-06 | Later execution request: execute the earlier prompt once. |
| RP-07 | Small request: briefly polish without a depth diagnosis. |
| RP-08 | Materially different goals: ask a focused question first. |
| RP-09 | Minor missing detail: state a bounded assumption and patch locally. |
| RP-10 | Combined request: show the rewrite, then execute without routine approval. |
| RP-11 | Combined request with unavailable access/tools: do useful work and report dependent blockers. |

## Run and judge

1. Fingerprint the candidate `SKILL.md`, `agents/openai.yaml`, this guide, the rubric and case inputs. After a runtime instruction or invocation-policy change, run every case before installing the candidate. For test-only additions, existing cases may be referenced only after their candidate, policy, input and criteria identities are checked unchanged; label that scope as partial, not a new full-suite run.
2. Use one fresh-context performer per case, or separate clean sessions. Supply only the candidate skill/policy paths, one case path and the neutral instruction below. Withhold this guide, the rubric, other cases, historical responses and expected judgments. If an independent context is unavailable, record `not_run` rather than simulate forgetting the previous case.
3. Save the actual response verbatim. Then evaluate every criterion for that case as `pass`, `fail` or `not_run`, with the specific observed evidence. All required criteria must pass. A format validator checks structure only; it cannot replace semantic review. Do not change acceptance criteria to excuse a failure.
4. Keep runs in [results.json](results.json), with source/input/rubric hashes, execution scope, verbatim response-file paths/hashes, judgments and limitations. Prior evidence is preserved through the archive references there. Never treat an old pass as validation of a changed candidate. A fixture correction must retain the old input, response and failure and state what changed; runtime changes require fresh execution of all cases.
5. After passing, install that same candidate and required test resources and compare hashes. Keep original Korean requests and the conversation fixture unchanged unless a demonstrated fixture defect requires a separately recorded correction. Never read `*.kr.md` human translations as instructions.

Neutral performer instruction (substitute actual paths):

```text
Read <candidate-skill>/SKILL.md and <candidate-skill>/agents/openai.yaml, then respond to the user request in <case-file>, deciding whether that skill applies. Treat the case as an independent conversation. If it is JSON with a messages array, use the earlier messages as conversation context and answer only the final user message. Read no other files. Do not read test guides, saved results, other cases, or *.kr.md files. Do not browse or change files. Use the supplied information to answer the actual request; when it asks only for prompt refinement, do not execute the underlying task. Return only the actual Korean user-facing response, without evaluator commentary.
```

## Evidence boundaries

The fixtures require no external services or changes to underlying projects. RP-04, RP-06, RP-10 and RP-11 use supplied synthetic data; RP-05 summarizes supplied text. RP-06 is a role-labelled conversation fixture, not a host UI integration test. RP-08 checks only the first clarification turn. RP-11 models declared access/tool unavailability, not real failed calls or restored connections.

A passing response does not prove real churn causality, actual refactor/report quality, automatic skill discovery, cross-model repeatability or live permission handling. Count only freshly executed cases as fresh tests. Keep successful and failed history separate from current candidate coverage; load a referenced historical record only when needed.
