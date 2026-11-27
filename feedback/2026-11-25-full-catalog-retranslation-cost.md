# Feedback: Adding one knowledge entry requires retranslating the whole domain catalog

- Date: 2026-11-25
- OneStep version used: a9fb9f8 (2026-11-24) checkout; working-tree state not checked
- Relevant skills/instructions: skills/vegabond-knowledge/references/storage.md (section "Refresh and validate catalogs": save order, regenerate translations for every English path in `catalogs_written`); a working project's local rule that forbids inserting rows into a catalog translation by script
- Kind: suggestion
- Status: received
- Task context: a Claude Code session in a game project saved one small, generalized Git reference entry to the `code` knowledge domain after an unrelated tooling task

## Expected and observed

Expected: saving one new entry costs roughly the entry, its translation, and a catalog refresh proportional to the change. Observed: `catalog.py build` changed three lines in `knowledge/code/index.md`, but the save order requires regenerating `knowledge/code/index.kr.md` in full from the roughly 41,700-character English catalog, without reading the old translation. The session delegated that retranslation to a subagent because of its size. The retranslation was larger than the rest of the knowledge save combined, and it rewrites 37 unchanged rows, so their wording can drift between saves even when nothing about them changed.

## Evidence and suspected cause

Observed in this session: `build` reported `catalogs_written: ["knowledge/code/index.md"]` and `git diff --stat` showed `3 insertions(+)` for that file; `wc -c` reported 41,685 bytes. The storage guide says to "regenerate human translations for the English paths listed in `catalogs_written`" and to generate every changed translation from English without reopening it. Combined with the never-read-`*.kr.md` rule, the only compliant option is a full retranslation. This cost grows with each domain catalog; `code` currently has 38 structured entries. Suspected cause: the rule treats the catalog translation as one unit, while the change unit is a row. Not measured: token cost in other harnesses, or how often catalogs are rebuilt.

## Suggested improvement

Options, each needing a check:

1. Have `catalog.py` emit the translation catalog itself from per-entry translated metadata (for example a `title_ko` and `summary_ko` kept in each entry's `.kr.md` header or a sidecar), so a catalog rebuild needs no free-text retranslation. Check: adding one entry changes only that row in both catalogs.
2. Allow the helper to splice regenerated rows for changed IDs into the translation by ID, as a tool-owned operation that does not expose old text to the agent. Check: the agent transcript shows no read of the `.kr.md` file, and unchanged rows are byte-identical.
3. Drop table rows from catalog translations and keep only translated prose with a link to the English table. Check: human readers still find entries; `check` still validates pair existence.

Related but distinct: `2026-11-20-translation-regeneration-vs-write-tool.md` covers how to replace an existing translation; this report covers the size of what must be regenerated.

## Review and verification

Maintainer fills during processing.
