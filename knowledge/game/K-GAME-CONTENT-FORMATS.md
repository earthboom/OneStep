---
id: K-GAME-CONTENT-FORMATS
title: "Select game data formats by writer, access path and compatibility"
summary: "Give each fact an authoring source. Validate and import it into the shipping representation, keeping stable IDs and separate versions for schema, content and publication."
kind: method
scope: "Authored content, game state, local saves and live catalogs in Unity, Unreal and engine-independent tools."
keywords: ["game data","JSON Schema","CSV","FlatBuffers","SQLite","stable ID","contentRevision","schemaVersion","catalog","게임 데이터","데이터 포맷","JSON 스키마","데이터 파이프라인","기획 데이터","스테이지 JSON","구버전 세이브","고정 ID","데이터 삭제"]
status: active
checked_at: "2026-11-22"
---
# Select game data formats by writer, access path and compatibility

## Guidance

Identify the writer and the access pattern first. Designers edit definitions, the build produces distributable artifacts, a runner mutates session state, the save system persists progress, and an authoritative service commits transactions. Select JSON for hierarchical interchange, sheets/CSV for comparing rows, TOML or similar text for simple settings, and engine assets for spatial editing and reference previews. Binary representations can reduce parsing or transfers. SQLite supports indexed partial reads and transactions. Server-side constraints and transactions matter for concurrent grants or trades. Keep generated inputs read-only and trace them to their source.

For a puzzle define schemaVersion, stageId, rulesId, board dimensions, spawn, walls, boxes and goals, with coordinate origin, units and bounds. Reject duplicate JSON keys before schema validation. Fix UTF-8, key spelling, supported numeric ranges and ordering of arrays. Use strings for IDs that exceed exact integer precision in intermediate tools. Validate types and structure, then references, missing/duplicate IDs, overlaps and a solution through actual play. Report source, stage ID, field path and repair condition. Explicitly decide which unknown fields older readers may ignore.

In Unity, a TextAsset or importer can convert the external form to supported serialized types. Nested coordinate arrays need conversion or a compatible parser when using JsonUtility. In Unreal, use row-oriented Data Tables for regular records, assets or custom imports for hierarchical definitions. Resolve engine-specific asset keys at the boundary and open a stage from the shipped catalog. Incremental builds must invalidate results when input assets, tools or settings change.

## Applicability and exceptions

Keep identity through rename, moves and reorder. Separate schemaVersion (reader compatibility), contentRevision (layout, ghost or resume validity) and catalog publication version. When retiring an ID choose history retention, tombstone, fallback or migration and re-evaluate unlocks. Pin an active session to a complete compatible release and retain the prior usable set on a failed download. A save migrated under a new catalog can outlive rollback. For pack conflicts define load order, replacement, merge-by-ID and null semantics. JSON Merge Patch removes keys on null and may replace whole arrays.

## Checks

Add one stage, rename and reorder it, retire its ID, then load and resave real supported older files. Exercise a duplicated key, missing asset, unsupported rule, partial download, previous catalog and old Player. Compare clean and incremental import. Before changing formats, measure compressed size, cold/warm I/O, parse, reference resolution, initialization, peak memory, save write latency, recovery and authoring/review costs independently.

## Evidence

The November 22 format/pipeline review and the data-lifetime section of the development practices review drew on format specifications, engine contracts, schema compatibility and build-system research, and production accounts. Measurements reported by other teams depend on payload, compression and workload. This entry proposes checks for a target project.

[Durable saves and migration](K-GAME-TECH-SAVE.md) · [Authoring workflows](K-GAME-CONTENT-PRODUCTION.md) · [Stage ownership](K-GAME-STAGE-AUTHORING.md)

