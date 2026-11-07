# Request-to-application evaluation

Use these cases when changing information-needs judgment or a consuming skill. They supplement query-to-ID checks; they do not score judgment by keyword counts or claim universal coverage. The six projects and histories are synthetic. Do not promote them to real knowledge/problem stores.

## Prepare blind inputs

```text
python skills/vegabond-knowledge/tests/information-needs/prepare.py --project .
```

The helper uses the existing catalog/PyYAML runtime, creates fresh isolated projects under the Git-ignored `.cache/onestep/information-needs/<run>/`, and returns case IDs, skill names and request paths. `--case ID` selects cases. It never reads or copies the answer key. It creates test-only human-file existence stubs; no evaluator may read them as evidence. Existing projects are never overwritten. Do not put evaluation output in real stores.

Give a fresh performer only its case's request/project path, the named skill and relevant shared guidance. Let it derive questions and search terms from the request and supplied artifacts. Do not supply expected sources, omitted-risk hints, prior conclusions, queries or [rubric.json](rubric.json). Keep cases in separate project scopes; use an independent context per case when measuring blind performance. Skill loading is allowed; external research, real services and source changes are outside these cases.

Ask it to return the requested bounded result plus a concise evidence trace: decisions/questions and why they matter, selected source paths/IDs and useful passages, adoption/conditional/rejection/deferral where consequential, gaps and dependent actions, and proposed versus executed checks. A small local edit may need only the result and a short scope explanation. Do not force an elaborate table or extra research into the negative-control case.

## Judge meaning and observable use

After execution, the evaluator may read the case's rubric and compare it with the actual response and inspected artifacts/lookup trace. Inspect the substantive reasoning and application, not whether expected words or ID names appear. Equivalent sound questions or evidence routes can satisfy the intended behavior; an ID citation without the source's conditions does not.

For each case record separately:

- Essential questions omitted, with the decision or preserved condition affected.
- Relevant evidence not inspected or materially misread; explain equivalent evidence when acceptable.
- Wrong transfers, unsupported certainty, or an action taken beyond scope.
- Applied action or example, preservation, and verification/gap status.
- Unnecessary retrieval or blocking that does not help the requested boundary.

Pass only when material questions and evidence are accounted for, none of the critical failures occurs, and the bounded result handles remaining uncertainty correctly. A missing source may be the intended condition: success is then refusing the unsupported commitment while completing independent analysis. An empty store is not a reason to block a sufficient local input. Do not change a rubric to excuse an observed failure; clarify an ambiguous criterion with its governing input and retain the reason.

## Cases and limits

The cases cover a readability-only callback edit, provider replacement with missing guarantees and a misleading same-symptom incident, a fantasy testimony/reveal scene with conflicting authority, a cross-domain combat/economy/capacity plan, an incomparable retention claim, and a spacing-only negative control. The evaluator-only rubric retains expected judgments and failure conditions. Inputs intentionally omit prescribed queries and expected answers.

Keep the evaluated skill revision/content identity, cases run, actual artifact/response locations, findings, corrections and affected rerun results in existing task evidence or a bounded evaluation report. Distinguish human semantic review from executable fixture/search checks. No compiler, engine, audience or live-payment test is implied by these simulations. Repeat affected cases after changes; run the full set for a shared-judgment change. This finite suite samples failure modes and cannot prove no future omission or misapplication.

The [2026-11-07 checked run](evaluation-results.md) records one six-case blind execution and its limitations. It is a historical result, not an automatic pass for later skill changes.

The separate [real-work regression](real-work-regression.md) records actual coding, fiction and planning paths after the four retrieval/source/design corrections, with reproduction commands and original-evidence limits. Keep actual-data reruns, synthetic judgment evaluations and query-to-ID scores distinct.

The later [retrieval corrections and scale rerun](retrieval-scale-results.md) records Korean paraphrase/negative cases, exact-body diversity, the mixed-coverage failure exposed by actual data, and 70–30,000-entry regression results. It preserves the earlier historical reports and distinguishes the fixed corpus from concurrent live additions.
