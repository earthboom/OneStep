# 작성자·접근 방식·호환성에 맞춰 게임 데이터 형식 선택하기

K-GAME-CONTENT-FORMATS · 방법 · 적용 중 · 근거 확인 2026-11-22

각 데이터의 편집 원본을 한 곳에 두고 배포 형식으로 검증·변환한다. 영속 ID와 구조·콘텐츠·배포 버전을 구분한다.

적용 범위 — Unity·Unreal 및 외부 도구에서 편집하는 콘텐츠, 실행 상태, 로컬 세이브, 라이브 카탈로그.

## 적용 방법

먼저 누가 어떤 방식으로 읽고 쓰는지 정한다. 기획자는 정의를 편집하고 빌드는 배포물을 만들며 러너는 세션 상태를 갱신하고 세이브 시스템은 진행을 저장한다. 온라인 거래는 권한 있는 서비스가 확정한다. 계층형 교환에는 JSON, 행 비교에는 시트·CSV, 단순 설정에는 TOML 같은 텍스트, 배치·참조 미리보기에는 엔진 에셋을 고려한다. 이진 형식은 파싱·전송 비용을 줄일 수 있고 SQLite는 인덱스 조회와 트랜잭션에 적합하다. 동시 지급·거래는 서버 제약과 트랜잭션이 중요하다. 생성물은 원본을 추적할 수 있게 하고 직접 편집하지 않는다.

퍼즐에는 schemaVersion, stageId, rulesId, 크기, 시작점, 벽, 상자, 목표와 좌표 원점·단위·범위를 정의한다. 중복 JSON 키는 스키마 검사 전에 파서에서 거부한다. UTF-8, 키 이름, 숫자 범위, 배열 순서를 합의한다. 중간 도구의 정수 정밀도를 넘는 ID는 문자열로 전달한다. 타입과 구조를 확인한 뒤 참조, ID 누락·중복, 겹침, 실제 입력으로 풀 수 있는지 검사한다. 오류에는 원본·스테이지 ID·필드 경로·수정 조건을 담는다. 이전 리더가 무시해도 될 새 필드는 명시한다.

Unity에서는 TextAsset이나 임포터로 직렬화가 가능한 형태로 변환한다. JsonUtility로 중첩 좌표 배열을 다루려면 변환하거나 호환 파서를 쓴다. Unreal에서는 일정한 행 구조에 Data Table, 계층형 정의에 에셋이나 전용 임포터를 검토한다. 엔진 고유의 에셋 키는 경계에서 해석하고 실제 배포 카탈로그로 진입한다. 원본·도구·설정 변경이 증분 빌드에서도 산출물을 무효화해야 한다.

## 적용 조건과 예외

이름·경로·순서가 바뀌어도 ID를 유지한다. schemaVersion은 읽기 호환성, contentRevision은 배치·고스트·중간 저장 유효성, 카탈로그 버전은 배포 단위를 구별한다. ID를 폐기할 때 기록 보존·삭제 표시·대체·이관 중 정책을 정하고 해금 조건도 살핀다. 진행 중 세션은 완전한 호환 릴리스에 고정하고 다운로드 실패 시 이전 세트를 유지한다. 새 카탈로그로 변환한 저장 데이터는 배포를 되돌린 뒤에도 남는다. 팩 충돌은 로드 순서, 통째 교체, ID별 병합, null 의미를 정의한다. JSON Merge Patch는 null로 키를 지우고 배열 전체를 바꿀 수 있다.

## 확인 방법

스테이지를 추가하고 이름·순서를 바꾸고 ID를 폐기한 뒤 실제 지원 대상의 이전 저장 파일을 읽고 다시 저장한다. 중복 키, 누락 에셋, 미지원 규칙, 부분 다운로드, 이전 카탈로그와 구버전 Player를 검사한다. 클린·증분 임포트 결과를 비교한다. 형식 교체 전 압축 크기, 최초·반복 I/O, 파싱, 참조 연결, 초기화, 최대 메모리, 쓰기 지연, 복구, 편집·검토 비용을 구분해 측정한다.

## 근거

11월 22일 포맷·파이프라인 조사와 게임 개발 조사 중 데이터 수명 절은 형식 명세, 엔진 계약, 스키마 호환성·빌드 시스템 연구, 제작 사례를 근거로 삼았다. 다른 팀의 측정값은 페이로드와 압축, 작업량에 따라 달라진다. 여기의 검사는 대상 프로젝트에서 수행할 제안이다.

