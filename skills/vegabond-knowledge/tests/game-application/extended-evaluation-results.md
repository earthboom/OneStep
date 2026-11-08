# Extended game application evaluation — 2026-11-07

Ten new independent scenarios exercised the **32 technical sheets not inspected by the prior six-case application suite**. Together the suites have inspected all 43 technical sheets for hypothetical adoption decisions. This is coverage of reference use, not verification of 43 implementations, all source-game claims or engine behavior. Earlier keyword probes and rehearsals are not counted as independent application trials.

## Frozen cases and actual judgments

[Requests](extended-cases.json) and [criteria](extended-rubric.json) were frozen before performers ran. Each fresh context received its own supplied project facts, named specialist and authorized canonical sources, without expected IDs, other cases, evaluator conclusions or old answers. [The baseline archive](extended-baseline-run.json) retains the ten actual responses, query traces and 148 frozen source identities, checked unchanged during execution. [Semantic review](extended-semantic-review.json) assesses the decisions against the original criteria, separately from ID discovery.

| Case | New sheets actually inspected | Decision informed by the supplied conditions |
| --- | --- | --- |
| N01: storefront rendering | REFLECTION, INTERIOR, NORMAL, BILLBOARD | Flat mirror versus sealed fake room versus distant cards versus lighting detail; reject one rendering trick for every surface. |
| N02: editable cave | NOISE, VOXEL, DUNGEON | Density/meshing, Hermite prerequisites and collision-space reachability are separate; noise alone is insufficient. |
| N03: evacuation/perception/targeting | PATH, CROWD, TRACE, LOCKON | Shared routes, local jams, occlusion and persistent target choice have different contracts; faster A* is insufficient. |
| N04: smoke/water/compositing | VOLUME, WATER, BLEND | Authoritative smoke visibility, matching wave queries and premultiplied blending replace an unsupported universal fluid-solver proposal. |
| N05: camera/door/comfort | CAMERA, EASING, LEVEL, SPEED | Time-consistent follow, finite-duration transition, physical clearance and optional visual effects are separate. |
| N06: doors and combat audio | SOUND, MUSIC | Obstruction/filter/reverb and persistent musical scheduling differ; longer fades alone do not repair either. |
| N07: losses and rewards | MATCH, RANDOM-DESIGN, DDA, INCENTIVES | Estimation/search, pity, PvE pacing and bounded recoverable health remain distinct; reject hidden ranked-rule changes. |
| N08: character and debris | IK, HAIR, DESTRUCTION | Contact support, guide/render/shadow costs and physical debris activation need separate decisions; retain gameplay collision. |
| N09: retro editor/importer | PIXEL, RETRO, MEMORY | File size is not GPU residency; one affine map is not perspective; missing private-format grammar blocks a decoder commitment. |
| N10: elements and damage | SYSTEMIC, HITBOX | Directed authored state rules and per-attack damage identity replace universal chemistry and every-tick contact damage. |

All ten satisfied the frozen critical criteria. No runtime, audio listening, GPU measurement, plugin integration or player study was performed. Some numeric checks used mathematical models only. N08 disclosed filename-only sibling discovery without reading their contents; N07 disclosed an initial raw-tool-output formatting excess. Neither exposed expected answers or affected the semantic assessment.

## Empty results and competing candidates

Three synthetic exact identifiers, PteroNav-Q31, OrioleCloth-K9 and TileScript-Z17, deliberately have no corresponding contract in the supplied inputs or store. Their exact queries return **zero**; successful retrieval with zero hits is not proof a product/format is unsupported or nonexistent. Broader queries sometimes returned generic or misleading entries. The performers did not turn those into vendor guarantees. They named the missing API/version/thread/lifetime or grammar/length/endian/offset contract, deferred only dependent integration, and completed the independent route, rendering or parser-boundary analysis.

