# 시드 기반 던전의 연결성과 실제 이동 여유를 검사하기

**K-GAME-TECH-DUNGEON** · 이진 공간 분할로 방을 배치한 뒤 그래프 연결성과 실제 이동체의 통과 여유를 각각 검사한다.

## 지침

이진 공간 분할(BSP)은 영역을 재귀적으로 나눈다. 잎 영역 안에 방을 배치하고 각 내부 분할의 양쪽 방을 통로로 잇는다. 입구에서 격자를 채우는 flood fill로 도달 가능한 바닥을 구한다. 이동 비용이 일정하면 너비 우선 탐색으로 최단 거리와 먼 출구 후보도 찾을 수 있다. 무작위 보행과 문법 기반 생성은 구조를 제어하는 방식이 다르다.

## 적용 조건과 예외

시드 기반 격자 생성에서 언리얼의 `FRandomStream`은 명시한 시드로 재현 가능한 난수열을 만든다. 재현에는 호출 순서, 생성기, 입력 설정도 같아야 한다. 하위 비트 품질이 낮으므로 제한 범위 선택에는 나머지 연산 대신 제공되는 범위 함수를 사용한다. 격자가 이어져도 캡슐이 지나기에 좁거나 중력 조건에서 통과가 불가능할 수 있다.

## 확인 방법

같은 시드를 다시 실행하고 최종 지도에서 독립적으로 도달 영역을 계산한다. 실제 캡슐로 통로 모서리와 출입구를 스윕한다. 최소 잎 크기, 좁은 통로, 도달 불가능한 목표, 난수 호출 순서 변경을 검사하고 진행 리듬은 플레이테스트로 판단한다.

## 근거

PCG 교재는 구성적 생성 방법을 설명하고 Epic 문서는 시드 스트림의 동작을 명시한다. 기존 언리얼 관찰은 정적인 평면 격자와 수직 캡슐 통과에 한정된다. 실제 캐릭터의 전체 이동과 레벨 품질은 별도 평가가 필요하다.

- [Shaker et al. — Constructive Generation Methods for Dungeons and Levels](https://www.pcgbook.com/chapter03.pdf)
- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Epic — FRandomStream](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Core/FRandomStream)
- [Epic — Random Streams](https://dev.epicgames.com/documentation/en-us/unreal-engine/random-streams-in-unreal-engine)
