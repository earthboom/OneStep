# 언리얼 프로젝트의 렌더링 경로와 확장 위치 파악하기

항목 `K-CODE-UE-RENDER-ORIENTATION` · 상태 활성 · 확인일 2026-11-05

----------

## 지침

RendererSettings에서 전방·지연 셰이딩을 독립적으로 확인한다. Nanite는 가상화 지오메트리, Lumen은 동적 전역 조명·반사, Virtual Shadow Maps는 페이지 기반 고해상도 그림자다. r.Nanite, r.DynamicGlobalIlluminationMethod, r.ReflectionMethod, r.Shadow.Virtual.Enable, r.AllowStaticLighting, r.GenerateMeshDistanceFields, r.CustomDepth의 설정과 실제 패스를 대조한다. 정적 조명이나 거리장 지원이 활성화돼도 해당 패스를 쓴다는 뜻은 아니다.

DefaultScalability.ini·DefaultDeviceProfiles.ini 및 사용자 설정에서 품질 단계와 업스케일러를 본다. [엔진 체크아웃](K-CODE-UE-ENGINE-CHECKOUT.md)에서 Renderer, RenderCore, RHI·백엔드, Engine/Shaders의 변경 이력을 조사한다. 자체 코드와 외부 업스케일러의 책임 범위를 구분한다.

ISceneViewExtension은 뷰 수명주기 콜백, FGlobalShader와 IMPLEMENT_GLOBAL_SHADER는 머티리얼과 독립된 셰이더 타입과 구현 등록이다. RDG(Render Dependency Graph)는 패스와 리소스 의존성을 기술하고 FRDGBuilder::AddPass로 패스를 추가한다. .usf·.ush와 장면 프록시, 셰이더에 정점 데이터를 공급하는 버텍스 팩터리를 찾는다. PSO는 그래픽 파이프라인 상태를 묶고 생성·컴파일 지연이 끊김을 일으킬 수 있다. 기존 측정 자료에서 후보를 고른다. 학습에는 GPU 캡처의 패스를 FDeferredShadingSceneRenderer::Render와 대조하고 컴포넌트→프록시→메시 배치→패스 프로세서→그리기 명령을 따라가는 방법이 있다.

## 적용 범위와 예외

UE5 프로젝트의 구조 조사에 적용한다. 엔진 수정 이력을 보려면 해당 소스가 필요하다. 런처 엔진은 기본 엔진을 기준으로 확인한다. 기술 선택에 따라 Lumen 장면, Nanite 래스터화, VSM 페이지 등의 비용 후보가 달라진다.

## 점검

플랫폼 ini와 기기 프로필·사용자 설정 적용 후 유효값을 대조한다. 주석의 조명 개수 및 설정값은 측정 후보이며 GPU 비용은 캡처나 텔레메트리로 확인한다.

## 근거

2026-11-05 Windows UE 5.8의 설정·소스에서 렌더러 선택, 엔진 변경과 자체 확장 위치를 찾은 기록이다. 런타임 재정의, GPU 비용 및 제시한 학습 순서는 검증하지 않았다. [Epic, Render Dependency Graph](https://dev.epicgames.com/documentation/unreal-engine/render-dependency-graph-in-unreal-engine?application_version=5.8) · [FRDGBuilder](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/RenderCore/FRDGBuilder?application_version=5.8)

검색어 Unreal Engine, rendering, renderer settings, Nanite, Lumen, Virtual Shadow Maps, distance field shadows, static lighting, SceneViewExtension, ISceneViewExtension, RDG, FRDGBuilder, IMPLEMENT_GLOBAL_SHADER, usf, vertex factory, scalability, PSO, Render Dependency Graph, FRDGBuilder::AddPass, FGlobalShader, FDeferredShadingSceneRenderer::Render, pipeline state object