[세이브 복구와 이관](K-GAME-TECH-SAVE.md) · [콘텐츠 제작 절차](K-GAME-CONTENT-PRODUCTION.md) · [스테이지 소유권](K-GAME-STAGE-AUTHORING.md)

- [LDtk export and loading](https://ldtk.io/docs/game-dev/loading/) · [Build Systems à la Carte](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf)
- [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.html) · [JSON Schema validation standard](https://json-schema.org/draft/2020-12/json-schema-validation) · [RFC 4180](https://www.rfc-editor.org/rfc/rfc4180.html) · [W3C tabular data model](https://www.w3.org/TR/tabular-data-model/) · [YAML 1.2.2](https://yaml.org/spec/1.2.2/)
- [TOML](https://toml.io/en/v1.0.0) · [JSON5](https://spec.json5.org/) · [W3C XML](https://www.w3.org/TR/xml/) · [Unity asset metadata](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html) · [Unreal Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine)
- [Unreal Perforce guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine) · [Protobuf evolution practices](https://protobuf.dev/best-practices/dos-donts/) · [FlatBuffers schema evolution](https://flatbuffers.dev/evolution/) · [MessagePack](https://msgpack.org/) · [Binary format comparison study](https://arxiv.org/abs/2201.03051)
- [When to use SQLite](https://www.sqlite.org/whentouse.html) · [Application file format](https://www.sqlite.org/appfileformat.html) · [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html) · [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html) · [JSON and JSONB](https://www.postgresql.org/docs/current/datatype-json.html)
- [Factorio data lifecycle](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html)
- [Unreal Asset Manager](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine) · [I-JSON message format](https://www.rfc-editor.org/rfc/rfc7493.html) · [JSON Schema object constraints](https://json-schema.org/understanding-json-schema/reference/object) · [Paper on JSON schema compatibility](https://software-lab.org/publications/issta2021_JSON.pdf) · [GDC talk on loading imperfect data during development](https://media.gdcvault.com/gdc2013/slides/822192Fredriksson_Andreas_Loading_Imperfect_Data.pdf)
- [Tiled JSON format](https://doc.mapeditor.org/en/stable/reference/json-map-format/) · [LDtk JSON structure](https://ldtk.io/docs/game-dev/json-overview/) · [JSON canonicalization standard](https://www.rfc-editor.org/rfc/rfc8785.html)
- [ScriptableObject](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/scriptableobject) · [Text assets](https://docs.unity3d.com/6000.0/Documentation/Manual/class-TextAsset.html) · [ScriptedImporter](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AssetImporters.ScriptedImporter.html) · [Data Driven Gameplay Elements](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine) · [UDataTable JSON import](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UDataTable?application_version=5.8)
- [Unity JSON serialization](https://docs.unity3d.com/6000.0/Documentation/Manual/json-serialization.html) · [Addressables content updates](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/content-update-builds-overview.html) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Cooking](https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-in-unreal-engine) · [Unity serialization rules](https://docs.unity3d.com/6000.0/Documentation/Manual/script-serialization-rules.html)
- [Factorio migrations](https://lua-api.factorio.com/latest/auxiliary/migrations.html) · [Mojang DataFixerUpper](https://github.com/Mojang/DataFixerUpper) · [Unreal SaveGame](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine) · [JSON Merge Patch](https://www.rfc-editor.org/rfc/rfc7396.html)
- [Witch Beam, Unpacking, GCAP 2023 — Developer talk](https://youtu.be/2j7AJj1oRSQ) · [Witch Beam, Unpacking, GCAP 2023 — Talk segments](https://confpad.io/conferences/gcap-2023-empower/empowering-design-the-tools-and-pipelines-of-unpacking) · [GDC video](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Brandon Moro, Destiny 2, GDC 2018 — Slides](https://media.gdcvault.com/gdc2018/presentations/Moro_Brandon_Bungies_Asset_Pipeline.pdf) · [Developer paper](https://history.siggraph.org/wp-content/uploads/2022/09/2019-Talks-Santiago_Procedural-System-Assisted-Authoring.pdf)
- [GDC video](https://www.gdcvault.com/play/1025765/Level-Design-in-a-Moment)
- [Unity bundle reproducibility](https://docs.unity.com/en-us/engine/6000.3/manual/building-and-publishing/build-deterministic-builds/assetbundles-addressables) · [Data Registries](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-registries-in-unreal-engine) · [Unity ScriptableObject](https://unity.com/how-to/separate-game-data-logic-scriptable-objects) · [Addressables shipped-game case study](https://unity.com/resources/marvel-snap)
