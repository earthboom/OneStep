---
id: R-CODE-PS-STARTPROCESS-ARG-QUOTING
title: Start-Process 가 공백 든 인자를 쪼개 실행된 프로그램이 잘린 옵션을 받았다
summary: PowerShell Start-Process 는 -ArgumentList 원소를 따옴표 없이 공백으로 이어 붙인다. 그래서 -TestExit="Automation Test Queue Empty" 같은 원소를 따옴표를 넣지 않고 쓰면 여러 인자로 도착한다. 공백이 든 원소마다 큰따옴표를 넣고, 프로그램이 로그에 남긴 명령줄을 확인한다.
kind: error
scope: 옵션에 공백이 든 네이티브 프로그램을 실행하는 Windows PowerShell 5.1 과 PowerShell 7 의 Start-Process
keywords: [PowerShell, Start-Process, ArgumentList, quoting, double quotes, spaces in arguments, command line, native executable, UnrealEditor-cmd.exe, "-ExecCmds", "-TestExit", headless automation, LogInit Command Line]
status: resolved
checked_at: 2026-11-24
context:
  platform: Windows 11
  shell: "PowerShell 7"
trigger: 옵션 값에 공백이 든 네이티브 실행 파일을 Start-Process -ArgumentList 로 실행함. 예를 들어 -ExecCmds 와 -TestExit 를 쓰는 Unreal 에디터 자동화 실행
symptom: 실행된 프로그램이 옵션이 첫 공백에서 잘린 것처럼 동작한다. Unreal 에디터 자동화 실행이 테스트를 돌리지 않고 frame 0 근처에서 끝났고, 로그에 -TestExit=Automation 과 떨어진 단어들이 찍혔다
cause_status: confirmed
prevention: 공백이 든 옵션 값마다 -ArgumentList 원소 안에 이스케이프한 큰따옴표를 넣고, 실행 결과를 믿기 전에 프로그램이 스스로 남긴 명령줄을 의도한 것과 비교한다
prevention_status: verified
---

## Expected and observed

스크립트가 `Start-Process -ArgumentList @(...)` 로 Unreal 에디터 자동화 실행을 띄웠다. 한 원소는 `-ExecCmds=Automation RunTests <name>` 이고 다른 원소는 공백이 든 종료 조건 문자열이었다. 기대: 에디터가 테스트를 돌리고 큐가 비면 끝난다. 관측: 에디터가 거의 바로 끝났고 테스트 결과가 없었다. 로그의 명령줄에는 옵션이 공백마다 쪼개져 있었다 (예 `-TestExit=Automation`).

## Cause and resolution

`Start-Process` 는 `-ArgumentList` 원소를 공백으로 이어 명령줄 문자열 하나를 만들고, 공백이 든 원소에 따옴표를 붙이지 않는다. 받는 프로그램이 그 문자열을 다시 토큰으로 나누므로 옵션 하나가 여럿이 되었다. 실패 실행에서 프로그램이 스스로 남긴 명령줄로 확인했다.

해결: 값에 공백이 든 원소는 따옴표를 직접 넣는다. 예 ``"-ExecCmds=`"Automation RunTests $Tests`""`` 와 `'-TestExit="Automation Test Queue Empty"'`. 공백이 든 경로도 같은 방식으로 감쌌다. 다음 실행은 테스트를 돌리고 결과를 보고했다.

## Recheck and prevention

2026-11-24 에 고친 실행의 `LogInit: Command Line:` 줄에서 옵션이 모두 온전했고, 실행은 자동화 결과 줄로 끝났다. 로그에 남은 명령줄과 의도한 인자를 비교하는 것이 처음 실패를 드러낸 점검이다.

`Start-Process` 에 해당한다. 호출 연산자 `&` 로 실행 파일을 직접 부르면 배열 원소를 따로 넘기며 다른 따옴표 규칙을 따르는데, 여기서는 살펴보지 않았다. 프로그램 종료 코드만으로는 문제가 드러나지 않았다.

## Evidence

- 세션 관측, 2026-11-24, Windows 11 의 PowerShell 7: 위에 적은 실패 실행, 그 로그 명령줄, 고친 실행.
- [Start-Process 문서, ArgumentList 매개변수](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process): 공백이 든 인자는 이스케이프한 큰따옴표로 감싸야 한다. 이 세션에서 문서를 다시 받아 보지 않았다. 로그 명령줄이 확인한 증거다.
