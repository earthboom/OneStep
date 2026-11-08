# Three targeted repairs — 2026-11-08

Scope: corrections following the review of commit `3df5e3d4804a21645bacfb271decc28f86d94334`. These are knowledge, lexical-retrieval and offline-analysis repairs. Existing frozen semantic cases, historical engine results and engine sources remain intact.

## Rollback awards

[ROLLBACK](../../../../knowledge/game/K-GAME-TECH-ROLLBACK.md) now distinguishes restored simulation state, reversible presentation and irreversible external effects. A predicted event is insufficient for an external award, even if deduplicated. Eligibility must pass the protocol's trusted confirmation boundary; peer confirmation does not inherently require a server. Stable event/recipient/match keys prevent merging or duplicating distinct confirmed effects. Durable external delivery remains a separate service contract.

The actual query `롤백 예측 KO가 방어로 보정될 때 업적 보상 확정과 재전송 중복을 어떻게 처리할까` returned ROLLBACK first within five results. Applied decision: a KO corrected to a block grants zero; a pending or untrusted event grants zero; a confirmed eligible event can be delivered idempotently. A server requirement was not inferred. These are authored, inspected regression decisions, not an unseen agent benchmark.

[Eight controlled traces](rollback-reward-cases.json) passed [the contract check](check_rollback_rewards.py), including replay/retry, separate events in one tick, separate matches and recipients, and an ineligible confirmed event. Two dedup-only negative controls demonstrably produce false awards. The model trusts a supplied confirmation flag and keeps keys only in memory. No SDK, game, network, restart, database, receiver, determinism or performance behavior was executed or established. Photon official documentation supports the distinction between predicted/cancelable and verified events; external delivery guidance is engineering synthesis.

## Query expansion

The `transparent-dark-edge` condition accepted the fragment `검`, so `검토`, `검사` and `검증` incorrectly activated blending. The pre-fix unit regression failed on all three review/inspection/verification queries. The condition now requires specific darkness forms (`검은`, `검게`, `검정`, `검다`) or the existing darkness/bleeding symptoms.

The same three negative queries pass both the fixture and real-store checks without BLEND. Existing `검은` and new `검게`/`검정` symptom queries retain BLEND. [Extended lexical cases](extended-retrieval-cases.json) add these nearby controls without changing frozen semantic requests or rubrics. This is a local lexical repair, not general Korean understanding or a completeness/precision guarantee.

## Build-independent reanalysis

Previously Traffic/Stream failed on missing ignored EXE/DLL files; original/Dynamic silently skipped absent binary verification. The pre-fix build-free integration suite exposed those failures, missing result dimensions, ignored CLI flags and implicit summary writes.

All four analyzers now validate retained reports/source identity by default, report binary verification separately, and write only stdout unless a new `--output` file is requested. `missing` is explicit; `--require-binaries` rejects it. Present mismatches/unavailable targets fail either policy. `--binary-root` supports archived layouts. Conflicting expected digests fail. Existing source/hash/numeric/archived-pilot assertions are retained. [The analysis contract](../../../../prototypes/TechniqueLab/ANALYSIS.md) defines scopes, statuses and commands.

The build-free copied fixture passed all four analyzers. Strict missing cases failed explicitly, a present wrong binary failed, changed Traffic source and a failed retained behavior check failed, and existing outputs could not be overwritten. All historical metric fields matched exactly. All four local recorded-build strict checks also passed: original EXE, Dynamic assembly, Traffic EXE/assembly and Stream EXE/assembly. The four historical summaries retained byte hashes and modification timestamps during strict reanalysis. Unity source and historical Results files have no changes. These verify analysis/provenance, not new engine execution or a complete-build certification.

## Final checks

| Check | Result |
| --- | --- |
| Knowledge unit/CLI suite | 76 passed |
| Analyzer integration/helper suite | 12 passed |
| Common / game / extended lexical cases | 23/23, 11/11, 25/25; required recall 1.0 and zero declared forbidden hits |
| Rollback contract examples | 8 passed; 2 dedup-only negative controls detected |
| Existing weighted-flow graph checks | 3 passed |
| Local recorded-binary strict runs | 4/4 analyzers passed |
| Strict game catalog | 69 entries; 0 errors, 0 warnings |
| Independent read-only code/evidence review | No actionable findings in the scoped delta |

Run the knowledge tests with `python -B -m unittest discover -s skills/vegabond-knowledge/tests` (PyYAML available), and analyzer tests with `python -B -m unittest discover -s prototypes/TechniqueLab/tests`. Run the two named contract scripts directly. Evaluate each listed JSON case file using `search.py evaluate --project . --no-cache --cases PATH`. Execute each analyzer with `--require-binaries` only when its recorded files are available. Use a writable `ONESTEP_TEST_ROOT` for temporary fixtures where needed.

Detailed command output, query results and summary identities for this local run are in the ignored `.cache/onestep/three-fixes/2026-11-08/` task evidence. Human translations were regenerated/appended from canonical or authored source data without loading translation contents. AI verification complete; awaiting vagabond testing or review.
