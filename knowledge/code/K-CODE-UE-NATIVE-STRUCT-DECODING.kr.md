---
id: K-CODE-UE-NATIVE-STRUCT-DECODING
title: native 직렬화를 쓸 수도 있고 안 쓸 수도 있는 언리얼 구조체 프로퍼티를 해석하는 방법
summary: native 직렬화기가 있는 구조체라도 Serialize가 false를 반환하면 tagged 프로퍼티로 저장됩니다. 알려진 native 레이아웃은 Serialize 소스의 사용자 정의 버전 조건에 따라 해석하고, 그 밖에는 tagged 스트림을 시도해 값 크기를 정확히 소비할 때만 채택합니다.
kind: method
scope: 엔진 없이 StructProperty 값과 1012 미만 Set/Map 구조체 원소를 해석하는, cook하지 않은 Unreal Engine 5 패키지의 독립 리더
keywords: [Unreal Engine, uasset, StructProperty, native serialization, STRUCT_SerializeNative, Serialize returns false, tagged fallback, exact size, custom version, MovieSceneFloatChannel, MovieSceneDoubleChannel, SmartName, PerQualityLevelInt, UniversalObjectLocatorFragment, FontData, FrameRate, FTimeline, Set, Map, 구조체 직렬화, 언리얼 에셋]
status: active
checked_at: "2026-11-10"
context:
  engine: Unreal Engine 5.8 기본 직렬화
  package: cook 안 함, versioned 프로퍼티, 객체 버전 1004~1018
---

## 지침

1. **알려진 native 레이아웃:** 프로퍼티 태그가 아니라 구조체의 `Serialize` 소스에서 읽은 사용자 정의 버전 조건으로 해석합니다. UE 5.8에서 확인한 레이아웃은 다음과 같습니다.
   - `SmartName`: FName, AnimPhys 사용자 정의 버전 < 5이면 uint16, AnimPhys < 10이면 Guid.
   - `PerQualityLevelInt`, `PerQualityLevelFloat`: bool32 cooked, Default, `TMap<int32, T>`.
   - `UniversalObjectLocatorFragment`: FName 타입, 그다음 tagged 스트림인 페이로드.
   - `FontData`: Editor 사용자 정의 버전 9(AddedFontFaceAssets) 이상이면 bool32 cooked 뒤에 tagged, 그 전에는 tagged만.
   - `MovieSceneFloatChannel`, `MovieSceneDoubleChannel`(`MovieSceneCurveChannelImpl.cpp`)은 Sequencer 사용자 정의 버전 ≥ 12이거나 FortniteMain ≥ 53일 때 다음과 같습니다: uint8 앞뒤 외삽; int32 원소 크기, int32 개수, 원시 키 시간; int32 원소 크기, int32 개수, 원시 키 값; 기본값; bool32 기본값 유무; int32 틱 해상도 분자와 분모; FortniteMain ≥ 53이면 bool32 show-curve. 두 조건 모두 미만이면 채널은 tagged입니다.
2. **알려진 레이아웃이 없음:** 값 크기 안에서 tagged 스트림을 읽어 보고, 정확히 그 크기에서 끝날 때만 채택합니다. 아니면 원시 바이트를 보관하고 미지원 값으로 보고합니다. native 직렬화기를 선언해도 `Serialize`가 false를 반환하는 구조체는 tagged입니다. 예: `FTimeline`, `AlphaBlend`, `InputAlphaBoolBlend`, `GameplayEffectModifierMagnitude`. `FrameRate`는 tagged입니다.
3. **1012 미만 Set과 Map 원소**는 구조체 이름을 기록하지 않습니다. 후보 레이아웃(tagged 스트림, 16바이트 Guid, 그다음 Niagara 변수 같은 도메인 레이아웃)을 시도해 원소에 정확히 맞는 첫 번째를 채택합니다.

## 적용 범위와 예외

정확한 크기 검사는 근거일 뿐 증명이 아닙니다. 다른 레이아웃이 우연히 맞을 수 있습니다. tagged 스트림은 `None` 태그로 끝나야 하므로 위험이 낮고, 고정 크기 원시 후보는 위험이 더 큽니다. 조건과 레이아웃은 엔진 버전마다 바뀌므로 대상 엔진 소스에서 다시 확인합니다. 원시 배열이 있는 big-endian 패키지는 바이트 순서를 바꿔야 합니다.

## 확인 방법

- 부분적으로 맞는 것은 절대 채택하지 않습니다. 남는 바이트는 해석 오류입니다.
- 콘텐츠를 스윕해 미지원 값을 구조체 이름별로 셉니다. 자주 나오는 것에는 native 디코더를 만듭니다.

## 근거

출처: 독립 실행형 읽기 전용 .uasset 뷰어 프로젝트, 2026-11-10. 레이아웃은 위 구조체들의 UE 5.8 `Serialize` 함수에서 읽었습니다. export 약 460만 개 스윕에서 이 단계로 정확한 소비율이 클래스 기본 객체는 92.7%에서 99.98%로, 그 밖의 하위 객체는 79.5%에서 99.94%로 올랐습니다. 읽지 못한 1012 미만 Set/Map 원소는 약 114,000개에서 160개 값으로 줄었습니다.

검증하지 않음: 5.8 이외의 엔진 버전, 에디터 덤프와의 값 대조.
