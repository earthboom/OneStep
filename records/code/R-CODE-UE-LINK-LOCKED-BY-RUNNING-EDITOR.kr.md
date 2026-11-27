# 같은 프로젝트의 헤드리스 에디터 인스턴스가 모듈 DLL을 잡고 있어서, Unreal 에디터 빌드가 컴파일은 통과하고 링크에서 실패했다

- ID: `R-CODE-UE-LINK-LOCKED-BY-RUNNING-EDITOR`
- 종류: error, 상태: resolved, 확인일: 2026-11-26
- 범위: Windows에서 같은 프로젝트의 다른 에디터 프로세스가 어떤 모드로든 떠 있는 동안 명령줄 UnrealBuildTool로 에디터 타깃을 빌드할 때
- 환경: Unreal Engine 5.8 소스 빌드, Windows 11, 원격 작업자를 쓰는 Unreal Build Accelerator 다음 로컬 NoUba 재시도
- 발생 조건: 다른 작업 흐름이 서버 모드나 다른 헤드리스 모드로 띄운 같은 프로젝트의 에디터 프로세스가 아직 살아 있는 동안 명령줄에서 에디터 타깃을 빌드함
- 증상: 모든 컴파일 단계는 성공하고, 그 뒤 UbaSessionServer가 프로젝트의 UnrealEditor-<Module>.dll을 쓰기로 열지 못하며(오류 코드 9001), NoUba 재시도가 LINK fatal error LNK1104로 실패하고, 결과는 Failed (OtherCompilationError)
- 원인 확인 상태: confirmed
- 재발 방지: 에디터 빌드 전에 명령줄에 프로젝트 .uproject 경로가 들어간 프로세스를 모두 나열한다(-server와 헤드리스 실행, 그리고 그 CrashReportClientEditor 포함). "에디터를 닫았다"는 말에 기대지 말고 프로세스 ID로 각각 끝났는지 확인한다.
- 재발 방지 상태: verified

## 기대와 관찰

코드만 바꾼 변경을 엔진의 `Build.bat`으로 에디터 타깃, Development 구성으로 빌드했다. 기대: 정상 컴파일과 링크. 관찰: 바꾼 파일을 포함해 모든 컴파일 단계가 오류 없이 끝났다. 그 뒤 프로젝트 게임 모듈 DLL의 링크가 실패했다. `UbaSessionServer`는 20초 동안 다시 시도한 뒤에도 `Binaries/Win64/UnrealEditor-<Module>.dll`을 쓰기로 열 수 없다고 보고했고, 잡고 있는 프로세스로 `UnrealEditor.exe`와 `CrashReportClientEditor-Win64-Development.exe`를 들었다(UBA 종료 코드 9001). 로컬 `[NoUba]` 재시도는 `LINK : fatal error LNK1104: cannot open file`로 실패했다.

열려 있는 대화형 에디터는 없었다. DLL을 잡은 것은 약 40분 전에 별도의 측정 작업 흐름이 같은 프로젝트 파일과 `-server -nullrhi -NoLiveCoding -NoCompile -unattended`로 띄운 `UnrealEditor.exe`였다. `CrashReportClientEditor` 프로세스는 같은 초에 시작됐다. 이는 크래시가 아니라 평소의 동반 실행이다. 사용자가 에디터를 닫았다고 말한 뒤에도 같은 프로세스 ID가 메모리 값도 그대로인 채 살아 있었다.

## 원인과 해결

원인 확인됨. Windows는 실행 중인 프로세스가 올린 DLL에 쓰기 접근을 거부한다. 서버 모드나 다른 헤드리스 모드로 띄운 에디터도 대화형 에디터와 같은 에디터 모듈 바이너리를 올린다. `-NoLiveCoding`은 [R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS](R-CODE-UE-UBT-LIVECODING-ACROSS-CHECKOUTS.kr.md)에 적힌 Live Coding 뮤텍스만 피할 뿐이다. 출력 파일은 풀어 주지 않으므로, 이 실패는 처음에 거절되는 형태가 아니라 링크 단계에서 나타난다.

해결: 사용자 승인을 받아 그 에디터와 `CrashReportClientEditor`, `UnrealTraceServer`를 프로세스 ID로 종료했다. 같은 빌드 명령을 다시 돌리자 남은 단계만 다시 링크하고 성공했다.

## 재확인과 재발 방지

수정 확인, 2026-11-26: 프로세스가 끝난 뒤 다시 돌린 빌드가 `Result: Succeeded`로 끝났다.

재발 방지 확인, 2026-11-26: 첫 빌드 전에 프로젝트 파일 경로로 거른 프로세스 목록(`Get-CimInstance Win32_Process`에서 `CommandLine` 선택)이 서버 모드 에디터를 찾았다. 사용자가 닫았다고 알린 뒤 다시 나열해도 같은 프로세스 ID가 보였다. 이어진 빌드 실패가 바로 이 프로세스들이 DLL을 잡고 있었음을 확인해 주었고, 이들이 끝나자 빌드가 성공했다. 이 점검이 실제 원인을 찾아냈으므로 이 조건에서 상태는 verified다.

적용 범위: 이 점검은 같은 프로젝트의 모든 에디터 프로세스를 다룬다. 같은 엔진을 쓰는 다른 프로젝트의 프로세스는 이 프로젝트의 바이너리를 잠그지 않지만, 관련 기록의 Live Coding 거절은 일으킬 수 있다. 컴파일만 성공한 것은 부분 증거다. 바꾼 소스가 컴파일된다는 것은 보여 주지만 타깃이 링크된다는 것은 보여 주지 않는다. 링크가 성공할 때까지 막힘(blocked)으로 보고한다.

## 근거

- 세션 관찰, 2026-11-26: 위에 인용한 빌드 로그 줄(UBA 9001, LNK1104, `Result: Failed (OtherCompilationError)`), 명령줄과 시작 시각이 담긴 프로세스 목록, 사용자 승인 후 프로세스 ID로 한 종료, 성공한 재빌드.
- 올라간 이미지 파일의 Windows 공유 동작: [Microsoft, LNK1104](https://learn.microsoft.com/en-us/cpp/error-messages/tool-errors/linker-tools-error-lnk1104) (다른 프로세스가 쓰고 있는 파일을 원인 중 하나로 든다).
