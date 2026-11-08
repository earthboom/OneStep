# 빌보드·이미지 대체물의 방향 설정

기준 항목: K-GAME-TECH-BILLBOARD · 확인일: 2026-11-07 · 상태: 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

파티클·원거리 식생·스타일화된 물체에 이미지 평면을 쓴다. 화면 정렬, 시점 지향, 축 고정 방식을 구분한다. 지면 물체는 위쪽 축을 유지하고 단일 이미지로 부족하면 방향별 아틀라스를 사용한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

평면 교차·스테레오·그림자·투명도 정렬·수직 시점에서 한계가 보인다. 화면을 크게 덮으면 빌보드도 비싸다.

## 적용 전 점검

적용 전 점검: 위아래로 시점을 회전하고 실제 카메라·알파 오버드로를 확인한다.

## 근거

- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- 출발 영상: V43. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).

