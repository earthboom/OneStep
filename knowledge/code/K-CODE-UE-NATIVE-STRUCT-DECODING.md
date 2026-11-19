---
id: K-CODE-UE-NATIVE-STRUCT-DECODING
title: How to decode an Unreal struct property that may or may not use native serialization
summary: A struct with a native serializer is still saved as tagged properties when its Serialize returns false. Decode known native layouts by the custom version gates in their Serialize source; otherwise try a tagged stream and accept it only when it consumes the value size exactly.
kind: method
scope: Standalone readers of uncooked Unreal Engine 5 packages that decode StructProperty values and pre-1012 Set or Map struct elements without the engine
keywords: [Unreal Engine, uasset, StructProperty, native serialization, STRUCT_SerializeNative, Serialize returns false, tagged fallback, exact size, custom version, MovieSceneFloatChannel, MovieSceneDoubleChannel, SmartName, PerQualityLevelInt, UniversalObjectLocatorFragment, FontData, FrameRate, FTimeline, Set, Map, 구조체 직렬화, 언리얼 에셋, "FStructProperty", "UScriptStruct::UseNativeSerialization", "UScriptStruct::SerializeItem", "RawStructPropertyData", "UAssetAPI", "PerQualityLevelFloat", "AlphaBlend", "InputAlphaBoolBlend", "GameplayEffectModifierMagnitude"]
status: active
checked_at: "2026-11-10"
context:
  engine: Unreal Engine 5.8 stock serialization
  package: uncooked, versioned properties, object versions 1004 to 1018
---

## Guidance

`FStructProperty` describes a reflected structure property. `UScriptStruct::UseNativeSerialization` reports whether a native serializer exists. `UScriptStruct::SerializeItem` serializes an instance; the archive, custom versions and native serializer's return determine the path used. `STRUCT_SerializeNative` alone cannot identify the bytes on disk.

1. **Known native layout:** decode it with the custom version gates read from the struct's `Serialize` source, not from the property tag. Layouts checked in UE 5.8:
   - `SmartName`: FName, then uint16 if AnimPhys custom version < 5, then a Guid if AnimPhys < 10.
   - `PerQualityLevelInt` and `PerQualityLevelFloat`: bool32 cooked, Default, then `TMap<int32, T>`.
   - `UniversalObjectLocatorFragment`: FName type, then the payload as a tagged stream.
   - `FontData`: at Editor custom version 9 (AddedFontFaceAssets) or later, bool32 cooked, then tagged; earlier, tagged only.
   - `MovieSceneFloatChannel` and `MovieSceneDoubleChannel` (`MovieSceneCurveChannelImpl.cpp`), when Sequencer custom version ≥ 12 or FortniteMain ≥ 53: uint8 pre- and post-extrapolation; int32 element size, int32 count and raw key times; int32 element size, int32 count and raw key values; the default value; bool32 has-default; int32 tick resolution numerator and denominator; bool32 show-curve if FortniteMain ≥ 53. Below both gates the channel is tagged.
2. **No known layout:** try reading a tagged stream inside the value's size, and accept it only if it ends exactly at the size; otherwise keep the raw bytes and report the value as unsupported. Structs whose `Serialize` returns false are tagged even though they declare a native serializer, for example `FTimeline`, `AlphaBlend`, `InputAlphaBoolBlend`, `GameplayEffectModifierMagnitude`. `FrameRate` is tagged.
3. **Pre-1012 Set and Map elements** do not record their struct name. Try candidate layouts (a tagged stream, a 16-byte Guid, then any domain layout such as the Niagara variable) and accept a candidate only when independent element boundaries and version/type evidence support it. If several fit or boundaries cannot be established, retain the bytes as unresolved.

## Applicability and exceptions

The exact-size test is evidence, not proof: another layout can fit by chance. Tagged streams carry low risk because they must end with a `None` tag; raw fixed-size candidates carry more. Gates and layouts change between engine versions; recheck them in the target engine's source. Big-endian packages with raw arrays need byte swapping.

## Checks

- Never accept a partial fit; leftover bytes are a decoding error.
- Sweep content and count unsupported values by struct name; frequent ones deserve a native decoder.
- When wrapping another parser, propagate its opaque struct types as unsupported/partial even when the outer export read succeeds. For UAssetAPI 1.1.0, `RawStructPropertyData` retains raw bytes; it does not establish a decoded value. Exercise nested arrays in a real engine-saved asset as well as scalar fixtures.

## Evidence

Historical source reading and an editor-content sweep on 2026-11-10 (UE 5.8, versioned uncooked objects 1004–1018) improved exact boundary consumption; some old container elements remained unidentified. A separate wrapper check on 2026-11-13 found that nested raw struct payloads in an engine-saved animation had been counted as decoded. Treating those properties as unsupported and their exports as partial corrected the reported coverage. This did not verify individual native struct values against the Editor. Other versions and byte orders require new comparisons. [Epic, UScriptStruct](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/CoreUObject/UScriptStruct?application_version=5.8) · [UAssetAPI, RawStructPropertyData](https://github.com/atenfyr/UAssetAPI/blob/master/UAssetAPI/PropertyTypes/Structs/RawStructPropertyData.cs)
