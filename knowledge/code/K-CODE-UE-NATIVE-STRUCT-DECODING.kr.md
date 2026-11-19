# 언리얼 구조체 프로퍼티의 네이티브 및 태그 직렬화 판별

항목 `K-CODE-UE-NATIVE-STRUCT-DECODING` · 상태 활성 · 확인일 2026-11-10

----------

## 지침

반영된 구조체 프로퍼티는 `FStructProperty`다. `UScriptStruct::UseNativeSerialization`은 네이티브 직렬화 함수의 존재를, `UScriptStruct::SerializeItem`은 인스턴스의 직렬화 진입점을 나타낸다. `STRUCT_SerializeNative`만으로 저장 형식을 결정할 수 없다.

- UE 5.8에서 SmartName은 FName 다음에 AnimPhys 버전 5 미만이면 uint16, 10 미만이면 Guid를 기록한다. PerQualityLevelInt·Float는 bool32 cooked, 기본값, `TMap<int32, T>` 순이다. UniversalObjectLocatorFragment는 타입 FName 다음에 태그 페이로드를 쓴다. FontData는 Editor 버전 9 이상에서 bool32 cooked 뒤에 태그를 쓰고 이전에는 태그만 쓴다.
- MovieSceneFloatChannel·MovieSceneDoubleChannel은 Sequencer 버전 12 또는 FortniteMain 53 이상일 때 외삽 모드 두 바이트, 크기·개수와 원시 키 시간 배열, 크기·개수와 원시 키 값 배열, 기본값과 존재 여부, 틱 해상도 분자·분모를 기록한다. FortniteMain 53 이상이면 곡선 표시 bool32가 추가된다. 두 기준 미만이면 태그 형식이다.
- 모르는 레이아웃은 값 크기를 넘지 않는 태그 읽기를 시도하고 끝이 정확히 맞아야 한다. 네이티브 Serialize가 false를 반환하는 FTimeline, AlphaBlend, InputAlphaBoolBlend, GameplayEffectModifierMagnitude는 태그로 기록될 수 있다. FrameRate도 태그다.
- 1012 이전 Set·Map 구조체 원소는 구조체 이름이 없다. 태그 스트림, 16바이트 Guid 또는 Niagara 원소 등 가능한 형식을 검토하되 독립적인 경계 및 버전·타입 근거가 없거나 여러 후보가 맞으면 원본 바이트를 미해석으로 보존한다.

## 적용 범위와 예외

정확한 크기만으로 올바른 값을 보장할 수 없다. None 종결 태그까지 확인하는 형식에 비해 고정 크기 구조체는 우연히 맞을 수 있다. 엔진 버전과 엔디언을 확인한다.

## 점검

남은 바이트와 미지원 값을 구조체별로 집계한다. UAssetAPI 1.1.0의 `RawStructPropertyData`는 원시 바이트다. 중첩 배열을 포함한 실제 에디터 에셋으로 원시 프로퍼티가 미지원, 해당 익스포트가 부분 해석으로 보고되는지 확인한다.

## 근거

2026-11-10 UE 5.8 소스 및 오브젝트 버전 1004~1018의 익히지 않은 콘텐츠에서 정확히 끝까지 읽는 비율이 개선됐으나 일부 이전 컨테이너는 미해석으로 남았다. 11-13 별도 래퍼 검사는 애니메이션에 중첩된 원시 값의 상태 오분류를 확인했다. 개별 네이티브 값을 에디터와 대조하지 않았고 다른 버전·바이트 순서는 추가 검증이 필요하다. [Epic, UScriptStruct](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/CoreUObject/UScriptStruct?application_version=5.8) · [UAssetAPI, RawStructPropertyData](https://github.com/atenfyr/UAssetAPI/blob/master/UAssetAPI/PropertyTypes/Structs/RawStructPropertyData.cs)

검색어 Unreal Engine, uasset, StructProperty, native serialization, STRUCT_SerializeNative, Serialize returns false, tagged fallback, exact size, custom version, MovieSceneFloatChannel, MovieSceneDoubleChannel, SmartName, PerQualityLevelInt, UniversalObjectLocatorFragment, FontData, FrameRate, FTimeline, Set, Map, 구조체 직렬화, 언리얼 에셋, FStructProperty, UScriptStruct::UseNativeSerialization, UScriptStruct::SerializeItem, RawStructPropertyData, UAssetAPI, PerQualityLevelFloat, AlphaBlend, InputAlphaBoolBlend, GameplayEffectModifierMagnitude
