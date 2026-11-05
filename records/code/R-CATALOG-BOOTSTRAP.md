---
id: R-CATALOG-BOOTSTRAP
title: First build rejected references to its own future catalogs
summary: Catalog build checked root links before generated indexes existed. Validate file existence after planning all selected catalogs and allow only those planned outputs during build.
kind: error
scope: OneStep; vegabond-knowledge catalog.py build and check
keywords: [bootstrap, first-build, broken_reference, domain-index, catalog-planning]
status: resolved
checked_at: 2026-11-05
trigger: First build with valid domain details and root routing links to not-yet-generated domain catalogs
symptom: Build reports broken_reference for its future index.md targets and writes no catalogs
cause_status: confirmed
prevention: Run bootstrap regressions for multiple stores, planned archives, unselected catalogs and genuinely missing files when changing catalog planning or link validation
prevention_status: verified
---

## Expected and observed

A first build should create domain catalogs from valid details even when the root routing document already links them. The integration exercise and pre-fix regressions returned exit 1 with broken_reference and no catalog writes. Creating index headings manually worked around the ordering dependency, but should not be required.

## Cause and resolution

File existence was checked while reading inputs, before all selected generated outputs were known. The helper now collects local references, plans every selected catalog, and then validates targets. Build permits a missing target only if that exact resolved path is in its output plan. Check permits no missing target. Ordinary broken references still stop writes; no initialization command, extra folder, or placeholder file is needed.

## Recheck and prevention

On 2026-11-05, three newly added bootstrap tests failed before the fix and passed after it; the ordinary-missing-file negative case passed both times. All 24 catalog tests passed after the repair. The four bootstrap tests cover first build across both stores and multiple domains, read-only check before creation, idempotent rebuild, canonical detail preservation, planned archive/detail references, missing files and unselected catalogs.

This verifies the specific helper behavior through executable regressions; it does not claim CI enforcement or compatibility with unrelated knowledge systems. Keep the negative cases when modifying the build-only planned-output exception.

## Evidence

- [Executable regressions](../../skills/vegabond-knowledge/tests/test_catalog.py): test_bootstrap_builds_multiple_stores_without_index_stubs, test_bootstrap_still_rejects_unplanned_missing_files, test_bootstrap_does_not_exempt_unselected_catalogs, and test_bootstrap_resolves_planned_archive_and_detail_links.
- [Helper](../../skills/vegabond-knowledge/scripts/catalog.py): local references are collected by links and resolved after all domain plans in run.
- [Storage procedure](../../skills/vegabond-knowledge/references/storage.md#first-catalog-build): write details and routing, build, translate changed catalogs, then check.
