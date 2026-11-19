# 보간 끝값에 도달해도 컴포넌트 위치에 오차가 남을 수 있다

보간 계산이 목표값에 도달한 뒤에도 컴포넌트의 실제 위치에는 미세한 차이가 남았다. 계산 수렴과 적용된 트랜스폼을 독립적으로 검사한다.

- 식별자 · R-CODE-UE-TRANSFORM-TOLERANCE
- 종류 및 상태 · 오류, 해결됨. 당시 확인일 2026-11-12.
- 범위 · UE 5.8.3, 충돌 없는 단일 축 씬 컴포넌트 이동
- 검색어 · USceneComponent::SetWorldLocation, SetWorldLocation, USceneComponent::InternalSetWorldLocationAndRotation, TVector::Equals, UE_KINDA_SMALL_NUMBER, easing, floating-point tolerance, endpoint, 정밀도
- 발생 조건 · 스칼라 곡선과 실제 씬 트랜스폼에 같은 끝점 허용오차를 적용할 때
- 증상 · 곡선은 끝점에 도달했지만 실제 위치에 남은 차이가 설정 함수의 비교 임계값보다 작았다
- 원인 확신도 · 확인됨
- 예방 · 엔진 버전을 확인하고 계산값·시간·실제 컴포넌트 위치를 따로 검사한다 (당시 검증됨)

## 기대와 관찰

스칼라 곡선은 종료 조건을 충족했지만 컴포넌트에서 다시 읽은 월드 위치는 목표와 조금 달랐다. 같은 설정 호출을 반복해도 비트 단위의 일치는 보장되지 않았다.

## 원인과 해결

`USceneComponent::SetWorldLocation`은 월드 위치 변경을 요청한다. 당시 확인한 UE 5.8.3 경로에서 `USceneComponent::InternalSetWorldLocationAndRotation`은 `TVector::Equals`로 상대 위치의 각 좌표가 허용오차 안인지 비교했다. 이 경로의 기본 오차는 `UE_KINDA_SMALL_NUMBER`였다. 따라서 계산이 끝값에 도달해도 충분히 작은 변위는 실제 트랜스폼에 반영되지 않을 수 있었다.

## 재검증과 예방

과거 음성 대조 검사에서는 엔진 위치 허용오차 안에 있지만 잘못된 스칼라값과, 별도로 틀린 컴포넌트 위치를 각각 검출했다. 곡선값·시간·실제 위치 검사를 유지하고 축과 부모 트랜스폼에 맞춰 위치 오차를 정한다. 스윕 이동·부모 스케일·다른 엔진 버전에서는 다시 검증한다.

## 근거

공식 자료는 공개 타입을 확인하는 근거다. 내부 비교 경로와 두 대조 검사의 결과는 당시 UE 5.8.3 관찰이며 이번에 엔진 실험을 재실행하지 않았다. [Epic, USceneComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/Components/USceneComponent?application_version=5.5) · [Epic, TVector](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Core/TVector) · [보간 검증 출처 이력](../../knowledge/sources.md#src-ue-lab-easing-results-md)
