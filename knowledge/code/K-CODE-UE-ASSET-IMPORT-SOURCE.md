---
id: K-CODE-UE-ASSET-IMPORT-SOURCE
title: How to remove a stored import source path from an Unreal asset with editor Python
summary: An asset created by importing a file stores that file's relative path in its AssetImportData, which ships in the asset and breaks reimport for anyone without the file. In UE 5.8 editor Python the asset's AssetImportData property and its SourceData are read-only; AssetImportData.scripted_add_filename("", 0, "") replaces source 0 with an empty path while leaving the asset's other data unchanged.
kind: method
scope: Unreal Engine 5 editor Python on assets that carry UAssetImportData (for example UCurveBase, textures, meshes); headless commandlet or interactive editor
keywords: [UAssetImportData, AssetImportData, ScriptedAddFilename, scripted_add_filename, FAssetImportInfo, SourceData, RelativeFilename, ExtractFilenames, extract_filenames, K2_GetFirstFilename, AssetImportData read-only, VisibleAnywhere, reimport, source file path, CurveFloat, import 원본 경로, 재임포트]
status: active
checked_at: "2026-11-23"
context:
  engine: Unreal Engine 5.8 source and editor Python (UnrealEditor-Cmd -run=pythonscript)
---

## Guidance

Importing a file (for example a CSV into a float curve) records the source in the asset's `UAssetImportData::SourceData` as JSON: relative filename, timestamp, MD5 and label. The relative filename is resolved from the asset package, so a file kept in a personal or ignored folder leaves a path that other users cannot resolve, and the path text itself is published with the asset.

In editor Python:

- `asset.set_editor_property("asset_import_data", ...)` fails: the property is `VisibleAnywhere, Instanced` and therefore read-only to Python. `SourceData` on the import data object is also `VisibleAnywhere`.
- `asset.get_editor_property("asset_import_data").scripted_add_filename("", 0, "")` is the exposed path. It calls `Modify`, rebuilds the source list with entry 0 replaced, and calls `PostEditChange`. The stored entry becomes `"RelativeFilename" : ""` with an empty MD5. Save the asset afterwards.

`extract_filenames()` resolves stored relative names against a base directory, so after blanking it returns a directory (such as the process working directory), not an empty list. Judge the result from the saved asset bytes, not from that call.

## Applicability and exceptions

This blanks the path; it does not remove the entry. An asset authored in the editor without import has an empty source list (`[]`), which this method does not reproduce. Reimport through the editor is no longer meaningful for the asset; keep the authored data (curve keys, texture pixels) as the source of truth, or move the original file to a shared versioned location and reimport from there instead when future reimport is required. Assets with several source slots need each index handled.

## Checks

- Before the change, sample the asset's authored data (for a curve, `get_float_value` at fixed times) and compare after save.
- After save, search the asset bytes for the old path text and for the `RelativeFilename` JSON; the old path must be absent.
- Search content for other assets that still embed the same personal folder name.

## Evidence

- Engine source, UE 5.8: `Runtime/Engine/Classes/EditorFramework/AssetImportData.h` (`ScriptedAddFilename` is `BlueprintCallable`; `SourceData` is `UPROPERTY(VisibleAnywhere)`), `Private/EditorFramework/AssetImportData.cpp` (`ScriptedAddFilename` and `AddFileName`; `FAssetImportInfo::ToJson`).
- Task check (2026-11-23): on two float curve assets, `set_editor_property("asset_import_data", ...)` raised the read-only error; `scripted_add_filename("", 0, "")` plus save removed the personal path from the bytes, stored an empty `RelativeFilename`, and 21 sampled values per curve were identical before and after.
