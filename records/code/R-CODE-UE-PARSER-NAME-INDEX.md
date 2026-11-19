---
id: R-CODE-UE-PARSER-NAME-INDEX
title: "Check serialized name indices before accepting a decoded property"
summary: "UAssetAPI 1.1.0 can return decimal text for an invalid name-map reference. A consumer must validate the name reference and distinguish opaque export data from decoded properties."
kind: error
scope: "Versioned, single-file uncooked packages read with UAssetAPI 1.1.0"
keywords: ["FName","name map","UAssetAPI","AssetBinaryReader.ReadFName","UAsset.GetNameReference","RawExport","serialization","uncooked package"]
status: resolved
checked_at: '2026-11-13'
trigger: "Treating successful library reads as sufficient proof of a valid serialized property name"
symptom: "A name outside the package name map became decimal property text and the consumer reported full decoding"
cause_status: confirmed
prevention: "Validate the serialized name index and instance number, preserve opaque data as partial and recheck valid controls"
prevention_status: verified
---

## Expected and observed

A consumer reported an apparently named property where the serialized name reference was invalid. Other readable properties made the result look complete.

## Cause and resolution

`FName` is Unreal's compact name representation. In this package format the serialized name uses a name-map index and a number. `AssetBinaryReader.ReadFName` reads those fields. At the cited revision, `UAsset.GetNameReference` can turn an out-of-range reference into decimal text. When export data is preserved as a `RawExport`, its availability as bytes does not establish property-level decoding.

## Recheck and prevention

The historical reader check distinguished invalid references from valid uncooked UE4 and UE5 controls, and reported opaque output as partial. Retain both checks when changing backend versions. Cooked and split packages and independent editor comparison require separate evidence.

## Evidence

The originating reader project's verification report records the consumer checks and their coverage. The upstream references below explain the library behavior separately.

The upstream source pins the observed fallback and read operation. The scoped consumer regression and controls were recorded on 2026-11-13. [Epic, FName](https://dev.epicgames.com/documentation/unreal-engine/fname-in-unreal-engine) · [UAsset.GetNameReference](https://github.com/atenfyr/UAssetAPI/blob/73530811a9d91ffa8959a1a4cb74cc3b9c5c6bed/UAssetAPI/UAsset.cs) · [AssetBinaryReader.ReadFName](https://github.com/atenfyr/UAssetAPI/blob/73530811a9d91ffa8959a1a4cb74cc3b9c5c6bed/UAssetAPI/AssetBinaryReader.cs)
