---
id: K-CODE-UE-ASSET-EXPORT-LAYOUT
title: Where an Unreal package export's tagged properties start when reading it outside the engine
summary: In versioned UE 5 packages at object version 1010 or later, seek to the export's script serialization start, and treat a start and end of 0 as "no tagged properties". Older or unversioned packages need per-class rules, such as the import data JSON written before the tags.
kind: reference
scope: Standalone readers of uncooked Unreal Engine 5 packages (.uasset, .umap) that parse export data without the engine
keywords: [Unreal Engine, uasset, package format, export, tagged properties, ScriptSerializationStartOffset, ScriptSerializationEndOffset, SCRIPT_SERIALIZATION_OFFSET, UAssetImportData, URigVMLink, UInterchangeBaseNode, SerializeDefaultObject, class default object, CDO, sparse class data, 언리얼 에셋, 패키지 형식, 직렬화]
status: active
checked_at: "2026-11-10"
context:
  engine: Unreal Engine 5.8 stock serialization
  package: uncooked, versioned properties, object versions 1004 to 1018
---

## Guidance

Find the start of an export's UObject part in this order.

1. **Versioned package, object version 1010 or later** (`EUnrealEngineObjectUE5Version::SCRIPT_SERIALIZATION_OFFSET`): the export table entry holds `ScriptSerializationStartOffset` and `ScriptSerializationEndOffset`, relative to the export's serial offset. Seek to the start. If both are 0, the class wrote no tagged properties, because the saver records the range only when it writes tags (`Class.cpp`, `LinkerSave`). Do not read tags in that case.
2. **Older or unversioned package:** apply class rules.
   - `UAssetImportData` and its subclasses (`Fbx*ImportData`, `InterchangeAssetImportData`, `SpeedTreeImportData`, `AbcAssetImportData`, every `Datasmith*ImportData`) write an FString of source-file JSON before `Super::Serialize`, unless the package is `FilterEditorOnly` (`UAssetImportData::Serialize` in `AssetImportData.cpp`). The class default object does not.
   - `URigVMLink` (two FStrings) and `UInterchangeBaseNode` subclasses (attribute storage) do not call `UObject::Serialize`, so they have no tags.
3. **Class default object:** saved with `UClass::SerializeDefaultObject`, so no object GUID follows the tags. A Blueprint class's CDO is followed by sparse class data: at UE5Main custom version 33 or later, a struct PackageIndex, then that struct's tagged stream if it is not null (`BlueprintGeneratedClass.cpp`).

## Applicability and exceptions

Checked against stock UE 5.8 source and one project's editor content with object versions 1004 to 1018. Other engine versions, engine forks that change serialization, and cooked or unversioned packages are untested; step 1 does not apply to unversioned packages. Further classes with a custom `Serialize` that writes before `Super::Serialize`, or skips it, can exist; a sweep finds them.

## Checks

- Sweep every export of a large content folder and count the exports read exactly to their end, grouped by class. A class that fails consistently is the signal of another custom `Serialize`.
- Check that each import data JSON string starts with `[` or `{`.

## Evidence

Provenance: a standalone read-only .uasset viewer project, 2026-11-10. Engine source read in a UE 5.8 checkout: `AssetImportData.cpp` (`UAssetImportData::Serialize`), `RigVMLink.cpp`, `InterchangeBaseNode.cpp`, `Class.cpp` (script range recording), `BlueprintGeneratedClass.cpp` (sparse class data). A sweep of about 131,000 packages and 4.6 million exports read every export without an exception after these rules, except pre-1012 `RigHierarchy` and `RigVM` objects with their own serialization.

Not verified: cooked packages, Zen/IoStore containers, engine versions other than 5.8.
