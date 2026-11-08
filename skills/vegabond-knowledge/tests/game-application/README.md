# Game request-to-application evaluation

Use this suite to test the game evidence reuse convention and its consuming skills. It extends the [shared evaluation method](../information-needs/evaluation.md) with game-specific supplied artifacts. The cases are synthetic; they are not production incidents or engine execution.

## Independent execution

Freeze [cases.json](cases.json), [rubric.json](rubric.json), and hashes of the canonical guidance/knowledge before a run. Materialize each case's request and supplied files in a separate Git-ignored run directory. The supplied project facts are authoritative for that case. OneStep knowledge and records are explicitly authorized reusable references. Never copy or read human translations as evaluation inputs.

Give a fresh performer only its case directory, named skill, shared canonical guidance and store location. Derive queries from the request and artifacts. Do not reveal the rubric, expected IDs, other cases, evaluator conclusions or previous rehearsal answers. Use an independent context for each case. Do not contact external services, run an engine, change production files or treat a design proposal as a working implementation. Keep edits to the case's response and trace.

Return the requested bounded answer and a concise evidence trace: actual queries and returned IDs; inspected passages; material questions and why they affect the action; consequential adoption, conditional use or rejection; remaining gaps; proposed versus executed checks. Do not force a long research report onto the spelling-only control.

## Semantic assessment and repair

After execution, compare the actual response, inspected evidence and lookup trace with the frozen rubric. Judge meaning: did the source change the action appropriately, were material conditions handled, and was an attractive but wrong fix rejected? A retrieved expected ID alone is insufficient. Equivalent evidence or a different sound query may pass. Record query misses separately from application failures and unnecessary retrieval.

Keep omitted questions, wrong transfers, unsupported claims, scope overreach, evidence limits and concrete resulting actions visible per case. Do not relax criteria to match observed answers. A missing essential guarantee should leave the dependent commitment conditional while independent useful analysis proceeds.

Repair only demonstrated gaps. Re-run affected original cases in fresh contexts with the same inputs and rubric. A repeat with already-disclosed answers is a coached check, not a blind run. Add an uncoached variant when testing whether a repair generalizes. Save source/guidance identities, actual traces, before/after findings and limits in the bounded run report. Do not add synthetic facts to real knowledge or incident records.

Query-to-ID regression cases may be derived from actual failed queries after inspection. Their pass rate measures lexical discovery under the recorded filters and limits; semantic assessment remains separate. Catalog validity, source research, hypothetical judgment and runtime performance are four different results.

## Cases

The six requests cover jump input loss, an already-instanced GPU-bound forest, rollback prerequisites, checksum-valid save identity plus interrupted writes, static muzzle obstruction plus separate latency complaints, and a spelling-only game-menu control. The evaluator's rubric retains the discriminating conditions. This finite sample cannot establish universal recall or application correctness.

The [2026-11-07 run report](evaluation-results.md) preserves six baseline responses, four fresh retests, a nearby false-inference correction and final regression results. [retrieval-cases.json](retrieval-cases.json) is the separate lexical suite; its wording variants are author-visible regression examples, not unseen semantic holdouts.

The [extended run](extended-evaluation-results.md) exercises the other 32 technical sheets in ten new scenarios, including missing exact contracts and competing mechanisms. It retains [separate frozen requests](extended-cases.json), [criteria](extended-rubric.json), [lexical controls](extended-retrieval-cases.json), three fresh retests, and a later weighted-flow counterexample/variant check. Keep this added coverage and mathematical follow-up distinct from actual game runtime validation.

## Targeted repair checks

The [2026-11-08 repair report](repair-results.md) records rollback award confirmation, nearby Korean false-expansion controls and build-free retained-evidence reanalysis, with separate contract, retrieval and provenance limits. It supplements the frozen earlier evaluations without rewriting their results.
