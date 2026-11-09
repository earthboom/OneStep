# Retrieval and synthesis

Use this reference for search options, related records, multi-source briefs and retrieval evaluation. Markdown details remain authoritative; catalogs and the disposable search cache are projections. Use the catalog's existing Python/PyYAML runtime; no external service is needed.

## Search a concrete question

Invoke the helper by its installed path; `--project` names the working store:

```text
python skills/vegabond-knowledge/scripts/search.py search --project . --query "메모리 풀링" --domain code --limit 3
python skills/vegabond-knowledge/scripts/search.py search --project . --query "callback shutdown" --store records
python skills/vegabond-knowledge/scripts/search.py search --project . --query "ownership" --context "engine=UE 5.8"
```

The default searches both stores, including resolved incidents, while excluding superseded primary hits. Repeat `--domain` or `--status` for alternatives. Explicit `--status superseded` includes that state. `--scope` selects a scope substring. A `--context key=value` filter uses exact case-insensitive text equality on an existing key; it is not a compatibility solver. An absent key remains with an unknown-applicability caveat. Select actual metadata values: unequal descriptions alone do not establish semantic incompatibility.

The helper expands maintained Korean/English aliases from [search_terms.json](../scripts/search_terms.json), then searches metadata and full English bodies. Identifiers, titles/keywords, triggers/symptoms and query coverage contribute to ranking. Repetition and recent dates do not create authority. Scores are lexical heuristics, not truth or applicability. Known Korean alias substrings tolerate particles; general translation and semantic retrieval are not provided. Add aliases after observed misses, rather than collecting an exhaustive vocabulary.

Compact hits show ID, summary, scope/state, path/hash, matched fields/terms, coverage and a bounded snippet with a one-based line locator. Metadata-only matches identify the header. Read useful sections and original evidence before applying consequential advice. `total_matches` and `truncated` expose omitted candidates; vary the query, filters or limit when needed. Empty results mean no lexical match under the filters, not proof of absence.

Use `--offset N` to page primary search or `related` results beyond a result limit; limits range from 1 to 100. Continue until the relevant candidates are examined. Search's automatically attached relationship page starts at zero independently of the primary offset; page a specific ID with `related` for further edges.

Relationship pages retain traversed edges touching a returned candidate, even when the other endpoint ID is on another page. This preserves conflict and prerequisite types across page boundaries; retrieve an off-page endpoint by ID when necessary.

## Original-source state

Every returned primary or related hit includes an `evidence_notice`: its `checked_at` is a recorded evidence date and its `sha256` identifies the local entry, not a fresh original-source check. For actual links to the internal source registry, `source_checks` lists each source ID with separate `access_status` and `identity_status`. Ordinary search reports `unbound` for location-free provenance or `not_checked` for a binding that has not been checked, and adds a caveat; it reads registry metadata without opening external originals or machine root settings. Other evidence links still require appropriate review.

When original identity matters and access is authorized, explicitly check the registered IDs linked by the returned page:

```text
python <search-helper-path> search --project <working-project> --query "bandaging occupied hands" --domain fiction --verify-sources --source-root <project-ID>=<authorized-absolute-path> --no-cache
```

The placeholders above are not default locations. In the actual consuming project, reuse an authorized task path or known project metadata before asking for a needed root. Do not establish external project connections in OneStep; `unbound` provenance does not ask for a root. Repeat `--source-root project=absolute-path` for distinct projects; it requires `--verify-sources` and applies only to this call. It overrides that project's persistent mapping without writing settings. Checks cover only source IDs linked by returned primary and related hits, deduplicated within the call; retrieve omitted candidates or resolve additional needed IDs explicitly with the [source helper](storage.md#portable-source-references). This is not full-evidence or automatic web verification.

