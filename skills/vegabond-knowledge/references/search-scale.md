# Search scale and migration gates

Use this reference when records, text volume, query frequency, duplicate density or relationship degree grows. Markdown remains authoritative; cache and future indexes are disposable projections. Keep the ordinary skill entrypoint short. See [retrieval](retrieval.md) for the current contract and [the checked regression](../tests/information-needs/retrieval-scale-results.md) for actual results and limits.

## What currently grows

Each CLI invocation loads/validates the full JSON cache, enumerates all canonical paths and builds ID/relation information before query filters. A warm `read_files=0` means unchanged details were not reparsed; it does not mean constant-cost lookup. Search scans eligible text and sorts all matches. Returning three hits bounds output, not all matching work. An entry change reparses that entry but rewrites the whole JSON cache. Body fingerprints and page-only snippets reduce repeated work; they are not an inverted index.

Exact-body diversity helps distinct answers survive duplicate competition. It cannot infer authority, interpret arbitrary paraphrases or remove semantic near duplicates. Keep unknown context, conflicting evidence and unavailable originals visible. Relationships around a heavily referenced common prerequisite can cost more than a normal query: the current traversal still scans global edges and uses a list to track selected edges.

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
| Around 5,000 entries with continuing growth; routine use approaching 10,000 | Start an indexed-search comparison. The measured file/JSON approach already incurs seconds in this range on the audited workload. Do not wait for 30,000 before planning the transition. |
| Warm P95 exceeds 2 seconds across at least 50 representative requests, or repeated lookups materially delay a task | Prioritize a search index. Aim initially for about one second, then set the real budget from use. Do not infer P95 from the small regression sample. |
| First/no-cache operations repeatedly exceed 30 seconds, one-entry updates take seconds, or peak working set exceeds a proposed 512 MiB budget | Compare incremental persistence and candidate loading against whole-JSON reads/writes. Adjust the memory budget for the device and real workload. |
| Thousands of incoming relationships accumulate on common entries | Compare a set for edge deduplication and per-ID/type adjacency. Preserve incoming/outgoing discovery, conflict visibility, bounded pages and continuation. |
| Paraphrase misses survive routing and lexical improvements | Compare Korean tokenization/query reformulation and, if justified, semantic candidate retrieval/reranking. Keep exact-ID and applicability controls; embeddings do not certify evidence or replace required-source checks. |

## Candidate transition and acceptance

Compare a local metadata table plus SQLite FTS5 as a next candidate, keeping Markdown and IDs stable. Separate import/update/delete detection from query execution; index only canonical English. Filter store/domain and established context, retrieve text candidates, then apply source/state checks and diversity. Keep source identity/access status independent and original hashing explicit. Updating an index must not rewrite historical evidence.

FTS5 supplies ranking and tokenizer options; it needs its own language and identifier tests. In particular, trigram full-text queries shorter than three Unicode characters do not match, so two-character Korean terms need a deliberate path. A content-table projection requires index consistency on changes/deletes. See the primary [FTS5 tokenizer documentation](https://www.sqlite.org/fts5.html#the_trigram_tokenizer), [BM25](https://www.sqlite.org/fts5.html#the_bm25_function) and [external-content consistency requirements](https://www.sqlite.org/fts5.html#external_content_tables). This is a comparison candidate, not an implemented backend or a proven speedup.

Accept a transition only after the same judged questions, exact identifiers, unknown-context caveats, state filters, cross-store/conflict traversal, source notices, freshness and corruption/deletion checks pass, with measured latency/memory gains. Keep before/after evidence and rollback/rebuild instructions. For a busy or changed workspace, use an isolated index/corpus so comparison cannot modify real records. Never lower recall expectations or erase conflicting variants to obtain faster numbers.
