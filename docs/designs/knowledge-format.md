# Knowledge recording and retrieval design

Status: implemented. The [storage procedure](../../skills/vegabond-knowledge/references/storage.md) is the active format and CLI contract; this document retains the design rationale. The existing domain folders, project boundaries, human-only translations, and information-brief contract are preserved.

## Retrieval layers

Use three layers: the root index routes to domains, each domain catalog offers short searchable summaries, and each detail answers one independently reusable question or supplies one check. Split different applicability conditions or unrelated questions; merge examples of the same underlying method or cause. Keep full logs, source documents, and extended case histories at their original locations.

The detail is authoritative for its entry metadata. Catalog rows are generated projections, not a second manually maintained account. Referenced project sources remain authoritative for their facts; a knowledge summary does not become a second story bible or contract.

## Common entry header

Use a small YAML header in new or updated English knowledge details. Existing prose-only entries remain readable and are normalized during authorized maintenance, preserving IDs and evidence.

| Field | Purpose |
| --- | --- |
| `id` | Stable identity independent of title changes. |
| `title` | Specific question, method, or subject. |
| `summary` | One or two sentences stating the usable point with its essential condition. |
| `kind` | Reference, method, convention, or lesson; do not mistake a local choice for a universal fact. |
| `scope` | Project, component, work, or applicability boundary. |
| `keywords` | Useful English search terms, synonyms, and exact technical identifiers. |
| `status` | Existing knowledge states: active, enforced, or superseded. |
| `checked_at` | Actual last evidence check date; null if unknown, never an automatic edit timestamp. |

Add `context` only when needed for a version, engine, format, genre, viewpoint, or other applicability condition. Do not add irrelevant empty fields. Put detailed exceptions and evidence in the body.

Example only; this creates no live entry:

```yaml
---
id: K-FIC-001
title: Check information access in limited viewpoint
summary: Under limited narration, check each claim against the focal character's information access before line polishing.
kind: method
scope: naru-novel; Seorin-limited narration
keywords: [viewpoint, POV, character-knowledge]
status: active
checked_at: 2026-11-04
context:
  viewpoint: third-person limited
---
```

The header is data, not skill-discovery metadata. Human translations present the same information for readers without duplicating discovery frontmatter; they remain excluded from retrieval.

## Detail body

Use four short sections:

1. **Guidance:** what to do or understand, preferably as an applicable action rather than a vague reminder.
2. **Applicability and exceptions:** when to use it, when not to, and current source/version dependencies.
3. **Checks:** observable acceptance or prevention checks; distinguish automated enforcement from editorial judgment.
4. **Evidence:** original source references and locations, demonstrated cases or incident links, and the context of the evidence check.

Content length follows the question. Keep the immediately useful guidance short; link extended examples rather than copying them. An unsupported diagnosis stays in a problem record instead of being promoted into a lesson.

Problem details use the same searchable header fields, with finding kinds such as error, suggestion, or hypothesis and existing open/resolved/superseded states. Their body covers expected versus observed behavior, cause confidence, correction, recheck, and prevention links. Keep the reusable guidance in knowledge and the incident history in records, linked in both directions.

## Generated catalogs

Generate one row per entry from its header and file path: **ID/title/kind | summary | scope/context | keywords | status/checked date | detail**. The root index still lists domains only. Read catalog matches, not entire catalogs.

The [local helper](../../skills/vegabond-knowledge/scripts/catalog.py) rebuilds affected catalogs and validates duplicate IDs, missing fields, invalid states, local file references, and missing translation pairs. It preserves unknown legacy information rather than inventing metadata or silently dropping entries. No database or search service is required. Translation generation remains the knowledge skill's responsibility; the helper checks existence without opening translations.

## Lookup and delivery

1. Reuse the caller's project/profile and current information brief. Translate a Korean question into English search concepts while retaining exact source names and technical identifiers.
2. Select relevant domains and filter by scope, context, and lifecycle state. Rank by question fit and evidence applicability, not recency alone. Add shared material or related entries only for a concrete need.
3. Retrieve bounded matching catalog rows. Start with up to three promising details, reading their header and useful sections. Follow evidence or dependencies when the question requires them; three is a starting point, not an investigation limit.
4. Return the existing information brief: applicable guidance plus source IDs/paths, conditions/exceptions, concrete checks, and gaps/conflicts. Preserve the type and scope of each recommendation. Do not send a full document collection.
5. Reuse that brief until its question, scope, entry content, or governing source changes. Track the consulted IDs and content revisions/hashes in task evidence where needed; do not persist a global cache of project facts.

If the catalog is absent or demonstrably stale, use targeted metadata lookup within the selected domain. Rebuild only within authorized write scope; read-only work reports the catalog problem. A failed lookup is a gap, not evidence that knowledge does not exist. Existing research routing supplies genuinely missing information.

## Save and check

Search for the same topic/cause first. Update its canonical detail or create a genuinely distinct entry, then refresh the affected catalog and human translations together. Record a new checked date only after checking the relevant evidence. Keep superseded provenance and stable IDs; do not reread all history after unrelated work.

Validate the design with representative code, fiction, presentation, and planning requests plus incompatible versions, author-specific exceptions, missing knowledge, conflicting sources, legacy entries, and larger catalogs. Observe correct relevant-entry retrieval, irrelevant body reads, repeated reads avoided, lookup time/output volume, and catalog/detail consistency. Faster retrieval must preserve material caveats and unresolved evidence.
