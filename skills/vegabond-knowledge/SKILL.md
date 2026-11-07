---
name: vegabond-knowledge
description: Use when a task needs stored domain references, project conventions, prior corrections, or verification guidance, or when saving and maintaining knowledge and problem records.
---

# Vegabond Knowledge

Retrieve and maintain knowledge and problem records for the active task. Reuse scout's profile; the calling operation or specialist judges applicability and verifies the actual deliverable. Follow the [agent instructions](../../agents/vegabond-agent.md) for document boundaries and completion. This skill supplies information; it does not take over creation, revision, or research, and reading it does not spawn an agent.

## Request and return

A request states the **working project, question, relevant domains, target and constraints, and environment/version or story context** where relevant. Reuse the existing brief instead of asking for those details again. A storage request additionally supplies findings, evidence, resolution, proposed reusable checks, intended reuse conditions, and the context actually verified.

Use the shared [information-needs judgment](../vegabond-scout/references/information-needs.md): connect questions to the decisions they support and expose missing premises found in retrieval. Return candidate evidence and limits; the consuming specialist records consequential adoption, conditional use, rejection or deferral and verifies the action. Search coverage is not a completeness judgment.

Return a short information brief containing:

- **Applicable knowledge:** what can help this step, with source IDs and paths or links for each material claim.
- **Conditions and exceptions:** where it applies, why a prior incident matches, its cause confidence and verification context, and what conflicts with the present request or sources.
- **Checks:** concrete prevention or acceptance checks to carry into the work, with the originating record ID, prevention state and evidence. A resolved incident does not by itself establish verified prevention.
- **Gaps:** missing, stale, conflicting, or unconfirmed information and the question it leaves open.

## Find and synthesize

1. Reuse an existing information brief while its question, scope, consulted entry content, and governing sources remain valid. Search again when one changes or new evidence exposes a gap. Keep consulted IDs and revisions/hashes in task evidence when needed, without creating a global cache of project facts.
2. Use the working project's known stores first. The default routes are [knowledge](../../knowledge/index.md) and [records](../../records/index.md) in this repository; in another project, resolve paths there rather than automatically using OneStep's project facts. Use an existing native store when suitable. Shared OneStep material is an additional source only when explicitly configured or requested. Do not search unrelated projects.
3. Choose domains from the profile; combine them for mixed work. Use the [retrieval helper and synthesis procedure](references/retrieval.md) to search both stores by question, identifiers, scope/context and state, with compact match reasons and body locators. It expands maintained Korean/English aliases and excludes `*.kr.md`. Use `--no-cache` for strictly read-only work. If the helper is unavailable or a native store fits better, use bounded canonical catalog/body searches with equivalent conditions and report the capability gap. Prioritize applicability over recency; consult `shared` only for a relevant cross-domain need.
   Before work, search problem records by the planned action and conditions against `trigger`, even when no symptom is known. After a failure, search `symptom` and exact identifiers, then compare conditions and cause evidence. Keep resolved incidents in the candidate set. Exclude known incompatible scopes; retain unknown compatibility as a caveat instead of silently treating it as incompatible. Matching symptoms do not establish a matching cause. An absent trigger is a lookup gap, not evidence that an incident is irrelevant. Lexical rank does not establish applicability or evidence quality.

4. Start with up to three relevant detail files across the selected stores, reading the header and useful sections first. Check applicability and follow original evidence where needed; a summary is not proof. Separate source facts, confirmed corrections, author/project choices, editorial judgments, and hypotheses. Open records identify risks; legacy catalog text and unrecorded cause/prevention dimensions are unverified. Proposed checks may inform verification but must not be presented as demonstrated safeguards; invalidated checks need renewed investigation before reliance. A retired or incompatible-version item cannot silently govern the task. If a catalog is missing or demonstrably stale, use targeted metadata lookup in the selected domain and report the gap; rebuild only within authorized write scope.
5. Reconcile sources into the brief above, connecting each material answer to IDs, original evidence, conditions and checks. Follow relevant incoming/outgoing relationships and prose links; preserve disagreement and inspect truncated conflict/replacement candidates before relying on a conclusion. For broad requests, close each subquestion as answered, conditional, conflicting or missing. Expand for unanswered questions, dependencies, conflicts or failures; the initial detail count is not a completion limit. If no useful match appears, try alternate terms or the nearest scope once, then report the gap. Never infer absence from failed search. Send new investigation needs back to the active operation's research step.

Keep a recommendation's scope and caveats attached when summarizing. Stored knowledge cannot override current user intent, canon, contracts, or direct evidence. The caller remains responsible for applying and testing it.

For a registered `SRC-...` source needed by a claim, follow the [portable source procedure](references/storage.md#portable-source-references). Return its ID, relevant locator, identity/access result and remaining gap; a catalog link alone does not verify the original. Resolve only needed IDs within the authorized source scope, without changing machine settings or historical evidence during lookup.

## Close a knowledge gap

An empty store or insufficient match is a normal starting point. Turn the gap into the smallest questions needed for the current decision, with its conditions and required evidence; do not collect a whole subject in advance. Return these questions to the active operation's [research step](../vegabond-research/SKILL.md). Reuse the current brief so this handoff does not restart scout or recursively repeat the same lookup. Model recollection can suggest search terms, but is not checked source evidence.

Bring the answer back into the information brief, distinguishing **source-supported claims**, **methods checked in the actual task**, and **inferences or unresolved questions**. Source-based reference knowledge need not wait for an implementation, but a source check does not prove local execution. The calling specialist applies the findings and checks the actual result; return its evidence and exceptions here. Required evidence gaps still block dependent work under the common rules.

Before authorized storage, select what is worth finding again: a recurring decision, costly investigation, meaningful constraint, or useful check, including successful methods with no incident. Prefer one independently answerable question per entry, with just enough concept explanation to use it; link prerequisites only when needed. Apply the storage guide's consolidation rules rather than saving every new term or duplicating a research report. Keep unsupported candidates in the task findings unless a scoped hypothesis record needs follow-up. In read-only work, return proposed updates. Reuse existing fields and body sections, with source checks and task checks identified separately in Evidence.

On the next relevant task, retrieve by question and conditions, confirm applicability, and carry guidance into a concrete action or check. Record consulted IDs/hashes, decisions, gaps and misleading matches in existing task evidence. Use demonstrated misses or bad matches to improve affected summaries, aliases, scope or routing and extend the [retrieval evaluation cases](tests/retrieval_cases.json). Do not add a global usage ledger or reread the full store after each task. Catalog validation does not establish retrieval usefulness.

## Save and maintain

Read [storage and lifecycle](references/storage.md) when writing or reorganizing entries. Apply its [capture and consolidation decision](references/storage.md#capture-consolidate-and-promote) before creating a new entry: decide what merits reuse, what belongs in an existing entry, and what should remain in source material or task history. It defines the entry header/body and the [catalog helper](scripts/catalog.py) build/check workflow and is the single authority for format, evidence, deduplication, promotion, and retirement. Do not run full-store rebuilds or checks as part of ordinary lookup.

Write only within the task's authorized scope. In read-only or findings-only work, return proposed entries rather than changing stores. When saving is authorized, update the detail and its human translation, build affected catalogs, regenerate translations for changed English catalogs, and check them before handoff. Update root routing for a new domain. Do not edit generated rows or infer missing legacy metadata. Create no empty store merely for lookup, and never fabricate starter knowledge.
