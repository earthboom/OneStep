# Search scale and migration gates

Use this reference when records, text volume, query frequency, duplicate density or relationship degree grows. Markdown remains authoritative; cache and future indexes are disposable projections. Keep the ordinary skill entrypoint short. See [retrieval](retrieval.md) for the current contract and [the checked regression](../tests/information-needs/retrieval-scale-results.md) for actual results and limits.

## What currently grows

At 1,000 canonical entries the local helper creates `.cache/onestep/search-v2.sqlite3`. Subsequent commands enumerate canonical file names, sizes and modification times to detect external changes. An unchanged fingerprint opens a read snapshot. SQLite FTS5 selects candidate IDs, store/domain filters narrow the rows, and the lexical ranker reads their fields and bodies. Broad terms can still retrieve many candidates. The smaller JSON-cache path loads the whole snapshot. Both paths report canonical rereads in `index.read_files`.

Exact-body diversity helps distinct answers survive duplicate competition. It cannot infer authority, interpret arbitrary paraphrases or remove semantic near duplicates. Keep unknown context, conflicting evidence and unavailable originals visible. Relationships around a heavily referenced common prerequisite can cost more than a normal query: the indexed traversal follows incoming and outgoing edges at each depth, and retains relevant edges for pagination.

## Measure before deciding

Use a fresh isolated project or a read-only copy; never create benchmark records in the live stores. Keep originals and judged targets intact. Exclude human translations before reading and use existence-only stubs where validation needs them. Retain code/assets hashes, dataset provenance, entry/text/cache sizes, state/domain distribution, duplicate density, relation degree, platform/runtime and timing boundaries.

Measure separately: no-cache/first indexing, repeated warm CLI calls, common-term and scoped queries, one-entry updates and peak working set. Include source verification separately when required; default metadata notices do not hash external originals. Report startup versus helper time. Reuse enough representative requests to estimate tails; three repetitions support a median/range, not P95/P99. First access to newly created paths, OS caches, antivirus and other machine activity can dominate comparisons. Do not call a warmer second run an algorithmic improvement.

Evaluate required-ID recall within the actual result limit alongside relevance/precision judgments. Include Korean/English, paraphrases, exact identifiers, multiple required answers, unknown/incompatible contexts, active/resolved/superseded states, incoming conflicts, replacement chains and misleading same-symptom records. Hold out questions from tuning and include adjacent negative cases. A repeated-template experiment tests volume and rank competition, not the semantic accuracy of independent future knowledge. State whether catalogs, source registry size, long documents, graph shape and concurrent use also grew.

## Proposed operating gates

These are adjustable project budgets, not user-agreed SLAs or universal entry limits. Count and bytes both matter.

| Observation | Response |
| --- | --- |
| Any important judged question loses a required source or transfers the wrong context/cause | Investigate immediately, at any size. Preserve the failed input/expectation; refine routing, terms, diversity or the consuming decision and rerun affected positive/negative cases. |
| Around 1,000–5,000 entries, or earlier with long text/frequent queries | Build 50–100 real task questions plus held-out judgments. Watch known-group dominance and scope/context completeness. Compare domain/metadata prefiltering, normalized-text reuse, page-only snippets and indexed graph adjacency. |
| Around 5,000 entries with continuing growth; routine use approaching 10,000 | Check that the result reports `index.backend=sqlite` and compare end-to-end latency with the recorded baseline. |
| Warm P95 exceeds 2 seconds across at least 50 representative requests, or repeated lookups materially delay a task | Prioritize a search index. Aim initially for about one second, then set the real budget from use. Do not infer P95 from the small regression sample. |
| First/no-cache operations repeatedly exceed 30 seconds, one-entry updates take seconds, or peak working set exceeds a proposed 512 MiB budget | Compare incremental persistence and candidate loading against whole-JSON reads/writes. Adjust the memory budget for the device and real workload. |
| Thousands of incoming relationships accumulate on common entries | Compare a set for edge deduplication and per-ID/type adjacency. Preserve incoming/outgoing discovery, conflict visibility, bounded pages and continuation. |
| Paraphrase misses survive routing and lexical improvements | Compare Korean tokenization/query reformulation and, if justified, semantic candidate retrieval/reranking. Keep exact-ID and applicability controls; embeddings do not certify evidence or replace required-source checks. |

## Indexed search and recovery

The index encodes normalized Python word runs so its candidates include short Korean prefixes, postpositions and punctuated identifiers. Final matches, weights, snippets, source checks, pagination and exact-body diversity use the same rules as the scan. New and changed files are parsed once and removed paths are withdrawn. Document rows, postings, relations and the manifest commit together after ID and relation validation. An invalid edit fails the request and rolls back the transaction.

Use `--refresh` for edits preserving both size and modification time. `--no-cache` and `--portable-library` search canonical files directly. If SQLite/FTS5 or the database is unavailable, index preparation falls back to the scan and reports a warning. A damaged disposable database can be moved aside with search processes closed, then rebuilt on the next run. Initial indexing and very broad queries have separate costs.

Use the [30,000-entry workload](../tests/benchmark_scale.py) in the source checkout to reproduce fresh-process measurements. Compare the same queries, result limits, returned ID order and external-edit behavior. Classify P95 using at least 50 individual processes. Record OS cache conditions, tail outliers and build cost separately.
