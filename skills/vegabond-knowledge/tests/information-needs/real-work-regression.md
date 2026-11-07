# Real-work regression: retrieval and original evidence

Checked on 2026-11-07 against the working tree based on `9239e1c2c0b70b21cf168ac478b8818398251eb7`. This records the four requested corrections and bounded reruns of the actual OneStep/Novel_0 work. It supplements the [six synthetic cases](evaluation.md); it is not a new blind execution of them or proof of universal recall. Human acceptance remains pending.

## Corrections and executable checks

| Observed problem | Correction | Check |
| --- | --- | --- |
| The natural Korean first-catalog request missed an existing incident. | Add observed Korean/English catalog and first-build aliases. | The exact missed query and a separate variant both retrieve R-CATALOG-BOOTSTRAP within three hits against the real corpus; both are now versioned query cases. |
| Entry dates/hashes and registry links could obscure missing live-original checks. | Add evidence notices and per-source access/identity states to primary and related hits. Default lookup marks originals not checked. Explicit verification uses current reads and optional authorized temporary roots. | Default real fiction search reports nine unique IDs as not checked. Explicit verification reads all nine: one matched, eight unversioned. The two modes leave persistent settings unchanged. A regression mutates an original while the canonical entry stays cached and confirms a fresh mismatch. |
| Repeated source IDs silently returned only the last result. | Repeated `--id` returns ordered per-ID batch outcomes and counts, retaining the single-ID object shape. Invalid IDs do not hide other outcomes. | The actual eight-source fiction batch returns eight distinct outcomes: two matched, six unversioned, all accessible. Unit tests cover invalid-middle continuation, duplicate rejection and single-ID compatibility. |
| The design said referenced content was never read. | Specify that catalog validation reads internal registry metadata and explicitly related canonical entries, while external originals and local root settings remain outside catalog reads. | Observe the actual registry read during strict corpus validation and compare the corrected design with implementation. Preserve historical 19/20-test results and the separate human-acceptance boundary. |

The source helper's `completed` counts returned outcomes, including unsuccessful ones; it does not mean every identity matched. Search separately reports successfully read files. Nonzero verification from accessible unversioned files is the expected incomplete-identity result, not a failed current reading. No historical null hashes or evidence dates were filled.

## Actual request-to-application paths

### Coding: initial catalog generation and preservation

The working question was whether a first build can create its own missing catalog targets while preserving unrelated content and still rejecting unrelated missing files. Query the planned action before a symptom: `새 프로젝트 지식 카탈로그 최초 생성`, then `처음 만드는 지식 목록`. Both return the existing [bootstrap incident](../../../../records/code/R-CATALOG-BOOTSTRAP.md), rather than inferring that an empty first search proves no precedent.

Adopt the incident's scoped future-output distinction and [stable behavior-boundary checks](../../../../knowledge/code/K-CODE-CHANGE-TESTS.md). Use [data invariants](../../../../knowledge/code/K-CODE-DATA-INVARIANTS.md) as a review lens, without claiming static guarantees for Python or transferring engine-specific advice.

Replay the current real store in an isolated snapshot: 70 structured entries, 11 domain catalogs, 129 tracked nontranslation files copied; human translations represented by existence-only placeholders. Baseline build writes nothing. Remove only the snapshot's 11 catalogs: read-only check correctly fails, build recreates all 11, post-check passes, and a second build writes nothing. No noncatalog file changes. Separately remove one real generated row in the snapshot's code index: build restores the exact original index and preserves its prefix/suffix and all 71 noncatalog store Markdown files. These are current-data experiments, not a reconstruction of the incident's unavailable historical pre-fix revision.

### Fiction: existing Novel_0 chapters 002 and 003

Reuse the previously established questions about hand/weapon state, scene referents, author-selected dialogue, reader-versus-character information and the recovery's causal design. Retrieve both knowledge and resolved/open problem records. The real `bandaging occupied hands` lookup returns the hand-state incident and relevant knowledge, with original-source states attached; inspect all needed candidates rather than treating its first page as the whole manuscript review.

