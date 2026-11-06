# 코드 지식

소프트웨어 구현, 시스템, 런타임 동작, 검증.

[도메인 라우팅](../index.md) | [저장과 수명 주기](../../skills/vegabond-knowledge/references/storage.md)

영어 원본 `index.md`의 카탈로그를 번역한 것이다. 행은 상세 파일에서 고치고 이 표는 직접 고치지 않는다.

| ID / 제목 / 종류 | 요약 | 범위 / 맥락 | 키워드 | 상태 / 확인일 | 상세 |
| --- | --- | --- | --- | --- | --- |
| K-CODE-UE-ENGINE-CHECKOUT / 커스텀 언리얼 엔진 소스를 읽기 전에 현재 쓰는 체크아웃인지 확인한다 [lesson] | 엔진 경로 환경 변수가 오래된 체크아웃을 가리키고 실제 소스는 git worktree에 있을 수 있다. 엔진 소스나 이력에서 결론을 내기 전에 worktree, 브랜치, Build.version을 확인한다. | 환경 변수나 레지스트리 연결로 소스 빌드 또는 포크 언리얼 엔진을 찾는 프로젝트; {"engine": "Unreal Engine 5 source build", "vcs": "git with worktrees"} | Unreal Engine, custom engine, engine fork, git worktree, Build.version, EngineAssociation, engine source, stale checkout | active / 2026-11-06 | [K-CODE-UE-ENGINE-CHECKOUT](K-CODE-UE-ENGINE-CHECKOUT.kr.md) |
| K-CODE-UE-LOCAL-ONLY-WORK / 공유 DDC와 분산 컴파일 경로를 확인해 언리얼 에디터 작업을 로컬에만 둔다 [method] | 로컬에서 실행한 언리얼 빌드나 에디터도 공유 DDC, UBA/Horde 원격 컴파일, Incredibuild 셰이더 컴파일로 팀 인프라에 닿을 수 있다. User*.ini 오버라이드로 체크아웃별로 공유 DDC를 끄고, 각 경로를 로그로 확인한다. | 공유 DDC와 분산 컴파일 에이전트가 있는 스튜디오 네트워크의 언리얼 엔진 5 프로젝트에서 작업을 로컬 머신에만 두어야 할 때; {"engine": "Unreal Engine 5.8 source build", "platform": "Windows desktop"} | Unreal Engine, DDC, Derived Data Cache, shared DDC, UserEngine.ini, UnrealBuildTool, UBA, Horde, Incredibuild, XGE, distributed compile, local only | active / 2026-11-06 | [K-CODE-UE-LOCAL-ONLY-WORK](K-CODE-UE-LOCAL-ONLY-WORK.kr.md) |
| K-CODE-UE-RENDERDOC-ATTACH / 언리얼 에디터에 RenderDoc을 붙이고 시작을 막는 요소를 넘긴다 [method] | 엔진 RenderDoc 플러그인은 -AttachRenderDoc 또는 renderdoc.AutoAttach가 있어야 로드된다. 프로젝트에 DLSS가 있으면 RenderDoc 아래에서 NGX 초기화가 실패하고, 누군가 답할 때까지 모달 대화상자가 에디터 시작을 멈춘다. | RenderDoc으로 프레임을 캡처해야 하는 Windows D3D12의 언리얼 엔진 5 에디터, 특히 NVIDIA DLSS 플러그인이 들어 있는 프로젝트; {"engine": "Unreal Engine 5.8 source build", "platform": "Windows desktop, D3D12", "tool": "RenderDoc 1.47"} | Unreal Engine, RenderDoc, RenderDocPlugin, AttachRenderDoc, renderdoc.CaptureFrame, renderdoc.CapturePIE, DLSS, NGX, frame capture, editor startup hang, D3D12 | active / 2026-11-06 | [K-CODE-UE-RENDERDOC-ATTACH](K-CODE-UE-RENDERDOC-ATTACH.kr.md) |
| K-CODE-UE-RENDER-ORIENTATION / 언리얼 프로젝트의 렌더링 구성을 공부하거나 최적화하기 전에 파악하는 방법 [method] | 렌더러 설정으로 렌더링 경로를 분류하고, 수정 표시나 이력으로 엔진 렌더러 변경을 찾고, 뷰 익스텐션, 글로벌 셰이더, 셰이더 파일을 검색해 프로젝트 렌더 훅을 찾은 뒤에 공부나 최적화를 계획한다. | 언리얼 엔진 5 게임 프로젝트, 특히 커스텀 엔진과 프로젝트 내 렌더링 플러그인이 있는 경우; {"engine": "Unreal Engine 5.x", "platform": "Windows desktop"} | Unreal Engine, rendering, renderer settings, Nanite, Lumen, Virtual Shadow Maps, distance field shadows, static lighting, SceneViewExtension, ISceneViewExtension, RDG, FRDGBuilder, IMPLEMENT_GLOBAL_SHADER, usf, vertex factory, scalability, PSO | active / 2026-11-05 | [K-CODE-UE-RENDER-ORIENTATION](K-CODE-UE-RENDER-ORIENTATION.kr.md) |
