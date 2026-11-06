---
id: K-CODE-UE-RENDERDOC-ATTACH
title: 언리얼 에디터에 RenderDoc을 붙이고 시작을 막는 요소를 넘긴다
summary: 엔진 RenderDoc 플러그인은 -AttachRenderDoc 또는 renderdoc.AutoAttach가 있어야 로드된다. 프로젝트에 DLSS가 있으면 RenderDoc 아래에서 NGX 초기화가 실패하고, 누군가 답할 때까지 모달 대화상자가 에디터 시작을 멈춘다.
kind: method
scope: RenderDoc으로 프레임을 캡처해야 하는 Windows D3D12의 언리얼 엔진 5 에디터, 특히 NVIDIA DLSS 플러그인이 들어 있는 프로젝트
keywords: [Unreal Engine, RenderDoc, RenderDocPlugin, AttachRenderDoc, renderdoc.CaptureFrame, renderdoc.CapturePIE, DLSS, NGX, frame capture, editor startup hang, D3D12]
status: active
checked_at: "2026-11-06"
context:
  engine: Unreal Engine 5.8 source build
  platform: Windows desktop, D3D12
  tool: RenderDoc 1.47
---

## 지침

1. RenderDoc을 기본 경로에 설치한다. 플러그인은 그 경로에서 `renderdoc.dll`을 찾는다.
2. 에디터를 `-AttachRenderDoc`로 시작한다. 이 옵션이 없으면 로그에 `RenderDoc plugin will not be loaded`가 찍힌다. 준비된 플러그인은 `RenderDoc plugin is ready!`를 남긴다.
3. 프로젝트에 NVIDIA DLSS 플러그인이 있으면 NGX 초기화가 `NVSDK_NGX_Result_FAIL_PlatformError`로 실패한다. 에디터에서는 플러그인이 `Warning -- DLSS incompatible with plugins and/or API capture tools`라는 Yes/No/Cancel 모달 경고를 띄우고, 답할 때까지 시작이 멈춘다. Yes는 아무것도 바꾸지 않고 계속한다. No는 계속하면서 경고를 숨긴다. Cancel은 에디터를 종료한다. 그 실행 동안 DLSS는 꺼져 있으므로, 캡처에는 DLSS 대신 엔진 업스케일러 경로가 나온다. DLSS 패스는 NVIDIA Nsight Graphics로 캡처한다.
4. `renderdoc.CaptureFrame`이나 뷰포트 툴바 버튼으로 캡처하고, 게임 프레임은 `renderdoc.CapturePIE`로 캡처한다. 파일은 `<Project>/Saved/RenderDocCaptures/`에 저장된다. RenderDoc을 처음 실행하면 익명 통계를 묻는다. 작업을 로컬에만 두어야 하면 보내지 않는 쪽을 고른다.
5. UI를 조작하지 않고 패스 트리를 뽑으려면 `qrenderdoc.exe --python <script.py>`를 실행한다. 스크립트는 `renderdoc` 모듈이 있는 내장 Python 3.8에서 돈다. 그 환경에는 `__file__`이 정의되지 않으므로 경로를 고정값으로 쓴다. 끝은 `os._exit(0)`으로 맺는다. 잡히지 않은 오류가 나면 UI가 열린 채 프로세스가 기다린다. `controller.GetRootActions()`를 재귀로 돌고, 각 액션 이름은 `action.GetName(controller.GetStructuredFile())`로 얻는다.

## 적용 범위와 예외

에디터 빌드에 해당한다. DLSS 대화상자는 `WITH_EDITOR`에서만 컴파일되고, 무인 실행이거나 프로젝트 또는 로컬 DLSS 설정이 꺼 두면 뜨지 않는다. NGX가 호환되지 않는다고 보는 다른 캡처 도구도 같은 식으로 동작한다.

## 점검

- 프로세스는 응답하는데 에디터 로그가 몇 분째 늘지 않으면, 멈춤이라고 판단하기 전에 메인 창 제목으로 모달 대화상자를 확인한다.
- 재시작 뒤 에디터 로그의 줄을 기다릴 때는 먼저 로그 머리말이 새 시작 시각인지 확인한다. 이전 로그는 새 프로세스가 교체할 때까지 그 자리에 있으므로, 대기 루프가 오래된 줄에 걸릴 수 있다.
- `Total Editor Startup Time`에는 모달 대화상자가 사용자를 기다린 시간도 들어간다.
- 마커 범위만으로 비용을 나누지 않는다. 캡처 안의 언리얼 GPU 마커는 중첩이 어긋날 수 있어서, 마커 하나가 프레임 대부분을 덮기도 한다. 말단 패스별로 드로우와 디스패치를 센다.
- 스크립트 리플레이에서 GPU 시간용 `FetchCounters([EventGPUDuration])`가 빈 목록을 돌려주면, 패스 시간은 엔진(`ProfileGPU`)에서 잰다.

## 근거

Windows D3D12와 DLSS 플러그인을 쓰는 UE 5.8 게임 프로젝트에서 한 번 관찰했다(2026-11-06). 첫 번째 에디터 실행은 `-AttachRenderDoc` 없이 시작했고, 플러그인을 로드하지 않는다는 로그를 남겼다. 두 번째 실행은 RenderDoc API v1.7.0을 로드했고 NGX 초기화가 PlatformError로 실패했으며, 약 한 시간 동안 DLSS 모달에 머물렀다. 그동안 로그는 조용했고 프로세스는 Responding으로 보고됐다. Yes를 누른 뒤 뷰포트 캡처로 약 8,000개 이벤트의 390MB `.rdc`가 만들어졌고, RenderDoc 1.47이 문제없이 열었다. 대기 루프 하나는 교체되기 전 이전 실행의 로그에 걸려 너무 일찍 결과를 보고했다.

같은 날 이벤트 11,542개짜리 554MB PIE 캡처에 `qrenderdoc.exe --python`을 스크립트로 실행해 마커 행 843개를 10분 안에 뽑았다. 첫 시도는 `__file__`을 써서 로그를 쓰기 전에 실패했고, 시간 초과까지 멈춰 있었다. `EnumerateCounters`는 카운터 16개를 보여 줬지만, GPU 시간용 `FetchCounters`는 결과를 돌려주지 않았다. 뽑아낸 트리에서 `FXSystemPreRender`는 프레임 대부분을 덮었고, TSR 마커 하나 안에 드로우 17개가 들어 있었다.
