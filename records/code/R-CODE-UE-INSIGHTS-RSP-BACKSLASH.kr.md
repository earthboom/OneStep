---
id: R-CODE-UE-INSIGHTS-RSP-BACKSLASH
title: 응답 파일 경로의 역슬래시가 지워져 헤드리스 Unreal Insights 내보내기가 파일을 쓰지 않았다
summary: TimingInsights 내보내기 명령은 출력 경로를 이스케이프 토큰으로 읽는다. 그래서 -ExecOnAnalysisCompleteCmd 응답 파일 안의 따옴표 친 Windows 경로가 역슬래시를 모두 잃고 CSV 가 생기지 않았다. 경로를 슬래시로 쓰고, 내보내기 로그의 Filename 줄을 확인한다.
kind: error
scope: Windows 에서 UnrealInsights.exe 헤드리스 분석. 응답 파일로 실행하는 TimingInsights.ExportThreads, ExportTimers, ExportTimingEvents
keywords: [Unreal Insights, Timing Insights, UnrealInsights.exe, "-ExecOnAnalysisCompleteCmd", "@=", response file, "-NoUI", "-AutoQuit", "-OpenTraceFile", TimingInsights.ExportTimingEvents, TimingInsights.ExportTimers, TimingInsights.ExportThreads, FParse::Token, bUseEscape, backslash, escape, headless export, utrace, CSV]
status: resolved
checked_at: 2026-11-24
context:
  engine: "Unreal Engine 5.8 (UnrealInsights 프로그램과 TraceInsights 모듈)"
  platform: Windows 11
trigger: 내보내기 명령에 역슬래시가 든 따옴표 Windows 경로를 적은 응답 파일을 -ExecOnAnalysisCompleteCmd="@=<응답 파일>" 로 넘겨 UnrealInsights.exe -NoUI -AutoQuit 를 실행함
symptom: 분석이 끝나고 프로세스가 0 으로 끝나지만 내보낸 파일이 없다. 내보내기 로그의 출력 경로에서 역슬래시가 빠져 있다 (예 D:Projectfolder...)
cause_status: confirmed
prevention: 응답 파일 안의 모든 경로를 슬래시로 쓰고, 종료 코드 대신 로그의 Filename 줄과 파일 존재를 확인한다
prevention_status: verified
---

## Expected and observed

`-ExecOnAnalysisCompleteCmd="@=<file>"` 로 넘긴 응답 파일에 `TimingInsights.ExportThreads`, `ExportTimers`, `ExportTimingEvents` 명령과 `"D:\dir\exports\threads.csv"` 같은 따옴표 출력 경로를 적었다. 기대: 명령마다 CSV 하나. 관측: 분석 뒤 프로세스는 0 으로 끝났지만 대상 폴더에도, 찾아본 다른 곳에도 CSV 가 없었다. 내보내기 로그에는 경로가 `D:direxportsthreads.csv` 로 찍혔다.

## Cause and resolution

엔진 소스로 확인했다. `FInsightsManager::Exec` 는 `@=` 로 시작하는 명령을 `HandleResponseFileCmd` 로 보내고, 이 함수가 파일을 한 줄씩 실행한다. 각 내보내기 처리기는 `bUseEscape` 를 참으로 두고 `FParse::Token(Cmd, bUseEscape)` 로 파일 이름을 읽는다. 그래서 따옴표 토큰 안의 역슬래시가 이스케이프 문자로 처리되어 지워진다. 결과 경로는 의도한 폴더가 아니었다.

해결: 응답 파일을 쓰는 스크립트가 내보내기 폴더를 슬래시로 바꾼다. 같은 트레이스와 명령으로 네 내보내기가 모두 써졌다.

## Recheck and prevention

2026-11-24 에 슬래시 응답 파일이 162 MB 트레이스에서 `threads.csv`, `timers.csv` 와 타이밍 이벤트 CSV 두 개를 만들었다. 이후 실행에서 필터를 건 내보내기도 더했다 (`*` 와일드카드를 쓰는 `-threads=`, `-timers=`, 그리고 `-startTime=`, `-endTime=`, `-columns=`). 매번 로그 줄 `Filename: "<path>"` 이 전체 경로를 보였다. 앞선 역슬래시 실행이 이 점검이 잡아내는 실패 사례다.

종료 코드를 성공으로 보지 않는다. 해석된 Filename 줄과 출력 파일 존재도 확인한다. 명령줄에 직접 준 경로는 다른 코드가 읽으며 여기서 시험하지 않았다. 내보낸 GPU 타이머 이름은 `SceneRender- %s` 같은 형식 문자열일 수 있어, CSV 만으로는 뷰별 GPU 작업을 나누지 못할 수 있다.

## Evidence

- 엔진 소스, Unreal Engine 5.8: `Engine/Source/Developer/TraceInsights/Private/Insights/InsightsManager.cpp` (`FInsightsManager::Exec`, `HandleResponseFileCmd`). `Engine/Source/Developer/TraceInsights/Private/Insights/TimingProfiler/TimingProfilerManager.cpp` (`TimingInsights.ExportTimingEvents` 처리기, `const bool bUseEscape = true; FString Filename = FParse::Token(Cmd, bUseEscape);`). `Engine/Source/Runtime/Core/Private/Misc/Parse.cpp` (`FParse::Token` 이스케이프 처리). 엔진 기능 테스트 `Insights/Tests/FunctionalTests/ExportCommandsTests.cpp` 도 같은 `-ExecOnAnalysisCompleteCmd="@=%s"` 형태를 쓴다.
- 세션 관측, 2026-11-24: 위에 적은 역슬래시 실패 실행, 그 내보내기 로그, 슬래시 성공 실행.
- 관련 측정 지침: [K-CODE-PERFORMANCE-MEASUREMENT](../../knowledge/code/K-CODE-PERFORMANCE-MEASUREMENT.md).
