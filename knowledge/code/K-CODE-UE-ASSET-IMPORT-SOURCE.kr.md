---
id: K-CODE-UE-ASSET-IMPORT-SOURCE
title: 에디터 Python으로 언리얼 에셋에 저장된 import 원본 경로를 지우는 법
summary: 파일을 import해 만든 에셋은 그 파일의 상대 경로를 AssetImportData에 저장하고, 이 경로는 에셋에 실려 배포되며 파일이 없는 사람의 재임포트를 깨뜨린다. UE 5.8 에디터 Python에서 에셋의 AssetImportData 프로퍼티와 그 SourceData는 읽기 전용이다. AssetImportData.scripted_add_filename("", 0, "")은 에셋의 나머지 데이터는 그대로 두고 0번 원본을 빈 경로로 바꾼다.
kind: method
scope: UAssetImportData를 가진 에셋(예: UCurveBase, 텍스처, 메시)에 대한 언리얼 엔진 5 에디터 Python. 헤드리스 커맨들릿이나 대화형 에디터
keywords: [UAssetImportData, AssetImportData, ScriptedAddFilename, scripted_add_filename, FAssetImportInfo, SourceData, RelativeFilename, ExtractFilenames, extract_filenames, K2_GetFirstFilename, AssetImportData read-only, VisibleAnywhere, reimport, source file path, CurveFloat, import 원본 경로, 재임포트]
status: active
checked_at: "2026-11-23"
context:
  engine: 언리얼 엔진 5.8 소스와 에디터 Python(UnrealEditor-Cmd -run=pythonscript)
---

## 안내

파일을 import하면(예: CSV를 float 커브로) 에셋의 `UAssetImportData::SourceData`에 원본이 JSON으로 기록된다. 상대 파일 이름, 타임스탬프, MD5, 라벨이다. 상대 파일 이름은 에셋 패키지 기준으로 풀리므로, 개인 폴더나 무시되는 폴더에 둔 파일이면 다른 사람이 풀 수 없는 경로가 남고, 경로 문자열 자체도 에셋과 함께 공개된다.

에디터 Python에서:

- `asset.set_editor_property("asset_import_data", ...)`는 실패한다. 이 프로퍼티는 `VisibleAnywhere, Instanced`라 Python에서 읽기 전용이다. import 데이터 객체의 `SourceData`도 `VisibleAnywhere`다.
- `asset.get_editor_property("asset_import_data").scripted_add_filename("", 0, "")`이 열려 있는 경로다. `Modify`를 부르고, 0번 항목을 바꾼 원본 목록을 다시 만들고, `PostEditChange`를 부른다. 저장된 항목은 `"RelativeFilename" : ""`와 빈 MD5가 된다. 그 뒤 에셋을 저장한다.

`extract_filenames()`는 저장된 상대 이름을 기준 디렉터리로 풀기 때문에, 비운 뒤에는 빈 목록이 아니라 디렉터리(예: 프로세스 작업 디렉터리)를 돌려준다. 결과는 그 호출이 아니라 저장된 에셋 바이트로 판단한다.

## 적용 범위와 예외

이 방법은 경로를 비울 뿐 항목을 지우지 않는다. import 없이 에디터에서 만든 에셋은 원본 목록이 비어 있는데(`[]`), 이 방법으로는 그 상태가 되지 않는다. 그 에셋은 에디터 재임포트가 더는 의미 없다. 작성된 데이터(커브 키, 텍스처 픽셀)를 기준으로 삼거나, 앞으로 재임포트가 필요하면 원본 파일을 공유되고 버전 관리되는 위치로 옮겨 거기서 다시 import한다. 원본 슬롯이 여럿인 에셋은 인덱스마다 처리한다.

## 점검

- 바꾸기 전에 에셋의 작성 데이터를 표본 추출하고(커브면 정해진 시각의 `get_float_value`), 저장 뒤 비교한다.
- 저장 뒤 에셋 바이트에서 옛 경로 문자열과 `RelativeFilename` JSON을 찾는다. 옛 경로가 없어야 한다.
- 같은 개인 폴더 이름을 아직 담고 있는 다른 에셋이 있는지 콘텐츠를 검색한다.

## 근거

- 엔진 소스, UE 5.8: `Runtime/Engine/Classes/EditorFramework/AssetImportData.h`(`ScriptedAddFilename`은 `BlueprintCallable`, `SourceData`는 `UPROPERTY(VisibleAnywhere)`), `Private/EditorFramework/AssetImportData.cpp`(`ScriptedAddFilename`과 `AddFileName`, `FAssetImportInfo::ToJson`).
- 작업 확인(2026-11-23): float 커브 에셋 두 개에서 `set_editor_property("asset_import_data", ...)`는 읽기 전용 오류를 냈다. `scripted_add_filename("", 0, "")`과 저장으로 바이트에서 개인 경로가 사라지고 빈 `RelativeFilename`이 저장됐으며, 커브마다 21개 표본 값이 전후로 같았다.
