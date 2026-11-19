# 스켈레탈 메시 틱을 중지했을 때 LOD 선택 점검하기

항목 `K-CODE-UE-SKELETAL-LOD` · 상태 활성 · 확인일 2026-11-19

----------

## 지침

1. 렌더 스레드는 뷰별로 `FSkeletalMeshObject::UpdateMinDesiredLODLevel`을 실행한다. 썸네일 뷰와 포커스가 없는 뷰 패밀리는 건너뛴다. 바운드 구의 화면 반경 제곱에 `r.SkeletalMeshLODRadiusScale`(0.25~1.0으로 제한)의 제곱을 적용한다. `EngineShowFlags.LOD`가 켜지면 낮은 세부 수준부터 `(ScreenSize × 0.5)²`와 비교하고 기본값으로 LOD0을 쓴다. `LODHysteresis`는 상세 LOD로 복귀하는 경계를 다르게 하여 경계 부근 전환을 줄인다.
2. 새 프레임의 첫 호출은 직전 집계값을 `MinDesiredLODLevel`, `MaxDistanceFactor`로 넘기고 새 집계를 시작한다. 같은 프레임의 여러 뷰에서는 가장 상세한 LOD(최소 인덱스)와 최대 화면 크기를 보존한다. 여러 뷰가 병렬 처리될 때 뮤텍스가 집계를 보호한다.
3. 게임 스레드의 `USkinnedMeshComponent::TickComponent`가 `UpdateLODStatus`를 호출한다. 기본 경로에서 이전 프레임의 희망 LOD에 바이어스를 더하고 유효 범위로 제한한다. 강제 지정 등의 조건도 적용된다.
4. `SetComponentTickEnabled(false)`로 컴포넌트 틱을 끄면 보이는 메시의 렌더 계산은 계속돼도 게임 스레드 적용이 멈출 수 있다. 전역 음수 바이어스는 다른 메시의 세부 수준 비용까지 바꾼다. 고정 LOD가 적합하면 틱이 작동할 때 `USkinnedMeshComponent::SetForcedLOD`를 호출한다(1부터 시작, 0으로 해제). Epic 문서상 다음 틱에 적용되므로 실제 적용을 확인한 뒤 틱을 중단하고 재개 후에는 해제와 자동 선택을 확인한다.

## 적용 범위와 예외

UE 5.8의 비 Nanite 스켈레탈 메시 소스 경로다. Nanite 지오메트리의 세부 결정은 따로 검증한다. 장면 캡처도 뷰에 포함될 수 있다. 포즈의 가시성 기반 틱과 애니메이션 업데이트 빈도 최적화는 컴포넌트 틱 중지와 동작이 다르다.

## 점검

`a.VisualizeLODs 1`로 유효 LOD를 보고 실험에서 바이어스를 중립으로 맞춘다. 틱 제어 코드, `PrimaryComponentTick.bCanEverTick`, 에셋 ScreenSize·LODHysteresis, 최소 LOD, 부모·리더 동기화, 강제 지정을 확인한다. 전후 CPU·GPU 비용을 측정한다.

## 근거

2026-11-19 UE 5.8의 SkeletalRender.cpp, SkinnedMeshComponent.cpp, SceneView.h, EditorViewportClient.cpp에서 뷰 필터와 집계, 컴포넌트 갱신, 포커스 조건을 확인한 기록이다. 틱 중지에 따른 현상과 수정 순서는 소스 기반 추론이다. 게임 재현이나 성능 측정은 없었다. [Epic, FSkeletalMeshObject::UpdateMinDesiredLODLevel](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/FSkeletalMeshObject/UpdateMinDesiredLODLevel?application_version=5.8) · [USkinnedMeshComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/USkinnedMeshComponent?application_version=5.8) · [Set Forced LOD](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Components/SkinnedMesh/SetForcedLOD?application_version=5.8)

검색어 Unreal Engine, skeletal mesh, LOD, level of detail, MinDesiredLODLevel, UpdateMinDesiredLODLevel, FSkeletalMeshObject, UpdateLODStatus, TickComponent, SetForcedLOD, ForcedLodModel, r.SkeletalMeshLODBias, LOD bias, r.SkeletalMeshLODRadiusScale, ScreenSize, LODHysteresis, ComputeBoundsScreenRadiusSquared, MaxDistanceFactor, EngineShowFlags.LOD, bThumbnailRendering, GetIsInFocus, FSceneView, FSceneViewFamily, view relevance, double buffering, one-frame latency, render thread, game thread, mutex, race condition, clamp, hysteresis, LOD popping, scalability, FSkeletalMeshObject::UpdateMinDesiredLODLevel, USkinnedMeshComponent::TickComponent, USkinnedMeshComponent::SetForcedLOD, SetComponentTickEnabled
