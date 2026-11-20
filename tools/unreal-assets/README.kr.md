# 언리얼 에셋 리더

**단일 파일 uncooked·버전 정보가 있는 `.uasset` 패키지**를 읽는 오프라인 CLI입니다. UAssetAPI 1.1.0으로 패키지 구조, 선택한 직렬화 속성, 참조를 읽습니다. 에셋을 저장하거나 의존 패키지를 불러오지 않으며 실행에 언리얼 에디터가 필요하지 않습니다. 이 문서는 사람을 위한 번역본이며 AI는 영문 원본을 읽습니다.

## 빌드와 실행

.NET 8을 대상으로 빌드할 수 있는 .NET SDK와 .NET 8 런타임이 필요합니다. OneStep 루트에서 실행합니다.

```text
dotnet restore tools/unreal-assets/src --locked-mode
dotnet build tools/unreal-assets/src -c Release --no-restore
dotnet tools/unreal-assets/src/bin/Release/net8.0/OneStep.UnrealAssets.dll --help
```

접근 권한이 있는 작업 프로젝트의 파일을 전달합니다. 다음 경로는 자리표시자이며 프로젝트 연결을 저장하지 않습니다.

```text
dotnet tools/unreal-assets/src/bin/Release/net8.0/OneStep.UnrealAssets.dll <asset.uasset> --engine 5.7
dotnet tools/unreal-assets/src/bin/Release/net8.0/OneStep.UnrealAssets.dll <asset.uasset> --engine 5.7 --object <ObjectName> --properties --pretty
dotnet tools/unreal-assets/src/bin/Release/net8.0/OneStep.UnrealAssets.dll <asset.uasset> --engine 5.7 --object <ObjectName> --property ParentClass
```

공백이 있는 경로는 따옴표로 감쌉니다. `--engine`은 `4.27`, `5.7`, `5.8` 같은 라이브러리 버전을 받습니다. 호환성을 보증하는 옵션은 아닙니다. 생략하면 패키지의 버전을 사용합니다. 알 수 없는 값과 버전 정보가 없는 패키지는 거부합니다.

기본 조회는 export 본문을 읽지 않고 구조 테이블만 읽습니다. `--properties`는 선택한 export를 해석하며 `--object`가 없으면 전체를 읽습니다. `--object`에는 정확한 이름이나 구조 결과의 외부 객체 포함 경로(예: `TestActorBP.EventGraph`)를 넣습니다. 이름이 중복되면 실패합니다. `--property`는 속성 읽기를 포함하며 **최상위 속성 이름**으로 결과를 거릅니다. 중첩 필드나 테이블 행 필터가 아니며 해당 export 전체 해석은 필요합니다.

표준 출력에 JSON 하나를 씁니다. 필요하면 사용하는 프로젝트에 보고서를 저장합니다. 셸 리다이렉션 대상은 원본 에셋과 달라야 합니다. 셸은 프로그램의 보호가 시작되기 전에 출력 파일을 열기 때문입니다. CLI에는 출력 파일 지정·에셋 쓰기 명령이 없습니다.

## 보고서 해석

| 필드 | 의미 |
| --- | --- |
| `status`, 종료 코드 | `complete`/0: 요청 범위 완료, `partial`/1: 불투명·미지원 데이터 존재, `error`/2: 잘못되거나 미지원 또는 실패한 요청. |
| `input` | 입력 스냅샷의 파일명·크기·SHA-256. 기기 경로는 저장하지 않습니다. |
| `package` | 저장 엔진·선택 버전·객체 버전·플래그·import/export 개수. |
| `objects` | 패키지 내부 인덱스·외부 객체 포함 경로·클래스·바이트 영역·속성 상태. |
| `properties` | 중첩 컬렉션·배열 인덱스를 포함한 타입 보존 JSON. 요청했을 때만 있습니다. |
| `rows` | 필터 없이 속성을 요청하고 백엔드가 해석한 DataTable 행. |
| `references` | 객체 인덱스·인터페이스·델리게이트·소프트 경로 참조와 소유 속성·행 위치. 인덱스 0은 null이며 외부 파일을 따라가지 않습니다. |
| `imports`, `soft_package_references` | 패키지 목록이며 실제 사용·파일 존재의 증거가 아닙니다. |
| `analysis` | 클래스로 결정한 종류와 살펴볼 속성 제안. 제안한 속성의 실제 존재를 보증하지 않습니다. |
| `opaque_bytes`, `limitations` | AI의 판단에 함께 전달해야 할 미해석 데이터와 한계. |
| `inspection_elapsed_ms` | 프로세스 시작·JSON 출력 시간을 뺀 로컬 읽기·투영 시간. 일반 성능 수치가 아닙니다. |

`not_requested`는 빈 속성의 해석 완료와 다릅니다. `complete`는 게임 동작·상속 기본값·전체 의존성·모든 네이티브 필드의 해석을 증명하지 않습니다. 잘못된 이름 인덱스를 숫자 문자열로 받아들이지 않습니다. export 읽기·이동은 선언된 바이트 경계를 지킵니다. 미지원 속성·raw export·후행 네이티브 데이터를 빈 성공으로 바꾸지 않습니다.

