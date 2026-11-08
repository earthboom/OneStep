# Reanalyze retained evidence without rebuilding

All four analyzers use the same read-only contract. A fresh checkout contains source, process manifests and raw results (including gzip archives), but ignores generated Unity builds. Offline reanalysis must not depend on recreating an old executable. It does not launch Unity or repeat an experiment.

```powershell
python -B ./analyze_results.py
python -B ./analyze_dynamic.py
python -B ./analyze_traffic.py
python -B ./analyze_stream.py
```

Use Python 3.9+ with assertions enabled. Existing source hashes, run identities, behavioral checks, negative controls, archived assembly checks and metric calculations remain mandatory. A missing/corrupt report or changed recorded source still fails. Unrelated SDK, gameplay or cross-machine performance claims remain outside these checks.

## Independent result dimensions

The leading JSON object reports `analysis_ok: true` only after retained-data/source checks pass. It separately reports `binary_verification` with per-path expected/observed SHA-256 and one of:

| Status | Meaning | Default exit | With `--require-binaries` |
| --- | --- | --- | --- |
| `matched` | Available file matches the recorded digest | 0 if all other checks pass | 0 if all declared targets match |
| `missing` | Recorded binary is absent at the selected root | 0; `complete: false` | 1 |
| `mismatch` | Available file has a different digest | 1 | 1 |
| `unavailable` | Cannot read the target or its resolved path leaves the root | 1 | 1 |

`acceptable` states whether that binary policy passed; `complete` requires every declared target to match. Exit 0 with missing builds means offline analysis passed, **not** that the old binaries were independently checked. Invalid arguments/existing output paths exit 2; retained-data assertions and I/O failures exit nonzero without a success summary.

Binary scope preserves each analyzer's prior targets: original player EXE; Dynamic managed assembly; Traffic and Stream player EXE plus managed assembly. Even `complete: true` certifies only those paths against manifests, not an entire Unity build tree, trustworthy remote execution, rendering or current engine behavior. Run manifests must agree on declared binary hashes. The archived Stream UI pilot assembly remains a mandatory, separate historical check.

## Optional binary and output checks

```powershell
python -B ./analyze_traffic.py --require-binaries
python -B ./analyze_stream.py --binary-root C:/Archives/TechniqueLab --require-binaries
python -B ./analyze_stream.py --output C:/Reports/stream-analysis-new.json
```

The alternate root must have the same relative layout (`StreamBuild/...`, etc.); it does not redirect source/raw-data inputs. Use the actual archived binaries. Rebuilding can change their identity and is not a substitute for a recorded binary match. Default mode also rejects an available wrong binary; it never silently skips a mismatch.

By default no summary or evidence file is written. `--output` exclusively creates a **new** full JSON report; the parent must already exist. Existing files, including historical `Results/**/summary.json`, cannot be overwritten. This replaces the earlier implicit summary rewrite. Traffic/Stream stdout includes readable metric lines after its leading JSON object; the optional output file contains only full JSON. Strict failures can still write a report with `analysis_ok: true` and `binary_verification.acceptable: false`; check both dimensions and the exit code.

## Regression checks

```powershell
python -B -m unittest discover -s tests
```

The integration suite copies tracked source/results into a temporary tree with **no generated builds**. It checks all four analyzers, strict missing failures, changed source/report failures, present wrong binaries, protected outputs and exact equality of historical metric fields. Unit checks exercise a matching binary, corruption after success, unavailable targets and inconsistent manifest hashes. Set `ONESTEP_TEST_ROOT` to a writable temporary parent when needed. These are analysis/provenance tests, not new engine runs.
