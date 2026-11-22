# 게임 데이터 형식과 콘텐츠 제작 파이프라인

2026-11-22 · JSON, 엔진 에셋, 시트와 CSV, 바이너리, 데이터베이스 선택 기준

**JSON은 여러 편집기에서 읽고 쓸 수 있는 구조화된 콘텐츠와 교환 파일에 적합하다.** 여러 도구에서 편집하는 퍼즐 보드, 스테이지 목록, 조우 정의가 좋은 후보다. 특정 엔진에서 공간과 에셋 참조를 함께 편집하는 스테이지는 Unity 씬·에셋 또는 Unreal 맵·Data Asset을 저작 원본으로 삼을 수 있다. 저장, 서버 상태, 배포용 데이터는 각각의 읽기·쓰기 조건에 맞춰 결정한다. [JSON 표준](https://www.rfc-editor.org/rfc/rfc8259.html) · [LDtk의 JSON 구조](https://ldtk.io/docs/game-dev/json-overview/) · [Unity ScriptableObject](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/scriptableobject) · [Unreal Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine)

기존 [스테이지 프레임워크 조사](2026-11-22-stage-content-framework.md)와 [게임 개발 실무 연구](2026-11-22-game-development-practices.md)를 이어, 어떤 데이터를 어디에 두고 어떻게 추가·수정·삭제할지 정리한다. 아래 선택은 설계 기준이다. 성능이나 배포 호환성은 실제 프로젝트와 대상 플랫폼에서 확인해야 한다.

## 1. 형식보다 먼저 정할 데이터의 역할

| 데이터 | 누가 쓰고 언제 쓰는가 | 출발점 |
| --- | --- | --- |
| **콘텐츠 저작 원본** | 디자이너가 스테이지, 웨이브, 아이템, 대사를 편집한다. 변경 이력과 검토가 필요하다. | 파일 간 교환이 필요한 구조는 JSON, 열 중심 대량 편집은 CSV·시트, 씬과 오브젝트 참조 중심은 엔진 에셋 |
| **가져오기·배포 산출물** | 가져오기 도구나 빌드가 원본을 읽고 카탈로그, 에셋, 번들·패키지를 만든다. | 원본으로부터 재생성되는 타입이 있는 에셋과 엔진 패키지. 별도 바이너리는 측정에서 필요성이 확인될 때 |
| **플레이 중 상태** | 퍼즐 세션, 시뮬레이션, 서버 등 상태 소유자가 입력에 따라 바꾼다. | 게임 규칙에 맞는 메모리 자료구조. 필요한 시점에 지속 상태만 추출 |
| **로컬 저장과 리플레이** | 저장 모듈이 진행에 따라 쓴다. 이전 버전, 쓰기 중단과 복구를 다룬다. | 작은 프로필은 버전이 있는 저장 파일이나 엔진 저장 API. 많은 객체의 반복 부분 갱신·조회가 필요하면 SQLite도 비교 |
| **온라인 상태와 운영 설정** | 권한이 있는 서버가 계정, 소유권, 재화 등을 변경한다. 운영자는 카탈로그 공개 범위나 설정 스냅샷을 발행한다. | 동시 쓰기·제약·감사가 필요한 상태는 서버 DB. 읽기 중심 콘텐츠 설정은 버전이 있는 문서와 배포 목록도 가능 |

**같은 사실은 한 곳에서 편집한다.** 예를 들어 보드가 LDtk 프로젝트에 있으면 내보낸 JSON과 엔진에서 만든 에셋은 그 입력에서 다시 얻는 산출물이다. `StageId`와 챕터 순서를 별도로 관리할 수 있지만, 같은 순서를 시트·JSON·엔진 에셋에서 동시에 손으로 유지하면 어떤 수정이 반영될지 모호해진다. [LDtk 내보내기와 로딩](https://ldtk.io/docs/game-dev/loading/) · [Build Systems à la Carte](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf)

## 2. 형식별 선택과 바꿀 조건

| 선택 | 잘 맞는 작업 | 비용과 적용 조건 |
| --- | --- | --- |
| **JSON** | 계층이 있는 보드·퀘스트·웨이브, 외부 도구와 교환, 스테이지별 변경 검토 | 표준에는 주석이 없다. 타입과 관계 검증이 별도로 필요하다. 사람이 줄 단위로 편집한다면 포매터와 파일 분할 기준을 둔다. [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html) · [JSON Schema 검증 표준](https://json-schema.org/draft/2020-12/json-schema-validation) |
| **CSV·시트** | 아이템 수치, 적 능력치, 아이템별 지역화 키처럼 같은 열을 여러 행에서 비교하는 작업 | 인코딩·인용부호·헤더·빈 셀 정책을 정한다. 숫자로 보이는 문자열 ID, 날짜 자동 변환, 행 순서에 숨은 의미를 검증한다. 계산식이 있는 시트는 배포 입력이 되는 계산 결과와 내보내기 시점을 관리한다. [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180.html) · [W3C 표 형식 데이터 모델](https://www.w3.org/TR/tabular-data-model/) |
| **YAML·TOML·JSON5·XML** | YAML·JSON5는 주석이 필요한 사람 편집, TOML은 비교적 단순한 설정, XML은 기존 XML 도구 체인과의 교환 | YAML 파서의 버전·스칼라 해석과 JSON5 파서 지원을 맞춘다. 툴이 많으면 지원되는 형식이나 변환 비용부터 확인한다. Unity가 저장한 YAML은 Unity의 에셋 표현으로 취급한다. [YAML 1.2.2](https://yaml.org/spec/1.2.2/) · [TOML](https://toml.io/en/v1.0.0) · [JSON5](https://spec.json5.org/) · [W3C XML](https://www.w3.org/TR/xml/) |
| **Unity·Unreal 에셋** | 씬, 지형, 충돌, 라이팅, 프리팹·Blueprint, 드래그 앤 드롭 참조, 에디터 내부 검증 | 도구와 에셋 참조가 엔진에 묶인다. 자주 동시 수정하는 에셋은 작게 나누고, 병합이 어려운 파일은 소유·체크아웃 절차를 정한다. [Unity 에셋 메타데이터](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html) · [Unreal Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine) · [Unreal Perforce 안내](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine) |
| **Protobuf·FlatBuffers·MessagePack** | 배포 압축 크기, 파싱, 불필요한 복사, 네트워크 전송이 비용이 되는 경우 | 사람이 차이를 검토하기는 어렵다. 스키마와 필드 진화 규칙은 형식마다 다르다. 실제 스테이지 묶음에서 압축 후 용량과 디코딩·객체 초기화 비용까지 비교한다. [Protobuf 진화 규칙](https://protobuf.dev/best-practices/dos-donts/) · [FlatBuffers 스키마 진화](https://flatbuffers.dev/evolution/) · [MessagePack](https://msgpack.org/) · [바이너리 형식 비교 연구](https://arxiv.org/abs/2201.03051) |
| **SQLite** | 로컬에서 대량 레코드를 부분 조회·갱신하거나 여러 변경을 하나의 트랜잭션으로 묶는 작업 | 한 DB 파일에서 동시에 쓰는 주체는 한 번에 하나다. 바이너리 DB를 여러 디자이너의 Git 저작 원본으로 쓰면 변경 검토와 병합이 어렵다. 필요하면 검토 가능한 파일에서 DB를 생성하는 배포 방식을 쓸 수 있다. [SQLite 선택 기준](https://www.sqlite.org/whentouse.html) · [애플리케이션 파일 형식](https://www.sqlite.org/appfileformat.html) · [SQLite 원자 커밋](https://www.sqlite.org/atomiccommit.html) |
| **서버 관계형 DB와 JSON 컬럼** | 계정·재화·인벤토리처럼 동시 갱신, 관계 제약, 중복 방지와 트랜잭션이 필요한 경우. 설정처럼 형태가 달라지는 부가 정보는 JSON 컬럼에도 저장 가능 | 자주 조회하거나 제약이 필요한 값은 컬럼과 관계를 고려한다. 큰 JSON 문서를 한 행으로 쓰면 부분 갱신에도 행 단위 경합이 생길 수 있다. [PostgreSQL 트랜잭션](https://www.postgresql.org/docs/current/tutorial-transactions.html) · [JSON과 JSONB](https://www.postgresql.org/docs/current/datatype-json.html) |
| **스크립트로 조립하는 정의** | 모드가 기존 정의를 읽고 확장하거나 여러 정의를 계산해 생성하는 등 저작 단계에 동작이 필요한 경우 | 실행 순서와 호출 가능한 기능, 오류 전파, 결과 검증을 계약에 포함한다. Factorio는 프로토타입을 만드는 데이터 단계와 실제 게임 런타임을 구분한다. [Factorio 데이터 수명주기](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) |

유사한 자료량이라도 작업은 다르다. 디자이너가 200개 아이템의 가격을 가로로 보며 수정한다면 시트가 편하다. 각 스테이지에 여러 웨이브와 조건이 달리는 상황에는 스테이지별 구조화 파일이 명확하다. 매 입력마다 바뀌는 보드 상태나 몬스터 상태는 메모리에 두고, 로딩과 저장이 필요한 경계에서 선택한 형식으로 변환한다.

## 3. 스테이지를 JSON으로 저작할 때의 계약

다음은 기존 밀기 규칙을 사용하는 퍼즐 한 판의 저작 예시다. 좌표 원점과 경계, 타일의 정수 좌표 해석은 해당 보드 규칙에서 정의한다고 가정한다.

```json
{
  "schemaVersion": 1,
  "stageId": "warehouse-03",
  "rulesId": "puzzle.push-box",
  "board": {
    "width": 5,
    "height": 4,
    "spawn": [1, 1],
    "walls": [[0, 0]],
    "boxes": [[2, 1]],
    "goals": [[3, 1]]
  }
}
```

- **ID와 참조.** 파일 이름, 시트 행 번호, 엔진 오브젝트 이름과 `stageId`의 수명을 독립적으로 둔다. 그래야 재배치·이름 변경 뒤에도 저장을 찾을 수 있다. 엔진 간에 데이터를 공유한다면 `rulesId`와 필요한 에셋의 게임 ID를 각 엔진이 자기 규칙과 에셋에 연결한다. 3D 좌표까지 공유할 때는 축, 단위, 회전 표현을 데이터 계약에 정한다. [Unity 내부 에셋 ID](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html) · [Unreal Asset Manager](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine)
- **파싱 규칙.** UTF-8, 고정 키 이름, 중복 키 거부를 프로젝트 규칙으로 정한다. 키 순서에 게임 의미를 주지 않고, 순서가 중요한 웨이브·체크포인트는 배열로 표현한다. 도구 사이 숫자 범위를 정하고, JavaScript 도구를 거치는 큰 정수 ID는 문자열로 두면 변환 과정에서 값이 바뀌는 일을 피할 수 있다. [RFC 8259의 객체와 수 표현](https://www.rfc-editor.org/rfc/rfc8259.html) · [I-JSON 메시지 형식](https://www.rfc-editor.org/rfc/rfc7493.html)
- **구조 검사와 게임 검사.** JSON Schema로 필수 필드, 타입, 허용 범위를 검사한다. 보드 안 좌표, 금지된 기물 겹침, 규칙 ID와 에셋의 존재, 다른 스테이지와의 ID 중복은 게임 쪽에서 확인한다. 풀이 입력을 실제 규칙으로 재생하면 구조가 올바른 보드가 목표를 달성하는지도 확인할 수 있다. 중복 JSON 키는 스키마에 도달하기 전에 파서에서 잡아야 이미 덮어쓴 값을 놓치지 않는다. [JSON Schema 검증 표준](https://json-schema.org/draft/2020-12/json-schema-validation) · [스테이지 검증 설계](2026-11-22-stage-content-framework.md#6-자동-검증과-제작-검토)
- **실패 정책.** 작업 중에는 스테이지 ID·원본 파일·필드 경로와 고칠 조건을 알려준다. 출시 빌드에서는 필수 참조나 형식의 오류를 보고하고 해당 발행을 중단한다. 제작 중 알 수 없는 필드를 검사하면 오타를 잡을 수 있으므로 엄격하게 시작한다. 이전 Player가 읽을 수 있는 운영 데이터에 새 필드를 추가해야 할 경우에는 무시해도 안전한 필드와 지원 버전 조건을 계약에 명시한다. [JSON Schema의 객체 제약](https://json-schema.org/understanding-json-schema/reference/object) · [JSON 스키마 호환성 논문](https://software-lab.org/publications/issta2021_JSON.pdf) · [개발 중 불완전한 데이터 처리 GDC 발표](https://media.gdcvault.com/gdc2013/slides/822192Fredriksson_Andreas_Loading_Imperfect_Data.pdf)
- **협업 단위.** 대개 한 사람이 편집하는 스테이지를 파일 한 개로 두고, 재사용하는 규칙·프리셋은 자신의 ID로 참조한다. 시트나 레벨 편집기의 내보내기 결과를 버전 관리한다면 정렬·포맷을 고정해 의미 있는 차이가 남게 한다. 파일의 내용이 서명 또는 배포 식별자에 쓰이는 경우에만 바이트 단위 정규화 계약을 도입한다. [Tiled JSON 형식](https://doc.mapeditor.org/en/stable/reference/json-map-format/) · [LDtk JSON 구조](https://ldtk.io/docs/game-dev/json-overview/) · [JSON 정규화 표준](https://www.rfc-editor.org/rfc/rfc8785.html)

## 4. Unity와 Unreal에서 저작·가져오기 경로 선택

| 상황 | Unity | Unreal Engine |
| --- | --- | --- |
| **에디터가 원본인 경우** | 규칙 설정과 콘텐츠 정의는 `ScriptableObject`, 맵과 배치는 Scene·Prefab으로 편집한다. 에셋과 `.meta`를 함께 관리한다. [ScriptableObject](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/scriptableobject) · [에셋 메타데이터](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html) | 규칙과 콘텐츠 정의는 `UDataAsset`, 맵과 배치는 Map·Blueprint로 편집한다. 검색·로딩·쿠킹을 별도로 관리할 요구가 있으면 `UPrimaryDataAsset`과 Asset Manager를 검토한다. [Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine) · [Asset Manager](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine) |
| **외부 보드·조우 구조가 원본인 경우** | JSON은 `TextAsset`으로 읽을 수 있다. 별도 가져오기 단계에서 검사하고 타입이 있는 에셋을 만들거나, 런타임에서 읽어야 하는 제품 요건이 있으면 정해진 로드 시점에 파싱한다. `ScriptedImporter`는 Unity 기본 가져오기가 처리하는 확장자에 등록할 수 없으므로 필요하면 전용 확장자 또는 명시적 가져오기 도구를 사용한다. [Text assets](https://docs.unity3d.com/6000.0/Documentation/Manual/class-TextAsset.html) · [ScriptedImporter](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AssetImporters.ScriptedImporter.html) | 동일한 행 스키마의 밸런스 데이터는 `FTableRowBase` 계열과 Data Table의 CSV·JSON 경로를 활용한다. 퍼즐 보드·조우 트리처럼 고유한 구조가 있으면 에디터에서 정의 에셋으로 변환하거나 해당 데이터 계약을 읽는 로드를 따로 설계한다. [Data Driven Gameplay Elements](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine) · [UDataTable JSON 가져오기](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UDataTable?application_version=5.8) |
| **정의가 게임에 도달하는지 확인** | `JsonUtility`는 Unity 직렬화 규칙을 따르며 `Dictionary`나 루트 배열을 그대로 처리하는 용도에는 맞지 않는다. 대상 데이터 구조와 Player에서 지원되는 라이브러리를 고른다. Addressables 데이터 갱신이 필요하면 해당 Player의 콘텐츠 상태와 빌드 경로를 보존한다. [Unity JSON 직렬화](https://docs.unity3d.com/6000.0/Documentation/Manual/json-serialization.html) · [Addressables 콘텐츠 업데이트](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/content-update-builds-overview.html) | Data Validation으로 에셋·참조 검사와 CI 검증을 구성할 수 있다. 출시 카탈로그의 맵과 참조가 실제 cook·패키지에서 해석되는지 확인한다. [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Cooking](https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-in-unreal-engine) |

위 JSON 예시의 `walls`와 `boxes`는 중첩 배열이므로 Unity 기본 직렬화 형식에 그대로 대응하지 않는다. 공통 교환 형식을 유지해야 한다면 가져오기에서 좌표를 파싱해 Unity의 좌표 구조 목록으로 변환할 수 있다. 교환 형식도 함께 설계할 수 있다면 각 좌표를 `{ "x": 2, "y": 1 }`처럼 이름 있는 필드로 정하는 선택지가 있다. Unity와 Unreal은 가져온 규칙 ID에서 실제 엔진 에셋과 표시를 각각 연결한다. [Unity 직렬화 규칙](https://docs.unity3d.com/6000.0/Documentation/Manual/script-serialization-rules.html)

## 5. 추가·변경·삭제와 이전 저장

| 변경 | 데이터 운영 규칙 | 확인할 기존 입력 |
| --- | --- | --- |
| **추가** | 새 콘텐츠 ID를 발급하고 정의·참조를 검증한다. 카탈로그에 넣고 해금 조건을 정한다. 스키마 필드를 추가하면 새 리더가 예전 데이터의 누락을 어떻게 다룰지 정의한다. | 이전 저장에서 새 해금 조건이 어떻게 적용되는지, 새 빌드에서 해당 스테이지를 열 수 있는지 |
| **수정** | 표시 이름·경로·순서 변경은 같은 ID에서 처리한다. 클리어 기준이나 배치가 달라지는 수정은 기록·리플레이·중간 재개에 미치는 영향을 검토한다. | 이전 완료 이력, 같은 ID의 예전 고스트와 중간 저장, 다른 스테이지의 공용 부품 참조 |
| **삭제·교체** | 기존 저장이 참조하는 ID의 의미를 정한다. 가령 완료 이력은 숨기거나 유지하고, 교체할 필요가 있으면 ID 이전 규칙을 둔다. 호환 기간이 남은 ID는 새 개체에 재사용하지 않는다. | 폐기 스테이지의 완료·재개 기록, 그 ID를 가리키는 해금 조건, 이전 오프라인 데이터 |
| **출시 후 교체** | 독립 갱신이 필요하면 검증된 버전의 카탈로그와 산출물을 함께 발행한다. 호환되는 묶음이 준비된 시점에 전환하고 진행 중 세션이 사용하는 버전을 확정한다. 다운로드 실패에서 이전 호환 묶음으로 계속할 조건도 정한다. | 이전 Player가 새 카탈로그를 받는 경우, 일부 다운로드에 실패하는 경우, 플레이 도중 새 버전이 발행되는 경우 |

`schemaVersion`은 읽기 형식이 바뀌었는지 판단하는 데 쓴다. `contentRevision`이나 콘텐츠 해시는 같은 형식에서 배치·판정이 바뀌어 재개와 기록 비교에 영향을 줄 때 관리한다. 카탈로그 발행 버전은 독립 배포가 필요한 경우에 추가한다. 읽기 호환성을 단계별로 정하고, 이전 저장을 보존한 상태에서 변환 결과가 다시 읽히는지 확인한 뒤 교체한다. 엔진 저장 API를 쓰는 경우에도 장치의 배터리 종료·디스크 부족·복구 조건은 타깃 플랫폼에서 확인할 항목이다. [Factorio 마이그레이션](https://lua-api.factorio.com/latest/auxiliary/migrations.html) · [Mojang DataFixerUpper](https://github.com/Mojang/DataFixerUpper) · [Unreal SaveGame](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine) · [OneStep 저장 설계와 기존 검증](../../knowledge/game/K-GAME-TECH-SAVE.md)

패치·DLC·모드가 같은 정의에 손댈 수 있는 제품은 로드 우선순위와 충돌의 의미를 정한다. 중복 ID를 오류로 볼지 명시적 교체로 볼지, 리스트가 통째로 바뀌는지 ID별로 병합되는지, `null`이 값인지 삭제인지 각각 결정한다. 표준 JSON Merge Patch는 객체의 `null`을 삭제로 처리하고 배열은 전체 교체할 수 있으므로, 기물·웨이브를 부분 변경하려는 게임에는 그 의미가 맞는지 확인한다. [JSON Merge Patch](https://www.rfc-editor.org/rfc/rfc7396.html) · [Factorio 모드 데이터 단계](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html)

## 6. 제작 사례와 연구에서 가져올 기준

| 자료 | 이 결정에 적용할 내용 |
| --- | --- |
| **Witch Beam, Unpacking, GCAP 2023** | 물건·구역을 다루는 Unity 편집 도구와 시트 가져오기를 함께 사용했다. 공간 배치와 반복 입력처럼 작업의 모양이 다를 때 저작 도구도 달라질 수 있다. [개발팀 발표 영상](https://youtu.be/2j7AJj1oRSQ) · [발표 구간](https://confpad.io/conferences/gcap-2023-empower/empowering-design-the-tools-and-pipelines-of-unpacking) |
| **Brandon Moro, Destiny 2, GDC 2018** | 에셋의 의존성과 캐시 단위가 빌드 결과와 제작 반복 시간에 어떤 영향을 주는지 설명한다. 한 원본 변경에서 실제 재생성해야 할 에셋을 추적할 근거다. [GDC 영상](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [슬라이드](https://media.gdcvault.com/gdc2018/presentations/Moro_Brandon_Bungies_Asset_Pipeline.pdf) |
| **David Santiago 외, Marvel’s Spider-Man, SIGGRAPH 2019** | 아티스트가 제어하는 입력 위에 절차적 처리를 적용해 도시 콘텐츠를 제작했다. 공간 제작에서 편집 가능한 원본과 생성물을 어디에 둘지 판단할 사례다. [개발팀 논문](https://history.siggraph.org/wp-content/uploads/2022/09/2019-Talks-Santiago_Procedural-System-Assisted-Authoring.pdf) · [GDC 영상](https://www.gdcvault.com/play/1025765/Level-Design-in-a-Moment) |
| **Mokhov·Mitchell·Peyton Jones, ICFP 2018** | 빌드 작업의 실행 순서와 재빌드 판단을 구분한다. 콘텐츠 파이프라인에서는 원본·가져오기 규칙·의존 에셋·타깃을 바꿨을 때 무엇을 다시 생성하는지에 적용할 수 있다. [Build Systems à la Carte](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf) |
| **Habib 외, ISSTA 2021** | 두 JSON 스키마의 허용 범위 차이로 실제 데이터 호환성 문제를 찾았다. 새 명세가 예전 데이터를 읽을 수 있는지 검사할 근거다. ID 의미, 파생 데이터와 게임 판정 호환은 별도의 기존 입력 예제로 확인해야 한다. [논문](https://software-lab.org/publications/issta2021_JSON.pdf) |
| **Viotti·Kinderkhedia, 바이너리 직렬화 비교 연구** | 입력 크기와 구조, 압축 여부에 따라 비교 결과가 달라진다. 숫자가 반복되는 보드와 긴 문자열이 많은 설정을 함께 평가하고, 연구의 크기 비교를 특정 엔진에서의 로드 시간으로 해석하지 않는다. [논문](https://arxiv.org/abs/2201.03051) |

## 7. 프로젝트에서 처음 기록할 결정

1. **대표 콘텐츠를 고른다.** 격자 퍼즐, 별도 공간을 쓰는 코스, 열 중심 밸런스 표 중 해당 프로젝트에 있는 것을 고른다. 유형마다 한 사람이 어디서 수정하고 다른 사람이 어떤 차이를 검토하는지 정한다.
2. **소유권과 추가 경로를 기록한다.** 각 데이터의 저작 원본과 지속 ID, 가져오기·검증·등록, 런타임 읽기, 저장 버전과 삭제 정책을 문서에 적는다. `vegabond-code-design`에는 각 결정에서 사용할 기존 설계 항목이 있고, `vegabond-code`의 검증 지침은 실제 진입 경로를 요구한다. [콘텐츠 확장 경로](../../skills/vegabond-code-design/references/gameplay-framework.md#give-content-an-extension-path) · [검증 지침](../../skills/vegabond-code/references/verification.md)
3. **바꿀 이유를 측정한다.** JSON에서 바이너리나 DB로 바꾸기 전 대표 콘텐츠의 디스크 용량, 압축 후 배포 크기, 콜드·웜 로드에서 I/O·파싱·참조 해석·객체 초기화, 메모리 최고치를 나눠 본다. 로컬 저장이라면 쓰기 지연, 부분 갱신 비용과 실패 후 복구를 본다. 제작 기준은 새 스테이지를 추가하는 시간, 공용 코드 수정 수와 리뷰·병합 비용이다. [바이너리 형식 비교 연구](https://arxiv.org/abs/2201.03051) · [Bungie 에셋 파이프라인 사례](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s)
