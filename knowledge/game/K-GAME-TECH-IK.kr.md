# 제약이 있는 역운동학으로 발 접촉 맞추기

**K-GAME-TECH-IK** · 다리 길이, 무릎 방향, 좌표계, 보행 단계를 고려해 보정한 발바닥 접점으로 다리를 풀고 필요한 골반 보정을 적용한다.

## 지침

역운동학(IK)은 원하는 끝점인 이펙터를 기준으로 관절 트랜스폼을 구한다. 언리얼의 Two Bone IK는 세 관절로 된 사지에 Joint Target Location을 주어 굽힘 방향을 유도한다. FABRIK은 오차 목표와 반복 한도 안에서 체인을 뒤·앞으로 풀어 간다. 이펙터·무릎 목표·지지면을 솔버가 요구하는 좌표계로 맞추고 발바닥이나 신발 형상만큼 발목 목표를 보정한다.

## 적용 조건과 예외

정적 지지면에서는 지지기에 발을 고정하고 유각기에 해제한다. 원본 포즈에서 목표로 블렌딩한 뒤 그 끝점과 양쪽 다리의 도달 범위에 맞는 골반 이동량을 구한다. 양립 가능한 이동량이 없으면 대체 포즈를 쓴다. `UPoseableMeshComponent`로 본 포즈를 다룰 때는 호출한 API가 지원하는 좌표계를 명시한다. 시각 접지와 게임플레이 캡슐은 독립적으로 유지한다.

## 확인 방법

평지와 계단, 양쪽 접촉이 충돌하는 상황, 중간 블렌드, 닿지 않는 지지면, 유각기 해제에서 원본 포즈와 최종 스키닝 포즈를 비교한다. 뒤꿈치·발끝 관통, 무릎 방향, 이전 프레임 포즈 이력, 게임플레이 충돌 상태를 확인한다.

## 근거

Epic 문서는 솔버 제어와 포즈 메시 API를 설명한다. 기존 언리얼 관찰은 스키닝된 이족 모델의 정적 지지면, 보정한 접촉 샘플, 도달 불가 거부에 한정된다. 상용 신발 리그, 이동 지지면, 리타기팅, 실서비스 애니메이션 그래프는 확인하지 않았다.

- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine)
- [Epic — FABRIK AnimBP Node](https://dev.epicgames.com/documentation/unreal-engine/fabrik-animation-blueprint-in-unreal-engine?lang=en-US)
- [Epic — UPoseableMeshComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UPoseableMeshComponent?application_version=5.8)
