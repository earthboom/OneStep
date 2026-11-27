---
id: R-CODE-WAIT-LOOP-SELF-MATCH
title: 프로세스가 끝날 때까지 기다리는 루프가 명령줄 패턴에 자기 셸이 걸려 끝나지 않았다
summary: 프로세스 명령줄이 어떤 문자열과 맞는 동안 기다리는 폴링 루프는 그 문자열을 명령줄에 담은 자기 셸과 보조 프로세스도 잡으므로 끝나지 않는다. 프로세스 이미지 이름으로 먼저 거르고, 기다리기 전에 잡히는 프로세스가 의도한 것인지 한 번 확인한다.
kind: error
scope: 다른 프로세스를 명령줄 검색으로 기다리는 Windows 셸 폴링 루프(Get-CimInstance Win32_Process, wmic, ps/pgrep -f 방식 매칭)
keywords: [polling, wait loop, process wait, self-match, command line match, Get-CimInstance, Win32_Process, CommandLine, "pgrep -f", background task, UnrealBuildTool, dotnet.exe, build mutex wait]
status: resolved
checked_at: 2026-11-26
context:
  platform: Windows 11
  shell: "폴링마다 Windows PowerShell 5.1 을 띄우는 Git Bash"
trigger: 내 빌드를 시작하기 전에 다른 빌드를 기다리려고, CommandLine 이 도구 이름과 맞는 프로세스를 Get-CimInstance Win32_Process 가 찾는 동안 잠드는 백그라운드 루프를 띄움
symptom: 기다리던 빌드가 끝난 뒤에도 완료를 알리지 않는다. 같은 필터로 한 번 목록을 뽑으면 루프 자신의 bash.exe, powershell.exe 와 경로에 도구 이름이 든 무관한 보조 프로세스가 잡힌다
cause_status: confirmed
prevention: CommandLine 패턴을 맞추기 전에 프로세스 Name(예 Name -eq 'dotnet.exe')으로 거르고, 루프를 띄우기 전에 그 필터로 목록을 한 번 뽑아 기다리는 자신이나 무관한 보조 프로세스가 잡히지 않는지 확인한다
prevention_status: verified
---

## 기대와 관찰

빌드를 시작하기 전에, 다른 체크아웃의 빌드 도구와 에디터 프로세스가 끝날 때까지 기다리는 백그라운드 루프를 띄웠다. 폴링마다 `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'UnrealBuildTool' -or $_.Name -match '^UnrealEditor' }` 를 실행해 하나라도 잡히면 잠들었다. 기대: 다른 빌드가 끝나면 완료 줄을 찍는다. 관찰: 한참 지나도 기다리고 있었다. 같은 필터로 뽑은 목록에는 의도한 `dotnet.exe ... UnrealBuildTool.dll` 프로세스와 함께 루프 자신의 `bash.exe`, `powershell.exe` 여러 개, 실행 파일 경로에 도구 이름이 든 `UbaVisualizer.exe` 가 잡혔다.

## 원인과 해결

목록으로 확인했다. 루프 자신의 셸 명령줄에 패턴 문자열이 그대로 들어 있었고, 폴링마다 뜨는 PowerShell 프로세스도 그 문자열을 갖고 있어, 루프가 도는 동안 조건이 늘 참이었다. 설치 경로에 도구 이름이 든 오래 사는 보조 프로세스도 빌드가 끝난 뒤까지 조건을 참으로 남겼을 것이다.

해결: 루프를 멈추고 `($_.Name -eq 'dotnet.exe' -and $_.CommandLine -match 'UnrealBuildTool\.dll') -or $_.Name -match '^UnrealEditor'` 로 다시 띄웠다. 이미지 이름 필터가 기다리는 셸을 빼고, 좁힌 패턴이 보조 프로세스를 뺀다. 다시 띄운 루프는 기다리던 빌드가 끝나자 완료 줄을 찍었고, 이어서 기다리던 빌드가 돌았다.

## 재확인과 예방

2026-11-26 원래 필터로 한 번 뽑은 목록에 기다리는 자신의 프로세스가 잡혔고, 이것이 이 실패를 드러내는 점검이다. 고친 필터에서는 기다리던 빌드가 끝날 때 루프도 끝났다. 기다리는 명령이 찾는 문자열을 담는 모든 명령줄 문자열 매칭(`pgrep -f`, `ps | grep` 포함)에 해당한다. 확인하지 않은 것: 같은 이미지 이름을 쓰는 무관한 도구, 예를 들어 명령줄에 같은 어셈블리를 언급하는 다른 `dotnet.exe` 프로그램.

## 근거

- 세션 관찰, 2026-11-26, Windows 11, Git Bash 와 Windows PowerShell 5.1: 멈춘 루프, 자기 매칭을 보인 프로세스 목록, 고친 루프의 완료 줄.
