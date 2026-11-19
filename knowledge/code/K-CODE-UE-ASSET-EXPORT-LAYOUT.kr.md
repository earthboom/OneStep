# 언리얼 패키지에서 익스포트의 태그 프로퍼티 시작점 찾기

항목 `K-CODE-UE-ASSET-EXPORT-LAYOUT` · 상태 활성 · 확인일 2026-11-10

----------

## 지침

익히지 않은 UE 패키지(.uasset, .umap)에서 `FObjectExport`는 내보낸 객체 한 개를 나타낸다.

1. 버전 정보가 있고 오브젝트 버전이 1010(`EUnrealEngineObjectUE5Version::SCRIPT_SERIALIZATION_OFFSET`) 이상이면 `ScriptSerializationStartOffset`과 `ScriptSerializationEndOffset`은 `SerialOffset` 기준 상대값이다. 둘 다 0이면 태그가 기록되지 않았다.
2. 이전 형식은 클래스별 규칙을 확인한다. `UAssetImportData`와 Fbx·Interchange·SpeedTree·Abc·Datasmith 계열 파생 클래스는 에디터 전용 데이터가 제외되지 않았을 때 기본 직렬화 전에 원본 파일 JSON을 FString으로 기록한다. CDO에는 이 머리말이 없다. `URigVMLink`는 FString 두 개, `UInterchangeBaseNode` 계열은 속성 저장소를 기록하고 UObject 기본 태그 경로를 거치지 않는다.
3. 클래스 기본 객체(CDO)는 `UClass::SerializeDefaultObject`로 저장하므로 태그 뒤 객체 GUID를 기대하지 않는다. 블루프린트 CDO 뒤에는 UE5Main 커스텀 버전 33부터 희소 클래스 데이터의 구조체 PackageIndex와, null이 아닐 때 해당 구조체의 태그 스트림이 올 수 있다.

## 적용 범위와 예외

UE 5.8 소스와 오브젝트 버전 1004~1018의 에디터 콘텐츠를 조사했다. 쿠킹 및 무버전 패키지, 수정 엔진은 미검증이다. 다른 클래스도 기본 직렬화 전후에 고유 데이터를 쓸 수 있다.

## 점검

범위의 순서와 익스포트 크기 `SerialSize`를 먼저 검사한다. 클래스별로 끝까지 정확히 읽힌 익스포트를 집계하고 반복 실패하는 클래스의 Serialize를 조사한다. 임포트 데이터 JSON의 시작 문자도 확인한다.

## 근거

2026-11-10 조사한 UE 5.8 소스는 AssetImportData.cpp, RigVMLink.cpp, InterchangeBaseNode.cpp, Class.cpp, BlueprintGeneratedClass.cpp이다. 익히지 않은 콘텐츠를 읽은 결과가 해당 규칙을 뒷받침했다. 1012 미만 RigHierarchy·RigVM 고유 형식, Zen/IoStore 및 다른 엔진 버전에는 한계가 있다. [Epic, FObjectExport](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/CoreUObject/FObjectExport?application_version=5.8)

검색어 Unreal Engine, uasset, package format, export, tagged properties, ScriptSerializationStartOffset, ScriptSerializationEndOffset, SCRIPT_SERIALIZATION_OFFSET, UAssetImportData, URigVMLink, UInterchangeBaseNode, SerializeDefaultObject, class default object, CDO, sparse class data, 언리얼 에셋, 패키지 형식, 직렬화, FObjectExport, FObjectExport::ScriptSerializationStartOffset, FObjectExport::ScriptSerializationEndOffset, EUnrealEngineObjectUE5Version::SCRIPT_SERIALIZATION_OFFSET, UAssetImportData::Serialize, UClass::SerializeDefaultObject, SerialOffset, SerialSize
