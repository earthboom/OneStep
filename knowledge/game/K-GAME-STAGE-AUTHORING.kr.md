# 카탈로그·러너·진행 규칙을 통해 스테이지 추가하기

K-GAME-STAGE-AUTHORING · 방법 · 적용 중 · 근거 확인 2026-11-22

스테이지 ID, 플레이 상태, 캠페인 순서, 영구 기록의 소유자를 정한다. 편집기 미리보기와 배포 메뉴가 같은 러너를 사용하게 하고 대상 빌드에서 스테이지를 검증한다.

적용 범위 — 퍼즐 보드, 플랫폼 방, 웨이브 조우, 전술 임무, 레이싱 코스 제작.

## 적용 방법

선택→진입→실패·재시도 또는 완료→다음 스테이지 흐름을 따라간다. 정의는 고정 StageId·보드나 맵·규칙 참조·편집 설정을 가진다. 카탈로그는 배포 대상에 맞게 ID를 해석한다. 진행 시스템은 확정된 결과로 순서·챕터·선행 조건을 정한다. 러너는 로드·초기화·재시도·종료·해제를, 세션은 가변 보드·웨이브·타이머를, 저장 시스템은 확정된 ID와 점수를 관리한다. 작은 게임에서는 한 모듈이 여러 책임을 맡아도 된다.

미리보기와 메뉴 진입은 입력 검사·초기화·결과 판정 로직을 공유한다. 미리보기는 해금 우회와 테스트 프로필 저장을 허용할 수 있다. 비동기 로드를 교체하면 늦게 도착한 결과를 해제하고 새 세션을 건드리지 못하게 한다. 콘텐츠가 공유 규칙을 참조하도록 한다. 캠페인 순서를 진행 데이터에서 관리하면 독립 스테이지 사이에 에셋 의존성이 생기지 않는다.

ID를 발급하고 템플릿으로 제작한 뒤 누락 표식을 편집기에서 찾아 고친다. 배포 목록에 등록·검증한 다음 실제 빌드에서 연다. 보드·규칙만 달라지면 공용 씬·맵과 스테이지별 정의로 충분하다. 조명·충돌·배치가 다르면 별도 씬·맵이 적합할 수 있다. Unity는 직렬화 참조와 배포 Addressables, Unreal은 맵·에셋 참조와 쿠킹을 확인한다. 기존 규칙으로 표현할 수 없는 동작에만 새 규칙을 추가한다.

## 적용 조건과 예외

구조 검사를 통과해도 풀 수 있는지와 학습 순서는 별도 문제다. 알려진 해답은 경로 하나를 입증한다. 기록의 공정성, 퍼즐 대안 해법, 목표 가독성, 재도전 속도는 각각 확인한다. 협동 결과는 지정된 권한 주체가 확정한다. 중간 저장·고스트 호환성이 콘텐츠에 의존하면 스테이지·규칙 리비전이나 해시를 보존한다.

## 확인 방법

warehouse-03을 실제 밀기 규칙으로 풀고 순서를 바꾼 뒤 이전 완료 기록을 읽는다. 플랫폼 방에서는 출구 도달과 체크포인트 리스폰을, 웨이브는 중단 후 재진입 시 이전 적·타이머가 사라지는지 본다. 전술 맵은 목표를 바꾸어도 임무 상태가 섞이지 않아야 한다. quarry-loop를 대상 차량으로 완주한 뒤 체크포인트 생략·역주행을 검사한다. 팩 단독, 참조 누락, 중복 ID, 코스 변경 후 이전 기록도 확인한다. 대표 스테이지 두 개와 새 규칙 하나를 추가하는 데 걸린 시간과 고친 공통 파일을 기록한다.

## 근거

11월 22일 스테이지 프레임워크 조사는 Tanagra와 퍼즐 생성·학습 연구, Pig Eat Ball, Celeste, Unpacking, Bethesda 모듈 키트, Trackmania 코스 검증, Bungie 빌드, Factorio 이관 자료를 검토했다. 개발자 발표는 각 제작 사례를 보여 준다. 본문의 보드·코스는 검증 예시다.

[콘텐츠 포맷](K-GAME-CONTENT-FORMATS.md) · [게임플레이 회귀](K-GAME-GAMEPLAY-REGRESSION.md) · [레벨 설계](K-GAME-TECH-LEVEL.md)

- [FDG paper](https://pcgworkshop.com/archive/dormans2010adventures.pdf) · [IEEE author manuscript](https://sander.landofsand.com/publications/Dormans_Bakkes_-_Generating_Missions_and_Spaces_for_Adaptable_Play_Experiences.pdf) · [AAAI paper](https://cdn.aaai.org/ojs/12379/12379-52-15907-1-2-20201228.pdf) · [Taylor and Parberry paper](https://ianparberry.com/techreports/LARC-2011-01.pdf) · [Kartal et al. paper](https://cdn.aaai.org/ojs/12859/12859-52-16375-1-2-20201228.pdf)
- [Butler et al., CHI 2015 — Authors' paper](https://www.ericbutler.net/assets/papers/chi2015_progression.pdf) · [GDC video](https://gdcvault.com/play/1025182/Level-Design-Workshop-Set-this) · [Nathan Fouts, Pig Eat Ball, GDC 2018 — Talk slides](https://media.gdcvault.com/gdc2018/presentations/Fouts_Nathan_SetThisGame.pdf) · [GDC video](https://www.gdcvault.com/play/1024307/The-Gamer-s-Brain-How) · [Witch Beam, Unpacking, GCAP 2023 — Developer talk](https://youtu.be/2j7AJj1oRSQ)
- [Session and video segments](https://confpad.io/conferences/gcap-2023-empower/empowering-design-the-tools-and-pipelines-of-unpacking) · [Text of the developers' GDC talk](https://www.gamedeveloper.com/design/skyrim-s-modular-approach-to-level-design) · [Fallout 4 GDC video](https://www.gdcvault.com/play/1022930/-Fallout-4-s-Modular) · [Map submission documentation](https://doc.trackmania.com/create/map-review/submit-your-map-to-map-review/) · [Validation runs and review guidelines](https://doc.trackmania.com/create/map-review/weekly-grands-guidelines/)
- [Bungie talk](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Official Factorio migration documentation](https://lua-api.factorio.com/latest/auxiliary/migrations.html)
- [Tiled templates](https://doc.mapeditor.org/en/latest/manual/using-templates/) · [Tiled JSON format](https://doc.mapeditor.org/en/stable/reference/json-map-format/) · [LDtk typed entities](https://ldtk.io/docs/general/editor-components/entities/) · [LDtk JSON documentation](https://ldtk.io/docs/game-dev/json-overview/)
- [ScriptableObject documentation](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/scriptableobject) · [Data Assets documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine) · [Scene List](https://docs.unity.com/en-us/engine/6000.0/manual/building-and-publishing/build-settings/build-profile-scene-list) · [Unity Chop Chop scene authoring example](https://github.com/UnityTechnologies/open-project-1/wiki/Scene-structure-of-locations) · [Level Instancing](https://dev.epicgames.com/documentation/en-us/unreal-engine/level-instancing-in-unreal-engine)
- [Cooking Content](https://dev.epicgames.com/documentation/en-us/unreal-engine/cooking-content-in-unreal-engine) · [GetDependencies](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/AssetDatabase.GetDependencies.html) · [Build Layout](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/BuildLayoutReport.html) · [Content updates](https://docs.unity3d.com/Packages/com.unity.addressables%402.7/manual/content-update-builds-overview.html) · [Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine)
- [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Asset Management](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine)
