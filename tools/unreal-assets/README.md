# Unreal asset reader

A read-only, offline CLI for **single-file, uncooked, versioned `.uasset` packages**. It reads package structure, selected serialized properties and references with UAssetAPI 1.1.0. It never saves assets, loads dependency packages or needs an Unreal Editor process.

## Build and run

Install the .NET 8 SDK or a newer SDK able to target .NET 8, and the .NET 8 runtime. Run from the OneStep checkout:

```text
dotnet restore tools/unreal-assets/src --locked-mode
dotnet build tools/unreal-assets/src -c Release --no-restore
dotnet tools/unreal-assets/src/bin/Release/net8.0/OneStep.UnrealAssets.dll --help
```

Pass a file from your own authorized working project. Paths below are placeholders, not stored project connections:

```text
dotnet tools/unreal-assets/src/bin/Release/net8.0/OneStep.UnrealAssets.dll <asset.uasset> --engine 5.7
dotnet tools/unreal-assets/src/bin/Release/net8.0/OneStep.UnrealAssets.dll <asset.uasset> --engine 5.7 --object <ObjectName> --properties --pretty
dotnet tools/unreal-assets/src/bin/Release/net8.0/OneStep.UnrealAssets.dll <asset.uasset> --engine 5.7 --object <ObjectName> --property ParentClass
```

Quote paths containing spaces. `--engine` accepts explicit library versions such as `4.27`, `5.7` or `5.8`; this is a parser hint, not a compatibility guarantee. Omit it to use the package's recorded versions. Unknown selections are rejected. Unversioned packages are rejected even when an engine hint is supplied.

Default mode reads structural tables without loading export bodies. `--properties` parses selected exports; without `--object`, it parses all exports. `--object` accepts an exact name or outer-qualified path reported by the structure query, for example `TestActorBP.EventGraph`. Ambiguous names fail. `--property` implies property parsing and filters **top-level property names**, not nested fields or table rows. That export still needs to be decoded; a property filter is not a random-access binary seek.

The tool writes one JSON report to stdout. Save reports in the consuming project if needed. If using shell redirection, ensure its destination is different from the input and every source asset; the shell opens the destination before this program can protect it. No output-file or asset-writing command exists in the CLI.

## Interpret the report

| Field | Meaning |
| --- | --- |
| `status`, exit code | `complete` / 0: requested scope completed; `partial` / 1: opaque or unsupported selected data; `error` / 2: invalid, unsupported or failed request. |
| `input` | Basename, byte size and SHA-256 of the exact input snapshot. No machine path is stored. |
| `package` | Saved-by engine, selected version, object versions, flags and import/export counts. |
| `objects` | Stable package-local indices, outer-qualified paths, class identity, serial ranges and property state. |
| `properties` | Typed backend JSON for serialized values, including nested collections and array indices. Only present when requested. |
| `rows` | DataTable row payloads when properties are requested without a property filter and the backend decodes the table. |
| `references` | Known object-index, interface, delegate and soft-path references with owning property/row locators. Zero indices explicitly mean null; external targets are not followed. |
| `imports`, `soft_package_references` | Package catalogues, not proof that every entry is used or exists on disk. |
| `analysis` | Class-based family routing and suggested property names to inspect. Suggestions are not claims that those properties exist. |
| `opaque_bytes`, `limitations` | Uninterpreted data and limits that must remain attached to AI conclusions. |
| `inspection_elapsed_ms` | Local snapshot/read/projection time, excluding process startup and final JSON writing. Not a general benchmark. |

`not_requested` is different from an empty decoded property list. `complete` does not prove gameplay behavior, inherited effective defaults, full dependency coverage or that every native field was interpreted. Broken name indices are checked rather than accepting UAssetAPI's numeric-string fallback. Export-body reads and seeks are bounded by their declared serial ranges. Unknown property data, raw exports and trailing native bytes do not become complete empty values.

## Small extension structure

