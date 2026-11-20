# C++ guide routing evaluation

Run this evaluation after changing the linked C++ workflow or implementation guide. It checks what a fresh agent reads during a real edit in a synthetic linked project. Use the [existing blind evaluation method](../../../vegabond-knowledge/tests/information-needs/evaluation.md) when reviewing decisions and evidence.

## Prepare and run

1. From the OneStep checkout, run `python skills/vegabond-code/tests/cpp-routing/run.py prepare`. Use `--parent` to select an existing writable directory outside the checkout if needed. The command creates four isolated projects with local instructions and connects each through `link_project.py`.
2. Give each fresh performer only its project path and the contents of `request.md`. Ask it to start with the project's `AGENTS.md`, read Markdown through `python read_doc.py <path>` from that project, and report what it executed and any limits. The helper offers `--outline` and `--section "heading"` for targeted reading. Keep the rubric, other cases, and prior results outside the performer context.
3. Run `python skills/vegabond-code/tests/cpp-routing/run.py check <run-directory>`. The check compares recorded reads with the frozen rubric and rejects changed guidance or fixture inputs. Review the actual patch and verification separately using the review points in the output.

## Executable checks and evidence

- For a native C++ case, compile and run `check.cpp` with C++17 before and after the fix. On Unix-like systems, use `c++ -std=c++17 check.cpp -o route-check` and `./route-check`. In an MSVC developer prompt, use `cl /nologo /std:c++17 /EHsc check.cpp /Fe:route-check.exe` and `route-check.exe`. Record compilation and exit status separately. For the ownership case, the supplied check reproduces caller mutation. Verify destruction after the edit with an additional assertion when a compiler is available.
- For the Python case, use the command in the fixture's `AGENTS.md` before and after editing. Review that the `.uproject` and any Unreal code remain untouched.
- The Unreal ownership sample is source-only. Inspect the weak reference, getter, and public API, and keep compilation and runtime acceptance marked unverified unless you supply a suitable independent engine fixture.

Keep the run manifest, read logs, patch review, and observed executable results together. The reader captures excerpts returned through it. The evaluation samples four behaviors in fresh contexts and can be rerun after changes. Treat its results as scoped behavior evidence, and use the existing [feedback process](../../../../feedback/README.md) for demonstrated strategy defects.
