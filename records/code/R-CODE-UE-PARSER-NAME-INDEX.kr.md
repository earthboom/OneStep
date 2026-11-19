# 역직렬화한 속성을 수용하기 전에 이름 인덱스를 검증한다

UAssetAPI 1.1.0은 잘못된 이름 맵 참조를 숫자 문자열로 반환할 수 있다. 이름 참조를 검증하고 해석되지 않은 익스포트와 해석한 속성을 구분한다.

- 식별자 · R-CODE-UE-PARSER-NAME-INDEX
- 종류 및 상태 · 오류, 해결됨. 당시 확인일 2026-11-13.
- 범위 · UAssetAPI 1.1.0으로 읽는 버전 정보가 있는 단일 파일 언쿠크드 패키지
- 검색어 · FName, name map, UAssetAPI, AssetBinaryReader.ReadFName, UAsset.GetNameReference, RawExport, serialization, uncooked package
- 발생 조건 · 라이브러리의 정상 반환만으로 직렬화된 속성 이름이 유효하다고 판단할 때
- 증상 · 패키지 이름 맵을 벗어난 참조가 숫자 형태의 속성명으로 나타났고 소비자는 해석 완료로 보고했다
- 원인 확신도 · 확인됨
- 예방 · 직렬화한 이름 인덱스와 번호를 검증하고 불투명한 데이터는 부분 결과로 보존하며 정상 대조군을 확인한다 (당시 검증됨)

## 기대와 관찰

직렬화된 이름 참조가 유효하지 않은데도 이름이 있는 속성처럼 출력됐다. 다른 속성은 정상적으로 읽혀 전체가 해석된 것처럼 보였다.

## 원인과 해결

`FName`은 언리얼의 이름 표현이다. 이 패키지 형식에서는 이름 맵 인덱스와 번호를 직렬화하고 `AssetBinaryReader.ReadFName`이 이를 읽는다. 인용한 리비전의 `UAsset.GetNameReference`는 범위를 벗어난 참조를 숫자 문자열로 바꿀 수 있다. `RawExport`가 바이트를 보존해도 개별 속성을 해석한 것으로 볼 수 없다.

## 재검증과 예방

과거 검사에서는 유효하지 않은 참조와 정상 UE4·UE5 언쿠크드 대조군을 구별하고 불투명한 출력을 부분 결과로 보고했다. 백엔드 버전을 바꿀 때 두 검사를 모두 유지한다. 쿠크드·분할 패키지와 독립적인 에디터 대조는 별도 근거가 필요하다.

## 근거

리더를 개발한 프로젝트의 검증 보고서에 소비자 쪽 검사와 검사 범위가 기록되어 있다. 아래 업스트림 자료는 라이브러리의 동작을 설명한다.

고정된 업스트림 소스에서 대체 문자열과 읽기 동작을 확인할 수 있다. 해당 소비자 회귀 검사와 정상 대조 결과는 2026-11-13에 기록됐다. [Epic, FName](https://dev.epicgames.com/documentation/unreal-engine/fname-in-unreal-engine) · [UAsset.GetNameReference](https://github.com/atenfyr/UAssetAPI/blob/73530811a9d91ffa8959a1a4cb74cc3b9c5c6bed/UAssetAPI/UAsset.cs) · [AssetBinaryReader.ReadFName](https://github.com/atenfyr/UAssetAPI/blob/73530811a9d91ffa8959a1a4cb74cc3b9c5c6bed/UAssetAPI/AssetBinaryReader.cs)
