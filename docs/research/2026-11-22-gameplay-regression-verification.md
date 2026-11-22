# Unity·Unreal 게임플레이 회귀 검증 기본 규칙

2026-11-22 · AI 코드 변경, 스테이지 추가, 저장 호환성, 실제 빌드 검증

**변경하기 전에 유지할 플레이 동작과 관찰 지점을 정한다.** 공용 코드를 수정할 때는 영향을 받는 기존 스테이지에서 그 동작을 확인한다. 스테이지를 추가할 때는 새 콘텐츠가 실제 게임에서 열리고 끝나는 흐름과, 같은 규칙·부품·진행표를 쓰는 기존 콘텐츠를 확인한다. 테스트는 플레이어가 보는 결과와 규칙이 확정한 상태를 비교할 수 있어야 한다. [게임 개발 기본 전략](../designs/game-development-strategy.md) · [테스트 오라클 연구](https://web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf)

이 문서는 조사와 설계 기준이다. 엔진에서 실행한 결과나 성능 측정값을 포함하지 않는다. 도구 선택은 프로젝트가 사용 중인 엔진·패키지 버전, 타깃 기기, 지원하는 로컬·네트워크 구성을 기준으로 한다. [AI 코드 변경 품질 연구](2026-11-21-ai-codebase-quality.md) · [스테이지 프레임워크 연구](2026-11-22-stage-content-framework.md)

## 1. 연구와 제작 경험에서 가져올 원칙

| 자료 | 적용할 판단과 적용 범위 |
| --- | --- |
| **Barr 외, 테스트 오라클 연구, IEEE TSE** | 실행 결과가 맞는지 판단하는 기준은 입력을 실행하는 방법과 별개다. 사양, 잘 알려진 사례, 상태 사이 관계, 사람의 검토를 각 상황에 사용한다. 게임에 적용하면 AI가 수정 후 출력에서 기대값을 그대로 복사해 놓는 일을 피할 수 있다. [논문](https://web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf) |
| **Claessen·Hughes, QuickCheck, ICFP 2000** | 개별 정답 입력 외에도 시간·비용·상태를 제한하는 속성을 선언하고 생성한 입력으로 검사한다. 예를 들어 무효 이동 후 턴·재화·보드 상태가 같아야 한다는 계약이다. 속성 검사에서 통과한 입력의 범위는 생성 규칙이 정한다. [논문](https://www.cs.tufts.edu/comp/150FP/archive/john-hughes/quick.pdf) |
| **Rothermel·Harrold, 회귀 테스트 선택 연구, 1997 · Yu 외, GameRTS, ICSE 2023** | 전자는 소프트웨어 변경을 이용해 실행할 기존 테스트를 선택한다. 후자는 기록된 게임 상태·행동·경로를 추상화해 비디오 게임 사례에 적용했다. 실무에서는 코드 호출자와 함께 에셋 참조·등록·진행 경로를 확인해 대표 검증을 고르고, 영향이 불명확하면 인접한 흐름까지 넓힌다. 연구의 선택률과 검출률은 연구 대상과 관찰할 수 있는 경로에 한정된다. [회귀 테스트 선택 논문](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/p173-rothermel.pdf) · [GameRTS 논문](https://ttfish.cc/content/Papers/icse23.pdf) |
| **Luo 외, 불안정한 테스트 연구, FSE 2014** | 비동기 대기, 실행 순서 의존, 동시성은 연구가 분석한 주요 원인이다. 씬 준비 신호를 기다리고 매 실행에 저장·월드·옵션을 초기화한다. 진단용 재실행은 첫 실패의 환경과 결과를 보존한다. [논문](https://mir.cs.illinois.edu/~marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf) |
| **Ostrowski·Aroudj, 게임 회귀 자동화, 2013 · Balyo 외, 게임 회귀 계획·학습 연구, 2024** | 입력의 기록·재생을 게임 스크립트와 결합하거나, 상세 로그로 게임 규칙 모델을 만들어 탐색하는 접근이다. 두 번째 연구의 Unity RPG는 개념 증명이다. 팀에서는 이미 중요한 플레이 경로를 재현할 수 있도록 입력·초기 상태·결과 기록부터 갖추는 편이 도입하기 쉽다. [기록·재생 연구](https://link.springer.com/article/10.7603/s40601-013-0010-4) · [계획·학습 연구](https://arxiv.org/abs/2402.12393) |
| **Rare, Sea of Thieves · Mojang, Minecraft, GDC** | Rare는 팀원이 작성할 수 있는 게임플레이 자동화와 테스트별 적정 범위를 발표했다. Mojang 발표는 방식을 다른 게임과 팀에 적용하면서 얻은 교훈을 다룬다. 테스트 저작에 드는 비용, 환경 재현, 실패 원인을 찾는 시간이 함께 중요하다. [Rare 발표 영상](https://www.gdcvault.com/play/1026366/Automated-Testing-of-Gameplay-Features) · [Rare 발표 자료](https://media.gdcvault.com/gdc2019/presentations/Masella_Robert_AutomatedTestingOf.pdf) · [Minecraft 발표 영상](https://gdcvault.com/play/1027345/Lessons-Learned-in-Adapting-the) |
| **Ubisoft, The Division, GDC 2019** | AI 플레이어를 미션 완주·성능 데이터 수집·멀티플레이 작업·버그 재현에 사용했다. 봇은 오래 플레이하거나 여러 경로를 반복 확인할 때 적합하다. 기존 판정의 보존 여부를 알려면 봇이 무엇을 했고 어떤 결과가 나와야 하는지 함께 기록해야 한다. [발표 영상](https://www.gdcvault.com/play/1026382/Automated-Testing-Using-AI-Controlled) · [발표 자료](https://media.gdcvault.com/gdc2019/presentations/Paredes_Jose_AutomatedTestingUsing.pdf) |
| **Riot, League of Legends 결정성과 Chronobreak** | 동일 입력에서 게임에 중요한 서버 상태가 갈라지는 첫 지점을 찾는 방법을 공개했다. 측정 범위와 로그 비용을 선택하는 실무 사례다. 게임 전체에서 플랫폼 간 완전한 결정성 확보는 별도의 기술 결정이다. [구현 경험](https://www.riotgames.com/en/news/determinism-league-legends-implementation) · [상태 차이 추적](https://www.riotgames.com/en/news/determinism-league-legends-fixing-divergences) |
| **Kalibera·Jones, 성능 변화와 측정 불확실성** | 반복 측정의 변동을 감안해 개선·악화 크기를 해석한다. 게임에서도 동일 조건의 기준 빌드와 후보를 비교하고, 기기·빌드·실행 사이의 변동을 함께 기록한다. [논문](https://arxiv.org/abs/2007.10899) |

## 2. 프로젝트 시작 때 확보할 최소 검증 기준

1. **대표 플레이를 고른다.** 장르의 핵심 루프 하나와 품질을 깨뜨리기 쉬운 중단·오류 하나를 적는다. 예를 들어 퍼즐은 `선택 → 한 번 밀기 → 클리어`와 `무효 입력 → 재시작`, 협동은 `진입 → 역할 수행 → 보상`과 `로딩·전투 중 이탈 → 재접속`이다. 게임이 지원하는 기능을 기준으로 범위를 늘린다. [기본 플레이에서 프레임워크를 도출하는 지침](../../skills/vegabond-code-design/references/gameplay-framework.md#derive-the-framework-from-representative-play)
2. **무엇이 유지되는지 적는다.** 확인점마다 `초기 조건 → 행동 → 플레이어가 볼 결과 → 확정 상태`를 기록한다. 예를 들어 막힌 칸으로 이동을 요청하면 보드와 이동 횟수가 유지되고, 화면은 무효 이동에 대한 피드백을 표시한다. 저장·해금·보상처럼 루프 밖에 영향을 주는 결과만 지정된 소유자에게 기록한다.
3. **그 결과에 독립적인 근거를 둔다.** 승인된 규칙과 사양, 이전에 승인한 플레이, 수정 대상과 독립적으로 계산한 작은 기대값을 사용한다. 의도적인 규칙 변화는 변경할 기대값과 보존할 동작을 나눠 기록한다. 기존 출력에 알려진 결함이 있으면 수정할 행동을 사양에 명시한다. [오라클 연구](https://web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf)
4. **초기 조건과 재현 정보를 남긴다.** 지원 범위 안의 대표 스테이지 ID, 게임·콘텐츠 버전, 시작 상태, 입력 순서, 필요한 시드·틱, 모드와 기기를 기록한다. 저장 호환성이 필요하면 기록용 이전 버전 저장을 유지한다. 재현에 쓰는 사용자 계정과 데이터는 별도의 테스트용으로 관리한다.
5. **관찰할 수 있는 가장 작은 경로부터 사용한다.** 공용 판정은 빠르게 검사하고, 입력·맵·저장·조립이 맞물리는 문제는 실제 진입점에서 확인한다. QA와 디자이너가 게임에서 직접 재현하고 판단할 수 있는 상황에는 플레이 경로와 관찰 기준만으로 시작해도 된다. 반복 비용과 실패 영향이 큰 검증부터 자동화한다. [기존 검증 지침](../../skills/vegabond-code/references/verification.md) · [Rare 자동화 사례](https://www.gdcvault.com/play/1026366/Automated-Testing-of-Gameplay-Features)

다음과 같은 작은 계약은 게임 브리프와 테스트에서 공통으로 쓸 수 있다.

| 예시 | 처음 상태와 입력 | 유지할 결과 |
| --- | --- | --- |
| **기존 밀기 규칙** | 정식 메뉴에서 `warehouse-03` 진입. 상자 뒤가 비어 있는 위치에서 한 번 밀고, 막힌 위치에서 다시 밀기를 요청 | 첫 행동은 상자 위치와 이동 횟수를 바꾼다. 막힌 행동은 둘을 유지한다. 재시작 후 보드·이동 횟수가 초기 상태로 돌아온다. |
| **새 스테이지 등록** | 기존 진행이 포함된 지원 버전 저장을 로드하고, 스테이지 순서 사이에 `warehouse-04`를 추가한 빌드에서 새 보드를 선택 | 새 스테이지가 설계한 해금 조건을 따르고 플레이·재시도·클리어할 수 있다. `warehouse-03`의 완료 기록은 이전 ID에서 계속 확인된다. |

## 3. 변경 유형마다 고를 검증 범위

| 변경 | 빠른 검증 | 통합 경로에 남길 확인 |
| --- | --- | --- |
| **기존 규칙으로 새 스테이지 추가** | ID·참조·필수 마커·진행 조건을 검사한다. 퍼즐은 해결 입력, 레이싱은 체크포인트를 거치는 완주, 전술은 목표와 배치의 유효성을 확인한다. | 게임의 목록·해금 → 입장 → 재시도 또는 종료 → 결과 기록을 따라간다. 같은 부품·진행표를 쓰는 기존 스테이지를 하나 골라 영향 가능성을 확인한다. 새 씬·맵이나 팩을 넣었다면 대상 빌드에서 연다. |
| **공용 규칙 또는 상태 수명 수정** | 변경된 규칙의 정상·무효·경계 입력과 유지할 규칙을 확인한다. 재시도·중단·두 번째 진입 뒤 상태가 새로 만들어지는지 검증한다. | 기존 사용처 중 규칙을 다르게 조합하는 대표 스테이지를 확인한다. 공용 전투·이동·저장·로드처럼 호출 범위가 넓으면 동작이 다른 기존 호출자와 실패 경로로 넓힌다. |
| **기존 스테이지·프리셋 수정** | 바뀐 배치와 목표를 검사하고, 공용 에셋이나 규칙을 참조하는 다른 스테이지를 조사한다. | 이전 풀이·진행·타임어택 기록에 영향이 있는지 확인한다. 의도적으로 호환성을 끊는 경우 기록 표시·새로 시작·이전 경로 중 프로젝트의 정책대로 동작하는지 본다. |
| **진행·저장·콘텐츠 카탈로그 변경** | 대표 예전 저장을 복제해 읽고 재저장한 뒤 다시 읽는다. 표시명과 순서 변경, 폐기·대체 ID의 처리를 확인한다. | 선택 팩 누락, 로딩 취소, 잘못되거나 지원 범위 밖인 저장, 같은 저장을 다시 변환하는 경우 중 해당 시나리오를 검증한다. 정상 완료 이력과 새 진행이 남는지 확인한다. [OneStep 저장 기술](../../knowledge/game/K-GAME-TECH-SAVE.md) |
| **렌더링·스트리밍·AI 비용 수정** | 화면 밖에서 계속 유지돼야 하는 상태를 확인하고, 새 로딩·갱신 경계의 시작·종료를 계측한다. | 같은 빌드 설정·기기·콘텐츠에서 대표 동선을 반복한다. 프레임·메모리 추세와 함께 로딩 후 NPC 상태, 되돌아왔을 때 월드 결과, 필요한 화면·조작의 변화를 본다. |
| **멀티플레이 권한·이동·보상 변경** | 누가 판정하는지, 동시에 요청하거나 재전송할 때 결과가 몇 번 반영되는지 확인한다. | 지원하는 호스트·전용 서버 역할에서 복수 클라이언트를 쓴다. 지연·손실이나 재접속에서 권한 상태와 각자 보이는 결과를 비교한다. |

범위는 **코드 호출자, 프리팹·Blueprint·씬·맵 참조, 카탈로그·진행, 런타임 구독·정리, 배포 구성**에서 찾아낸다. 변경한 파일 이름만으로는 공유 프리셋과 해금표를 함께 쓰는 기존 경로를 알기 어렵다. 매 변경에는 관련 경로를 빠르게 얹고, 대표 빌드·기기와 장시간 경로는 팀의 일정에 따라 통합 검증 또는 출시 후보에서 실행한다. 실제 위험이나 지원 구성에 맞춰 주기를 선택한다. [회귀 테스트 선택 연구](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/p173-rothermel.pdf) · [기능 의존성 검토](../../skills/vegabond-code-design/references/gameplay-framework.md#make-feature-dependencies-explicit) · [에셋과 진행 구조](2026-11-22-stage-content-framework.md#6-자동-검증과-제작-검토)

## 4. Unity와 Unreal에서 같은 증거를 얻는 경로

| 검증 층 | Unity | Unreal Engine |
| --- | --- | --- |
| **규칙과 데이터** | 엔진과 분리된 게임 규칙·저장 변환은 Edit Mode에서 검사한다. 에디터에서 스테이지 정의·참조·ID와 배포 목록을 확인한다. [Unity Test Framework 모드](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/edit-mode-vs-play-mode-tests.html) | 프로젝트 설정을 기준으로 순수 C++ 책임은 Low-Level Tests(Catch2) 또는 모듈에 맞는 Automation Test로 확인한다. Data Validation으로 에디터와 커맨드릿에서 에셋 규칙을 검사할 수 있다. [Low-Level Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/write-low-level-tests-in-unreal-engine) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) |
| **실제 씬·입력·월드 조립** | Play Mode에서 게임 시작 씬과 콘텐츠를 로드하고, 상태 준비를 기다린 뒤 실제 입력·명령 경로를 써서 결과를 확인한다. Input System의 `InputTestFixture`로 격리된 입력 테스트가 가능하다. 실제 기기·프로젝트별 입력 등록은 해당 Player 경로에서 확인한다. [Play Mode](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/edit-mode-vs-play-mode-tests.html) · [Input Test Fixture](https://docs.unity3d.com/Packages/com.unity.inputsystem%401.11/manual/Testing.html) | Automation Framework와 Functional Testing으로 레벨·Actor·권한 환경을 조립한다. 레벨 스트리밍·연결을 시작하고 `IsReady`에서 준비 여부를 확인할 수 있다. 대표 흐름은 실제 입력·명령 또는 메뉴가 호출하는 동일한 경로를 지난다. [Automation Test Framework](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine) · [Functional Testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine) |
| **Player·패키지와 네트워크** | 지원 플랫폼에서 standalone Play Mode 테스트용 Player 또는 프로젝트의 플레이 자동화로 확인한다. 출시 후보의 씬·번들·스크립팅 설정을 확인하는 검증은 해당 설정으로 별도 실행한다. 복수 Player와 필요한 연결 장애를 시험한다. [Player 테스트 워크플로](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/workflow-run-playmode-test-standalone.html) · [Network Simulator](https://docs.unity3d.com/Packages/com.unity.multiplayer.tools%402.2/manual/network-simulator.html) | 대상 패키지를 실행해 맵 cook과 에셋 로드, 메뉴와 종료까지 확인한다. Gauntlet은 서버와 클라이언트 같은 프로세스 세션을 띄우고 결과를 수집할 때 사용한다. 네트워크 에뮬레이션으로 지원되는 지연·손실 항목을 검사할 수 있다. [Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine) · [네트워크 에뮬레이션](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-network-emulation-in-unreal-engine) |
| **계측과 진단** | Player의 Profiler 데이터를 수집한다. 반복 측정에는 필요한 경우 Performance Testing 패키지를 사용한다. 기기, 품질 설정, 빌드 방식, 옵션을 기록한다. [Player 프로파일링](https://docs.unity3d.com/6000.0/Documentation/Manual/profiler-profiling-applications.html) · [프레임 측정 API](https://docs.unity3d.com/Packages/com.unity.test-framework.performance%403.0/manual/measure-frames.html) | Unreal Insights에서 타이밍·메모리·네트워크에 필요한 트레이스를 선택한다. 화면 비교는 기준 이미지와 조건을 고정하고, 편차 허용 범위를 화면의 용도에 맞춘다. [Unreal Insights](https://dev.epicgames.com/documentation/unreal-engine/unreal-insights-in-unreal-engine) · [Screenshot Comparison](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine) |

결과 보고에는 실행 환경을 함께 표시한다. `Edit Mode`, `Editor Play Mode/PIE`, `게임용 Player·패키지`, `실기기`는 가능한 검증이 각각 다르다. 그래픽·타이밍·실물 컨트롤러처럼 환경에 의존하는 품질은 해당 모드와 기기에서 확인한다. 엔진 진입점에서 준비·완료 신호를 관찰할 수 있게 하고, 숨은 테스트 전용 초기화가 실제 게임의 초기화를 건너뛰는지 검토한다.

## 5. 재현, 시각과 성능 품질

- **기록·재생 범위를 고른다.** 결정적인 턴·퍼즐 규칙은 고정 입력 순서에서 턴 번호, 보드 위치, 목표 완료, 보상 ID를 비교한다. 물리·시간·스케줄이 달라질 수 있는 실시간 게임은 지원 조건을 명시하고 체크포인트 순서, 결과 상태, 위치·시간의 의미 있는 허용 범위를 검사한다. 서버 재접속이라면 클라이언트 화면과 서버 권한 상태를 적절한 완료 시점에서 비교한다. 차이가 생기면 첫 확인점의 입력과 필드 차이를 기록한다. [Riot 결정성 구현](https://www.riotgames.com/en/news/determinism-league-legends-implementation) · [Riot 상태 차이 추적](https://www.riotgames.com/en/news/determinism-league-legends-fixing-divergences)
- **불안정한 테스트를 진단한다.** 임의로 몇 초씩 기다리기 전에 월드 준비·복제 확인·권한 상태 확정 같은 의미 있는 신호와 제한 시간을 사용한다. 사례별 저장·난수·시간·구독·오브젝트를 초기화하고 첫 실패의 로그와 상태를 보관한다. 재실행에서 통과해도 첫 실패는 조사 대상으로 남긴다. 원인이 환경·테스트·게임 중 어디인지 구분하고, 불안정한 항목을 분리 실행한다면 담당자와 복귀 조건을 기록한다. [Luo 외 연구](https://mir.cs.illinois.edu/~marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf) · [Unreal Functional Testing의 준비 단계](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine)
- **시각과 조작감의 평가 지점을 고른다.** 비교 이미지에는 플랫폼·해상도·렌더링 설정·카메라·캡처 시점을 기록한다. 사진에서 확인할 수 있는 레이아웃과 마커 위치는 자동 비교할 수 있다. 카메라 추적, 타격의 피드백, 목표를 처음 알아차리는 순간은 짧은 대표 플레이와 사람의 평가를 함께 사용한다. 이미지 허용 오차나 기준 이미지를 바꾸면 실제 바뀐 모습을 검토한다. [Unreal Screenshot Comparison](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine) · [게임 파라미터 자동 플레이테스트 연구](https://sites.cc.gatech.edu/fac/riedl/pubs/zook-fdg14.pdf) · [플레이테스트 방식 선택](../../knowledge/game/K-GAME-PROTOTYPE-PLAYTEST.md)
- **성능 변화와 흔들림을 함께 본다.** 지원 기기와 비교 빌드, 해상도·품질·캡처 범위, 대표 부하를 고정한다. 첫 진입과 반복 진입을 구분하고 실행을 여러 번 측정한다. 목적에 맞춰 프레임 시간 중앙값과 상위 분위수, 긴 프레임 빈도, 로드 시간, 메모리 최고치와 반복 전환 뒤 상주량을 기록한다. 경계값은 목표 기기와 장르의 프레임·메모리·로드 예산에 근거해 미리 정한다. 변화가 실행 간 변동과 비슷하면 결론을 보류하고 흔들림 원인을 살핀다. [측정 불확실성 연구](https://arxiv.org/abs/2007.10899) · [게임 개발의 성능·스트리밍 연구](2026-11-22-game-development-practices.md)

## 6. AI에게 맡길 때의 기본 작업 규칙

| 시점 | 확인할 약속과 남길 근거 |
| --- | --- |
| **작업 전** | 의도한 변화, 유지할 플레이 결과, 현재 시작·판정·저장 위치, 대표 기존 콘텐츠를 작업에 명시한다. 재현 가능한 버그 수정에는 수정 전 실패 조건을 남긴다. 의도하지 않은 기존 실패도 기준 실행과 후보 실행에서 구분한다. |
| **구현 설계 검토** | 기존 테스트와 기존 진입점을 사용한다. 새 스테이지 문제를 해결하려고 공용 규칙을 바꾸는 경우 다른 사용처에 필요한 계약을 확인한다. 테스트를 추가할 때는 기존 검증으로 잡지 못하는 구체적인 회귀를 고른다. |
| **결과 판단** | 검증의 기대값, 허용 오차, 저장 예시나 기준 화면을 변경했으면 어떤 게임 규칙·디자인이 그 변경을 요구했는지 관련 차이와 함께 검토한다. 테스트 누락, 비활성화, 성공 조건 완화가 결과에 미치는 영향을 확인한다. |
| **완료 기록** | 대상 변경, 실행한 검증, 환경과 빌드·콘텐츠 버전, 결과, 남은 영역을 적는다. 설계 완료, 실행 통과·실패, 실행 대상에서 제외, 실행 불가를 구분한다. 플레이 검증 증거는 실제로 수행한 경로와 설정의 범위에서 보고한다. |

AI가 코드를 바꾸면서 테스트를 함께 편집하는 작업에는 변경 전 승인된 결과, 독립적으로 확인 가능한 규칙, 이전 저장·정답 입력 같은 증거를 붙인다. 검증 기준을 변경했다면 코드 변경과 함께 그 의미가 검토 가능해야 한다. 예를 들어 퍼즐의 정답 경로를 의도적으로 바꾼 작업은 새 정답과 이전 해법의 처리 정책을 각각 기록한다. [AI 코드 변경 품질 연구](2026-11-21-ai-codebase-quality.md) · [콘텐츠로 검토하는 설계 지침](../../skills/vegabond-code-design/references/gameplay-framework.md#review-the-change-through-content-and-play) · [검증 절차](../../skills/vegabond-code/references/verification.md)

작업 기록의 한 줄은 `변경 → 실행 환경 → 스테이지·시작 상태 → 입력 → 예상 결과 → 관찰 결과·차이 → 근거 위치`로 작성할 수 있다. 예를 들어 새 스테이지의 메인 메뉴 진입 확인은 대상 패키지와 목록에 쓰인 `StageId`, 해금에 사용한 저장을 연결한다. 설계 단계에서는 예상 결과와 확인할 조건까지만 기록한다.

## 7. 장르별 검증 설계 예시

| 게임과 변경 | 기존 품질을 확인하는 대표 플레이 | 함께 남길 관찰 |
| --- | --- | --- |
| **퍼즐에 기존 규칙으로 새 보드 추가** | 출시 목록에서 열어 풀이 입력을 재생한다. 재시작하고 기존 보드 하나에서 같은 밀기 규칙을 확인한다. 지원하는 이전 저장에서 스테이지 순서 변경 후 완료 기록을 확인한다. | 스테이지 ID, 클리어 여부, 중요 타일·기물의 위치, 완료·해금 ID |
| **레이싱에서 체크포인트 공용 코드 변경** | 기존의 단선·분기 지원 조건을 따라 대표 트랙을 고르고, 정상 완주·건너뛰기·리스폰 후 재진입·역주행을 확인한다. 예전 고스트의 재사용은 프로젝트의 기록 호환 정책을 기준으로 본다. | 확인된 체크포인트 순서와 랩 판정, 기록 저장 결과, 타이밍 오차 기준 |
| **턴제 전술에서 명령 처리 변경** | 같은 초기 배치와 명령으로 기존 미션을 확인한다. 무효 명령, 적 턴, 승리와 실패 조건이 동시에 발생하는 경우의 우선순위를 본다. | 행동력·턴 순서·목표 결과, 상태가 갈라진 첫 명령 |
| **협동에서 권한 또는 재접속 수정** | 프로젝트가 지원하는 구성으로 호스트·서버와 복수 클라이언트를 띄운다. 목표 달성 직전 또는 보상 처리 직후 연결을 끊고 다시 참가시킨다. | 플레이어·아바타 연결, 서버 확정 목표·인벤토리, 보상 중복 여부와 클라이언트 표시 |
| **월드 스트리밍 또는 화면 밖 AI 변경** | 대표 기기에서 `마을 → 숲 → 교전 → 복귀`를 실행하고, 같은 NPC ID가 화면을 벗어났다 돌아온 뒤 필요한 결과를 유지하는지 확인한다. | NPC 생존·퀘스트 상태, 첫 로드·반복 진입 시간, 긴 프레임, 복귀 뒤 자원 상주량 |

추가로 필요한 검증은 프로젝트의 계약에서 도출한다. 예를 들어 저장 기능이 없는 퍼즐은 클리어 후 목록 복귀를 확인하고, 시즌별 기록을 유지하는 게임은 이전 시즌 결과를 이어서 읽는 경로를 포함한다. 초기에는 기존 콘텐츠의 핵심 성공 경로 한 개, 중단 또는 실패 경로 한 개, 지원 구성에서 새 콘텐츠를 여는 경로부터 정한다. 그다음 반복하는 작업이 늘어날 때 패키지·호환성·성능 자동화의 범위를 넓힌다.
