# Storage and lifecycle

## Location and domain

Paths below are relative to the working project. Reuse its existing system if it supports scoped retrieval and provenance. Otherwise use:

```text
knowledge/index.md              # Domain routing only
knowledge/<domain>/index.md     # Searchable knowledge summaries
knowledge/<domain>/<id>.md      # One reusable topic or lesson
records/index.md                # Domain routing only
records/<domain>/index.md       # Searchable problem summaries
records/<domain>/<id>.md         # Problem, correction, and recheck history
```

The initial domains are `code`, `fiction`, `presentation`, `planning`, and `shared`; they are not an exhaustive list. Classify by the subject, not create/revise/research or file extension. Add a domain when actual content requires it. Put language, engine, genre, format, component, work identifier, and task subtype in metadata before introducing deeper folders.

Give a cross-domain item one primary home and link to it from other relevant domain indexes. Use `shared` only when evidence supports cross-domain applicability, not as a default catch-all. Project incidents and canon stay in their project; promote a general method to shared guidance only when the evidence supports that scope.

Do not create parallel `lessons/` and `knowledge/` stores. If an existing lesson system is present, reuse it or migrate relevant entries and references within the authorized scope, preserving IDs and evidence.

Maintained store documents include indexes, knowledge details, problem details, and archives. For each new or changed English document, create or update its `<stem>.kr.md` human translation from the English without reading the translation. Do not treat these entries as exempt from the agent's translation rule merely because they are records rather than skills. Before handoff, check English links and status consistency, and verify translation-pair existence without loading translation contents.

## Entry header and body

For the default Markdown stores, create or update one independently reusable topic/check per detail, with a YAML header containing these fields:

| Field | Rule |
| --- | --- |
| `id` | Stable project-unique ID; letters, digits, dots, underscores and hyphens. Comparison is case-insensitive. |
| `title` | Specific question, method or subject. |
| `summary` | One or two sentences giving the usable point and its essential condition. |
| `kind` | Knowledge: reference, method, convention or lesson. Records: error, suggestion or hypothesis. |
| `scope` | Project/component/work and applicability boundary, as a string. |
| `keywords` | Nonempty list of useful English concepts, synonyms and exact technical identifiers. |
| `status` | Knowledge: active, enforced or superseded. Records: open, resolved or superseded. |
| `checked_at` | Actual evidence-check date as YYYY-MM-DD, or null if unknown; never fill it from the edit date automatically. |

Optional `context` is a string or flat mapping of strings for relevant version, engine, format, genre, viewpoint or other conditions. Quote versions and YAML-reserved words. Avoid irrelevant empty fields. Header data is not skill-discovery frontmatter; human translations present the information for readers without becoming discovery inputs.

For example, a header might be:

```yaml
---
id: K-FIC-001
title: Check information access in limited viewpoint
summary: Under limited narration, check each claim against the focal character's information access before line polishing.
kind: method
scope: naru-novel; Seorin-limited narration
keywords: [viewpoint, POV, character-knowledge]
status: active
checked_at: null
context:
  viewpoint: third-person limited
---
```

This is a format example, not a live entry. Follow it with four nonempty H2 sections:

- Knowledge: **Guidance**, **Applicability and exceptions**, **Checks**, **Evidence**.
- Records: **Expected and observed**, **Cause and resolution**, **Recheck and prevention**, **Evidence**.

Keep the useful action short, explain exceptions, distinguish source facts/methods/conventions/editorial judgment, and cite original sources with location and verification context. Problem records retain cause confidence, corrections or proposed action, resolution and recheck evidence, and prevention links. Unknown causes remain unknown. Enforced status requires a demonstrated safeguard; saving a lesson does not prove enforcement.

Reference original issues, reports, tests, passages, screenshots or logs rather than copying them. Group minor same-cause findings where useful. Referenced project sources remain authoritative for their facts; the detail is authoritative for its entry metadata, and catalog rows are derived projections.

### Problem retrieval fields

New or normalized `records/` details additionally require all five fields below. These are incident metadata, not additional requirements for `knowledge/` details.

| Field | Rule |
| --- | --- |
| `trigger` | Short conditions/action under which the problem occurred; null if unknown. Enables lookup before a symptom exists. |
| `symptom` | Nonempty description of the observed failure, with discriminating characteristics. For suggestions/hypotheses describe the observed concern without asserting an unconfirmed defect. |
| `cause_status` | `unknown`, `suspected`, or `confirmed`, supported in Cause and resolution. A confirmed defect can still have an unknown cause. |
| `prevention` | A specific action/check with its essential condition, or null when none is established. Detailed steps, exceptions and evidence stay in Recheck and prevention. |
| `prevention_status` | `none`, `proposed`, `verified`, or `invalidated`. `none` requires null prevention; other states require the action. `verified` additionally requires a real `checked_at` and demonstration evidence in the body. |

