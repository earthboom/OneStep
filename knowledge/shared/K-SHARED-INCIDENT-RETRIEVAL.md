---
id: K-SHARED-INCIDENT-RETRIEVAL
title: "Find earlier work from the action, observed symptom or known identifier"
summary: "Store the requester's wording and the action that could have found the case before failure. Check environment, cause and prevention evidence before reusing the result."
kind: method
scope: "Retrieval and reuse of short knowledge and incident records across software, games and fiction"
keywords: ["incident retrieval", "known-item search", "symptom", "trigger", "prevention status", "first relevant rank", "사례 검색", "재발 방지", "증상으로 검색", "사고 기록"]
status: active
checked_at: 2026-11-23
---

# Find earlier work from the action, observed symptom or known identifier

## Guidance

Someone about to act knows the task and constraints. Capture these in the incident's `trigger`. Someone investigating a failure knows what they saw. Capture that wording in `symptom`, including a distinguishing observation. Someone continuing an earlier review may know an exact ID. Preserve its spelling and punctuation. When an existing entry covers the same cause and scope, add the missing expression and a useful check there. [KCS, capture in the requester's context](https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/030/010/020) · [Sadowski et al., developer search goals](https://research.google/pubs/how-developers-search-for-code-a-case-study/)

## Applicability and exceptions

After retrieval compare the environment, affected component, cause confidence, prevention status and demonstration. Repeat a verified check where its conditions hold. Try a proposed check before relying on it. A resolved case can remain useful. A similar symptom with a different cause calls for another diagnosis. Sun et al. combined text and product/component/version information to rank duplicate reports across three projects. Their fitted weights have no local validation here. [Sun et al., ASE](https://cs.uwaterloo.ca/~cnsun/public/publication/ase11/ase11.pdf) · [Google SRE incident management](https://sre.google/resources/practices-and-processes/incident-management-guide/)

## Checks

Freeze the expected results and limit for each kind of question. Check first required rank, recall of *all* required IDs, misleading neighbors and expected empty results separately. A high first rank leaves other required items and lower-ranked errors unaccounted for. Test technical names with Korean particles, nearby longer identifiers and unrelated suffixes. Batch independent questions when they share filters and environment. Check applicability for each answer. [OneStep retrieval contract](../../skills/vegabond-knowledge/references/retrieval.md) · [Stanford CS224U, index at 7:25 and metrics at 20:01–21:13](https://www.youtube.com/watch?v=e8zKKDMAze8)

## Evidence

In a 172-record local trial, adding tuple-order and field-limit checks to an existing pathfinding entry moved it from sixth to first. The prior search code also passed the existing questions with the expanded entry. To attribute improvements, compare the old and new ranker on the same corrected documents. Separate regressions covered Korean particle boundaries and exact-ID priority. A retrieved parser incident had verified prevention. A manuscript dialogue incident had only a proposed check. [Pathfinding entry](../game/K-GAME-TECH-PATH.md) · [Archived retrieval experiment](https://github.com/earthboom/OneStep/blob/9f553ba95ec7209a5bf3fcc6ab16b119ebeb8317/docs/research/2026-11-23-korean-retrieval-at-30000.md)

BEIR provides a lexical baseline across 18 datasets. MIRACL supplies human judgments in multiple languages including Korean. Use local judgments on the actual type of record when testing indexing, reranking or Korean analysis. Public benchmark scores cannot predict precision for these short records. [BEIR](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/65b9eea6e1cc6bb9f0cd2a47751a186f-Abstract-round2.html) · [MIRACL paper](https://aclanthology.org/2023.tacl-1.63/) · [MIRACL language coverage](https://project-miracl.github.io/)
