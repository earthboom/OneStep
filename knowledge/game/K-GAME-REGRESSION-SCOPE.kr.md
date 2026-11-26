---
id: "K-GAME-REGRESSION-SCOPE"
title: "영향받는 플레이 경로로 게임플레이 회귀 검증 범위를 정한다"
summary: "공유 규칙, 콘텐츠 등록, 호환성과 런타임 조립을 검사한다. 독립적으로 정한 기대값을 화면 결과와 확정된 게임 상태에 대조한다."
kind: "method"
scope: "Unity·Unreal 게임플레이 변경, 새 콘텐츠, 출시 저장, 멀티플레이와 성능 변경"
keywords: ["gameplay regression","test oracle","Unity Play Mode","Unreal Functional Testing","packaged build","replay","snapshot comparison","게임플레이 회귀","패키지 검증","회귀 테스트","스테이지 검증"]
status: "active"
checked_at: "2026-11-26"
---

# 영향받는 플레이 경로로 게임플레이 회귀 검증 범위를 정한다

## 지침

스테이지·빌드 버전, 초기 상태, 입력, 플레이어에게 보이는 결과와 확정 상태를 기록한다. 승인된 규칙, 인정된 표본 또는 독립 계산으로 기대값을 정한다. 변경 전 실패와 단언, 허용 오차, 표본, 비활성화 검사, 기준 이미지 변경의 이유를 남긴다.

- **공유 규칙이나 수명 변경.** 대표 기존 스테이지에서 유효·무효·경계 입력과 재시도·재진입을 실행한다. 코드, 씬·맵, 프리팹·블루프린트, 카탈로그, 구독과 배포 설정에서 영향받는 호출자를 찾는다.
- **콘텐츠 추가나 수정.** ID, 참조와 장르 규칙을 검사한다. 배포 빌드의 실제 목록 → 해금 → 진입 → 재시도 또는 퇴장 → 완료 경로를 따른다. 프리셋이나 진행표를 공유하는 기존 스테이지도 검사한다. 필요한 경우 과거 풀이·고스트를 실행하고 영향을 받는 기록의 처리 정책을 확인한다.
- **호환성과 권한.** 지원하는 이전 저장을 읽고 저장한 뒤 다시 읽는다. 이관을 반복하고 누락 팩, 로드 취소, 미지원 저장을 시험한다. 온라인 보상은 완료 직전과 승인 직후 연결을 끊고 권한 상태와 클라이언트 표시에서 보상 누락·중복을 확인한다.

## 적용 범위와 예외

주장하는 결과를 보여 줄 수 있는 가장 작은 실행 환경에서 시작한다. 콘텐츠 배포, 플랫폼 입력, 네트워크, 성능에 의존하면 대상 빌드에서도 확인한다.

| 확인할 결과 | Unity | Unreal |
| --- | --- | --- |
| 규칙, 변환과 에셋 유효성 | Edit Mode와 에디터 에셋 검사 | Low-Level Tests 또는 모듈 자동화와 에디터·커맨드릿의 Data Validation |
| 장면, 월드와 입력 연결 | 준비 신호를 기다린 뒤 Play Mode의 실제 입력·명령 경로. 격리 입력은 InputTestFixture. | 의도한 권한 환경과 레벨 준비 상태를 포함한 Automation 또는 Functional Testing |
| 배포 콘텐츠와 기기 및 네트워크 | 배포와 가까운 설정 및 필요한 클라이언트를 사용하는 standalone Player 또는 프로젝트 자동화 | 쿠킹된 에셋과 실제 실행을 위해 패키지 세션 사용. 필요하면 Gauntlet으로 클라이언트와 서버를 제어. |
| 측정 | 대상 Player를 프로파일링하고 같은 경로를 반복 | 필요한 Unreal Insights 트레이스와 고정 조건의 스크린샷 검사 |

## 확인

퍼즐은 정상 밀기, 막힌 밀기와 재시작 뒤 위치와 이동 횟수를 비교한다. 레이싱은 분기, 체크포인트 건너뛰기와 리스폰을 확인하고 과거 고스트를 실행한다. 전술 게임은 행동력, 턴 순서, 목표 동시 충족의 결과를 비교한다. 처음 달라진 지점과 근거 위치를 기록한다. 실행한 경로, 조건과 남은 검사를 적는다. [OneStep 검증 절차](../../skills/vegabond-code/references/verification.kr.md) · [스테이지 호환성](K-GAME-STAGE-COMPATIBILITY.kr.md)

### 재현, 시각과 성능 품질

