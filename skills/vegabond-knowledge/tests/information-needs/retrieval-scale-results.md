# Retrieval corrections and scale regression

Checked 2026-11-07 on the working tree based on `92e7ea2`. This is evidence for the Korean question expansion, exact-body diversity and scale guidance changes, not human acceptance or a new full-text backend.

## Corrections and regression evidence

- Added three conjunctive query concepts, with visible matched conditions. Three observed misses, three composition variants and the existing shutdown paraphrase are now versioned cases. Number/code/reader words alone do not establish intent. Independent review found false hardcoding expansion for direct arithmetic and resource measurements; three failing negatives were retained and the rule narrowed to actual embedding actions and word-start matches.
- Different exact bodies take turns before repeated bodies. Every candidate remains pageable; raw order is available with `--all-variants`. State/date/cause/prevention/relations, known-versus-unknown context caveats and explicit conflict/replacement endpoints stay separate. Context and bounded variant ID notices remain attached. Source records are never merged or rewritten.
- The first equal-coverage implementation passed small fixtures but failed on the actual 1,000-entry corpus: the required ownership answer matched only one of two terms. A failing mixed-coverage regression exposed this assumption. The final ordering permits partial distinct answers before stronger duplicate variants, retaining original scores/coverage. This is an intentional relevance/diversity tradeoff, not semantic certainty.
- Cache body fingerprints and page-only snippets support the ordering. Catalog schemas, historical evidence dates and expected source hashes are unchanged. The [scale reference](../../references/search-scale.md) owns proposed budgets and migration gates; [retrieval](../../references/retrieval.md) explains the query/result contract.

## Checks

- Final unit/CLI suite: **75/75 passed**. Tests include observed and variant paraphrases, seven adjacent negatives, mixed-coverage duplicate competition, all-ID pagination/raw order, exact-ID context, incoming conflicts, state preservation and known/unknown context separation.
- Live workspace at the check: **114 entries, 23/23 query cases passed**, no declared forbidden hits. Other game-knowledge additions were occurring concurrently and were preserved; this is a retrieval snapshot, not semantic certification of that separate work.
- Independent review reran focused CLI tests and a separate context-family probe. No material findings remained after the precision correction and global-order review.

## Fixed-corpus scale rerun

Reuse the preceding audit’s 70 actual records and cyclic copies with distinct IDs/scopes. Smaller projects are read-only hardlinks to that frozen corpus; their translation stubs are never read. The 30,000-entry corpus is reused directly and only disposable search caches are replaced. This isolates the comparison from concurrent live additions and preserves the failed phase-one evidence. A frozen `92e7ea2` query implementation reproduces the old GC crowding on the same loaded documents.

| Entries | Query cases passed | Warm identifier median | Broad ownership query |
| ---: | ---: | ---: | ---: |
| 70 | 23/23 | 0.026s | 0.035s |
| 1,000 | 23/23 | 0.207s | 0.341s |
| 5,000 | 23/23 | 0.986s | 1.647s |
| 10,000 | 23/23 | 2.009s | 3.591s |
| 30,000 | 23/23 | 9.603s | 13.914s |

All five sizes pass the unchanged required-source judgments plus the added paraphrases. The frozen old GC ranking still selects its first answer and two copies at scale; the final ordering returns both required sources in the first three. This is tested target recall, not general precision or independent knowledge at 30,000 topics.

Times are helper elapsed time, including index loading and source notices but excluding Python startup; identifier medians use three warm runs, broad queries one run. Do not infer P95 or a causal speedup. Data/filesystem caches and concurrent machine activity differ from the earlier first-build audit. The new runs still take seconds at scale: whole JSON/file enumeration and text scans remain. The [migration gates](../../references/search-scale.md) therefore remain necessary.

## Actual task paths

- **Coding:** retrieve the original first-catalog incident before work, adopt its future-output distinction, and replay the real 70-entry snapshot. Eleven missing catalogs are created, strict post-check passes, repeat build writes nothing and noncatalog changes remain zero. A separate generated-row deletion restores the original code index exactly and preserves its surrounding notes/canonical details.
- **Fiction:** the reader-evidence paraphrase retrieves Knox guidance; apply fair disclosure conditionally to the previously reviewed Novel_0 identity/reveal questions, without importing genre prohibitions. All eight primary originals resolve: two matched research fingerprints, six accessible unversioned files. Their bytes equal the preceding actual-read manifest, allowing bounded reuse of that reading. The recovery-causality record remains open/unknown; this is not a new complete manuscript reading or historical certification.
- **Planning:** compare the implemented problem-record decision with the current catalog boundary and the new proposed capacity criteria. The isolated real corpus passes strict validation with one internal registry read; original 19/20-test history is retained. The capacity thresholds remain proposals and the SQLite option is unimplemented. No fictional game plan or commercial feasibility was invented.

## Reproduce and scope

```text
python -m unittest discover -s skills/vegabond-knowledge/tests
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/retrieval_cases.json --no-cache
python skills/vegabond-knowledge/scripts/search.py search --project ISOLATED_CORPUS --query "UObject GC" --domain code --limit 3
python skills/vegabond-knowledge/scripts/search.py search --project ISOLATED_CORPUS --query "UObject GC" --domain code --limit 3 --all-variants
```

Local raw scripts, CLI JSON, frozen baseline tools, failed phase one, final phase2, actual replays and test log are retained under the Git-ignored `.cache/onestep/scale-fix/2026-11-07/`. The earlier audit corpus is under `.cache/onestep/scale-audit/2026-11-07/run-01/`. These are local task evidence, not portable committed dependencies. Translation contents were not read. No manuscript, canon, historical source identity or unrelated concurrent work was changed.

Limits: near-duplicate semantics, arbitrary Korean understanding, independent unseen-topic precision, large source registries/catalog maintenance, dense concurrent access and a new backend’s gains are not established. Partial-answer promotion is visible and reversible via raw order; consuming judgment and original-source checks still govern reliance.

AI verification complete; awaiting vagabond testing or review.