Keep these phrases short enough for a useful catalog row; do not repeat logs or every example. Use `keywords` for useful synonyms and exact identifiers, not redundant copies of every phrase. `summary` gives the finding and its essential condition, rather than duplicating the entire header. Use explicit scope/context for versions, canon or format differences that change applicability.

Record example only, not a live incident:

```yaml
---
id: R-FIC-EXAMPLE
title: Inaccessible private decision in limited narration
summary: A focal character asserted a private decision without an information source; revision restored uncertainty.
kind: error
scope: story-alpha; chapter-3
keywords: [viewpoint, POV, information-access, private-thought]
status: resolved
checked_at: null
context:
  canon: revision-B
trigger: Drafting third-person limited narration
symptom: Focal character states another character's private decision without access
cause_status: confirmed
prevention: Trace each private-knowledge assertion to a source available to the focal character
prevention_status: proposed
---
```

`resolved` describes the incident, not the prevention. Use `verified` only after the specified check demonstrably detects the original failure or a controlled equivalent in its stated context; a corrected artifact alone is insufficient. For editorial work, a documented review that detects the relevant defect is valid evidence without pretending to be automated enforcement. Record separate correction and safeguard check dates/results in Recheck and prevention; `checked_at` is the latest actual material evidence check, not an invented safeguard date. A date and valid header cannot prove the demonstration happened: the specialist must inspect its evidence.

Keep the existing four body sections. Expected and observed records the original contract, actual finding, occurrence conditions and location. Cause and resolution distinguishes diagnosis confidence, supporting evidence, correction and unknowns. Recheck and prevention records the corrected result's checks separately from future safeguards, their state, applicability and exceptions. Evidence links the original artifact/version and reports. A suggestion or hypothesis does not become an error merely because it has been recorded.

### Earlier structured records

A record with the common header but none of the five fields remains readable. The helper warns with `legacy_record_fields`, leaves its source unchanged and projects the new dimensions as **unrecorded**. `--strict` treats that migration gap as an error. A partial extension is an error, not a legacy exemption. New and edited records must use all five fields; the helper cannot infer when an old file was edited, so this writing rule also belongs to the skill. Normalize only during authorized maintenance, preserving ID, path, evidence and unknowns. Do not fill fields by guessing from a title or previous catalog row.

## Refresh and validate catalogs

[catalog.py](../scripts/catalog.py) uses Python 3.9+ with PyYAML from an existing runtime; it installs nothing. Commands below are run from the OneStep checkout. In another project, use the helper's absolute path and that working project's `--project` value.

```text
python skills/vegabond-knowledge/scripts/catalog.py build --project . --domain fiction
python skills/vegabond-knowledge/scripts/catalog.py check --project . --domain fiction
```

`--store knowledge`, `--store records`, or default `both` selects stores; repeat `--domain` for affected areas. Omitting domains performs explicit full-store maintenance, including project-wide duplicate-ID checking. Filtered runs validate only selected details and explicit related-entry references. Ordinary retrieval still uses bounded catalog searches; do not rebuild after every information request.

The helper generates six-column **ID/title/kind | summary | scope/context | keywords | status/checked date | detail** rows inside managed markers. For record rows, the summary column also exposes trigger and symptom; the status column also exposes cause confidence, prevention state and the short prevention action. Knowledge rows are unchanged. Keep resolved incidents searchable in the active catalog; only superseded entries move to archives. Preserve project notes outside managed markers. Related-domain references keep one primary detail; do not copy its content. Root indexes remain small routing documents maintained by this skill when domains change.

Save in this order: write canonical details and their translations; run `build`; regenerate human translations for the English paths listed in `catalogs_written`; then run `check`. Build is preparation: missing translations/routing are warnings so the English catalog can be produced first. Check requires catalog freshness, valid metadata/states, unique IDs, required body sections, local file references, routing and translation-pair existence. Duplicate YAML keys and malformed structured headers are errors. Metadata or reference errors stop build before writes; each changed catalog is replaced atomically. A filesystem failure can leave some catalogs updated, so rerun check and repair within scope. The helper never writes canonical details or translations.

Links outside the project and section-anchor accuracy require separate verification; the helper checks local file targets without loading referenced contents. It checks translation existence, not translation meaning or freshness. Generate every changed translation from English without reopening it. Diagnostics are bounded to the first 20 with total/error counts; narrow the selected domains to investigate larger result sets.