The summary `source_verification` gives requested mode, source IDs, completed outcomes, successfully read files and status counts. Reconcile IDs against the evidence needed for the decision. `retrieval_ok` can be true while original verification is incomplete. Exit 0 means retrieval succeeded and any requested registered checks matched; exit 1 means a requested check is incomplete (`unbound`, `unconfigured`, `missing`, `unavailable`, `unversioned` or `mismatch`); exit 2 reports invalid input/registry/settings/ID. With no registered IDs, verification `ok` is null, never proof that all evidence was checked. Default retrieval with unchecked or unbound provenance can exit 0; preserve its caveats.

Access `available` means the bytes were read; identity `unversioned` means no expected digest exists. A current reading can support a current claim within scope, but cannot establish a historical snapshot. A hash match proves content identity only; inspect the source for meaning, authority and applicability. Neither search mode updates historical dates, expected hashes, entries or settings. Original-source outcomes are never cached and are recomputed on each explicit verification, even when the canonical search cache stays warm.

## Follow meaningful relationships

Entries may declare optional `relations` in canonical YAML, mapping these types to nonempty lists of real entry IDs:

| Type | Meaning |
| --- | --- |
| `requires` | Target supplies an essential prerequisite or contract. |
| `derived_from` | Target provides originating evidence, not independent corroboration. |
| `prevention` | Problem record points to preventive knowledge; its prevention state is unchanged. |
| `supersedes` | Source replaces target in the stated scope; retain the old detail and set its status appropriately. |
| `conflicts_with` | Reconcile the claims under their conditions; neither automatically wins. |

```yaml
relations:
  requires: [K-EXAMPLE-PREREQUISITE]
  derived_from: [R-EXAMPLE-EVIDENCE]
```

The catalog helper validates shape and target identity, including explicit cross-store targets in filtered runs. Search follows incoming and outgoing declared edges across stores/domains, including superseded candidates. Visited-ID tracking terminates cycles. These are editorial assertions, not inferred associations; follow existing prose links when the question needs them.

```text
python skills/vegabond-knowledge/scripts/search.py related --project . --id K-CODE-CONCURRENCY-LIFETIMES --depth 2 --limit 10
```

Search adds a separate one-hop relationship result by default; `--depth 0` disables it. Maximum depth is three per call. Bounded output reports truncation. Related candidates do not inherit primary-query filters or applicability: inspect their scope/state. Retrieve omitted conflicts or replacements before a dependent decision; limits do not justify omitting contradictory evidence. Continue necessary chains with individual IDs.

## Assemble and check the information brief

Use the shared [information-needs judgment](../../vegabond-scout/references/information-needs.md) before fixing the question set and before applying consequential results. It owns question completeness and adoption decisions; this reference owns finding and assembling evidence for those questions.

1. Split broad requests into answerable questions, recording required context/evidence in the existing brief.
2. Search each question across relevant stores. Begin with a few details; expand for unanswered questions, prerequisites, conflicts, replacements or failures. The initial three-detail allowance is not a completion limit.
3. Connect each material **claim/action → entry ID and useful section/line → original evidence → applicability → check**. Preserve cause/compatibility uncertainty, author choices and research limits. Separate proposed checks from demonstrated safeguards.
4. Reconcile overlap without counting a derived summary as independent evidence. Record conflicting claims and the conditions that could resolve them. Replacements govern only their documented scope.
5. Close every question as answered, conditional, conflicting or missing. Explain further lookup needs; reading the top hits alone is not completion.

Use the existing brief, not a global usage ledger. For multiple questions, `Question | Answer/action | IDs/evidence | Conditions/conflicts | Check/gap` is sufficient. Local entry hashes identify consulted bytes, not external-source truth or identity; use the existing source registry where needed.

Before storage, search the proposed question, synonyms and underlying cause across both stores. Review likely existing entries and relationships. Update an existing answer when it gains evidence/exceptions; keep incidents separate when conditions or causes differ. Never auto-merge by similarity. Validate, build affected catalogs and regenerate translations under the [storage procedure](storage.md).

## Disposable index and freshness

`.cache/onestep/search-v1.json` under the working project is Git-ignored here. It contains canonical text/hashes, never translations, generated rows or external originals. Do not commit it. Changed paths, sizes or modification times trigger rereading/revalidation; removed files disappear. Unchanged canonicals are reused without reopening them. Implementation/schema changes invalidate the cache. Atomic replacement avoids partial JSON; concurrent searches may replace each other's disposable snapshots and refresh on the next call.

