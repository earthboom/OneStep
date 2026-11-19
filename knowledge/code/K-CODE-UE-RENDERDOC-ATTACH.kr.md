# 언리얼 에디터에 RenderDoc을 연결하고 시작 상태 확인하기

항목 `K-CODE-UE-RENDERDOC-ATTACH` · 상태 활성 · 확인일 2026-11-06

----------

## 지침

엔진 RenderDocPlugin 설정에서 설치된 renderdoc.dll의 위치를 지정한다. `-AttachRenderDoc` 또는 지원하는 renderdoc.AutoAttach로 연결하고 이번 실행 로그에서 플러그인 준비를 확인한다. 관찰된 조합에서는 DLSS(Deep Learning Super Sampling)가 사용하는 NVIDIA NGX SDK 초기화가 실패해 예/아니요/취소 대화상자가 시작을 막았다. 예는 계속, 아니요는 경고를 숨기고 계속, 취소는 종료였다. 이 실행은 DLSS가 꺼진 경로를 캡처했다. DLSS까지 필요하면 해당 도구 조합을 따로 검증한다.

`renderdoc.CaptureFrame`, 뷰포트 버튼 또는 `renderdoc.CapturePIE`로 프레임을 잡고 Saved/RenderDocCaptures를 확인한다. 외부 제출 제한이 있으면 첫 실행의 분석 데이터 설정을 확인한다. RenderDoc 1.47의 qrenderdoc.exe --python에서 내장 Python 3.8의 renderdoc 모듈로 `controller.GetRootActions()`를 재귀 탐색하고 `action.GetName(controller.GetStructuredFile())`로 이름을 읽는다. 관찰한 내장 환경에는 __file__이 없어 입출력 경로와 종료·오류 처리를 명시해야 했다.

## 적용 범위와 예외

Windows D3D12, UE 5.8 소스 빌드 에디터 및 RenderDoc 1.47에서 확인했다. DLSS 경고는 WITH_EDITOR와 무인 모드·로컬 경고 설정에 따라 달라진다. 다른 플러그인 버전의 모달이나 캡처 지원은 별도 확인한다.

## 점검

프로세스가 응답하지만 로그가 멈추면 모달을 확인하고, 재시작 시 이전 로그가 교체된 뒤 새 헤더 시각을 확인한다. 에디터 시작 시간에는 대화상자 대기가 포함될 수 있다. 중첩 GPU 마커만으로 비용을 나누지 말고 잎 패스의 draw·dispatch를 센다. FetchCounters에서 EventGPUDuration 결과가 없으면 ProfileGPU 등 유효한 계측을 사용한다.

## 근거

2026-11-06 RenderDoc API 1.7.0 연결, NGX 실패와 모달, DLSS 비활성 프레임 캡처 및 1.47에서의 열기를 확인했다. 이전 로그 때문에 준비 완료를 잘못 판단한 경우와 스크립트 경로 누락으로 대기한 경우가 있었다. 재생에서 액션은 열거했지만 GPU 지속 시간은 얻지 못했다. [Epic, Using RenderDoc with Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-renderdoc-with-unreal-engine?application_version=5.8)

검색어 Unreal Engine, RenderDoc, RenderDocPlugin, AttachRenderDoc, renderdoc.CaptureFrame, renderdoc.CapturePIE, DLSS, NGX, frame capture, editor startup hang, D3D12, renderdoc.AutoAttach, Render Hardware Interface, EventGPUDuration, ProfileGPU, GetRootActions
