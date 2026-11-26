# 게임 콘텐츠 편집부터 배포까지 제작 경로 정하기

K-GAME-CONTENT-PRODUCTION · 방법 · 적용 중 · 근거 확인 2026-11-22

실제 편집 과제로 제작 도구를 선택한다. 배포값의 승인된 원본을 추적하고 클린 빌드·재방문·배포 롤백에서 의도한 결과를 확인한다.

적용 범위 — 게임 밸런스 시트, 레벨 편집기, 콘텐츠 DSL, 절차적 생성, 라이브 상태, 독립 배포 팩.

## 적용 방법

밸런스·현지화는 승인된 시트 버전을 임포트한다. 열 타입, 단위, 복사된 수식, ID, 범위, 참조 키를 검사한다. 길이가 달라지는 웨이브는 하위 행이나 에셋으로 둔다. 배포한 공격력 값을 행·열·리비전까지 추적하고 실험용 시뮬레이션과 승인된 출력을 구분한다. 배치·그래프·충돌·조명을 편집할 때는 미리보기가 되는 에셋이나 레벨 편집기를 쓴다. Unity 에셋과 .meta를 함께 관리한다. Unreal One File Per Actor의 편집 단위는 쿠킹 후 레벨에 포함되는 배포 단위와 다르다.

동작 편집은 이름이 있는 조건과 액션으로 시작한다. 반복되는 조합이 충분하면 타입, 허용 연산, 실행 순서, 오류 위치, 실행 예산, 호환성을 유지할 수 있는 DSL이나 제한 스크립트를 검토한다. Wesnoth WML은 시나리오를 맵과 다음 시나리오에 연결하고 OpenTTD NML은 GRF로 컴파일한다. Factorio는 프로토타입 정의와 런타임 이벤트·이관을 분리한다.

절차적 생성은 레이아웃을 언제 확정할지 선택한다. 편집 중 생성안을 승인하거나, 빌드가 의존성 변경을 따라 재생성하거나, 실행할 때 월드를 재구성할 수 있다. 이전 월드 재방문을 보장하려면 생성기 버전·입력 팩·난수 계산 순서·사용자 편집 또는 최종 레이아웃을 보존한다. 도달 가능성과 생성 난이도의 분포를 각각 확인한다.

## 적용 조건과 예외

여러 쓰기가 함께 성공해야 한다면 관계 제약·트랜잭션을 쓰고 실제 외래 키 검사가 켜져 있는지 본다. 여러 기기 충돌에는 스냅숏 버전·쓰기 잠금을 고려한다. 감사·중복 탐지용 이력을 추가할 수 있다. 이벤트에서 원본 상태까지 복원하려면 순서, 스키마 진화, 재생 부수 효과, 조회용 데이터 재구축 책임이 생긴다. Roblox의 세션 잠금·구매 ID는 동시 갱신 문제의 사례다. 이벤트 소싱 연구는 엔지니어 25명과 시스템 19개를 조사했다. 런타임 엔티티 핸들은 해당 세션에서만 유효하므로 저장할 때는 재구성 가능한 ID를 쓴다.

## 확인 방법

퍼즐 말 이동, 체크포인트 순서 변경, 시설 레시피 추가, 협동 챕터 확장 중 대표 편집을 골라 배포한 콘텐츠를 게임에서 연다. 선택 팩은 ID 소유 범위, 의존성, 덮어쓰기, 누락 시 동작, 호환 릴리스를 정한다. 기본 게임, 팩 단독, ID 충돌, 다운로드 중단, 업데이트 후 쓴 세이브의 롤백 읽기를 확인한다. 클린·증분 산출물과 편집에서 플레이까지 걸린 시간을 비교한다. 전용 편집기가 실제 반복 수정을 줄였는지도 측정한다.

## 근거

11월 22일 조사는 Epic Tavern·Darkwater의 시트 작업, Unpacking 도구, 실제 DSL, 절차적 생성 연구, 관계형·이벤트 소싱 시스템, EVE의 버전 배포를 비교했다. 각 사례의 도구와 제작 조건은 다르다. 위 검사는 새 게임에서의 실행 결과가 아닌 제안이다.

