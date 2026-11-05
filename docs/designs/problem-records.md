# Problem record retrieval design and implementation plan

Status: implemented and AI-verified; awaiting vagabond review. The [storage procedure](../../skills/vegabond-knowledge/references/storage.md) remains the active format authority.

## Goal and approach

Find applicable incidents before a task by their triggering conditions and after a failure by observed symptoms. Return actionable prevention checks with evidence limits, without reading whole histories or treating a correction as proven prevention.

Considered approaches: body templates alone keep the helper unchanged but hide retrieval signals; record-specific header fields expose those signals in generated catalogs with a small local change; a separate incident database adds infrastructure without demonstrated need. Use record-specific fields in the existing stores, as approved in conversation.

## Contract

Keep the common header and four record sections. New or normalized records add `trigger` (nonempty string or null), `symptom` (nonempty observed description), `cause_status` (`unknown`, `suspected`, `confirmed`), `prevention` (specific check or null), and `prevention_status` (`none`, `proposed`, `verified`, `invalidated`). These fields belong to records, not knowledge entries. A full set is required when any of these fields is present. Unknown triggers and absent prevention use null, never inferred facts. `none` requires null prevention; the other prevention states require an action. A verified prevention also requires a real `checked_at`; evidence and applicability still need specialist review.

Existing structured records with none of the new fields remain readable with a migration warning (an error with `--strict`). Preserve their canonical bytes and show the new dimensions as unrecorded. Existing prose compatibility remains unchanged. New and edited records must use the extended format; the helper cannot detect an author's editing history.

Record catalogs keep six columns: identity; summary plus trigger/symptom; scope/context; keywords; incident state/date plus cause/prevention state; detail. Include the prevention action with its state. Knowledge catalogs remain unchanged. Resolved records remain searchable; superseded records retain archive provenance. Values are projections of canonical metadata, not a second source to edit.

Search by trigger before work, and by symptom/exact identifier after a failure. Filter known incompatible scopes; keep uncertain compatibility explicit rather than silently discarding candidates. Do not assume identical symptoms imply identical causes. Rank applicability and evidence ahead of recency. Return ID/path, why applicable, specific check, prevention state, and exceptions/gaps in the existing information brief. This remains an agent-guided search, not a new search CLI.

Consolidate only when cause and conditions support it. Keep uncertain matches linked, not merged. A recurrence adds a short dated evidence reference, result, and whether a prior check was skipped, inadequate, or invalidated by changed conditions. Preserve material history without copying logs. Only error records represent confirmed defects; suggestions and hypotheses retain their types.

## Implementation steps

> Execution: implement inline in this session under the user's instruction to apply the design; do not add a routine approval checkpoint.

- [x] Add CLI behavior tests for projected trigger/symptom/prevention, invalid field combinations, explicit unknowns, old structured records, state independence, and domain-scoped catalog lookup. Run them before implementation and observe the missing behavior.
- [x] Extend `skills/vegabond-knowledge/scripts/catalog.py` validation and record rows without changing knowledge rows or canonical entries. Run the complete catalog test suite.
- [x] Update `skills/vegabond-knowledge/SKILL.md`, its storage reference, and their human translations. Keep operation and specialist callers unchanged: they already request and return checks through this skill. Add only a short README pointer if needed.
- [x] Build affected record catalogs, regenerate every changed catalog's human translation from English, and run strict read-only checks. Validate skill structure, English references, pair existence, and realistic cross-domain retrieval. Keep synthetic incidents out of the repository's live stores.

## Review focus

- A resolved incident can have proposed or invalidated prevention; do not mark it verified automatically.
- Unknown conditions and suspected causes must remain visible and searchable.
- Proactive lookup must find a risk without the caller knowing its symptom.
- Same symptom across incompatible environments must not produce an unconditional repair recommendation.
- Historical canonical details and human-only translations must not be read or rewritten by catalog maintenance.

## Validation boundary

The helper validates shape, states, and local file targets, not whether a diagnosis is true or a safeguard works. Specialist evidence establishes cause and prevention, including judgment-dependent checks. Structural tests do not prove semantic retrieval quality; use realistic requests for that separately. No dependency installation, new service, or global store is introduced.

## Implementation evidence

The initial new tests failed because record fields were ignored and not projected. After implementation, all 19 catalog tests passed. An independent capture/reuse exercise covered four synthetic domain findings, proposed versus verified versus invalidated prevention, an unknown-version diagnostic candidate, and recurrence distinctions. The exercise preserved canonical details and passed strict catalog checks; it did not execute underlying products or establish real project history.

The independent review also found that preserved catalog notes and root-routing prose escaped local-file reference checks. A new regression reproduced both false successes. Calling the existing visible-link validator at those two read points fixed the gap; the full suite then passed **20 tests**. No changes to reference contents or translations are needed for this check. Project strict checks and idempotent build passed; English document/reference and translation-pair checks passed without reading translation contents. All four implementation steps are complete; no commit, push, installation or global configuration change was performed.
