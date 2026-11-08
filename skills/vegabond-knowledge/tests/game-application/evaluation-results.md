# Game application evaluation — 2026-11-07

Six independent synthetic requests exercised **project facts → questions → knowledge retrieval → technique choice → adoption decision → proposed validation**. All six handled the critical application criteria; the spelling control also exposed avoidable lookup overhead. Four fresh-context retests passed the same criteria after repair. This is AI semantic review of design responses, not game implementation or playtesting.

## Inputs and evidence

[Cases](cases.json) and the [rubric](rubric.json) were written before execution. Each performer received only its own supplied project/request, the named code or code-design skill, canonical guidance and authorized OneStep references. It did not receive expected IDs, the rubric, sibling answers or evaluator conclusions. No engine, web service or production changes were authorized within a case.

The [baseline archive](baseline-run.json) retains the six actual responses, lookup traces and hashes of 137 consultable canonical files. Those files were checked unchanged throughout baseline execution. The [semantic review](semantic-review.json) explains each criterion assessment; an ID match did not determine the outcome. Search traces are performer-recorded outputs, with evaluator inspection of responses and supporting entries. No human reviewer or independent gameplay test is implied.

## Application results

| Case | Inspected evidence → decision → proposed check | Result |
| --- | --- | --- |
| G01: jump lost before landing | Input reset/discard facts plus CONTROLLER/TIMESTEP → retain timestamped one-shot intent for the authored 80ms allowance; reject 120Hz as the missing-request repair → phase, hold, 79/80/81ms and display-rate tests. | Pass |
| G02: mobile forest | Already-instanced grass and GPU 42ms/pixel 25ms/shadow-off 34ms plus FOLIAGE/SHADOW → test distant coverage and caster cost while retaining near silhouette; reject another instancing conversion and additive savings → controlled variants, transitions and target-device p95. | Pass |
| G03: delayed fighting game | Missing snapshot fields, shared RNG and irreversible rewards plus ROLLBACK/LOCKSTEP/RNG → conditional rollback after full restoration, repeatability and effect confirmation; unknown gameplay physics remains a gate → replay hashes, wrong predictions, loss and bounded replay budget. | Pass |
| G04: wrong equipment after load | Runtime indices and unchanged schema plus SAVE → stable IDs and provenance-based migration, separately generation/commit recovery; do not guess the writer or promise Windows durability → catalog reorder/migration and interrupted-write tests. | Pass |
| G05: muzzle behind cover | Zero-latency wall reproduction plus HITSCAN/LAGCOMP → keep camera intention and add authoritative muzzle obstruction; investigate moving-target timing separately → static cover/inside-wall cases, advisory client hits and timed history traces. | Pass |
| G06: menu typo only | Complete supplied JSON → change only fallback_text; preserve localization key, action and layout → parsed field comparison. Baseline performed one unnecessary metadata query but applied no irrelevant game technique. | Critical criteria pass; efficiency finding |

G01's stylized lifecycle says the flag is cleared in the same Update, which suggests stronger loss than the intermittent symptom. The response explicitly identified this tension and requested actual writer/callback evidence; it did not claim a reproduced Unity schedule. This is a fixture limitation, not an executed engine diagnosis.

G04 also identified an important unstated migration prerequisite: both historical writers used schema 1, so an old catalog mapping alone does not identify which writer produced a save. Existing ambiguous files and already-resaved wrong equipment remain conditional instead of being silently repaired.

## Demonstrated gaps and repairs

1. **Korean discovery:** direct forest, muzzle and equipment-after-update requests returned no candidates even though the corresponding references existed. Add bounded forest/vegetation and muzzle aliases, an ordinary save alias group, and a save-compatibility concept requiring update/patch, loading, equipment/item **and a changed/wrong-item symptom**. These select candidates; they do not establish the defect's cause.
2. **Nearby false inference:** the first save concept also classified an item-icon UI loading task as save compatibility. [The intermediate observation](validation-results.json) retains that failure. Add the symptom prerequisite and a dedicated negative regression. Do not map every occurrence of loading or the ambiguous Korean word for pool/grass to a game technique.
3. **Mechanical-edit overhead:** the game reuse convention now permits complete local input to settle a spelling/format proposal without technique retrieval. G06's fresh retest performed zero searches and returned only the requested diff.

The initial ten-case lexical suite improved **5/10 → 10/10**. A subsequently added close negative exposed the intermediate overreach; the final expanded suite is **11/11**, including seven required-ID positives and four forbidden-ID controls. All three originally missed natural requests return the intended reference first. These are declared lexical cases, including author-visible wording variants; names containing `uncoached-wording` do not denote blind model trials or an unseen holdout set.

## Retests and automated checks

[Fresh retest evidence](retest-run.json) contains G02, G04, G05 and G06 with byte-identical inputs and the same rubric. All four retained sound application judgments. These runs followed the initial repair; the final Korean symptom guard was narrowed afterward. It changes lexical candidate expansion, not the entries' mechanisms. Final regression and recorded-query replays are reported separately from blind judgments.

Final results and identities are in [validation-results.json](validation-results.json): game retrieval 11/11; existing common retrieval 23/23; search unit tests 33/33; strict game catalog check 69 entries, zero errors/warnings; fixture, response and link checks. A broader exploratory run completed 75 tests with one failure: the existing source-root escape test could not create a Windows symlink or junction under this session's privileges. The other 74 passed. This environment-dependent source test is unresolved, and the full suite is not reported as all passing. Search implementation and that test were not modified.

The first broad attempt also used a restricted system temp path and inherited PYTHONPATH into a test deliberately checking missing PyYAML. Re-running in a workspace-local temporary directory and disposable venv with the existing PyYAML package resolved those setup errors. No network installation or relaxed test assertion was used.

Reproduce lexical checks with the existing Python/PyYAML runtime:

```text
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/game-application/retrieval-cases.json
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/retrieval_cases.json
python -m unittest discover -s skills/vegabond-knowledge/tests -p test_search.py
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain game --strict
```

Use a writable workspace-local TEMP/TMP/ONESTEP_TEST_ROOT for unit tests and install the already available PyYAML package into the test interpreter's site-packages rather than injecting it through PYTHONPATH: the `-S` dependency test intentionally disables site-packages. Blind semantic runs require fresh performers and the [evaluation procedure](README.md); replaying search commands does not reproduce application judgment.

No runtime, renderer, netcode, filesystem power-loss, performance or player-experience check was executed. The finite cases do not establish universal recall or correct future decisions. Keep unknown API/version guarantees and project-specific checks attached when reusing this knowledge.
