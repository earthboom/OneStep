# Uncooked asset reader

Provide a read-only command-line reader for local development assets. Use UAssetAPI 1.1.0 behind one adapter, then attach small, class-based family analyzers. Start with package structure, serialized properties and references. This is an offline inspection tool, not an asset editor or a proof of runtime behavior.

The user selected library reuse over a new binary parser. Direct parsing duplicates version-specific work; an engine-only exporter adds a project and engine runtime dependency. Engine comparison is a separate test route, with no editor dependency in the CLI. Existing knowledge `K-CODE-UE-ASSET-EXPORT-LAYOUT` and `K-CODE-UE-NATIVE-STRUCT-DECODING` informs opaque-data handling, not a claim of compatibility with their original experiments.

## Observable behavior

- `dotnet run --project tools/unreal-assets/src -- file.uasset --engine 5.7` emits compact structural JSON. It reads tables without decoding export bodies.
- `--properties` decodes serialized property values; `--object NAME_OR_PATH` selects an export before body parsing; `--property NAME` filters top-level properties after that export is decoded.
- Version, file fingerprint, object indices/paths/classes, import catalogue, soft package references and decoding limitations accompany results. Integers become object references only when the serialized property type identifies them as such.
- Class identities select blueprint, animation, montage, data, widget or generic analysis. This first version reports observed family structure and relevant serialized property names, not reconstructed behavior or visual fidelity.
- Unsupported/raw exports and opaque trailing data remain visible. Partial output exits 1; rejected input or a failed request exits 2. Exit 0 means the requested inspection scope completed, not every byte or gameplay behavior was understood.

## Boundaries

Only `.uasset` input is accepted. Reject cooked/filter-editor-only packages, unversioned properties requiring mappings, unsupported engine selections, corrupt input and conflicting selectors. No dependency traversal, source rewriting, editor launch, cache, or arbitrary output path exists in the initial CLI. Standard output is the report; the caller owns safe redirection. Snapshot the explicitly supplied input through a read-only stream and pass an in-memory reader to the library; do not let it discover neighbouring projects. Split export/bulk payloads are outside this initial uncooked single-file path and must not become complete empty values.

The backend uses `SkipPreloadDependencyLoading`, `SkipParsingBytecode` and initial `SkipLoadingExports`. Decode selected exports on the same in-memory package. Bound input size, validate export ranges before body parsing, then enforce each selected range on actual reads and seeks. Retain native extras as counts and property JSON with the backend's type information; do not deserialize untrusted JSON type names. No performance claim is made before measurement.

## Checks and extension

Build on .NET 8; pin the dependency and its transitive lock. Exercise real public editor fixtures from a pinned upstream commit with SHA-256 checks, including UE 4.27 and UE 5.7 blueprints. Compare literal object/property/reference expectations with fixture data. Test cooked, truncated, invalid selectors, unknown versions, partial native data, input immutability and actual CLI exit codes. Synthetic library-written family fixtures check routing only and never establish engine fidelity.

Keep the real-engine fixture project under tests, outside the runtime path. Create controlled nondefault animation, montage, widget and data assets in an isolated directory, then reopen them in a second editor process without saving. Compare the CLI with those native observations and preserve file hashes. Version-specific fixes stay small: a registered TextProperty subclass consumes Base-history developer notes at the actual custom-version gate; declared script offsets locate prefixed ImportData tags while retaining opaque prefix/trailer bytes. Raw struct wrappers never imply decoded animation tracks. Full graph semantics, track decompression, rendered widgets and general engine compatibility remain outside supported claims.

Keep implementation under `tools/unreal-assets/`, with a backend, result projection/analyzers and CLI. Add a family analyzer only when an actual request needs richer semantics. Project paths and generated reports belong to the consuming workspace.