Legacy prose entries remain usable: preserve existing catalog rows and their conditions under an explicitly unverified Legacy entries section; unindexed legacy files get an unknown-metadata pointer. Do not infer IDs, dates, rules or states. Migrate a legacy entry during authorized maintenance, preserving its path/ID/evidence, then rebuild. Default runs warn; `--strict` treats legacy entries as errors for scopes already normalized. New or changed entries must use the header even if older neighbors remain legacy. Strict checking is not permission to rewrite historical evidence or all unrelated files.

## Capture, consolidate, and promote

Before saving, identify the future decision, action, or check the material can support and the conditions under which it applies. Reusable means useful in another task under matching conditions, not universally valid. Choose the smallest useful destination:

- **Knowledge:** state the usable principle or method, its rationale, checks, and exceptions. Make the title and summary about the reusable question or action rather than a project's task chronology.
- **Problem record:** retain the minimum incident evidence needed to distinguish the trigger, symptom, cause confidence, correction, and recheck. Link to the common knowledge entry instead of repeating its full procedure.
- **Existing source or task history:** keep unique project facts, story canon, author preferences, and one-off progress in their authoritative source. Add a scoped reference or convention only when repeated retrieval benefits from it, without copying whole profiles or specifications. Findings with neither reuse value nor a tracking need can stay in the task report; unresolved problems that need follow-up still deserve records.

Search existing indexes for the same principle, question, or underlying cause before writing. Prefer updating applicability, exceptions, evidence, or recurrence in an existing entry over creating a project-specific copy. One knowledge entry can link to several incident records, each retaining its relevant circumstances. Consolidate incidents only when the cause and occurrence conditions support the same prevention; a shared symptom is insufficient. Link uncertain matches without merging their diagnoses. Keep material disagreement explicit; do not overwrite one version merely because it is newer. Preserve the link from a problem to its prevention and from a reusable lesson to its originating evidence.

Generalize the explanation without erasing the evidence boundary. Keep essential version, lifecycle, genre, viewpoint, audience, or other conditions in the existing `scope`, `context`, body, and source references. Retain exact identifiers needed to find or reproduce the incident; omit incidental names and long logs from the reusable guidance. Distinguish the conditions actually checked from broader applicability inferred from a mechanism or rationale, and name what remains untested. A successful case can support a bounded lesson, but cannot establish verification in other environments. Never universalize canon or preferences, or promote a proposed safeguard merely by generalizing its wording. Generalization does not move records across projects or make a domain-specific method belong in `shared` automatically; the location and authorization rules above still apply. Use the existing schema and stores.

Keep recurrence history short: occurrence date or unknown, location/version, evidence link, correction/recheck result, and the prior safeguard's outcome. Distinguish **not executed**, **executed but insufficient**, and **invalidated by changed conditions**; retain unknown outcomes rather than inventing one. When contrary evidence invalidates the recorded prevention claim, mark it `invalidated`, retain the old demonstration context, and investigate a replacement. A missed check does not automatically disprove that check. Add separate incidents when materially different conditions require different remedies. Keep long logs at their source instead of growing the detail into a transcript.

Promote only confirmed, consequential lessons when recurrence, likely reuse, or a useful safeguard warrants it. Store the incident in `records/` and its distilled reusable content in `knowledge/`, with reciprocal links instead of copied narratives. The specialist supplies the diagnosis and domain checks; this skill organizes them and does not invent a resolved cause or certify the deliverable.

Prefer preventing recurrence through structure, types, validation, lint, or regression checks. Retain evidence that the safeguard detects the original failure or a controlled equivalent. For judgment-dependent work, record a specific conditional review check and its rationale. Saving an entry alone does not establish prevention.

## Retire without losing provenance

During normal use, merge duplicates and correct stale applicability. To supersede an entry, set its canonical status and record the reason/replacement; rebuilding routes its row to the domain's `archive.md`, creating that catalog only when needed. Reactivation routes it back. Keep detail paths and evidence stable; do not hand-edit generated rows. Existing native systems use their own archive mechanism. Age alone does not invalidate useful knowledge.

Recheck affected entries when their source, version, canon, or safeguard changes. An old information brief must be refreshed if such a change invalidates it. If targeted searches repeatedly return too much unrelated material, split the affected domain index by actual project area and retain a small routing index. Expand structure only in response to observed retrieval friction; do not schedule full-history rereads after every task.

## First catalog build

For a new store/domain, write valid details and their human translations in the domain directory, and create or update the root routing document and its translation. Root links may point to domain catalogs that this build will create; no index stubs or special initialization command are needed. Run the usual build/translate/check sequence above. The helper checks local file existence after all selected catalog outputs are planned: only a missing catalog in that build plan is allowed. Other missing files and unselected missing catalogs still block writes. `check` remains read-only and requires catalogs to exist, including on the first run.
