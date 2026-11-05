---
name: vegabond-knowledge
description: Use when a task needs stored domain references, project conventions, prior corrections, or verification guidance, or when saving and maintaining knowledge and problem records.
---

# Vegabond Knowledge

Retrieve and maintain knowledge and problem records for the active task. Reuse scout's profile; the calling operation or specialist judges applicability and verifies the actual deliverable. Follow the [agent instructions](../../agents/vegabond-agent.md) for document boundaries and completion. This skill supplies information; it does not take over creation, revision, or research, and reading it does not spawn an agent.

## Request and return

A request states the **working project, question, relevant domains, target and constraints, and environment/version or story context** where relevant. Reuse the existing brief instead of asking for those details again. A storage request additionally supplies findings, evidence, resolution, and proposed reusable checks.

Return a short information brief containing:

- **Applicable knowledge:** what can help this step, with source IDs and paths or links for each material claim.
- **Conditions and exceptions:** where it applies, why a prior incident matches, its cause confidence and verification context, and what conflicts with the present request or sources.
- **Checks:** concrete prevention or acceptance checks to carry into the work, with the originating record ID, prevention state and evidence. A resolved incident does not by itself establish verified prevention.
- **Gaps:** missing, stale, conflicting, or unconfirmed information and the question it leaves open.

## Find and synthesize

1. Reuse an existing information brief while its question, scope, consulted entry content, and governing sources remain valid. Search again when one changes or new evidence exposes a gap. Keep consulted IDs and revisions/hashes in task evidence when needed, without creating a global cache of project facts.
2. Use the working project's known stores first. The default routes are [knowledge](../../knowledge/index.md) and [records](../../records/index.md) in this repository; in another project, resolve paths there rather than automatically using OneStep's project facts. Use an existing native store when suitable. Shared OneStep material is an additional source only when explicitly configured or requested. Do not search unrelated projects.
3. Choose the relevant domain indexes from the profile; combine domains for mixed work. Translate Korean questions into useful English concepts and synonyms while retaining exact source names and technical identifiers. Read small routing indexes to select locations. Retrieve bounded matching catalog rows by question, scope/context, and state; prioritize applicability over recency. Keep retrieval at that level after a successful search rather than opening the entire catalog. Exclude `*.kr.md` before retrieval. Consult `shared` only for a relevant cross-domain need.
   Before work, search problem records by the planned action and conditions against `trigger`, even when no symptom is known. After a failure, search `symptom` and exact identifiers, then compare conditions and cause evidence. Keep resolved incidents in the candidate set. Exclude known incompatible scopes; retain unknown compatibility as a caveat instead of silently treating it as incompatible. Matching symptoms do not establish a matching cause. An absent trigger is a lookup gap, not evidence that an incident is irrelevant. This is scoped catalog retrieval using available tools, not an automatic ranking service.

4. Start with up to three relevant detail files across the selected stores, reading the header and useful sections first. Check applicability and follow original evidence where needed; a summary is not proof. Separate source facts, confirmed corrections, author/project choices, editorial judgments, and hypotheses. Open records identify risks; legacy catalog text and unrecorded cause/prevention dimensions are unverified. Proposed checks may inform verification but must not be presented as demonstrated safeguards; invalidated checks need renewed investigation before reliance. A retired or incompatible-version item cannot silently govern the task. If a catalog is missing or demonstrably stale, use targeted metadata lookup in the selected domain and report the gap; rebuild only within authorized write scope.
5. Reconcile sources into the brief above, preserving material disagreement. Expand only for a concrete dependency, conflict, or observed failure. If no useful match appears, try alternate terms or the nearest scope once, then report the gap. Never invent knowledge or treat a failed search as proof that no prior incident exists. Send new investigation needs back to the active operation's research step; required investigation is not capped by this lookup default.

Keep a recommendation's scope and caveats attached when summarizing. Stored knowledge cannot override current user intent, canon, contracts, or direct evidence. The caller remains responsible for applying and testing it.

## Save and maintain

Read [storage and lifecycle](references/storage.md) when writing or reorganizing entries. It defines the entry header/body and the [catalog helper](scripts/catalog.py) build/check workflow. Use it as the single authority for format, evidence, deduplication, promotion, and retirement. Do not run full-store rebuilds or checks as part of ordinary lookup.

Write only within the task's authorized scope. In read-only or findings-only work, return proposed entries rather than changing stores. When saving is authorized, update the detail and its human translation, build affected catalogs, regenerate translations for changed English catalogs, and check them before handoff. Update root routing for a new domain. Do not edit generated rows or infer missing legacy metadata. Create no empty store merely for lookup, and never fabricate starter knowledge.
