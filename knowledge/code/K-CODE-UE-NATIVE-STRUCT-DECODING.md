---
id: K-CODE-UE-NATIVE-STRUCT-DECODING
title: How to decode an Unreal struct property that may or may not use native serialization
summary: A struct with a native serializer is still saved as tagged properties when its Serialize returns false. Decode known native layouts by the custom version gates in their Serialize source; otherwise try a tagged stream and accept it only when it consumes the value size exactly.
kind: method
scope: Standalone readers of uncooked Unreal Engine 5 packages that decode StructProperty values and pre-1012 Set or Map struct elements without the engine
keywords: [Unreal Engine, uasset, StructProperty, native serialization, STRUCT_SerializeNative, Serialize returns false, tagged fallback, exact size, custom version, MovieSceneFloatChannel, MovieSceneDoubleChannel, SmartName, PerQualityLevelInt, UniversalObjectLocatorFragment, FontData, FrameRate, FTimeline, Set, Map, 구조체 직렬화, 언리얼 에셋]
status: active
checked_at: "2026-11-10"
context:
  engine: Unreal Engine 5.8 stock serialization
  package: uncooked, versioned properties, object versions 1004 to 1018
---

## Guidance

1. **Known native layout:** decode it with the custom version gates read from the struct's `Serialize` source, not from the property tag. Layouts checked in UE 5.8:
   - `SmartName`: FName, then uint16 if AnimPhys custom version < 5, then a Guid if AnimPhys < 10.
   - `PerQualityLevelInt` and `PerQualityLevelFloat`: bool32 cooked, Default, then `TMap<int32, T>`.
   - `UniversalObjectLocatorFragment`: FName type, then the payload as a tagged stream.
   - `FontData`: at Editor custom version 9 (AddedFontFaceAssets) or later, bool32 cooked, then tagged; earlier, tagged only.
   - `MovieSceneFloatChannel` and `MovieSceneDoubleChannel` (`MovieSceneCurveChannelImpl.cpp`), when Sequencer custom version ≥ 12 or FortniteMain ≥ 53: uint8 pre- and post-extrapolation; int32 element size, int32 count and raw key times; int32 element size, int32 count and raw key values; the default value; bool32 has-default; int32 tick resolution numerator and denominator; bool32 show-curve if FortniteMain ≥ 53. Below both gates the channel is tagged.
2. **No known layout:** try reading a tagged stream inside the value's size, and accept it only if it ends exactly at the size; otherwise keep the raw bytes and report the value as unsupported. Structs whose `Serialize` returns false are tagged even though they declare a native serializer, for example `FTimeline`, `AlphaBlend`, `InputAlphaBoolBlend`, `GameplayEffectModifierMagnitude`. `FrameRate` is tagged.
3. **Pre-1012 Set and Map elements** do not record their struct name. Try candidate layouts (a tagged stream, a 16-byte Guid, then any domain layout such as the Niagara variable) and accept the first that fits the element exactly.

## Applicability and exceptions

The exact-size test is evidence, not proof: another layout can fit by chance. Tagged streams carry low risk because they must end with a `None` tag; raw fixed-size candidates carry more. Gates and layouts change between engine versions; recheck them in the target engine's source. Big-endian packages with raw arrays need byte swapping.

## Checks

- Never accept a partial fit; leftover bytes are a decoding error.
- Sweep content and count unsupported values by struct name; frequent ones deserve a native decoder.

## Evidence

Provenance: a standalone read-only .uasset viewer project, 2026-11-10. Layouts read from the UE 5.8 `Serialize` functions of the structs named above. In a sweep of about 4.6 million exports, these steps raised exact consumption from 92.7% to 99.98% for class default objects and from 79.5% to 99.94% for other subobjects. Unread pre-1012 Set and Map elements fell from about 114,000 to 160 values.

Not verified: engine versions other than 5.8; values compared against an editor dump.
