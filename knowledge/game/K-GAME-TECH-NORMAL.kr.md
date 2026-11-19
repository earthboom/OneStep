# 노멀 매핑으로 조명 디테일 추가

기준 항목: K-GAME-TECH-NORMAL · 확인일: 2026-11-07 · 상태: 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

메시보다 세밀한 조명 디테일이 필요할 때 사용한다. 저장 벡터를 정해진 공간으로 복원하고 호환 탄젠트 기저로 변환한 뒤 정규화한다. 베이크·임포트·렌더링의 노멀맵 규약을 일치시킨다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

일반 노멀 매핑은 실루엣·충돌·실제 높이를 바꾸지 않는다. 2D 스프라이트도 노멀맵을 사용하는 조명 파이프라인이 필요하다.

## 적용 전 점검

적용 전 점검: 조명을 회전시키고 UV 반전·경계·압축·낮은 밉 단계에서 확인한다.

## 근거

- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- 출발 영상: V26. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


## tangent-space normal map의 적용과 확인

탄젠트 공간 노멀 맵은 메시 표면을 기준으로 한 방향을 저장한다. 노멀 맵 규약에는 탄젠트 공간 Y축의 부호도 포함된다. Godot는 OpenGL 방식의 노멀을 기대한다. 조명이나 형상을 수정하기 전에 돌출 방향을 아는 표면에서 광원을 움직여 확인한다.

검색어 · tangent-space normal map, normal map convention

[Godot, Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html)은 용어와 적용 조건의 근거다. 제안한 검사는 대상 환경에서 수행한다.