결정적 규칙은 같은 입력으로 정확한 체크포인트를 비교한다. 실시간 플레이는 허용한 시간·위치 오차 안에서 체크포인트 순서, 게임 상태와 처음 갈라지는 지점을 확인한다. 시간 제한을 두고 월드 준비나 권한 상태 확인을 기다린다. 저장, 난수, 타이머, 구독과 객체를 초기화하고 첫 실패 자료를 남긴다.

비교 캡처에서는 기기, 해상도, 설정, 카메라와 시점을 고정한다. 카메라, 조작감, 목표 발견은 상태·배치 자동 검사와 실제 플레이 관찰을 함께 쓴다. 변경 전후의 부하를 맞추고 첫 진입과 반복을 나눈다. 상위 프레임 시간, 긴 프레임, 로딩과 최고·상주 메모리를 기기 예산과 실행 간 차이에 대조한다. [월드 런타임 예산](K-GAME-WORLD-RUNTIME-BUDGET.kr.md) · [플레이테스트](K-GAME-PROTOTYPE-PLAYTEST.kr.md)

## 근거

테스트 오라클과 QuickCheck는 기대값과 불변 조건을 실행 방식과 구분한다. 회귀 테스트 선별과 GameRTS는 의존성과 관찰 가능한 플레이 경로를 기준으로 검사 범위를 잡는다. Luo 등은 대기나 순서 때문에 흔들리는 테스트를 다룬다. Rare·Mojang·Ubisoft는 제작 자동화 사례를, Riot은 게임 상태가 처음 달라지는 지점을 찾는 방법을 보여 준다. Kalibera와 Jones는 반복 성능 측정의 불확실성을 다룬다. 제안 경로의 결과는 대상 게임과 실행 조건에 달려 있다.

- 방법과 측정 · [테스트 오라클](https://web.eecs.umich.edu/~weimerw/2024-481F/readings/testoracles.pdf) · [QuickCheck](https://www.cs.tufts.edu/comp/150FP/archive/john-hughes/quick.pdf) · [회귀 검사 선별](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/p173-rothermel.pdf) · [GameRTS](https://ttfish.cc/content/Papers/icse23.pdf) · [불안정한 테스트](https://mir.cs.illinois.edu/~marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf) · [기록과 재생](https://link.springer.com/article/10.7603/s40601-013-0010-4) · [RPG 모델 검증 사례](https://arxiv.org/abs/2402.12393) · [자동 플레이테스트](https://sites.cc.gatech.edu/fac/riedl/pubs/zook-fdg14.pdf) · [측정 불확실성](https://arxiv.org/abs/2007.10899)
- 제작 사례 · [Rare 발표](https://www.gdcvault.com/play/1026366/Automated-Testing-of-Gameplay-Features) · [Rare 슬라이드](https://media.gdcvault.com/gdc2019/presentations/Masella_Robert_AutomatedTestingOf.pdf) · [Mojang 발표](https://gdcvault.com/play/1027345/Lessons-Learned-in-Adapting-the) · [Ubisoft 발표](https://www.gdcvault.com/play/1026382/Automated-Testing-Using-AI-Controlled) · [Ubisoft 슬라이드](https://media.gdcvault.com/gdc2019/presentations/Paredes_Jose_AutomatedTestingUsing.pdf) · [Riot 구현](https://www.riotgames.com/en/news/determinism-league-legends-implementation) · [Riot 발산 추적](https://www.riotgames.com/en/news/determinism-league-legends-fixing-divergences)
- Unity · [Edit·Play Mode](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/edit-mode-vs-play-mode-tests.html) · [InputTestFixture](https://docs.unity3d.com/Packages/com.unity.inputsystem%401.11/manual/Testing.html) · [standalone Player 검사](https://docs.unity3d.com/Packages/com.unity.test-framework%401.4/manual/workflow-run-playmode-test-standalone.html) · [네트워크 시뮬레이터](https://docs.unity3d.com/Packages/com.unity.multiplayer.tools%402.2/manual/network-simulator.html) · [Player 프로파일링](https://docs.unity3d.com/6000.0/Documentation/Manual/profiler-profiling-applications.html) · [프레임 반복 측정](https://docs.unity3d.com/Packages/com.unity.test-framework.performance%403.0/manual/measure-frames.html)
- Unreal · [Low-Level Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/write-low-level-tests-in-unreal-engine) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Automation](https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine) · [Functional Testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine) · [Gauntlet](https://dev.epicgames.com/documentation/en-us/unreal-engine/gauntlet-automation-framework-in-unreal-engine) · [네트워크 에뮬레이션](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-network-emulation-in-unreal-engine) · [Unreal Insights](https://dev.epicgames.com/documentation/unreal-engine/unreal-insights-in-unreal-engine) · [스크린샷 비교](https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine)