[포맷과 스키마 계약](K-GAME-CONTENT-FORMATS.md) · [스테이지 등록과 진행](K-GAME-STAGE-AUTHORING.md) · [난수 스트림 소유권](K-GAME-TECH-RNG.md)

- [Luban features, validation, and target-specific exports](https://www.datable.cn/en/docs/reference/features) · [Unreal Data Tables and Curve Tables](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine) · [Epic Tavern, Tomo Moriwaki, GDC 2026 — Developer talk](https://gdcvault.com/play/1035719/Spreadsheets) · [Engels and Erwig, ClassSheets, ASE 2005 — Authors' paper](https://web.engr.oregonstate.edu/~erwig/papers/ClassSheets_ASE05.pdf) · [TU Delft research](https://repository.tudelft.nl/record/uuid%3A47944256-3559-4c30-a5d2-a795f4bf8e3a)
- [Unity production guide](https://unity.com/how-to/architect-game-code-scriptable-objects) · [Unreal Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine) · [Unreal Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine) · [Unreal OFPA](https://dev.epicgames.com/documentation/en-us/unreal-engine/one-file-per-actor-in-unreal-engine) · [Unity asset metadata](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html)
- [Unreal Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Unite talk](https://www.youtube.com/watch?v=raQ3iHhE_Kk) · [Unpacking developer talk](https://youtu.be/2j7AJj1oRSQ)
- [GDC talk on gameplay scripting design](https://www.gdcvault.com/play/1023204/Sculpting-a-Gameplay-Scripting) · [ScenarioWML](https://wiki.wesnoth.org/ScenarioWML) · [WML campaign authoring guide](https://wiki.wesnoth.org/MakingCampaignInWML) · [Official NML source and compiler](https://github.com/OpenTTD/nml) · [NewGRF usage guide](https://wiki.openttd.org/en/Manual/NewGRF)
- [Data lifecycle](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) · [Migrations](https://lua-api.factorio.com/latest/auxiliary/migrations.html)
- [Goals and design challenges in PCG research](https://drops.dagstuhl.de/entities/document/10.4230/DFU.Vol6.12191.61) · [Insomniac's Marvel’s Spider-Man production paper](https://history.siggraph.org/wp-content/uploads/2022/09/2019-Talks-Santiago_Procedural-System-Assisted-Authoring.pdf) · [Tanagra paper](https://cdn.aaai.org/ojs/12379/12379-52-15907-1-2-20201228.pdf) · [Bungie asset pipeline talk](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Build Systems à la Carte paper](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf)
- [No Man’s Sky continuous world generation talk](https://www.gdcvault.com/play/1024265/Continuous-World-Generation-in-Noby) · [Horizon Zero Dawn GPU runtime placement talk](https://www.gdcvault.com/play/1024700/) · [Paper on measuring the expressive range of procedural generation](https://cdn.aaai.org/ojs/13012/13012-52-16529-1-2-20201228.pdf)
- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html) · [Roblox player data example](https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing) · [SQLite foreign keys](https://www.sqlite.org/foreignkeys.html) · [Wube development article on Factorio saving and loading](https://www.factorio.com/blog/post/fff-270) · [Unity Cloud Save write locks](https://docs.unity.com/en-us/cloud-save/concepts/write-locks)
- [Martin Fowler on Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) · [Industry study by Overeem et al.](https://arxiv.org/abs/2104.01146) · [Archetypes in Unity Entities](https://docs.unity3d.com/Packages/com.unity.entities%401.0/manual/concepts-archetypes.html) · [Unreal MassEntity](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine)
- [Unreal Data Registries](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-registries-in-unreal-engine) · [Unreal Game Features](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine) · [Unity CCD releases and badges](https://docs.unity.com/en-us/ccd/dashboard) · [CCP's EVE static data transformation pipeline](https://developers.eveonline.com/blog/reworking-the-sde-a-fresh-start-for-static-data) · [CCP's versioned distribution API](https://developers.eveonline.com/blog/the-sde-over-http-static-data-dynamically)