```text
src/Cli.cs            Arguments and failure contract
src/AssetReader.cs    Read-only snapshot, package gates, selective reading, index resolution
src/Analysis.cs       Typed projection, references, DataTable rows and family rules
src/ReadOnlyTextPropertyData.cs  Version-gated FText editor extension
src/Program.cs        JSON/stdout and process exit boundary
```

The common backend owns binary reading. Family rules use **root export class paths**, including their script package, with widget → montage → animation → data → blueprint precedence and generic fallback. They do not classify by filename or a merely imported class. Unrecognized custom subclasses remain generic unless their base is represented by a recognized root export; no external inheritance lookup occurs.

Blueprint, animation, montage, data and widget currently share structural/property extraction. To extend one, add a focused analyzer to `Analysis.cs`, deriving findings from actual object/property evidence; split a file only when it becomes independently substantial. Keep property locations, partial states and real fixture checks. Add another backend only if an observed unsupported format requires it.

## Scope and checks

- Maximum input: 256 MiB. Only the explicitly supplied, little-endian `.uasset` is read. The input is snapshotted through a read-only stream; the library receives a memory stream with no asset path and dependency loading disabled.
- Cooked/editor-stripped, unversioned, split export payloads and container formats such as IoStore are unsupported. Adjacent `.uexp`/`.ubulk` files are not read. Unsupported bulk/native content can remain opaque even when tagged properties are readable.
- Bytecode execution, graph/control-flow reconstruction, animation track decompression, rendered widgets, effective inherited values and runtime behavior are outside scope. Specialized native fields other than exposed DataTable rows are not projected.
- A size bound and structural checks do not make the third-party parser a hardened sandbox for hostile files. Use known, authorized development assets.

Reproduce the complete CLI suite:

```text
python tools/unreal-assets/tests/fetch_fixtures.py
dotnet restore tools/unreal-assets/tests/writer
dotnet build tools/unreal-assets/tests/writer -c Release --no-restore
python -B -m unittest discover -s tools/unreal-assets/tests -v
```

The fetch helper contacts only pinned public fixture URLs and verifies SHA-256 before saving locally ignored test files. Tests fail clearly if fixtures or built binaries are absent; no network runs during test discovery. The writer is **test-only**, saves derived fixtures to temporary directories, and is not part of the production CLI. Genuine upstream editor assets cover UE 4.27 and UE 5.7 blueprints. Synthetic family fixtures check routing and portable regressions.

The separate [engine fixture recipe](tests/engine/README.md) creates genuine UE 5.8 animation, montage, widget, PrimaryAssetLabel and DataTable packages. A fresh editor process reopens them without saving and supplies native comparison values. The CLI passed 31 comparisons, including nondefault properties, nested references and unchanged hashes. This controlled sample does not establish compatibility with every asset, engine build or native payload. Raw animation structs remain unsupported; ImportData prefixes/trailers remain opaque. The small FText override uses the serialized FortniteMain custom version to consume the editor-only Base-history developer notes absent from UAssetAPI 1.1.0; nested text histories still rely on upstream support. See [verification](verification.md) for executed results and limits.

## Dependencies and provenance

- [UAssetAPI](https://github.com/atenfyr/UAssetAPI): NuGet 1.1.0, package source commit `73530811a9d91ffa8959a1a4cb74cc3b9c5c6bed`, MIT. Dependency closure is pinned by `src/packages.lock.json`; its transitive packages retain their own licenses. The upstream license is retained in [UAssetAPI.LICENSE.txt](UAssetAPI.LICENSE.txt).
- Public test file identities and download paths: [tests/fixtures.json](tests/fixtures.json), upstream revision `05910ba8f6d278201120e10d87adbb06dfb3a097`. Original binaries are fetched on demand rather than redistributed here.
- [Design](../../docs/designs/uncooked-asset-reader.md) and [implementation plan](../../docs/superpowers/plans/2026-11-13-uncooked-assets.md).

Human readers may use `README.kr.md`; AI agents must not load translations.