Use `--refresh` after operations preserving file size and modification time, or when the snapshot is suspect: it rereads/hashes all canonicals, without checking external originals. Corrupt cache JSON is rebuilt. Invalid canonical metadata, duplicate IDs or unresolved declared relations produce explicit errors rather than successful partial results. Unavailable cache storage permits canonical results with a warning. `--no-cache` writes nothing and reads canonicals directly, for strictly read-only tasks.

Each query scans indexed text in memory; this is not an inverted or vector index. Measure representative growth before adding another engine. Timings and fixture results do not establish arbitrary future recall.

## Evaluate retrieval usefulness

```text
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/retrieval_cases.json
python -m unittest discover -s skills/vegabond-knowledge/tests
```

Versioned cases declare realistic questions, filters, required/forbidden IDs and result limits. Evaluation reports required-ID recall within limits, forbidden hits, returned IDs, snippet characters and query time; failures exit nonzero. Judgments are incomplete: forbidden-hit checks are not general precision. Extend cases after meaningful misses, bad matches, language failures, incompatible contexts or omitted conflicts. Do not alter expectations merely to fit ranking.

Unit/CLI checks cover body-only matches, resolved/superseded states, known/unknown context, incoming/cross-store relations, cycles/truncation, invalid data, cache refresh/deletion, translation exclusion and read-only use. The synthetic scale test records 1,000-entry cold/warm runs and checks retrieval, bounded output and zero warm rereads. Retain environment and limits in task evidence. Storage validation and retrieval evaluation are separate acceptance checks.

## Korean question expansion and candidate diversity

The maintained `concepts` in [search_terms.json](../scripts/search_terms.json) require a combination of observed fragments: embedded values in code plus an embedding action; implementation details plus concealment; or a mystery, reader, evidence and disclosure action. Fragments start at a word boundary and allow Korean suffixes. A generic word such as number, source or reader alone does not imply the concept. For example, source text must not be inferred from the substring inside resource. `inferred_concepts` reports the matched conditions; it is a query aid, not a confirmed interpretation of intent. Preserve the original question and check the returned evidence. This is bounded lexical expansion, not general Korean understanding. Extend positive variants and nearby negative cases together after an observed miss or misleading expansion.

Default search gives different exact bodies a turn before repeated copies, including distinct answers matching fewer query terms. It retains each candidate, its lexical score and coverage; scores and coverage need not decrease monotonically after this ordering. This trades some raw ranking priority for answer diversity, not semantic certainty. Only identical canonical bodies qualify after the parser's existing line-ending normalization, without additional case/whitespace/code normalization. Store, domain, kind, state, evidence date, cause/prevention dimensions, declared relations and context-caveat classes separate groups. Both endpoints of declared conflicts and replacements remain separate, including incoming edges outside the query filter.

This ordering does not merge records or certify interchangeable evidence. Scope and context may differ even with identical bodies. Hits expose their context and a bounded `similar_content` notice with other-match count, sample IDs and truncation. Inspect relevant variants before a version-, project- or authority-dependent decision. Resolve a sampled ID with an exact-ID query and open its canonical sections. `total_matches` still counts every matched entry; `--offset` reaches all candidates. The summary `diversity` reports eligible groups and variant matches, not semantic uniqueness or completeness.

Use `search --all-variants` to retain raw lexical order when examining individual variants or auditing the ordering. It applies only to search; relationships continue to traverse every declared ID without grouping. Differences elsewhere in a body are not grouped, even if they are near duplicates. No duplicate file, historical date or source fingerprint is rewritten. Snippets are produced only for the returned page, preserving literal locators and their 300-character bound.

For capacity decisions, use the [scale budgets, measurements and migration gates](search-scale.md). A passing 1,000-entry sentinel test is not evidence that natural-language retrieval, mixed-source judgment or tens of thousands of files will stay fast.
