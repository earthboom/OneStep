---
id: R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS
title: 빌드할 프로젝트를 연 에디터가 없는데도 Live Coding 때문에 Unreal 빌드가 거부됐다
summary: UnrealBuildTool 은 프로젝트가 아니라 에디터 실행 파일 경로로 만든 이름 있는 뮤텍스를 확인한다. 그래서 같은 엔진을 쓰는 다른 체크아웃의 에디터가 Live Coding 중이면 그 엔진의 모든 프로젝트 빌드가 막힌다. 그 에디터를 닫거나, 독립 빌드가 목적일 때 -NoHotReloadFromIDE 로 빌드한다.
kind: error
scope: 여러 프로젝트 체크아웃이 엔진 설치나 소스 빌드 하나를 같이 쓰는 Windows 의 UnrealBuildTool
keywords: [UnrealBuildTool, UBT, Live Coding, LiveCoding, "Unable to build while Live Coding is active", named mutex, "Global\\LiveCoding_", HotReload.cs, "-NoHotReloadFromIDE", bAllowHotReloadFromIDE, shared engine, multiple checkouts, Build.bat]
status: resolved
checked_at: 2026-11-24
context:
  engine: "Unreal Engine 5.8 소스 빌드"
  platform: Windows 11
trigger: 같은 엔진을 쓰는 다른 프로젝트 체크아웃의 에디터가 Live Coding 을 켠 채 실행 중일 때 명령줄로 에디터 타깃을 빌드함
symptom: "대상 체크아웃을 연 에디터가 없는데도 UBT 가 \"Unable to build while Live Coding is active\" 로 멈춘다"
cause_status: confirmed
prevention: 명령줄 빌드 전에 같은 프로젝트만이 아니라 같은 엔진 실행 파일을 쓰는 에디터가 떠 있는지 본다. 닫거나, 그 에디터에 영향을 주지 않아야 하는 빌드일 때만 -NoHotReloadFromIDE 를 준다
prevention_status: proposed
---

## Expected and observed

한 체크아웃에서 코드만 다시 빌드하는 에디터 빌드를 시작했다. 그 체크아웃을 연 에디터는 없었다. 기대: 보통 빌드. 관측: UBT 가 `Unable to build while Live Coding is active` 로 거부했다. 같은 엔진 빌드를 쓰는 같은 게임의 두 번째 체크아웃 에디터가 실행 중이었다.

## Cause and resolution

UBT 소스로 확인했다. Live Coding 점검은 `Global\LiveCoding_` 뒤에 에디터 실행 파일 경로를 붙인 이름의 뮤텍스를 연다. 이름에 프로젝트 경로가 없으므로 그 엔진 실행 파일의 어떤 Live Coding 세션이든 걸린다. 다른 체크아웃의 에디터를 닫자 뮤텍스가 풀렸고 같은 빌드가 성공했다.

UBT 소스에 따르면 IDE 에서의 핫 리로드를 끄면 이 점검을 건너뛴다 (`bAllowHotReloadFromIDE`, 명령줄 `-NoHotReloadFromIDE`). 이 우회는 읽기만 하고 실행하지 않았다. 다른 에디터가 살아 있는 동안 쓰면, 두 쪽이 출력 바이너리를 같이 쓸 때 그 에디터가 올린 모듈이 낡은 상태로 남는다.

## Recheck and prevention

2026-11-24 에 다른 에디터를 닫은 뒤 빌드가 성공했다. 제안한 점검 (빌드 전에 같은 엔진 실행 파일로 뜬 에디터 프로세스를 찾기) 은 별도 안전장치로 실행하지 않았으므로 제안 상태로 둔다.

엔진 설치가 따로면 실행 파일 경로가 달라 뮤텍스를 같이 쓰지 않는다. 다른 플랫폼 동작은 살펴보지 않았다.

## Evidence

- 엔진 소스, Unreal Engine 5.8: `Engine/Source/Programs/UnrealBuildTool/System/HotReload.cs` (에디터 실행 파일 경로로 만든 Live Coding 뮤텍스 이름 `Global\LiveCoding_`, `bAllowHotReloadFromIDE` 가 참일 때만 확인). `Engine/Source/Programs/UnrealBuildTool/Configuration/BuildConfiguration.cs` (`bAllowHotReloadFromIDE` 에 붙은 `[CommandLine("-NoHotReloadFromIDE", Value = "false")]`).
- 세션 관측, 2026-11-24: 거부된 빌드, 다른 체크아웃의 에디터 프로세스, 그 에디터를 닫은 뒤 성공한 재빌드.
