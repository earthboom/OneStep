# Uncooked Asset Reader Implementation Plan

> **For agentic workers:** Use the existing authorized inline execution. This plan is task evidence, not authorization for delegation, Git commits or pushes.

**Goal:** Deliver a read-only uncooked asset CLI with extensible family analysis.
**Architecture:** UAssetAPI adapter → structural/property projection and class-based analyzers → JSON CLI.
**Tech stack:** .NET 8, UAssetAPI 1.1.0, Python unittest subprocess checks.
**Spec:** [Design](../../designs/uncooked-asset-reader.md).

## Global constraints

Preserve existing unrelated changes. English guidance and separate human-only Korean translations. No project location configuration. No original asset writes, recursive dependency reads, cooked support or invented decoded values. No commit/push requested in this turn.

## Review focus

Reject cooked and malformed inputs before presenting success. Preserve nested property types and object-reference provenance. Expose raw export and native trailing bytes. Select exact exports without silently falling back. Verify original hashes and public CLI failures, not just backend calls.

### Task 1: Establish the executable boundary

- [x] Add `tools/unreal-assets/src/OneStep.UnrealAssets.csproj` and CLI behavior tests in `tests/test_cli.py`; pin public fixtures with `tests/fixtures.json` and a reproducible fetch helper.
- [x] Run the initial failing help/structure/property checks against the minimal executable shell, then implement `Program.cs` and argument validation in `Cli.cs`.

### Task 2: Implement package and property reading

- [x] Add read-only snapshots, header gates, range checks and selective export decoding in `AssetReader.cs`; expose `Read(Options)` to the CLI.
- [x] Add projection, typed-reference extraction and class-based family dispatch in `Analysis.cs`.
- [x] Verify UE4.27/UE5.7 fixtures, literal property/reference values, cooked/truncated errors, missing selections, partial data, large inputs and immutability through the real CLI.

### Task 3: Complete the usable path

- [x] Add English/Korean README, dependency/license provenance and commands. Keep fixture binaries/generated output ignored locally.
- [x] Build Release, run the whole tool suite, exercise actual commands, review code and document measured scope/limitations and evidence. Hand back for vagabond's independent review.

## Progress

2026-11-13, initial reader: Library 1.1.0 restored; genuine upstream UE4.27/UE5.7 blueprint probes succeeded. Release builds, 24 CLI tests, empty-directory fixture bootstrap and locked restore passed. A separate reviewer found export-size bypass and soft-path subclass omissions; both were reproduced and corrected. Reusable name-index prevention is in the code records. Existing unrelated changes retained.

### Task 4: Validate real animation, montage, widget and data packages

- [x] Add an isolated test-only UE5.8 project and native reflection helper; generate five genuine engine-saved samples and reopen them in a second process without saving.
- [x] Compare typed properties and references with that independent oracle; reproduce and correct PrimaryAssetLabel routing, opaque nested struct status, prefixed ImportData tags and Base-history FText developer-note alignment.
- [x] Keep source hashes unchanged; add reproducible native comparison checks and a portable legacy-text regression. Retain unsupported track/native data explicitly.
- [x] Review changes, run final build/regressions/native comparisons and update English/Korean documentation. No commit or push is requested.

[Executed evidence and limits](../../../tools/unreal-assets/verification.md). Independent user review remains pending.
