# 게임 데이터 관리 방법론과 제작 사례

2026-11-22 · 시트와 코드 생성, 엔진 에셋, 콘텐츠 언어, 절차 생성, 트랜잭션과 버전별 배포

**데이터 관리 방식은 바꾸려는 작업을 기준으로 고른다.** 수백 개의 값을 한눈에 조정하려는 팀, 씬을 보면서 스테이지를 편집하는 팀, 사용자에게 확장팩 제작 도구를 제공하려는 팀은 각각 다른 저작 방법이 필요하다. 게임 한 편에서도 시트에서 밸런스를 조정하고, 엔진 에셋으로 공간을 저작하고, 데이터베이스에서 계정 상태를 갱신할 수 있다. [Epic Tavern·Darkwater 제작 발표](https://gdcvault.com/play/1035719/Spreadsheets) · [Unity ScriptableObject 제작 사례](https://unity.com/how-to/architect-game-code-scriptable-objects) · [Roblox 플레이어 데이터 설계 사례](https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing)

[게임 데이터 형식 비교](2026-11-22-game-data-formats-and-pipeline.kr.md)에서 살펴본 선택지를 실제 제작 흐름에 적용한다. 각 방법의 적용 범위, 생산 비용, 기존 스테이지·저장과 충돌할 지점을 함께 다룬다.

## 1. 시트와 타입이 있는 데이터 생성

**맞는 상황.** 아이템 가격, 적 수치, 보상표, 대사와 지역화처럼 열이 여러 행에서 반복되고, 디자이너가 비교·필터·일괄 편집을 해야 할 때다. 스테이지 자체도 하나의 행으로 요약할 수 있다. `스테이지 ID`, `보드 참조`, `목표 규칙 ID`, `보상 ID`를 열로 두고 여러 웨이브나 유닛 배치처럼 개수가 달라지는 데이터는 스테이지 ID가 포함된 별도 표 또는 편집 에셋으로 관리한다. 지역화 텍스트와 게임 규칙이 참조하는 키의 소유자도 정한다.

**운영 방법.** 지정한 시트 리비전에서 내보낸 입력을 가져오기 도구가 읽는다. 열의 타입·단위·필수 여부, ID 중복과 다른 표 참조, 값 범위를 검사한다. 그 결과로 엔진 에셋, 타입이 있는 조회 코드, 바이너리 등 필요한 산출물을 만든다. 시트에서 계산한 값을 배포한다면 당시 사용된 값을 재현할 수 있게 내보내기 입력을 보관한다. 시뮬레이션과 그래프는 비교용으로 유지하고 배포되는 표에서 실험값과 확정값을 식별한다. 팀이 배포한 파일에서 `공격력 20`이 어떤 행·열에서 왔는지 역추적할 수 있어야 한다. [Luban 기능·검증·대상별 내보내기](https://www.datable.cn/en/docs/reference/features) · [Unreal Data Tables와 Curve Tables](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine)

| 자료 | 제작 판단에 적용할 내용 |
| --- | --- |
| **Epic Tavern, Tomo Moriwaki, GDC 2026** | Google Sheets의 데이터를 게임 입력으로 가져오면서 이야기 작업도 가능하도록 팀 협업 방식을 조정했다. 대사·퀘스트 편집에서 키 관리와 전체 이야기 검토를 함께 설계할 사례다. [개발자 발표 영상](https://gdcvault.com/play/1035719/Spreadsheets) |
| **Darkwater, Guillaume Pierre, GDC 2026** | 절차 생성되는 공간과 아이템 드롭을 시트에서 시뮬레이션했다. 보상표를 편집하는 표와 보상 분포를 분석하는 시뮬레이터가 함께 필요한 경우다. [GDC 발표 영상](https://gdcvault.com/play/1035719/Spreadsheets) |
| **Engels·Erwig, ClassSheets, ASE 2005** | 스프레드시트의 반복 구조와 관계를 모델로 정의해 시트를 생성하는 방식을 제안했다. 게임에 적용하면 시트 양식도 검사할 수 있는 스키마로 다룰 이유가 생긴다. [저자 논문](https://web.engr.oregonstate.edu/~erwig/papers/ClassSheets_ASE05.pdf) |
| **Hermans 외, 스프레드시트 수식 연구** | 수식의 반복과 복잡성, 숨은 참조가 유지보수에 미치는 문제를 분석했다. 게임 수식에 일반화하려면 해당 프로젝트에서 참조 변경·복제 오류를 확인한다. [TU Delft 연구](https://repository.tudelft.nl/record/uuid%3A47944256-3559-4c30-a5d2-a795f4bf8e3a) |

## 2. 엔진 에셋과 전용 편집기

**맞는 상황.** 위치·충돌·라이팅·프리뷰와 에셋 참조가 중요한 스테이지, 대화 그래프, 조우 배치다. Unity에서는 씬·Prefab과 `ScriptableObject`, Unreal에서는 Map·Blueprint와 `UDataAsset`을 조합할 수 있다. 예를 들어 레이싱 코스에 체크포인트와 리스폰 지점을 놓고, 별도 정의에서 랩 규칙과 해금 ID를 지정한다. 공용 프리셋을 바꾸면 어느 스테이지가 영향을 받는지 검색할 수 있도록 참조를 남긴다. [Unity 제작 가이드](https://unity.com/how-to/architect-game-code-scriptable-objects) · [Unreal Data Assets](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-assets-in-unreal-engine) · [Unreal Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine)

**운영 방법.** 저작 원본을 일반적으로 함께 바꾸는 단위로 나눈다. Unreal의 One File Per Actor는 편집기에서 액터 파일을 분리해 같은 레벨의 병행 작업을 돕고, cook에서는 액터가 레벨에 포함된다. 따라서 버전 관리상의 편집 단위와 런타임 스트리밍 단위를 따로 결정해야 한다. Unity에서는 원본 에셋과 `.meta`를 함께 관리하고, 스테이지를 중복 등록하거나 필수 참조가 빠졌을 때 에디터에서 해당 에셋을 열어 고칠 수 있게 한다. [Unreal OFPA](https://dev.epicgames.com/documentation/en-us/unreal-engine/one-file-per-actor-in-unreal-engine) · [Unity 에셋 메타데이터](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html) · [Unreal Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine)

Ryan Hipple의 Unite 발표는 에셋을 활용한 설계 패턴을, Witch Beam의 *Unpacking* 발표는 배치 구획과 물건·상자 저작에 맞춘 도구를 보여준다. 현재 작업에서 반복되는 편집을 먼저 확인하고, 예를 들어 체크포인트 순서와 누락된 스폰 위치를 표시하는 검증부터 붙이면 기본 에디터를 활용하면서도 오류를 빨리 찾을 수 있다. [Unite 발표 영상](https://www.youtube.com/watch?v=raQ3iHhE_Kk) · [Unpacking 개발팀 발표](https://youtu.be/2j7AJj1oRSQ)

## 3. 선언형 콘텐츠 언어와 제한된 스크립트

**맞는 상황.** 스테이지 저작자가 데이터의 배치뿐 아니라 `문을 열면 증원`, `세 턴 안에 구출하면 분기` 같은 동작을 조합해야 하거나, 외부 제작자에게 정해진 기능의 콘텐츠를 제공할 때다. 먼저 에디터나 표에 조건·행동의 목록을 두고, 조합의 종류와 패키지 수가 늘면 전용 언어 또는 스크립트의 가치를 비교한다. 실행 시점·권한이 중요한 판정은 규칙 모듈이 소유하고, 각 스테이지는 공개된 조건·행동을 선택한다. [게임플레이 스크립트 설계 GDC 발표](https://www.gdcvault.com/play/1023204/Sculpting-a-Gameplay-Scripting)

| 사례 | 저작과 실행이 갈리는 지점 |
| --- | --- |
| **Battle for Wesnoth의 WML** | 시나리오 ID, 맵 파일, 승리 시 다음 시나리오 ID를 선언한다. 이벤트와 전처리기 기능이 필요한 규모에서 시나리오 네트워크를 저작하며, 테스트 모드에서 특정 시나리오를 바로 열 수도 있다. [ScenarioWML](https://wiki.wesnoth.org/ScenarioWML) · [WML 캠페인 제작 문서](https://wiki.wesnoth.org/MakingCampaignInWML) |
| **OpenTTD의 NML과 NewGRF** | 제작자는 전용 언어와 리소스를 작성하고 컴파일해 게임이 읽는 GRF를 배포한다. 언어와 배포 산출물의 역할을 분리하며, 진행 중 변경에서 호환되는 범위는 게임이 별도로 정한다. [공식 NML 소스와 컴파일러](https://github.com/OpenTTD/nml) · [NewGRF 사용 문서](https://wiki.openttd.org/en/Manual/NewGRF) |
| **Factorio의 Lua 프로토타입** | 정해진 데이터 단계에서 모드가 프로토타입을 만들거나 조정하고, 플레이 중 이벤트와 상태 변경은 런타임 단계에서 처리한다. 여러 모드가 수정할 수 있는 정의의 로드 순서와 기존 저장의 변환 규칙을 읽어 볼 수 있다. [데이터 수명주기](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) · [마이그레이션](https://lua-api.factorio.com/latest/auxiliary/migrations.html) |

**운영 방법.** 함수·타입 목록, 실행 순서, 기본값과 오류 위치, 버전 호환성을 도구와 함께 관리한다. 콘텐츠 팩을 지원하면 팩 단위로 참조와 필수 기능을 검사한다. 사용자가 만든 스크립트를 실행하는 제품은 허용 동작·실행 예산을 실행 환경에서 적용하고, 필수 기믹에 대해서는 실제 스테이지 진입과 종료까지 시험할 경로를 둔다. DSL의 개발·문서·디버깅 비용을 감당할 제작량이 있는지 작은 조건·행동 목록과 비교한다.

## 4. 절차 생성과 콘텐츠 빌드

수백 개의 지형 배치에서 비슷한 순서로 조립한다면 사람은 템플릿·접점·배치 제약을 저작하고 생성기는 결과를 만든다. 이때 **언제 결과를 확정하는지**가 저장과 디버깅 방법을 바꾼다. [PCG 연구의 목표와 설계 과제](https://drops.dagstuhl.de/entities/document/10.4230/DFU.Vol6.12191.61)

| 방법 | 역할과 유지보수 비용 |
| --- | --- |
| **저작 중 생성** | 디자이너 도구가 방·도시 블록을 제안하고 검토한 배치를 확정한다. 고정 스테이지에서 사람의 수정과 결정 이력을 추적하기 좋다. [Insomniac의 Marvel’s Spider-Man 제작 논문](https://history.siggraph.org/wp-content/uploads/2022/09/2019-Talks-Santiago_Procedural-System-Assisted-Authoring.pdf) · [Tanagra 논문](https://cdn.aaai.org/ojs/12379/12379-52-15907-1-2-20201228.pdf) |
| **빌드 중 생성** | 타일, 사전 계산된 배치, 검색용 카탈로그 등 산출물을 출시에 맞춰 재생성한다. 원본·도구·참조 에셋이나 플랫폼이 바뀌면 어느 결과가 무효가 되는지 추적한다. 깨끗한 빌드 결과와 변경 후 재빌드 결과가 동일한 입력을 반영하는지 점검한다. [Bungie 에셋 파이프라인 발표](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Build Systems à la Carte 논문](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf) |
| **실행 중 생성** | 필요한 공간이나 시각 요소를 조건에 따라 생성한다. 게임 규칙에 영향을 주는 지형은 생성 순서, 호환성, 재현이 필요하다. 플레이 결과와 무관한 장식 배치는 더 쉽게 재생성할 수 있다. [No Man’s Sky 연속 월드 생성 발표](https://www.gdcvault.com/play/1024265/Continuous-World-Generation-in-Noby) · [Horizon Zero Dawn GPU 런타임 배치 발표](https://www.gdcvault.com/play/1024700/) |

시드가 같아야 같은 스테이지가 필요한 제품은 생성기 버전, 입력 팩, 랜덤 계산 순서와 타깃 간 동작을 함께 검증한다. 이전 저장의 재방문을 보장할 방법은 호환 생성기를 보존하거나, 필요한 배치와 유저가 바꾼 결과를 저장하는 것이다. 자동 생성된 스테이지가 규칙상 클리어되는지, 산출물의 종류와 난이도가 한쪽으로 몰리는지도 별도 지표로 확인한다. [절차 생성의 표현 범위 측정 논문](https://cdn.aaai.org/ojs/13012/13012-52-16529-1-2-20201228.pdf) · [격자 퍼즐과 레이싱 검증 방식](2026-11-22-stage-content-framework.kr.md#6-자동-검증과-제작-검토)

## 5. 관계형 데이터, 스냅샷과 이벤트 이력

라이브 게임과 큰 시뮬레이션에서는 **어떤 변경들이 함께 성공해야 하는지**, **두 작성자가 같은 값을 바꾸면 어떻게 되는지**가 중요하다. 콘텐츠 카탈로그처럼 읽기 중심인 데이터에는 이 문제가 작을 수 있다. 여러 서버에서 동시 처리하는 보상과 교환에는 권한, 트랜잭션, 재시도 정책이 필요하다. [PostgreSQL 트랜잭션](https://www.postgresql.org/docs/current/tutorial-transactions.html) · [Roblox 플레이어 데이터 예시](https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing)

| 방법 | 적용과 확인할 실패 |
| --- | --- |
| **관계형 테이블과 제약** | 유닛·레시피·보상 관계가 크고 조인·부분 조회가 필요하면 SQLite 같은 임베디드 DB를 비교한다. 작은 프로필도 여러 값을 동시에 갱신해야 할 수 있고, 서버 경제는 중복 지급 방지와 트랜잭션이 필요하다. 참조 삭제 규칙과 실제 DB의 외래 키 적용 여부, 갱신 실패 후 일관성을 확인한다. [SQLite 외래 키](https://www.sqlite.org/foreignkeys.html) · [PostgreSQL 트랜잭션](https://www.postgresql.org/docs/current/tutorial-transactions.html) |
| **버전이 있는 스냅샷** | 현재 스테이지 진행, 인벤토리와 월드 상태를 복구에 필요한 시점에 저장한다. 이전 버전에서 읽은 후 변환하고 성공한 결과를 확인한다. 여러 기기가 같은 데이터를 갱신할 수 있다면 저장 버전이나 쓰기 잠금으로 충돌을 감지해, 어느 상태를 채택할지 계약으로 정한다. [Wube의 Factorio 저장·로딩 개발 글](https://www.factorio.com/blog/post/fff-270) · [Unity Cloud Save 쓰기 잠금](https://docs.unity.com/en-us/cloud-save/concepts/write-locks) |
| **변경 이력과 이벤트 소싱** | 스냅샷과 완료 이벤트를 함께 남기면 장애 분석과 중복 보상 확인에 쓸 수 있다. 과거 이벤트로 상태를 재구축해야 할 요구가 있으면 이벤트 소싱을 비교한다. 이 경우 이벤트 순서·중복·버전, 재생에서 발생할 외부 부작용 처리, 조회용 데이터 재구축까지 책임이 늘어난다. [Martin Fowler의 Event Sourcing 설명](https://martinfowler.com/eaaDev/EventSourcing.html) · [Overeem 외 산업 사례 연구](https://arxiv.org/abs/2104.01146) |

Roblox의 공개 예시는 서버가 프로필을 활성화할 때 세션 잠금을 잡고, 구매 요청에는 처리 ID를 사용한다. 여러 서버에서 같은 프로필을 열거나 응답 전 재시도할 수 있는 제품에서 어떤 경쟁 조건을 고려해야 하는지 보여준다. Overeem 외는 25명의 엔지니어와 19개 이벤트 소싱 시스템을 바탕으로 이벤트 스키마 진화, 학습 비용, 조회용 데이터 재구축 등을 과제로 보고했다. 게임에 이 방식을 선택할 때는 재생·감사의 요구와 실제 쓰기 수명을 먼저 확인한다. [Roblox 구현 사례](https://create.roblox.com/docs/cloud-services/data-stores/player-data-purchasing) · [이벤트 소싱 연구](https://arxiv.org/abs/2104.01146)

시설이나 NPC를 많이 시뮬레이션한다면, 프레임마다 함께 읽는 상태를 모으는 메모리 구조를 별도로 평가한다. Unity Entities와 Unreal MassEntity는 같은 데이터 구성을 가진 엔티티를 묶어 처리하는 예다. 저장에는 세션에서 할당된 엔티티 핸들과 메모리 배치 대신 영속 ID와 다시 구성할 값을 기록하고, 기존 오브젝트 기반 처리와 비교해 실제 프레임 비용이 줄어드는지 측정한다. [Unity Entities의 Archetype](https://docs.unity3d.com/Packages/com.unity.entities%401.0/manual/concepts-archetypes.html) · [Unreal MassEntity](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine)

## 6. 콘텐츠 팩과 버전별 배포

선택형 스테이지 팩이나 시즌 데이터는 기본 콘텐츠와 선택 팩의 **ID 범위, 의존 팩, 버전, 교체 허용 범위**를 명시한다. 등록과 조회에는 프로젝트에 맞는 목록이나 레지스트리를 둔다. Unreal Data Registry는 여러 소스를 조회 순서에 따라 사용해 덮어쓰기와 대체 조회를 구성할 수 있다. 같은 ID가 여러 팩에 등장할 때 어떤 값이 쓰이는지 저작자가 예측할 수 있게 하고, 팩이 없을 때 새 게임과 기존 저장이 어디까지 진행되는지 정한다. [Unreal Data Registries](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-registries-in-unreal-engine) · [Unreal Game Features](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine)

**운영 방법.** 출시 콘텐츠는 확정된 묶음으로 발행하고, 업데이트에서 여러 파일이 같은 발행 버전에 속하도록 조회·로드 경로를 고정한다. 게임에 이미 들어간 세션이 언제 새 묶음을 볼지, 구버전을 언제까지 읽을지 정한다. 새 버전에서 저장을 바꿨다면 콘텐츠 배포 포인터를 이전 버전으로 되돌린 후에도 해당 저장을 읽을 수 있는지 별도 확인한다. Unity CCD는 발행본을 가리키는 badge를 제공한다. CCP는 변환 규칙을 통해 게임 클라이언트의 정적 데이터를 공개용 산출물로 만들고, 공개 API에서 FlatBuffers, 개별 발행본 URL, 변경 목록과 ETag를 제공한다. 같은 구조를 게임 업데이트에 쓰려면 저장 호환성과 발행본 보존 기간을 따로 결정한다. [Unity CCD releases와 badges](https://docs.unity.com/en-us/ccd/dashboard) · [CCP의 EVE 정적 데이터 변환 파이프라인](https://developers.eveonline.com/blog/reworking-the-sde-a-fresh-start-for-static-data) · [CCP의 버전별 배포 API](https://developers.eveonline.com/blog/the-sde-over-http-static-data-dynamically)

## 7. 장르별로 적용할 시작점

| 작업 | 적합한 조합과 실제 추가 경로 | 바꿀 시점 |
| --- | --- | --- |
| **격자 퍼즐에 스테이지 추가** | 보드 편집기의 원본 파일이나 엔진의 타입이 있는 에셋으로 보드를 만든다. 카탈로그와 진행표에 새 ID를 추가하고 에디터와 실제 게임에서 풀이 입력을 확인한다. | 여러 사람이 같은 보드를 자주 편집하면 공간·속성 편집을 개선한다. 새 조건 조합이 늘면 규칙의 조합을 저작하는 도구를 검토한다. |
| **레이싱·턴제 전술에 새 맵 추가** | 엔진에서 공간과 마커를 편집한다. 기존 경기 규칙이나 전술 목표를 선택한다. 속도 제한, 유닛 수치, 보상은 팀이 비교하기 좋은 표에서 관리한다. | 맵 작업 충돌이 반복되면 자주 바뀌는 액터·에셋을 분리한다. 같은 지형에 여러 미션이 붙으면 공간과 목표 정의의 수명을 나눈다. |
| **경영 시뮬레이션에 시설 추가** | 시설·생산 레시피·비용·업그레이드 관계를 타입이 있는 시트에서 검증하고, 플레이 중 시설과 재고는 시뮬레이션이 유지한다. 저장에는 필요한 시설 ID와 상태를 담는다. | 대량 객체에서 부분 조회·갱신과 복구 요구가 커지면 저장 쿼리와 갱신 부하에서 DB와 기존 저장을 비교한다. |
| **던전·협동 액션에 챕터 추가** | 통과 가능한 접점이 있는 방 에셋과 조우 프리셋을 저작한다. 빌드에서 생성하거나 실행 중 확정한다. 선택 챕터의 범위와 버전은 팩에 기록하고 보상은 권한 있는 세션이 확정한다. | 콘텐츠 팩이 출시마다 달라질 때 독립 발행 경로를 검토한다. 실행 중 생성으로 바꿀 때는 재접속·리플레이·저장에 필요한 버전과 배치를 먼저 정한다. |

예를 들어 엔진 에디터로 만드는 밀기 퍼즐에 `warehouse-04`를 추가한다면, Unity는 새 보드 `ScriptableObject`, Unreal은 새 보드 `UDataAsset`을 만든다. 같은 밀기 규칙과 기존 보상표의 행을 선택하고, 카탈로그와 챕터 진행에 ID를 등록한 뒤 재시도와 클리어를 확인한다. 기존 스테이지를 앞뒤로 옮겨도 저장의 완료 ID는 그대로 읽는다. 보상 수치를 일괄 조정하는 작업은 표에서 수행한다. [스테이지 상태 소유권 설계](2026-11-22-stage-content-framework.kr.md#2-공통-프레임워크와-상태-소유권)

### 개발을 시작할 때 문서에 남길 결정

- 누가 어디에서 원본을 편집하는지, 새 스테이지를 작성한 뒤 미리보기·검증·등록·빌드까지 어떤 경로를 거치는지 적는다. 작업자가 두 번째 스테이지를 만들 때 수정하는 파일과 공용 코드의 범위를 확인한다.
- 표시 이름을 바꾼 스테이지, 기존 저장에서 참조하는 스테이지를 삭제하는 경우, 배포에 포함된 선택 팩이 빠지는 경우 중 지원 범위에 해당하는 변경을 추적한다. 보존할 ID와 이전 데이터의 처리를 정하고 실패한 가져오기·발행·갱신에서 복구할 상태를 명시한다.
- 프로젝트가 감당할 유지보수 비용을 검토한다. 시트는 수정 이력과 검토 비용, 에셋은 병합 충돌과 참조 오류, 생성기는 재현과 폐기 비용, DB는 쓰기 충돌과 스키마 변경 비용이 판단 기준이다. [콘텐츠 확장 경로](../../skills/vegabond-code-design/references/gameplay-framework.md#give-content-an-extension-path) · [프로젝트 검증 지침](../../skills/vegabond-code/references/verification.kr.md)
