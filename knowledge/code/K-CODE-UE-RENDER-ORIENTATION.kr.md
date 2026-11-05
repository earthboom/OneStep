---
id: K-CODE-UE-RENDER-ORIENTATION
title: 언리얼 프로젝트의 렌더링 구성을 공부나 최적화 전에 파악하는 방법
summary: 렌더러 설정으로 렌더링 경로를 분류하고, 표시나 이력으로 엔진 렌더러 변경을 찾고, 뷰 익스텐션, 글로벌 셰이더, 셰이더 파일을 검색해 프로젝트 렌더 진입점을 찾은 뒤 공부나 최적화를 계획한다.
kind: method
scope: Unreal Engine 5 게임 프로젝트, 특히 커스텀 엔진과 프로젝트 내 렌더링 플러그인이 있는 경우
keywords: [Unreal Engine, rendering, renderer settings, Nanite, Lumen, Virtual Shadow Maps, distance field shadows, static lighting, SceneViewExtension, ISceneViewExtension, RDG, FRDGBuilder, IMPLEMENT_GLOBAL_SHADER, usf, vertex factory, scalability, PSO]
status: active
checked_at: "2026-11-05"
context:
  engine: Unreal Engine 5.x
  platform: Windows desktop
---

## 지침

아래 순서로 렌더링 구성을 파악한다. 각 단계는 짧은 읽기나 검색이다.

1. **렌더링 경로 분류**: `Config/DefaultEngine.ini`의 `[/Script/Engine.RendererSettings]`에서 `r.Nanite`, `r.DynamicGlobalIlluminationMethod`(Lumen), `r.ReflectionMethod`, `r.Shadow.Virtual.Enable`, `r.AllowStaticLighting`, `r.GenerateMeshDistanceFields`, `r.CustomDepth`, 포워드 또는 디퍼드 셰이딩을 본다. Nanite, Lumen, VSM이 꺼져 있고 정적 라이팅이 켜져 있으면 고전적인 디퍼드 경로(라이트맵, 섀도우 맵, 거리장 그림자)다. 공부 계획과 비용 중심이 Lumen, Nanite 프로젝트와 다르다.
2. **품질 단계 읽기**: `DefaultScalability.ini`, `DefaultDeviceProfiles.ini`, 그리고 스케일러빌리티, 안티에일리어싱, 업스케일러를 적용하는 게임 사용자 설정 클래스를 본다. 모든 단계에 똑같이 들어간 설정(예: `r.ForceLODShadow`)은 살펴볼 만하다.
3. **엔진 렌더러 변경량 측정**: 엔진 체크아웃([K-CODE-UE-ENGINE-CHECKOUT](K-CODE-UE-ENGINE-CHECKOUT.md) 참고)에서 `Renderer`, `RenderCore`, `RHI`, RHI 백엔드, `Engine/Shaders` 아래의 스튜디오 수정 표시를 검색하거나 `git log`를 그 경로로 거른다. 변경이 적으면 개선은 프로젝트 코드와 플러그인에서 해야 한다. 엔진 렌더러 수정은 엔진을 갱신할 때마다 병합 비용이 든다.
4. **프로젝트 렌더 진입점 찾기**: 프로젝트 `Source/`와 `Plugins/`에서 `SceneViewExtension`, `FGlobalShader`, `IMPLEMENT_GLOBAL_SHADER`, `FRDGBuilder`, `AddPass`, 씬 프록시, 버텍스 팩토리, `*.usf`와 `*.ush` 파일을 검색한다. 자체 코드와 서드파티 업스케일러 플러그인(DLSS, XeSS, FSR)을 구분한다. 업스케일러는 RDG 읽기 자료로는 좋지만 직접 소유한 코드는 아니다.
5. **기존 측정 찾기**: 렌더 뷰, 픽셀 수, GPU 메모리, PSO 끊김의 게임 내 텔레메트리와 팀이 이미 쓰는 프로파일링 절차를 찾는다. 구조를 바꾸기 전에 이것으로 후보 순위를 정한다.

편집상 판단이며 학습 효과는 검증하지 않았다: 공부는 GPU 프레임 캡처(RenderDoc, `ProfileGPU`, Unreal Insights GPU 트랙)로 시작해 각 패스를 `FDeferredShadingSceneRenderer::Render`와 대응시켜 이름 붙인다. 그다음 프리미티브 하나를 컴포넌트, 씬 프록시, 메시 배치, 메시 패스 프로세서, 메시 드로우 커맨드 순서로 따라간다. 이때 자체 버텍스 팩토리를 가진 프로젝트 플러그인을 구체 예제로 쓴다. 가장 작은 자체 뷰 익스텐션은 렌더 스레드와 게임 스레드 경계를 처음 읽기에 좋다.

## 적용 범위와 예외

1~5단계는 모든 UE5 프로젝트에 해당한다. 3단계는 엔진 소스가 있어야 하며, 런처 엔진이면 렌더러를 순정으로 본다. Lumen, Nanite 프로젝트라면 1단계가 다른 공부 대상과 비용(Lumen 씬, Nanite 래스터화, VSM 페이지 비용)을 가리킨다.

## 점검

- 이 파악에서 나온 최적화 후보는 캡처나 텔레메트리로 측정하기 전까지 가설이다. 측정 없이 설정을 비용이라고 보고하지 않는다.
- 설정값을 유효하다고 보기 전에 플랫폼 ini, 디바이스 프로파일, 사용자 설정이 덮어쓰지 않는지 확인한다.
- 코드 주석에 적힌 광원이나 그림자 캐스터 수는 측정할 입력이지 비용의 근거가 아니다.

## 근거

Windows의 UE 5.8 멀티플레이 던전 게임에 한 번 적용했다(2026-11-05). 1~4단계로 고전적인 디퍼드 구성(Nanite, Lumen, VSM 꺼짐, 정적 라이팅과 거리장 켜짐), 렌더러 관련 엔진 수정 지점 세 곳, 자체 버텍스 팩토리와 컴퓨트 셰이더를 가진 자체 플러그인 하나, 텔레메트리용 작은 렌더 스레드 뷰 익스텐션 하나, 서드파티 업스케일러 플러그인을 찾았다. 공부 순서는 권고이며 아직 끝까지 따라가 보지 않았다.

검증하지 않은 것: 디바이스 프로파일과 사용자 설정 덮어쓰기 뒤의 실제 값, 나열한 후보의 GPU 비용.
