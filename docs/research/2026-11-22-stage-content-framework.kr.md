# 스테이지를 계속 추가할 수 있는 게임 프레임워크

2026-11-22 · 퍼즐, 플랫포머, 액션, 턴제 전술, 레이싱의 저작·검증·배포 설계

**기존 규칙으로 표현할 수 있는 새 스테이지는 디자이너가 스테이지 원본을 작성하고 등록해, 편집기와 실제 게임에서 같은 규칙으로 플레이할 수 있어야 한다.** 이 경우 변경은 새 콘텐츠, 재사용할 부품, 카탈로그와 진행표에 모인다. 스테이지마다 게임 시작 코드나 저장 형식을 수정해야 한다면, 다음 스테이지를 만들기 전에 공통 구조에서 어떤 사실을 콘텐츠로 옮길 수 있는지 확인한다.

이 문서는 연구 결과에서 도출한 설계 기준과 확인 방법을 다룬다. [게임 개발 기본 전략](../designs/game-development-strategy.md)의 콘텐츠 추가 경로를 스테이지 제작 관점에서 확장한다.

## 1. 논문과 제작 경험에서 가져올 원칙

| 자료 | 확인한 내용과 적용 범위 |
| --- | --- |
| **Joris Dormans, FDG 2010 · Dormans와 Bakkes, TCIAIG 2011** | 수행해야 할 목표와 선후 관계를 미션으로, 방문 가능한 위치와 연결을 공간으로 모델링한다. 같은 지형에 다른 목표를 얹는 전술전이나 던전에서 두 정의를 독립적으로 바꿀 수 있다. 간단한 단선 코스는 목표와 공간의 관계를 한 정의 안에서 표현해도 충분하다. [FDG 논문](https://pcgworkshop.com/archive/dormans2010adventures.pdf) · [IEEE 저자본](https://sander.landofsand.com/publications/Dormans_Bakkes_-_Generating_Missions_and_Spaces_for_Adaptable_Play_Experiences.pdf) |
| **Smith·Whitehead·Mateas, Tanagra, AIIDE 2010** | 디자이너가 배치를 편집하면 도구가 플레이어 이동 모델과 지형 사이 제약을 사용해 가능한 배치를 찾는다. 플랫포머에선 점프 거리 같은 계산을 편집기에 되돌려줄 수 있다. 검증 범위는 모델에 표현된 이동과 제약까지다. [AAAI 논문](https://cdn.aaai.org/ojs/12379/12379-52-15907-1-2-20201228.pdf) |
| **Taylor·Parberry, 2011 · Kartal 외, AIIDE 2016** | 소코반 사례들은 되감기식 생성이나 탐색을 활용해 풀이 가능한 배치를 얻는 방법을 보여준다. 고정 스테이지에서도 실제 게임 규칙으로 정답 입력을 재생하면 배치나 규칙 수정 뒤 회귀를 잡을 수 있다. 대규모 탐색은 시간 제한에 걸릴 수 있고, 검증된 풀이의 존재만으로 사람이 느끼는 난이도를 알 수는 없다. [Taylor·Parberry 논문](https://ianparberry.com/techreports/LARC-2011-01.pdf) · [Kartal 외 논문](https://cdn.aaai.org/ojs/12859/12859-52-16375-1-2-20201228.pdf) |
| **Butler 외, CHI 2015 · Refraction** | 풀이에 쓰이는 기술을 분석해 새 개념을 언제 도입하고 조합할지 설계했다. 해당 수학 퍼즐에서 2,377명의 플레이를 관찰했고, 반복 조정 뒤 연구가 사용한 참여 지표에서 전문가가 만든 진행과 비슷한 수준을 보고했다. 스테이지 개별 난이도와 등장 순서를 따로 살펴볼 근거다. [저자 논문](https://www.ericbutler.net/assets/papers/chi2015_progression.pdf) |
| **Nathan Fouts, Pig Eat Ball, GDC 2018** | 스테이지가 계속 재배열되는 상황에서 시트, 폴더 검색, 레벨 검색 도구로 각 메커닉과 조우가 어디서 등장하는지 추적했다. 제작 초기에는 `도입 / 연습 / 조합`을 스테이지에 표시하고 목록에서 검색하는 정도로 같은 문제를 다룰 수 있다. [GDC 영상](https://gdcvault.com/play/1025182/Level-Design-Workshop-Set-this) · [발표 슬라이드](https://media.gdcvault.com/gdc2018/presentations/Fouts_Nathan_SetThisGame.pdf) |
| **Maddy Thorson, Celeste, GDC 2017** | 300개가 넘는 플랫포머 스테이지를 챕터 안에서 배치하고 연결한 사례다. 방 자체의 리듬뿐 아니라 앞에서 배운 조작, 다음 방의 난이도, 장면 전환까지 함께 검토할 때 도움이 된다. [GDC 영상](https://www.gdcvault.com/play/1024307/The-Gamer-s-Brain-How) |
| **Witch Beam, Unpacking, GCAP 2023** | 팀은 Unity에서 물건을 놓을 수 있는 영역을 편집하고 물건과 상자 배치를 작성하는 반복 작업에 도구를 만들었다. 공간, 배치 가능 조건, 물건 목록을 디자이너가 실제로 바꾸는 단위에 맞춰 저작한 사례다. [개발팀 발표 영상](https://youtu.be/2j7AJj1oRSQ) · [세션과 영상 구간](https://confpad.io/conferences/gcap-2023-empower/empowering-design-the-tools-and-pipelines-of-unpacking) |
| **Joel Burgess·Nathan Purkeypile, Skyrim과 Fallout 4** | 결합 가능한 공간 키트와 반복 배치를 이용한 생산 사례다. 맞물리는 치수와 접점, 가시성, 다양한 조합에서의 일관성이 중요하다. 새 던전과 전술 맵을 만들 때 벽·문·계단의 결합 규칙을 정하고 조명이나 오브젝트 배치로 변주할 수 있다. [개발팀 GDC 발표 본문](https://www.gamedeveloper.com/design/skyrim-s-modular-approach-to-level-design) · [Fallout 4 GDC 영상](https://www.gdcvault.com/play/1022930/-Fallout-4-s-Modular) |
| **Nadeo, Trackmania 코스 제작과 리뷰** | 코스를 제작·검증해 제출하고 별도의 리뷰를 받는다. 공식 가이드의 검증 주행 고스트는 완주한 입력을 결과로 남기는 사례다. 코스 구조 검사, 해당 차량·규칙으로 완주 확인, 주행감 리뷰를 각각 설계하는 데 참고할 수 있다. [맵 제출 문서](https://doc.trackmania.com/create/map-review/submit-your-map-to-map-review/) · [검증 주행과 리뷰 가이드](https://doc.trackmania.com/create/map-review/weekly-grands-guidelines/) |
| **Brandon Moro, Bungie, GDC 2018 · Factorio 마이그레이션** | Bungie는 에셋의 의존성을 어떻게 기록하느냐가 반복 빌드의 비용과 무효화에 미치는 영향을 보여준다. Factorio는 게임에 저장된 정의가 바뀔 때 이름 변경과 데이터 변환을 별도로 관리한다. 스테이지를 바꿀 때 다시 빌드할 입력과 이전 저장이 여전히 참조할 ID를 각각 추적할 이유다. [Bungie 발표](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Factorio 공식 마이그레이션 문서](https://lua-api.factorio.com/latest/auxiliary/migrations.html) |

## 2. 공통 프레임워크와 상태 소유권

먼저 `선택 → 입장 → 실패·재시도 또는 클리어 → 다음 스테이지`를 실제 플레이 방식으로 그린다. 여기에서 무엇이 스테이지마다 달라지고, 누가 현재 상태를 바꾸며, 종료 후 무엇이 남는지 결정한다. 표의 항목은 책임의 구분이다. 단순한 게임에서는 하나의 에셋이나 모듈이 여러 항목을 담을 수 있다.

| 소유자 | 소유하는 데이터와 변경 계약 |
| --- | --- |
| **스테이지 정의** | 고정된 `StageId`, 보드·씬·맵 등 공간 원본, 선택한 규칙과 저작 설정을 가진다. 필요한 경우 목표·조우·사용할 부품을 정의한다. 플레이 세션은 정의를 읽어 초기화한다. |
| **스테이지 카탈로그** | `StageId`로 정의를 찾고 각 배포 대상에 제공되는 스테이지를 결정한다. 개수에 맞춰 수동 목록 또는 저작 원본에서 생성한 목록을 선택하고, 중복 ID·누락·제외를 발행 전에 검증한다. |
| **진행 시스템** | 표시 순서, 해금 조건과 챕터 구성을 결정한다. 단선 게임은 ID 목록이면 충분하다. 분기나 선택 목표가 있을 때 선행 관계를 표현한다. 스테이지가 다음 씬을 직접 호출하는 대신, 진행 시스템이 클리어 결과와 현재 캠페인 정의로 다음 선택을 정한다. |
| **스테이지 실행 모듈과 세션** | 실행 모듈이 정의 확인, 로드, 초기 상태 생성, 재시도·종료와 자원 정리를 맡는다. 세션이 현재 보드, 타이머, 체크포인트 통과, 적 웨이브처럼 플레이 중 바뀌는 상태를 소유한다. 협동 플레이에서는 호스트나 서버가 결과를 확정하고 클라이언트는 그 상태를 표시한다. |
| **저장과 기록** | 완료 ID, 별·점수·기록 등 계속 남길 결과를 소유한다. 정해진 저장 시점에 확정된 결과를 반영한다. 중간 재개, 고스트, 리플레이가 있는 경우 해당 포맷이 의존하는 스테이지·규칙 버전 또는 콘텐츠 해시를 기록하고 호환 범위를 정한다. |

스테이지 선택 화면과 편집기 미리보기에는 같은 `StageId` 입력과 시작·재시도·종료 동작을 제공한다. 편집기에서는 작업 중인 정의를 주입하거나 해금을 우회할 수 있다. 런타임의 입력 검사, 규칙 초기화, 결과 판정은 같은 경로를 사용하며 미리보기 결과의 저장은 별도 테스트 프로필로 보낸다. 비동기 입장이라면 새 요청이 이전 요청을 취소했을 때, 늦게 도착한 로드의 자원을 해제하고 현재 세션을 덮어쓰지 않도록 계약에 명시한다.

콘텐츠는 공용 부품과 규칙을 참조한다. 공용 모듈은 ID나 규칙의 입력을 받아 동작하므로 각 스테이지의 구체적인 참조를 알 필요가 없다. 앞 스테이지를 완료해야 하는 관계는 진행 정의에 둔다. 이로써 캠페인에서 A를 먼저 플레이하도록 구성하면서도 B의 자산이 A의 맵을 로드할 필요는 없다. [vegabond-code-design의 콘텐츠 추가 경로](../../skills/vegabond-code-design/references/gameplay-framework.md#give-content-an-extension-path) · [기능 의존성 검토](../../skills/vegabond-code-design/references/gameplay-framework.md#make-feature-dependencies-explicit)

## 3. 디자이너가 매번 밟는 추가 경로

1. **작성한다.** 대표 스테이지나 빈 템플릿에서 시작하고 새 `StageId`를 발급한다. 보드 배치나 씬을 만든 뒤 이미 지원되는 목표·적·기믹을 선택한다. 복제할 때 ID는 새로 만들고 공용 부품의 정의는 참조로 유지한다.
2. **즉시 확인한다.** 보드의 잘못된 좌표, 빠진 시작점, 미등록 부품을 편집 시점에 보고한다. 오류에는 스테이지 ID와 에셋·필드 위치, 고칠 조건을 포함한다. 현재 스테이지부터 실행하고 초기화·실패·재시도 루프를 짧게 확인할 수 있게 한다.
3. **등록한다.** 배포 카탈로그에 포함하고 진행표에서 순서·해금을 지정한다. 난이도가 중요한 팀은 플레이어가 처음 접하는 기믹과 이전에 배운 것을 조합하는 지점을 함께 표시한다. 공개 전에 열어 볼 작업물은 미리보기 목록에서 찾을 수 있게 한다.
4. **발행한다.** 전체 목록의 ID와 참조, 진행 조건을 검증하고 목표 플랫폼 빌드에서 새 스테이지에 실제로 진입한다. 지원되는 기존 저장에서 해금이나 클리어 이력이 연결되는지 확인한다.

저작 원본은 한 곳에서 수정한다. 초기 팀은 Unity나 Unreal의 기본 에셋과 편집 기능으로 시작하고, 2D 배치를 대량 편집하거나 외부 도구와 공유할 때 Tiled나 LDtk의 사용을 검토한다. 외부 편집기를 선택한 경우 원본과 변환 규칙을 관리하고 엔진 에셋은 그 입력으로 다시 만든다. 외부 편집기의 파일·내부 ID와 게임이 저장하는 `StageId` 사이 매핑을 명시한다. 여러 사람이 같은 목록을 자주 편집해 충돌한다면 정의를 스테이지별로 저장하고 배포 목록을 생성하는 방식의 가치를 측정할 수 있다. [Tiled 템플릿](https://doc.mapeditor.org/en/latest/manual/using-templates/) · [Tiled JSON 형식](https://doc.mapeditor.org/en/stable/reference/json-map-format/) · [LDtk의 타입이 있는 엔티티](https://ldtk.io/docs/general/editor-components/entities/) · [LDtk JSON 문서](https://ldtk.io/docs/game-dev/json-overview/)

공용 부품은 여러 스테이지가 함께 갱신되길 원하는 동작을 담는다. 체크포인트 공용 부품의 판정을 바꾸면 그 부품을 참조하는 코스가 모두 영향을 받는다. 코스별 효과음이나 위치처럼 개별 조정할 값은 배치에서 설정하고, 공용 동작을 바꿀 때는 영향받는 스테이지를 참조 목록에서 찾아 검토한다. 방을 조합해 스테이지를 생성하는 게임에서도 방의 접점·이동 조건과 최종 스테이지의 진행 가능성을 각각 검증한다. [Skyrim 모듈 제작 사례](https://www.gamedeveloper.com/design/skyrim-s-modular-approach-to-level-design) · [Tanagra의 지형 제약](https://cdn.aaai.org/ojs/12379/12379-52-15907-1-2-20201228.pdf)

콘텐츠 추가 중 어디에 코드 변경이 필요한지도 구분한다.

| 요청 예 | 편집 범위 |
| --- | --- |
| 기존 상자와 목표를 다른 위치로 옮긴 퍼즐 | 보드와 목표 데이터, 카탈로그 또는 진행표 |
| 같은 지형에 구출 목표를 얹은 전술 맵 | 구출 규칙이 있으면 목표 정의와 배치 데이터. 규칙이 새로 필요하면 구출의 성공·실패·턴 전이를 공용 규칙에 추가한 뒤 등록 |
| 기존 적과 스폰 포인트로 만든 보스 앞 웨이브 | 조우 정의와 기존 부품. 취소 후 보스전에 영향을 주는 플래그가 필요하면 그 소유자와 저장 시점을 함께 설계 |
| 새로운 순간이동 타일이나 레이싱 랩 판정 방식 | 적용 범위가 드러나는 규칙을 추가하고, 기본값과 이전 콘텐츠 영향을 확인한 뒤 해당 스테이지에서 선택 |

## 4. 장르별 저작 단위와 검증

| 장르 | 스테이지에서 바꿀 수 있어야 하는 것 | 구조 검사 이후 확인할 플레이 |
| --- | --- | --- |
| **격자 퍼즐** | 보드 크기, 타일, 플레이어·기물의 초기 배치, 목표, 선택한 규칙 | 실제 판정으로 입력을 재생해 목표가 성립하고 초기화가 재현되는지 확인한다. 힌트와 특정 해법 교육을 의도하면 우회 풀이와 기믹 발견도 플레이테스트한다. |
| **플랫포머** | 화면·방, 시작과 출구, 체크포인트, 방 사이 연결, 재사용 구간과 이동 부품 | 주어진 캐릭터 능력으로 출구와 필수 체크포인트에 도달하고 사망 후 의도된 위치에서 재개한다. 새 기믹을 도입하는 방의 앞뒤 순서도 검토한다. |
| **웨이브 액션·던전** | 공간, 스폰 지점, 적 조합, 웨이브 시작·종료 조건, 문·출구·목표 | 적이 접근할 수 있고, 처치·시간 경과 등 규칙이 웨이브를 끝내는지 확인한다. 중단·재진입 뒤 이전 웨이브의 타이머나 적이 새 세션에 남아 있지 않아야 한다. |
| **턴제 전술** | 지형과 유닛 초기 배치, 목표, 턴 제한, 증원 타이밍, 보상 | 초기 템플릿의 배치 가능성, 필수 목적지 도달과 증원 순서를 확인한다. 같은 지형으로 목표를 바꿨을 때 원래 미션의 상태·결과가 섞이지 않아야 한다. |
| **레이싱** | 코스, 출발 그리드, 체크포인트 순서 또는 분기, 랩 수, 리스폰 지점, 해당 차량 등급 | 대상 차량·규칙으로 한 번 완주하고, 체크포인트 건너뛰기나 역주행이 잘못된 완주를 만들지 않는지 확인한다. 코스 수정이 타임어택 기록의 공정성에 영향을 주면 기록을 버전별로 관리한다. |

예를 들어 새 `warehouse-03` 퍼즐은 기존 조작을 이용하는 보드 배치와 예상 클리어 입력을 추가한다. 동일한 실행 모듈에서 입력을 재생해 클리어하고 목록에서 세 번째에 표시한다. 새 `quarry-loop` 코스는 별도 맵과 체크포인트·리스폰 정의를 추가해 기존 타임어택 규칙으로 완주한다. 어느 쪽도 표시 순서가 바뀌었을 때 예전 저장의 완료 ID를 바꿀 필요가 없다. [퍼즐 진행 연구](https://www.ericbutler.net/assets/papers/chi2015_progression.pdf) · [Trackmania 제작·검증 사례](https://doc.trackmania.com/create/map-review/weekly-grands-guidelines/)

## 5. Unity와 Unreal에서의 기본 선택

| 결정 | Unity | Unreal Engine |
| --- | --- | --- |
| **같은 실행 환경에서 배치가 달라지는 2D 퍼즐** | 공용 Scene과 스테이지별 `ScriptableObject`나 임포트된 보드 에셋을 조합한다. 세션이 초기 배치를 읽어 C# 게임 상태를 만들고 화면을 갱신한다. [ScriptableObject 문서](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/scriptableobject) | 공용 Map과 스테이지별 `UDataAsset`을 조합한다. 게임 규칙을 실행하는 C++ 쪽 세션이나 게임플레이 객체가 정의를 읽고 상태를 가진다. [Data Assets 문서](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine) |
| **공간 저작이 중심인 레이싱·액션·전술** | 씬에 공간과 스폰·체크포인트를 두고, 공용 Prefab과 스테이지 정의에 규칙·목표를 둔다. 출시 대상 씬은 Build Profiles의 Scene List 같은 기존 경로에 포함한다. 공용 환경이나 기존 상태를 유지하면서 콘텐츠만 교체할 때 additive 로드를 고려한다. [Scene List](https://docs.unity.com/en-us/engine/6000.0/manual/building-and-publishing/build-settings/build-profile-scene-list) · [Unity Chop Chop 씬 저작 사례](https://github.com/UnityTechnologies/open-project-1/wiki/Scene-structure-of-locations) | 스테이지별 Map에 배치와 마커를 두고, `UDataAsset`과 공통 게임 규칙을 연결한다. 복수 맵에서 공간 부품을 재사용할 때 Level Instance를 검토한다. 맵과 종속 에셋이 대상 cook에 포함돼 패키지에서 열리는지 확인한다. [Level Instancing](https://dev.epicgames.com/documentation/en-us/unreal-engine/level-instancing-in-unreal-engine) · [Cooking Content](https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-in-unreal-engine) |
| **의존성과 배포 단위를 별도로 관리할 때** | `AssetDatabase.GetDependencies`로 에디터 참조를 확인한다. Addressables가 필요하면 Build Layout에서 실제 번들 의존성과 중복을 조사하고, 콘텐츠 업데이트를 사용할 때 기존 Player와 짝이 되는 빌드 경로를 관리한다. [GetDependencies](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/AssetDatabase.GetDependencies.html) · [Build Layout](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/BuildLayoutReport.html) · [콘텐츠 업데이트](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/content-update-builds-overview.html) | Reference Viewer로 의존성 방향을 확인하고 Data Validation에서 정의와 참조 규칙을 검사할 수 있다. 프로젝트에서 독립 콘텐츠 팩의 검색·비동기 로딩·쿠킹을 제어할 필요가 생기면 Asset Manager와 Primary Assets를 검토한다. [Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Asset Management](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine) |

선택 기준은 스테이지마다 **보드와 규칙 설정**이 달라지는지, **공간·라이팅·충돌과 배치**가 달라지는지다. 전자는 공용 씬·맵에서 데이터를 바꿔 시작하기 쉽고 후자는 각 씬·맵을 독립적으로 편집하기 쉽다. 출시 콘텐츠가 한 번에 묶이는 프로젝트는 기본 로드와 패키징으로 출발할 수 있다. 독립 팩, 출시 후 갱신, 메모리 예산처럼 별도 요건이 있을 때 로드·배포 정책을 늘린다.

## 6. 자동 검증과 제작 검토

| 검증 | 잡아야 할 문제와 확인 방법 |
| --- | --- |
| **원본과 참조** | 중복 ID, 정의되지 않은 타입·규칙, 필수 마커 누락, 다른 스테이지로 향하는 의도치 않은 참조를 편집기와 CI에서 확인한다. 해당 플랫폼의 지원 콘텐츠 목록과 필요한 에셋을 대조한다. |
| **규칙과 진행** | 퍼즐의 풀이 입력, 레이싱의 검증 주행, 전술의 승리·실패 조건과 재시작을 실제 게임 규칙으로 확인한다. 선행 ID 누락과 새 게임에서 도달할 수 없는 필수 스테이지를 확인하고, 의도된 반복과 정상 진행을 막는 선행 조건 순환을 구분한다. 퍼즐 솔버에는 `풀이 있음`, `풀이 없음이 확인됨`, `시간·탐색 한도로 미판정`을 구분해 기록한다. |
| **실제 배포 경로** | 지원하는 Player 또는 패키지 빌드의 메뉴에서 등록된 새 스테이지를 열고 나간다. 선택형 팩을 지원한다면 팩이 포함된 빌드와 빠진 빌드에서 각자의 정상 흐름을 확인한다. 편집기의 강제 참조 로드는 패키지 내 존재 여부를 확인하는 별도 검사와 함께 사용한다. |
| **저장 호환성** | 콘텐츠의 표시 이름, 파일 위치, 캠페인 순서를 바꾼 뒤 이전 저장의 완료 ID가 이어지는지 확인한다. 삭제·교체 시 옛 ID를 유지해 완료로 표시할지, 새 ID로 옮길지, 표시만 숨길지 정한다. 기존 기록을 해석할 수 없는 규칙 변경은 기록의 호환 범위를 명시한다. |
| **플레이 경험** | 목표를 읽을 수 있는지, 의도한 순서로 기믹을 접하는지, 반복 시 재시도 시간이 적절한지 플레이테스트한다. 필요하면 실패 위치·재시도·중도 이탈 분포로 다음 수정 대상을 찾는다. [Tanagra 논문](https://cdn.aaai.org/ojs/12379/12379-52-15907-1-2-20201228.pdf) · [Refraction 플레이 연구](https://www.ericbutler.net/assets/papers/chi2015_progression.pdf) |

예를 들어 `warehouse-03`을 앞으로 옮겨도 이전에 해당 퍼즐을 완료한 저장은 계속 완료를 표시해야 한다. 중간 저장을 지원한다면 보드 편집 후 기존의 말 위치를 그대로 불러올 수 있는지도 별도로 정한다. `quarry-loop`의 조명만 바꾼 경우와 체크포인트 판정을 바꾼 경우에는 예전 기록을 비교할 수 있는 조건이 다르다. 완료 이력의 ID와 기록·재개에 필요한 콘텐츠 버전을 따로 유지하면 각 정책을 적용하기 쉽다. [기존 게임 데이터 변경 사례](https://lua-api.factorio.com/latest/auxiliary/migrations.html) · [OneStep 저장 설계](../../knowledge/game/K-GAME-TECH-SAVE.kr.md)

## 7. 게임 개발을 시작할 때 정할 기본 규칙

- 대표 스테이지 두 개와 변형 하나를 고른다. 가령 기본 퍼즐, 기존 기믹을 조합한 퍼즐, 새로운 기믹이 필요한 퍼즐이다. 첫 두 스테이지의 차이를 저작할 위치와 세 번째가 요구하는 공용 규칙 변경을 설계에 적는다.
- 스테이지 ID, 실행·종료 권한, 진행 조건, 지속 상태를 누가 관리하는지 정한다. 로컬 게임과 서버 권한 게임은 같은 콘텐츠 형태를 활용할 수 있어도 결과를 확정하는 주체는 달라진다.
- 디자이너와 AI가 볼 문서에 `원본 위치 → 공용 부품 → 검증 → 등록 → 실제 게임에서 열기`를 적는다. 기존 규칙으로 만들 수 있으면 그 경로로 추가하고, 공용 규칙을 바꾸는 경우 영향을 받는 기존 스테이지와 확인할 플레이를 함께 기록한다.
- 제작이 진행되면 새 스테이지를 열기까지 걸린 시간, 수정한 공용 파일, 누락으로 되돌아간 작업을 살핀다. 반복 비용이 확인된 저작 단계에 목업·미리보기·검증·자동 등록을 보강한다. [vegabond-code-design의 게임 시작 설계](../../skills/vegabond-code-design/references/gameplay-framework.md#plan-a-new-game-foundation) · [vegabond-code의 검증 지침](../../skills/vegabond-code/references/verification.kr.md)
