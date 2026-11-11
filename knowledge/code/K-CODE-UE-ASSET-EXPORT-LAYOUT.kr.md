---
id: K-CODE-UE-ASSET-EXPORT-LAYOUT
title: 엔진 밖에서 언리얼 패키지 export를 읽을 때 tagged 프로퍼티가 시작하는 위치
summary: 객체 버전 1010 이상의 versioned UE 5 패키지는 export의 스크립트 직렬화 시작 위치로 이동하고, 시작과 끝이 모두 0이면 "tagged 프로퍼티 없음"으로 봅니다. 그보다 오래되었거나 unversioned인 패키지는 태그 앞에 쓰는 import data JSON 같은 클래스별 규칙이 필요합니다.
kind: reference
scope: 엔진 없이 export 데이터를 해석하는, cook하지 않은 Unreal Engine 5 패키지(.uasset, .umap)의 독립 리더
keywords: [Unreal Engine, uasset, package format, export, tagged properties, ScriptSerializationStartOffset, ScriptSerializationEndOffset, SCRIPT_SERIALIZATION_OFFSET, UAssetImportData, URigVMLink, UInterchangeBaseNode, SerializeDefaultObject, class default object, CDO, sparse class data, 언리얼 에셋, 패키지 형식, 직렬화]
status: active
checked_at: "2026-11-10"
context:
  engine: Unreal Engine 5.8 기본 직렬화
  package: cook 안 함, versioned 프로퍼티, 객체 버전 1004~1018
---

## 지침

export의 UObject 부분이 시작하는 위치는 다음 순서로 찾습니다.

1. **객체 버전 1010 이상인 versioned 패키지**(`EUnrealEngineObjectUE5Version::SCRIPT_SERIALIZATION_OFFSET`): export 테이블 항목에 export의 serial offset 기준 `ScriptSerializationStartOffset`과 `ScriptSerializationEndOffset`이 있습니다. 시작 위치로 이동합니다. 둘 다 0이면 그 클래스는 tagged 프로퍼티를 쓰지 않은 것입니다. 저장기는 태그를 쓸 때만 범위를 기록하기 때문입니다(`Class.cpp`, `LinkerSave`). 이때는 태그를 읽지 않습니다.
2. **그보다 오래되었거나 unversioned인 패키지:** 클래스 규칙을 적용합니다.
   - `UAssetImportData`와 하위 클래스(`Fbx*ImportData`, `InterchangeAssetImportData`, `SpeedTreeImportData`, `AbcAssetImportData`, 모든 `Datasmith*ImportData`)는 패키지가 `FilterEditorOnly`가 아니면 `Super::Serialize` 앞에 원본 파일 JSON FString을 씁니다(`AssetImportData.cpp`의 `UAssetImportData::Serialize`). 클래스 기본 객체는 쓰지 않습니다.
   - `URigVMLink`(FString 두 개)와 `UInterchangeBaseNode` 하위 클래스(속성 저장소)는 `UObject::Serialize`를 부르지 않으므로 태그가 없습니다.
3. **클래스 기본 객체:** `UClass::SerializeDefaultObject`로 저장되므로 태그 뒤에 객체 GUID가 없습니다. Blueprint 클래스의 CDO 뒤에는 sparse class data가 옵니다. UE5Main 사용자 정의 버전 33 이상에서는 구조체 PackageIndex가 오고, null이 아니면 그 구조체의 tagged 스트림이 옵니다(`BlueprintGeneratedClass.cpp`).

## 적용 범위와 예외

기본 UE 5.8 소스와, 객체 버전 1004~1018이 섞인 한 프로젝트의 에디터 콘텐츠에서 확인했습니다. 다른 엔진 버전, 직렬화를 바꾼 엔진 포크, cook했거나 unversioned인 패키지는 시험하지 않았습니다. 1단계는 unversioned 패키지에 적용되지 않습니다. `Super::Serialize` 앞에 데이터를 쓰거나 이를 건너뛰는 사용자 정의 `Serialize`를 가진 클래스가 더 있을 수 있으며, 스윕으로 찾습니다.

## 확인 방법

- 큰 콘텐츠 폴더의 모든 export를 스윕하고, 끝까지 정확히 읽은 export 수를 클래스별로 셉니다. 계속 실패하는 클래스는 또 다른 사용자 정의 `Serialize`가 있다는 신호입니다.
- 각 import data JSON 문자열이 `[` 또는 `{`로 시작하는지 확인합니다.

## 근거

출처: 독립 실행형 읽기 전용 .uasset 뷰어 프로젝트, 2026-11-10. UE 5.8 체크아웃에서 읽은 엔진 소스: `AssetImportData.cpp`(`UAssetImportData::Serialize`), `RigVMLink.cpp`, `InterchangeBaseNode.cpp`, `Class.cpp`(스크립트 범위 기록), `BlueprintGeneratedClass.cpp`(sparse class data). 패키지 약 131,000개, export 약 460만 개 스윕에서 이 규칙을 넣은 뒤에는 자체 직렬화를 가진 1012 미만 `RigHierarchy`와 `RigVM` 객체를 빼고 모든 export를 예외 없이 읽었습니다.

검증하지 않음: cook한 패키지, Zen/IoStore 컨테이너, 5.8 이외의 엔진 버전.
