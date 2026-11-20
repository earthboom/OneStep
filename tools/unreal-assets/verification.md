# Executed verification

2026-11-13, Windows x64, .NET SDK 10.0.404 targeting .NET 8, UAssetAPI 1.1.0. Results cover serialized structure, selected properties and references in controlled samples. vagabond's independent review remains pending.

## Real engine comparison

An isolated UE 5.8.0-0+UE5 test project saved five real uncooked packages. A **second editor process** reopened those packages without saving; native reflection and property text produced the comparison oracle. The parser did not consume the oracle. The verifier compared its JSON with those independent observations: **31 checks passed, zero failed**.

| Real package | Compared observations |
| --- | --- |
| Animation | Nonempty tutorial sequence, 188 source frames, RateScale 1.25, root motion true, length 6.266666889, skeleton reference; import translation [1,2,3]; nested raw tracks remain unsupported. |
| Montage | RateScale 0.75, skeleton, Default section, one slot track and its animation reference. Native text omits default-valued fields; no inferred default SlotName is presented as independent evidence. |
| Widget | Compiled Blueprint, source WidgetTree/root/child references, TextBlock text `Reader verification 37`, opacity 0.625 and focused text selection. |
| PrimaryAssetLabel | Data family, priority 37, chunk 7 and all three explicit soft asset references. |
| DataTable | Both GameplayTagTableRow rows, names, tags, comments and RowStruct reference. |

Every package's SHA-256 matched before and after the independent native read and CLI inspection. The engine tutorial animation and skeleton source hashes also matched their captured originals. Generated binary fixtures and reports are ignored; no engine content is distributed. Reproduction: [engine project and commands](tests/engine/README.md), [comparison verifier](tests/verify_engine_assets.py).

## Reproduced defects and corrections

- PrimaryAssetLabel initially fell through to generic routing. Its script-qualified class now selects data analysis.
- The animation's 68 `RawStructPropertyData` track wrappers initially counted as decoded. They now retain unsupported property and partial export states; track bytes are not interpreted.
- FBX import metadata serializes a prefix before UObject property tags. Declared script offsets now locate those tags and exact tag consumption is checked; prefix and trailing bytes stay opaque. The nondefault translation matches the native read.
- Both real TextBlock exports initially became raw. Direct library diagnostics showed Base-history FText consumed its source string but omitted newer editor developer notes, misaligning the following property. A small registered TextProperty subclass consumes that FString only when serialized FortniteMain version >= 260 and editor data is present, matching the checked engine's `FTextHistory_Base::Serialize`. The same unmodified files now expose text and following opacity. Nested text histories still depend on upstream support; this does not promise every FText format.
- Review found that the native verifier accepted source `Content` itself as an output directory. The equality case now fails before creating output, with a portable regression.

The actual native comparisons failed before the relevant corrections and pass afterward; opaque tracks deliberately remain partial. Legacy FText and a subsequent integer are checked in a separate UE4.27-derived fixture, without claiming native fidelity for that synthetic fixture.

## CLI regression scope

Release CLI and test writer build with zero warnings/errors. The subprocess suite has **26 passing tests**, no skips. Existing checks retain genuine UE4.27/UE5.7 blueprint values and class references; synthetic routing, rows and typed reference cases; exact selectors; malformed/cooked/unversioned input rejection; export bounds; unknown name indices; neighbouring-file isolation and input immutability. The new tests cover verifier output protection and legacy text alignment. Dependency versions remain locked; the initial locked restore and clean pinned-fixture download passed.

The initial reader review also reproduced and corrected export-size bypass and omitted soft-path subclasses. [R-CODE-UE-PARSER-NAME-INDEX](../../records/code/R-CODE-UE-PARSER-NAME-INDEX.md) retains its reusable name-index prevention. [Native struct guidance](../../knowledge/code/K-CODE-UE-NATIVE-STRUCT-DECODING.md) records opaque-wrapper handling without revalidating its older layout table.

## Evidence and limits

Local ignored evidence is under `.cache/onestep/asset-reader/native/`: `creation.json`, `oracle.json`, `evidence-before-text-fix/results.json`, `evidence-final/results.json`, reports, build/test logs, original-hash checks and final code fingerprints. The engine helper compiled/linked through UBT; the official WriteMetadata stage generated project loading metadata. A conventional full project build was not claimed. Creation and fresh read exited successfully with zero errors; optional ACL/PDB warnings remain in engine logs. Editor startup used process-local SDK-discovery skipping after the Win64 toolchain had compiled the helper. These are task-local artifacts, not installed project connections.

The CLI itself runs offline without an editor. Engine runs here establish serialized comparison values, not animation playback, montage gameplay, widget rendering or PIE acceptance. Full graph semantics, compressed/raw track decoding, other native payloads, all engine forks and broad production-project compatibility remain unverified. ImportData and animation native bytes may correctly yield `partial`; a focused decoded widget property can yield `complete` while other exports remain partial. No new performance benchmark is claimed. No commit or push was performed; unrelated changes were preserved.
