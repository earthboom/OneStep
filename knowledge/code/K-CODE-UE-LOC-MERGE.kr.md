# 언리얼 현지화 병합과 locres 재컴파일 검증

항목 `K-CODE-UE-LOC-MERGE` · 상태 활성 · 확인일 2026-11-06

----------

## 지침

manifest는 수집한 원문과 식별 문맥, 문화권별 archive는 번역 데이터, locres는 런타임용 컴파일 결과, PO는 번역 교환 파일이다.

1. Git의 공통 조상·양쪽 버전에서 manifest와 각 archive를 추출한다. 파일별 인코딩·BOM·들여쓰기·개행을 읽고 재직렬화해 기준 입력과 바이트 단위로 대조한다.
2. 확인한 JSON 스키마에서 중첩 Namespace 경로와 Key를 식별자로 평탄화한다. 중복 식별자는 거부한다. manifest의 Source와 추가 키 메타데이터, archive의 나머지 필드를 보존한다. 양쪽이 같은 변경이거나 한쪽만 변경하면 채택하고, 서로 다른 동시 수정은 사람이 결정할 충돌로 기록한다.
3. 유지하는 쪽 트리의 복사본에 차이만 반영한다. 기존 정렬 순서, 빈 배열, BOM, 탭, LF와 마지막 개행을 보존하고 다시 평탄화해 병합 맵과 대조한다.
4. 최소 .uproject, 해당 대상의 Config/Localization/<target>_Compile.ini, Content/Localization/<target> 입력으로 `UnrealEditor-Cmd.exe <dummy>.uproject -run=GatherText -config=Config/Localization/<target>_Compile.ini -unattended -nullrhi -nosplash -NoShaderCompile`를 실행한다. 기준 커밋의 locres가 모든 문화권에서 바이트 단위로 재현된 다음 병합 입력을 컴파일한다.
5. archive가 기준일 때 PO는 교차 확인용이다. 번역가의 미반영 PO 변경이 원본인 워크플로에서는 먼저 대조·임포트한다.

## 적용 범위와 예외

UE 5.3 JSON 입력을 특정 5.8 소스 빌드로 컴파일한 사례다. 기존 브랜치에서 쓰던 컴파일러를 선호하며 다른 빌드는 동등성을 새로 증명한다. 불필요한 플러그인의 로딩 실패는 최소 프로젝트에서 분리한다. 동일 항목의 양측 수정은 결정권자의 판단이 필요하다.

## 점검

각 문화권별 자체 기준과 추가·삭제·수정에 비추어 수와 값을 대조한다. 기준 파일을 재직렬화해 바이트를 비교하고 개행 차이는 명시한다. 병합 locres에서 키와 번역을 함께 파싱해 양측 변경을 확인한다. 바이트 검색만으로 번역의 연결 관계를 보장할 수 없다. 세 입력에 이미 존재한 PO 차이도 분리한다.

## 근거

2026-11-06 UE 5.3 입력과 Windows UE 5.8 엔진 한 빌드에서 기준 locres의 바이트 동등성, 양쪽 추가분, 오래된 PO 차이를 관찰했다. 구형 스키마, 다른 컴파일러 및 서로 다른 동일 항목 변경은 미검증이다. [Epic, Localization Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/localization-overview-for-unreal-engine?application_version=5.8)

검색어 Unreal Engine, localization, Game.manifest, Game.archive, Game.locres, Game.po, GatherText, GenerateTextLocalizationResource, Game_Compile.ini, UTF-16LE, three-way merge, semantic merge, locres parity, localization manifest, localization archive, Portable Object, localization resource