Several queries returned competing mechanisms and unrelated lexical matches. Responses were reviewed for **which decision each candidate solves**, its inputs, authority, cost and limitations. They did not choose by score or combine every hit. The game reuse convention now states both branches explicitly: bounded alternate lookup for empty results, and decision decomposition/contract comparison for multiple results. This clarifies behavior already demonstrated by the baseline; it is not presented as a newly discovered universal reasoning capability.

Three fresh-context retests (N03, N04, N09) used byte-identical inputs and the original rubric; all passed. [Their archive](extended-retest-run.json) distinguishes them from final query replay and from the later weighted-path follow-up.

## Demonstrated repairs

**Lexical discovery:** only 3/14 new Korean mechanism/symptom positives initially retrieved every required sheet within five results. The expanded initial suite, including six nearby negative controls, scored 8/20. Add mechanism aliases and bounded multi-cue rules from these observed failures. The first alias-only pass reached 12/20 and displaced one reward candidate in a multi-topic query; that intermediate result is retained in [validation evidence](extended-validation-results.json). Add the missing bounded cues and a probability-pity phrase, without treating bare ceiling, sleep, reflexes, array elements or memory fragmentation as the corresponding game mechanisms.

**Scope precision:** a general indoor-music request retrieved INTERIOR because its keyword was simply the Korean word for indoors. Narrow that sheet's Korean keywords to decorative/non-enterable windows and interior mapping. This improves retrieval scope; its rendering mechanism and evidence are unchanged.

The final lexical suite is **20/20**: 14 declared positives and six specific forbidden-ID controls. The three exact unknown-contract queries remain zero. These are author-visible finite regressions, not unseen semantic holdouts or a general precision estimate. The earlier 11-case game suite and 23-case common suite also pass.

**Weighted-flow ambiguity:** a later review noticed that PATH's old phrase “follow decreasing cost” could be transferred incorrectly to unequal edge costs. The original criteria did not specify a numeric counterexample; original passes were retained, not rescored. A baseline response explicitly included the edge cost, while a fresh retest's summary remained coarse. This exposed an ambiguity in the stored explanation, not an observed production bug or proof that the performer chose a wrong edge.

The original author's [movement-cost relaxation](https://www.redblobgames.com/pathfinding/a-star/introduction.html#movement-costs) and [flow-field discussion](https://www.redblobgames.com/pathfinding/tower-defense/) were rechecked. The corrected sheet explicitly selects c(u,v)+T(v), preserves original directed costs during reverse search, and requires a progress-guaranteed successor policy for zero-cost ties. These clauses are engineering derivations, not verbatim vendor claims. [Three graph counterexamples](weighted-flow-cases.json) show a naive total cost 101 versus 3, a zero-cost tie that can cycle, and asymmetric directed costs.

A fresh performer then solved different-number variants without receiving the expected answers: next hops Q/Z/L and costs **8/4/5**, including correct zero-cost termination and reverse-edge accounting. [Actual response and independently recomputed results](weighted-followup-run.json) are separate from the original ten-case run. The [repeatable math checker](check_weighted_flow.py) tests graph arithmetic and termination, not engine navigation or collision safety.

## Final checks and limits

[Validation evidence](extended-validation-results.json) retains exact query/filter/result replays, identity changes, empty responses, catalog checks, semantic reviews and arithmetic results. Current relevant checks: extended retrieval 20/20; earlier game retrieval 11/11; common retrieval 23/23; search unit tests 33/33; three supplemental graph checks and three independent variant calculations. Catalog and pair/link checks cover current final documents. Recorded-query replay verifies continued discoverability after changes; it does not rerun application judgment.

```text
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/game-application/extended-retrieval-cases.json
python skills/vegabond-knowledge/tests/game-application/check_weighted_flow.py
python -m unittest discover -s skills/vegabond-knowledge/tests -p test_search.py
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain game --strict
```

Use the existing Python/PyYAML runtime and writable workspace-local test temporary directories as described in the [previous report](evaluation-results.md). The broader source-root symlink/junction privilege limitation recorded there was not retested or declared fixed. No synthetic plugin API or format was added as real knowledge. No finite suite establishes perfect future recall, gameplay correctness or performance.
