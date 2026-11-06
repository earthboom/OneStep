---
id: K-CODE-UE-LOCAL-ONLY-WORK
title: 공유 DDC와 분산 컴파일 경로를 확인해 언리얼 에디터 작업을 로컬에만 둔다
summary: 로컬에서 실행한 언리얼 빌드나 에디터도 공유 DDC, UBA/Horde 원격 컴파일, Incredibuild 셰이더 컴파일로 팀 인프라에 닿을 수 있다. User*.ini 오버라이드로 체크아웃별로 공유 DDC를 끄고, 각 경로를 로그로 확인한다.
kind: method
scope: 공유 DDC와 분산 컴파일 에이전트가 있는 스튜디오 네트워크의 언리얼 엔진 5 프로젝트에서 작업을 로컬 머신에만 두어야 할 때
keywords: [Unreal Engine, DDC, Derived Data Cache, shared DDC, UserEngine.ini, UnrealBuildTool, UBA, Horde, Incredibuild, XGE, distributed compile, local only]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5.8 source build
  platform: Windows desktop
---

## 지침

작업을 로컬 머신에만 두어야 하면, 에디터 빌드나 에디터 세션이 팀 인프라에 닿는 경로를 하나씩 확인한다. 로컬 명령이 로컬에 머문다고 가정하지 않는다.

1. 공유 DDC. `<Project>/Config/UserEngine.ini`를 만들고 `[DerivedDataCacheStores]` 아래에 `Shared=(Type=FileSystem, Path=None)`를 적어 체크아웃 하나에서만 끈다. 저장소 이름은 프로젝트 `DefaultEngine.ini`가 쓰는 이름을 따른다. `.git/info/exclude`(`<Project>/Config/User*.ini`)로 이 파일을 버전 관리에서 빼 팀에는 아무것도 바뀌지 않게 한다. 에디터를 시작하면 `LogDerivedDataCache`가 `Shared: Disabled because the path is configured to 'None'`를 찍어야 한다.
2. C++ 컴파일. UnrealBuildTool은 사용자별 `%APPDATA%\Unreal Engine\UnrealBuildTool\BuildConfiguration.xml`을 읽는다. `<Horde>` 서버와 `bAllowUBAExecutor`가 있으면 컴파일 작업이 원격 에이전트로 간다. 빌드 출력에서 `RemoteExecutor:`와 `Horde URL:`을 찾는다.
3. 셰이더 컴파일. 에디터 로그에 `Using XGE Controller for shader compilation`이 찍히고 Incredibuild(`xgConsole.exe`)가 설치되어 있으면 셰이더 작업이 Incredibuild 에이전트로 갈 수 있다. `LogUbaHorde: ... Not Enabled`는 UBA만 다루며 Incredibuild는 다루지 않는다.

작업이 로컬에만 있다고 말하기 전에, 아직 켜져 있는 경로를 모두 보고한다.

## 적용 범위와 예외

공유 DDC, Horde/UBA, Incredibuild가 있는 스튜디오 구성에 해당한다. 이것들이 없는 머신에는 확인할 것이 없다. `User*.ini` 계층(GameDirUser)은 그 체크아웃에만 영향을 준다. 로컬 DDC(엔진 `DerivedDataCache` 폴더와 로컬 ZenServer)는 이 머신에서 같은 엔진을 쓰는 다른 프로젝트와 여전히 공유된다. 항목이 내용으로 키가 매겨지므로 문제는 없다.

## 점검

- 에디터 로그에서 DDC 증거 줄은 `LogDerivedDataCache` 범주로 찾는다. 그냥 `Shared:`로 찾으면 `LogEOSShared:` 같은 다른 범주에도 걸린다.
- `git status`가 깨끗하고, `git check-ignore -v`가 오버라이드 파일에 대한 exclude 규칙을 보여 준다.
- 원격 컴파일을 꺼야 하면 빌드 출력에 `RemoteExecutor:` 줄이 없어야 한다.
- 원격 컴파일 에이전트는 CPU만 빌려 주고 공유 파일은 바꾸지 않는다. 사용자가 그것마저 금지하면 빌드가 끝난 뒤가 아니라 시작하기 전에 끈다.

## 근거

Windows의 UE 5.8 게임 프로젝트에서 한 번 관찰했다(2026-11-06). `UserEngine.ini` 오버라이드로 `Shared: Disabled because the path is configured to 'None'`가 찍혔고, `ZenShared`와 `Cloud`는 이미 호스트 `None`으로 꺼져 있었다. 에디터 빌드 작업 549개 중 336개가 Horde UBA 에이전트 네 대에서 돌았다. 명령줄 플래그 없이 사용자 자신의 `BuildConfiguration.xml` 때문이었다. 에디터를 시작하자 셰이더 컴파일러는 XGE 컨트롤러를 골랐고 Incredibuild가 설치되어 있었다. 사용자에게 처음 보고할 때는 로그를 읽기 전에 빌드를 "로컬"이라고 했다가 나중에 바로잡았다.

검증하지 않은 것: 로컬 UBA는 유지하면서 빌드 한 번만 원격 UBA 실행을 끄는 플래그나 설정이 무엇인지, 셰이더 작업이 실제로 원격 Incredibuild 에이전트에 도달했는지.
