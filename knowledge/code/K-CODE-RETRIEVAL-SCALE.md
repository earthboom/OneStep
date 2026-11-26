---
id: K-CODE-RETRIEVAL-SCALE
title: "Verify Korean retrieval quality and caller latency when scaling a Markdown index"
summary: "Compare ranked IDs on fixed questions and distractors, check external edits, and time the caller through decoding. A per-round percentile and an every-response limit can reach different verdicts."
kind: method
scope: "OneStep Markdown search, SQLite index and sequential client sessions with a prebuilt index"
keywords: ["search benchmark", "caller latency", "FTS5", "P95", "Korean paraphrase", "index freshness", "검색 성능", "3만 건", "세션 검색", "개별 응답", "색인 갱신"]
status: active
checked_at: 2026-11-23
---

# Verify Korean retrieval quality and caller latency when scaling a Markdown index

## Guidance

Freeze the corpus hashes, query order, required and forbidden IDs, result limits and acceptable empty responses. Compare displayed IDs **and their order** under the same filters. Include paraphrases, exact technical names, incident IDs and nearby questions with different causes. For a Korean paraphrase, require a meaningful combination of concepts before expanding it. Inspect terms activated by the query and an adjacent case that should leave the rule inactive. [Judged cases and transfer controls](../../skills/vegabond-knowledge/tests/scale_korean_cases.json)

## Applicability and exceptions

Time empty-index construction, warm fresh-process requests, edits and persistent sessions separately. Filesystem enumeration still grows with the canonical file count. An unchanged index can accelerate candidate selection even when some queries match most of the corpus. If real paraphrases keep failing, compare a Korean analyzer or hybrid retrieval on the same positive and negative cases. Compound decomposition and part-of-speech filtering can discard meaningful text. [SQLite FTS5](https://sqlite.org/fts5.html) · [Nori part-of-speech filter](https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-nori-speech) · [Scale and migration criteria](../../skills/vegabond-knowledge/references/search-scale.md)

## Checks

Use the caller's monotonic clock. For each new session start immediately before process launch for the first question, and immediately before encoding for later questions. Stop after reading and decoding the complete reply. With 50 sequential queries per round, the nearest-rank P95 is the 48th sorted duration. For an every-response limit, compare every unrounded duration inclusively. Count canonical rereads, verify each expected ranking and isolate build time and source verification. Insert, edit and delete one canonical file between lookups. Check that only the changed file is reread and that removal withdraws its result.

## Evidence

The 2026-11-23 experiment combined 172 project entries with 29,828 fixtures across 12 repeated topics. Top-three recall on nine Korean paraphrases increased from 3/9 to 9/9. Only eight placed the required answer first. On 50 fixed fresh-process questions the same-environment JSON control had P95 3.213 s and two SQLite runs had P95 0.527 and 0.448 s, with identical displayed order. Later fresh-process runs reached P95 1.997 and 2.405 s as machine conditions varied. For five sessions on a ready index all five P95 values passed two seconds, but only 243/250 responses passed individually. A common query produced 29,846 candidates. Ranking before building snippets reduced its traced ranking phase from 747 to 130 ms. Five subsequent sessions passed 250/250, with the same displayed results and a maximum of 1.282 s. Synthetic competition, uncontrolled OS caching and sequential requests limit inference about diverse real incidents, concurrent load and other machines. [Archived retrieval experiment](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-23-korean-retrieval-at-30000.md)
