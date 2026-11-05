# Code problem records

Software implementation, systems, runtime behavior, and verification.

[Domain routing](../index.md) | [Storage and lifecycle](../../skills/vegabond-knowledge/references/storage.md)

<!-- onestep-catalog:start -->
Generated from canonical English metadata; edit detail files, not these rows.

| ID / title / kind | Summary / trigger / symptom | Scope / context | Keywords | Status / checked / cause / prevention | Detail |
| --- | --- | --- | --- | --- | --- |
| R-CATALOG-BOOTSTRAP / First build rejected references to its own future catalogs [error] | Catalog build checked root links before generated indexes existed. Validate file existence after planning all selected catalogs and allow only those planned outputs during build.; Trigger: First build with valid domain details and root routing links to not-yet-generated domain catalogs; Symptom: Build reports broken_reference for its future index.md targets and writes no catalogs | OneStep; vegabond-knowledge catalog.py build and check | bootstrap, first-build, broken_reference, domain-index, catalog-planning | resolved / 2026-11-05; Cause: confirmed; Prevention [verified]: Run bootstrap regressions for multiple stores, planned archives, unselected catalogs and genuinely missing files when changing catalog planning or link validation | [R-CATALOG-BOOTSTRAP](R-CATALOG-BOOTSTRAP.md) |
<!-- onestep-catalog:end -->