Use the user-confirmed Novel_0 root for this call only. Resolve the eight primary originals needed by the earlier review: BODY-MOTION, SPATIAL-BLOCKING, STYLE, N2-002-CURRENT, N2-003-CURRENT, N2-PREMISE, N2-POSSESSED-CHARACTER and N2-REVIEW-20261106. Every requested ID has an outcome. Research originals match; the six mutable/unversioned originals are readable but cannot prove their historical versions. Current bytes match the earlier actual-read manifest, so that reading remains reusable; this rerun does not claim a new full manuscript reading. The returned search page links nine IDs, a different scope from this explicitly chosen eight-source batch, and its verification counts remain separate.

Adopt current canon and the documented dialogue choice. Use physical continuity and fair-disclosure guidance within their conditions; do not impose Knox's supernatural prohibition on wuxia or turn an author preference into a universal defect. The earlier review's preserved corrections remain supported by unchanged source bytes. [The recovery-causality record](../../../../records/fiction/R-FIC-N2-RECOVERY-GAP-20261106.md) remains open/unknown: a confirmed recovery outcome does not establish how it occurred. No manuscript or canon was changed or certified historically.

### Planning: the actual problem-record design decision

Inspect the [implemented decision record](../../../../docs/designs/problem-records.md), current storage contract and helper. Extend lookup from planning to code because the decision concerns retrieval software; an empty planning domain does not end the investigation. Adopt separate cause/prevention states and scoped validation. Treat original 19/20-test results as historical evidence, not current suite counts or human acceptance.

Strict check of the actual corpus passes with 70 entries, zero errors and 43 expected `source_unverified` warnings. Instrumenting `SourceRegistry.read_internal` observes one internal `knowledge/sources.md` read; no catalog writes occur. The corrected design matches this boundary. This tests an existing software-system planning decision, not a full game's commercial viability, balance or production feasibility.

## Reproduction and limits

```text
python -m unittest discover -s skills/vegabond-knowledge/tests
python skills/vegabond-knowledge/scripts/search.py evaluate --project . --cases skills/vegabond-knowledge/tests/retrieval_cases.json --no-cache
python skills/vegabond-knowledge/scripts/search.py search --project . --domain code --store records --query "새 프로젝트 지식 카탈로그 최초 생성" --limit 3 --no-cache
python skills/vegabond-knowledge/scripts/search.py search --project . --domain fiction --query "bandaging occupied hands" --limit 3 --no-cache
```

For explicit original checks, append `--verify-sources --source-root novel0=AUTHORIZED_ABSOLUTE_ROOT` to the fiction query; never guess that root. For the exact eight-source batch, repeat `--id SRC-NOVEL0-...` with the IDs above and use `sources.py resolve --project . --root novel0=AUTHORIZED_ABSOLUTE_ROOT`. Catalog mutation experiments belong only in an isolated copy, never the live corpus or originals.

The final run passed **69 unit/CLI tests** and **16 real-corpus query cases**. An independent reviewer passed the 13 source and 27 search tests and separately checked related-hit state propagation. Review exposed a missing-PyYAML import regression; a failing CLI test was added and the structured dependency diagnostic restored before the final suite. These synthetic/unit results are distinct from the real-data paths above.

Local raw commands/results and isolated replay scripts are retained in the Git-ignored `.cache/onestep/real-work-audit/2026-11-07/fixes/`, alongside the preceding audit evidence. They are local task evidence, not portable committed dependencies. Original-source hashes, stored source identity and machine settings were unchanged by the checks. Translations were generated from English and checked for existence only. This finite audit does not establish all future recall, historical authenticity of unversioned originals, scientific truth of reference research, reader acceptance or resolution of the open fictional causal design.

AI verification complete; awaiting vagabond testing or review.
