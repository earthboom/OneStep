# 영향받는 실제 플레이 경로에서 게임플레이 회귀 검증하기

K-GAME-GAMEPLAY-REGRESSION · 방법 · 적용 중 · 근거 확인 2026-11-22

지원하는 실제 진입점에서 초기 상태와 독립적인 기대 결과를 정하고 중단 경로도 검사한다. 규칙·에셋·진행·배포 의존 관계로 인접 검사 범위를 고른다.

적용 범위 — Unity·Unreal의 게임 규칙, 씬, 패키지, 멀티플레이, 화면 및 성능 검증.

## 적용 방법

대표 성공 경로, 중단 경로, 새 콘텐츠 진입을 고른다. 기준 빌드·콘텐츠 ID, 옵션, 세이브, 난수 시드, 역할, 초기 상태, 입력, 체크포인트별 화면 결과와 권한 상태를 기록한다. 승인된 규칙, 고정 사례, 별도 계산, 합의한 불변식에서 기대값을 구한다. 실행한 경로 수를 남기고 기존 실패는 구분한다. 재생 결과가 달라지면 처음 어긋난 명령과 필드를 추적한다.

호출부·직렬화 참조·구독·팩 등록·해금·배포 구성을 따라간다. 새 퍼즐은 메뉴 진입·해답 재생·재시도와 같은 규칙을 쓰는 기존 판을 확인한다. 레이싱 체크포인트는 정상·건너뛰기·역주행·리스폰과 고스트 정책을 본다. 전술은 행동력·턴 순서·무효 명령·승패 동시 성립을 비교한다. 협동은 보상 확정 전후로 재접속해 서버 상태와 각 클라이언트 표시를 본다. 스트리밍은 같은 NPC에 돌아와 퀘스트와 최초·반복 진입 비용을 확인한다.

Unity는 Edit Mode에서 규칙·데이터, Play Mode에서 입력·씬 조립, Player에서 번들·백엔드·빌드 설정을 확인한다. Unreal은 저수준 또는 Automation 테스트로 규칙, Data Validation으로 에셋, Functional Testing으로 월드 준비를 확인하고 패키지로 쿠킹·메뉴 경로를 연다. Gauntlet으로 서버·클라이언트를 함께 실행할 수 있다. 계약에 필요한 실제 기기 입력과 네트워크도 검사한다.

## 적용 조건과 예외

결정적 턴은 정확한 상태를 비교한다. 실시간 물리는 허용 오차와 지원 실행 조건을 정한다. 봇의 미션 완주는 도달 가능성을 보여 주고, 규칙 판정에는 별도의 기대 근거가 필요하다. 스크린샷 기준은 기기·설정·카메라·캡처 시점을 고정한다. 의도·가독성·조작감은 사람이 플레이해 평가한다. 성능은 반복 동선의 분포와 편차를 보고, 차이가 편차 안에 있으면 판단을 유보한다.

## 확인 방법

준비 신호나 권한 측 확인을 제한 시간과 함께 기다린다. 세이브·시간·시드·구독·월드 객체를 초기화한다. 재실행이 통과해도 첫 실패 로그를 남긴다. 격리한 테스트는 담당자와 복구 조건을 둔다. 단언·픽스처·이미지 오차·필터 변경을 검토하고 대표 검사가 의도적으로 잘못된 후보를 거부하는지 확인한다. 이관은 구버전 읽기·재저장·다시 읽기와 중복 변환·팩 누락을 포함한다.

## 근거

11월 22일 검토는 기대값·속성 연구, 게임별 테스트 선택 연구와 그 대상, 개념 검증 자동화, Rare·Mojang·Ubisoft 제작 사례, Riot의 서버 결정성 작업을 구분했다. 장르별 사례는 로컬 실행 결과가 아닌 검증 설계다.

[스테이지 제작](K-GAME-STAGE-AUTHORING.md) · [세이브 복구](K-GAME-TECH-SAVE.md) · [플레이테스트 선택](K-GAME-PROTOTYPE-PLAYTEST.md)

- [Barr et al., test oracle research, IEEE TSE — Paper](https://web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf) · [Claessen and Hughes, QuickCheck, ICFP 2000 — Paper](https://www.cs.tufts.edu/comp/150FP/archive/john-hughes/quick.pdf) · [Regression test selection paper](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/p173-rothermel.pdf) · [GameRTS paper](https://ttfish.cc/content/Papers/icse23.pdf) · [Luo et al., flaky tests, FSE 2014 — Paper](https://mir.cs.illinois.edu/~marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf)
- [Record and replay research](https://link.springer.com/article/10.7603/s40601-013-0010-4) · [Planning and learning research](https://arxiv.org/abs/2402.12393) · [Rare talk video](https://www.gdcvault.com/play/1026366/Automated-Testing-of-Gameplay-Features) · [Rare presentation materials](https://media.gdcvault.com/gdc2019/presentations/Masella_Robert_AutomatedTestingOf.pdf) · [Minecraft talk video](https://gdcvault.com/play/1027345/Lessons-Learned-in-Adapting-the)
- [Ubisoft, The Division, GDC 2019 — Talk video](https://www.gdcvault.com/play/1026382/Automated-Testing-Using-AI-Controlled) · [Presentation materials](https://media.gdcvault.com/gdc2019/presentations/Paredes_Jose_AutomatedTestingUsing.pdf) · [Implementation account](https://www.riotgames.com/en/news/determinism-league-legends-implementation) · [Tracing state divergences](https://www.riotgames.com/en/news/determinism-league-legends-fixing-divergences) · [Kalibera and Jones, performance changes and measurement uncertainty — Paper](https://arxiv.org/abs/2007.10899)
- [Unity Test Framework modes](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/edit-mode-vs-play-mode-tests.html) · [Low-Level Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/write-low-level-tests-in-unreal-engine) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Input Test Fixture](https://docs.unity3d.com/Packages/com.unity.inputsystem%401.11/manual/Testing.html) · [Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine)
- [Functional Testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine) · [Player test workflow](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/workflow-run-playmode-test-standalone.html) · [Network Simulator](https://docs.unity3d.com/Packages/com.unity.multiplayer.tools%402.2/manual/network-simulator.html) · [Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine) · [Network emulation](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-network-emulation-in-unreal-engine)
- [Player profiling](https://docs.unity3d.com/6000.0/Documentation/Manual/profiler-profiling-applications.html) · [Frame measurement API](https://docs.unity3d.com/Packages/com.unity.test-framework.performance%403.0/manual/measure-frames.html) · [Unreal Insights](https://dev.epicgames.com/documentation/unreal-engine/unreal-insights-in-unreal-engine) · [Screenshot Comparison](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine)
- [Automated playtesting of game parameters](https://sites.cc.gatech.edu/fac/riedl/pubs/zook-fdg14.pdf)