## 작은 확장 구조

```text
src/Cli.cs            인자와 실패 계약
src/AssetReader.cs    읽기 전용 스냅샷·패키지 제한·선택 읽기·인덱스 해석
src/Analysis.cs       타입 투영·참조·DataTable 행·분류 규칙
src/ReadOnlyTextPropertyData.cs  버전 조건이 있는 FText 편집 데이터 확장
src/Program.cs        JSON 출력과 프로세스 종료 경계
```

공통 백엔드가 바이너리를 읽습니다. 분류는 스크립트 패키지를 포함한 **루트 export 클래스 경로**를 사용하며 위젯→몽타주→애니메이션→데이터→블루프린트 순서로 선택하고 나머지는 generic입니다. 파일명이나 단순 import로 추측하지 않습니다. 알려진 루트 export가 없는 사용자 하위 클래스는 generic이며 외부 상속을 조사하지 않습니다.

현재 다섯 종류는 구조·속성 추출을 공유합니다. 확장이 필요하면 실제 객체·속성 근거로 판단하는 작은 분석기를 `Analysis.cs`에 추가합니다. 독립적으로 커졌을 때만 파일을 나누고 속성 위치·partial 상태·실제 fixture 검증을 유지합니다. 확인된 미지원 형식이 있을 때만 백엔드를 추가합니다.

## 범위와 검사

- 입력 최대 256 MiB. 전달한 little-endian `.uasset` 하나만 읽습니다. 읽기 전용 스트림으로 복사하고 라이브러리에는 경로 없는 메모리 스트림을 전달하며 의존성 로딩을 끕니다.
- cooked·에디터 데이터 제거·unversioned·분리 export·IoStore는 미지원입니다. 인접 `.uexp`·`.ubulk`는 읽지 않습니다. 태그 속성을 읽어도 bulk·네이티브 데이터는 불투명할 수 있습니다.
- 바이트코드 실행·그래프 제어 흐름·애니메이션 트랙 압축 해제·위젯 렌더링·상속 최종값·런타임 동작은 범위 밖입니다. DataTable 행 외 전문 네이티브 필드는 결과에 투영하지 않습니다.
- 파일 크기와 구조 검사는 외부 파서를 악성 파일용 보안 샌드박스로 만들지 않습니다. 권한이 있는 알려진 개발 에셋을 사용합니다.

CLI 검사 재현:

```text
python tools/unreal-assets/tests/fetch_fixtures.py
dotnet restore tools/unreal-assets/tests/writer
dotnet build tools/unreal-assets/tests/writer -c Release --no-restore
python -B -m unittest discover -s tools/unreal-assets/tests -v
```

다운로더는 고정된 공개 주소만 사용하고 SHA-256을 확인한 뒤 로컬 제외 파일을 저장합니다. fixture·빌드 결과가 없으면 명확하게 실패하며 테스트 탐색 중 네트워크를 사용하지 않습니다. writer는 **테스트 전용**이고 임시 디렉터리에 파생 파일을 저장하며 CLI에는 포함되지 않습니다. 실제 공개 UE4.27·UE5.7 에셋은 블루프린트 검증에, 합성 사례는 분류·회귀 검증에 사용합니다.

별도 [엔진 fixture 절차](tests/engine/README.kr.md)는 실제 UE5.8 애니메이션·몽타주·위젯·PrimaryAssetLabel·DataTable을 만듭니다. 새로운 에디터 프로세스가 저장 없이 다시 열어 기준값을 제공합니다. CLI는 비기본 속성·중첩 참조·해시 보존 등 31개 비교를 통과했습니다. 모든 에셋·엔진·네이티브 데이터의 호환성을 보증하지 않습니다. 원시 애니메이션 구조체는 미지원이고 ImportData 접두부·후행 데이터는 불투명합니다. 작은 FText 확장은 실제 FortniteMain 커스텀 버전에 따라 UAssetAPI 1.1.0이 누락한 Base 이력의 편집용 개발 메모를 읽습니다. 중첩 텍스트 이력은 기존 라이브러리 지원에 의존합니다. 실행 결과와 한계는 [검증 문서](verification.kr.md)에 있습니다.

## 의존성과 출처

- [UAssetAPI](https://github.com/atenfyr/UAssetAPI): NuGet 1.1.0, 소스 커밋 `73530811a9d91ffa8959a1a4cb74cc3b9c5c6bed`, MIT. `src/packages.lock.json`으로 하위 의존성도 고정합니다. 하위 패키지의 라이선스는 각각 유지됩니다. [상위 라이선스](UAssetAPI.LICENSE.txt)를 보존합니다.
- 공개 fixture 파일·주소·해시: [manifest](tests/fixtures.json), 상위 리비전 `05910ba8f6d278201120e10d87adbb06dfb3a097`. 원본 바이너리는 재배포하지 않고 필요할 때 받습니다.
- [설계](../../docs/designs/uncooked-asset-reader.kr.md), [구현 계획](../../docs/superpowers/plans/2026-11-13-uncooked-assets.kr.md).