- [LDtk export and loading](https://ldtk.io/docs/game-dev/loading/) · [Build Systems à la Carte](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf)
- [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html) · [JSON Schema validation standard](https://json-schema.org/draft/2020-12/json-schema-validation) · [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180.html) · [W3C tabular data model](https://www.w3.org/TR/tabular-data-model/) · [YAML 1.2.2](https://yaml.org/spec/1.2.2/)
- [TOML](https://toml.io/en/v1.0.0) · [JSON5](https://spec.json5.org/) · [W3C XML](https://www.w3.org/TR/xml/) · [Unity asset metadata](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html) · [Unreal Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine)
- [Unreal Perforce guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine) · [Protobuf evolution practices](https://protobuf.dev/best-practices/dos-donts/) · [FlatBuffers schema evolution](https://flatbuffers.dev/evolution/) · [MessagePack](https://msgpack.org/) · [Binary format comparison study](https://arxiv.org/abs/2201.03051)
- [When to use SQLite](https://www.sqlite.org/whentouse.html) · [Application file format](https://www.sqlite.org/appfileformat.html) · [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html) · [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html) · [JSON and JSONB](https://www.postgresql.org/docs/current/datatype-json.html)
- [Factorio data lifecycle](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html)
- [Unreal Asset Manager](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine) · [I-JSON message format](https://www.rfc-editor.org/rfc/rfc7493.html) · [JSON Schema object constraints](https://json-schema.org/understanding-json-schema/reference/object) · [Paper on JSON schema compatibility](https://software-lab.org/publications/issta2021_JSON.pdf) · [GDC talk on loading imperfect data during development](https://media.gdcvault.com/gdc2013/slides/822192Fredriksson_Andreas_Loading_Imperfect_Data.pdf)
- [Tiled JSON format](https://doc.mapeditor.org/en/stable/reference/json-map-format/) · [LDtk JSON structure](https://ldtk.io/docs/game-dev/json-overview/) · [JSON canonicalization standard](https://www.rfc-editor.org/rfc/rfc8785.html)
- [ScriptableObject](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/scriptableobject) · [Text assets](https://docs.unity3d.com/6000.0/Documentation/Manual/class-TextAsset.html) · [ScriptedImporter](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AssetImporters.ScriptedImporter.html) · [Data Driven Gameplay Elements](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine) · [UDataTable JSON import](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UDataTable?application_version=5.8)
- [Unity JSON serialization](https://docs.unity3d.com/6000.0/Documentation/Manual/json-serialization.html) · [Addressables content updates](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/content-update-builds-overview.html) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Cooking](https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-in-unreal-engine) · [Unity serialization rules](https://docs.unity3d.com/6000.0/Documentation/Manual/script-serialization-rules.html)
- [Factorio migrations](https://lua-api.factorio.com/latest/auxiliary/migrations.html) · [Mojang DataFixerUpper](https://github.com/Mojang/DataFixerUpper) · [Unreal SaveGame](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine) · [JSON Merge Patch](https://www.rfc-editor.org/rfc/rfc7396.html)
- [Witch Beam, Unpacking, GCAP 2023 — Developer talk](https://youtu.be/2j7AJj1oRSQ) · [Witch Beam, Unpacking, GCAP 2023 — Talk segments](https://confpad.io/conferences/gcap-2023-empower/empowering-design-the-tools-and-pipelines-of-unpacking) · [GDC video](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Brandon Moro, Destiny 2, GDC 2018 — Slides](https://media.gdcvault.com/gdc2018/presentations/Moro_Brandon_Bungies_Asset_Pipeline.pdf) · [Developer paper](https://history.siggraph.org/wp-content/uploads/2022/09/2019-Talks-Santiago_Procedural-System-Assisted-Authoring.pdf)
- [GDC video](https://www.gdcvault.com/play/1025765/Level-Design-in-a-Moment)
- [Unity bundle reproducibility](https://docs.unity.com/en-us/engine/6000.3/manual/building-and-publishing/build-deterministic-builds/assetbundles-addressables) · [Data Registries](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-registries-in-unreal-engine) · [Unity ScriptableObject](https://unity.com/how-to/separate-game-data-logic-scriptable-objects) · [Addressables shipped-game case study](https://unity.com/resources/marvel-snap)
