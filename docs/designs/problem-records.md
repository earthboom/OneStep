# Problem record retrieval decisions

Status: implemented design record. This preserves the choice and original implementation evidence, not an active implementation plan. The [knowledge skill](../../skills/vegabond-knowledge/SKILL.md) owns retrieval/capture; the [storage guide](../../skills/vegabond-knowledge/references/storage.md) owns the current format and CLI contract. Human acceptance is established only by explicit feedback, not this record's status.

## Goal and alternatives

The goal was to find relevant incidents before work from triggering conditions and after failure from observed symptoms, returning usable prevention checks with evidence limits. Body-only templates concealed those signals; record-specific header fields exposed them in the existing catalogs with a small helper change. A separate incident database added infrastructure without demonstrated need, so the existing stores and six-column catalogs were retained.

## Decisions and their reasons

- Trigger and symptom support different lookup moments. Cause confidence and prevention state remain separate from incident resolution, preventing a corrected artifact from implying proven prevention.
- Explicit unknowns and legacy warnings preserve missing information rather than inventing it. Record-only fields keep ordinary knowledge entries lightweight. The current [record fields and legacy rules](../../skills/vegabond-knowledge/references/storage.md#problem-retrieval-fields) are defined in one place.
- Resolved incidents remain searchable; superseded provenance remains available. A symptom match alone cannot establish a shared cause, and uncertain compatibility should remain visible rather than silently disappear.
- A recurrence can mean a check was not run, was insufficient, or became invalid under changed conditions. Those outcomes have different implications; linking concise evidence avoids duplicating long logs.
- The helper reads canonical English entry metadata and checks visible local-reference targets for existence, but does not load referenced contents, rewrite canonical details, or load human translations. Structural validation cannot determine whether a diagnosis or safeguard is true.

## Original implementation and evidence

The completed work added behavior tests for retrieval signals, invalid/unknown fields, legacy compatibility, state independence and scoped catalogs; extended validation and record projections; updated skill/storage guidance and translations; and refreshed affected catalogs. The current procedures live in those guides rather than in a second session-specific checklist here.

These are historical results from that implementation, not the current suite count or a new test run:

- Initial tests failed because record signals were ignored and not projected; the implementation then passed 19 catalog tests.
- An independent four-domain synthetic exercise checked proposed, verified and invalidated prevention, uncertain-version candidates and recurrence distinctions. It preserved canonical details and passed strict catalog checks. It did not execute the underlying products or create real project incidents.
- Independent review found that preserved catalog notes and root-routing prose escaped local-reference checks. A regression reproduced both false successes; applying the existing reference validator at those points brought the suite to 20 passing tests. Project strict checks, an idempotent build, English references and translation-pair checks also passed at that stage without reading translations.

The current test source is [test_catalog.py](../../skills/vegabond-knowledge/tests/test_catalog.py). Later changes and current verification should be assessed from that source and actual run evidence, not these historical counts.

## Limits

The implementation introduced no new service or global store and required no dependency installation. Format tests and catalog checks do not prove semantic retrieval, cause attribution or prevention. The specialist must inspect the original evidence and applicability. Read-only lookup is not permission to rewrite historical entries, and project-external local references require separate verification within the authorized source scope.
