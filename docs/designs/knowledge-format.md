# Knowledge recording and retrieval decisions

Status: implemented design record. This document explains why the existing storage and retrieval structure was chosen; it is not another execution procedure. The [knowledge skill](../../skills/vegabond-knowledge/SKILL.md) owns retrieval and capture, and the [storage guide](../../skills/vegabond-knowledge/references/storage.md) owns the current format and maintenance contract.

## Why three retrieval layers

The root index routes to domains, each domain catalog exposes searchable summaries, and each detail answers one independently reusable question or supplies one check. This lets a task narrow candidates before loading their bodies. Full logs, source documents and extended histories remain at their original locations.

The detail owns its entry metadata; catalogs are generated projections. Original project sources remain authoritative for facts, so an entry does not become a competing story bible or contract. One primary home with related-entry links avoids copies that diverge. Scope/context metadata supports different versions and works without introducing a deep folder hierarchy in advance.

## Why structured details and generated catalogs

A small header makes identity, applicability, search terms, lifecycle and evidence freshness available without reading every body. Guidance, exceptions, checks and source evidence remain in the detail. Explicit unknowns prevent an edit date or a plausible title from becoming invented verification.

The [catalog helper](../../skills/vegabond-knowledge/scripts/catalog.py) derives searchable rows and checks structural consistency. This avoids maintaining the same metadata in two places and works without a database or search service. Human translations remain separate and excluded from AI retrieval; maintenance checks their existence without loading their contents. Existing legacy material remains readable until authorized normalization, preserving provenance.

The schema, examples and CLI sequence are maintained only in the storage guide: [entry format](../../skills/vegabond-knowledge/references/storage.md#entry-header-and-body), [catalog maintenance](../../skills/vegabond-knowledge/references/storage.md#refresh-and-validate-catalogs), and [capture/lifecycle decisions](../../skills/vegabond-knowledge/references/storage.md#capture-consolidate-and-promote). This record does not duplicate those rules.

## Why bounded retrieval and selective capture

Catalog-first lookup keeps irrelevant bodies and long histories out of the working context. The information brief carries usable guidance, source pointers, conditions, checks and gaps rather than a document collection. Valid briefs can be reused; source or scope changes invalidate only affected information. Missing knowledge can lead to focused research instead of fabricated starter entries.

Capture admission and deduplication are current skill decisions, not a requirement to save every uncertainty as a record. Reusable guidance and incident history have different roles and link to each other. The skill's [lookup procedure](../../skills/vegabond-knowledge/SKILL.md#find-and-synthesize) and [knowledge-gap flow](../../skills/vegabond-knowledge/SKILL.md#close-a-knowledge-gap) are the operational authority.

## Evaluation boundary

The helper checks format and local-reference consistency, not factual truth, applicability, literary quality or whether a safeguard works. Retrieval quality needs realistic tasks, including incompatible versions, author-specific choices, conflicting sources, missing knowledge and legacy material. Useful observations include relevant matches, unnecessary body reads, avoided repeat investigation and retained caveats. Timing or larger-store claims require measurements; this design record does not establish them.
