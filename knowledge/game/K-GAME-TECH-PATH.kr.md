---
id: K-GAME-TECH-PATH
title: 질의 구조에 따라 A*와 흐름장 선택하기
summary: 그래프 비용, 공유하는 목적지, 개체가 차지하는 공간을 기준으로 탐색을 선택한다. 예약 기반 다중 개체 이동에서는 공간과 시간을 함께 다룬다.
kind: reference
scope: 게임 개발. 공유 경로가 바뀔 때 통과 가능 여부와 실제 통로 폐쇄를 구분한다.
keywords: ["A*", "Dijkstra", "flow", "field", "navigation", "topology", "dynamic-obstacle", "door", "traversal", "reservation", "길찾기", "에이스타", "다익스트라", "플로필드", "bidirectional", "corridor", "radius", "clearance", "deadlock", "교행", "양방향", "반경", "통로", "교착", "경로장", "개체", "lifelong", "sustained", "inflow", "queue", "FIFO", "starvation", "overload", "throughput", "unlaned", "time-expanded", "지속", "유입", "개별", "무한", "대기", "차선", "없는", "지형", "시간", "확장", "예약", "과부하", "breadth-first search", "admissible heuristic", "consistent heuristic", "flow field", "time-expanded graph", "multi-agent path finding", "configuration space", "priority queue", "horizon pruning", "owned paths", "snapshot", "source destruction", "path order", "언리얼", "점유", "문 닫힘", "국소 회피"]
status: active
checked_at: '2026-11-11'
---
# 질의 구조에 따라 A*와 흐름장 선택하기

## 지침

너비 우선 탐색은 가중치가 없는 그래프에서 최단 경로를 찾습니다. 다익스트라는 음이 아닌 누적 비용이 가장 낮은 정점을 먼저 확장합니다. A*는 누적 비용과 휴리스틱의 합으로 순서를 정합니다. 허용적 휴리스틱은 남은 비용을 과대평가하지 않습니다. 닫힌 노드를 다시 열지 않는 그래프 탐색에서 통상적인 최적성 보장을 얻으려면 일관적인 휴리스틱을 사용합니다. 여러 개체의 목적지가 같다면 목적지에서 역방향 탐색을 수행해 비용이 낮아지는 이웃을 가리키는 흐름장을 만들 수 있습니다. 간선 방향, 이동 비용, 개체별 통과 여유를 반영합니다.

## 적용 조건과 예외

공유 경로가 바뀔 때는 새로운 진입 금지와 실제 폐쇄를 구분합니다. 새 경로부터 막고 이미 지나가는 개체가 빠져나간 뒤 문을 닫습니다. 시간 확장 그래프는 상태에 위치와 시간을 함께 둡니다. 정점 점유, 반대 방향 간선, 몸체가 휩쓰는 공간, 마지막 위치 점유를 같은 시간 기준으로 예약합니다. 계획 시간창이 짧으면 경로를 놓칠 수 있습니다. 가능한 모든 경로가 해당 절단면을 통과한다는 그래프 근거가 있을 때만 통로를 가지치기합니다. 우선순위 큐의 압축 키는 오버플로 없이 원래 순서와 동점 처리, 값 범위를 보존해야 합니다.

경로를 재생용으로 저장하거나 다른 스레드에서 읽을 때는 대기와 마지막 상태까지 포함한 순서 있는 경로 전체를 소유하는 스냅샷을 만듭니다. 계획기의 저장소를 참조만 하면 원본이 파괴되거나 재사용될 때 무효화됩니다. 전부 복사한 뒤 공개합니다. 원본을 바꾸거나 제거한 뒤에도 저장된 각 단계와 순서가 최초 경로와 일치하는지 비교합니다. 언리얼에서 개체가 문을 지나고 있다면 새 진입 경로 갱신, 이동 중 몸체의 통과 공간 유지, 물리 충돌로 닫기 순서를 플레이에서 별도로 확인합니다. 경로장만으로 근거리 회피가 구현되지는 않습니다. [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-ptr)

## 검사

우선순위 키(`PriorityKey`)를 압축할 때 압축 키로 정렬한 상태 순서를 원래 우선순위 튜플로 정렬한 결과와 대조합니다. 거리가 같은 동점, 마지막 상태 동점 기준, 각 필드 최댓값 근처를 포함합니다. 둘 다 목적지에 도달해도 순서가 바뀌면 선택한 경로가 달라질 수 있습니다.

방향 간선, 막힌 간선, 다시 열린 간선, 좁은 간선을 포함해 독립적인 최단 경로 해와 도달 가능성 및 비용을 대조합니다. 예약에서는 동시 이동의 휩쓸림, 위치 교환, 최종 점유를 검사합니다. 충돌 없이 교착되는 경우와 정상 우회를 대조군에 포함합니다. 최적화를 채택하기 전에 같은 요청 부하에서 전체 경로와 시간을 비교합니다.

## 근거

Patel은 단일 목표 탐색과 재사용할 수 있는 목적지 필드를 설명합니다. LaValle은 구성 공간과 고정 경로 조정을 다룹니다. 아래 다중 개체 논문들은 그래프와 스케줄링 가정이 서로 다릅니다. 이전 Unity·Unreal 격자 관찰은 일부 통로 폐쇄, 반경 제한, 유한한 이동 예약을 다뤘습니다. 임의의 연속 공간, 무한히 이어지는 요청의 공정성, 실제 서비스 처리량은 별도 검증이 필요합니다.

- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Amit Patel — Flow Field Pathfinding for Tower Defense](https://www.redblobgames.com/pathfinding/tower-defense/)
- [Li et al., corridor symmetry](https://mapf.info/index.php/Main.SKoen20k)
- [LaValle footprint/C-space](https://lavalle.pl/planning/node161.html)
- [fixed-path coordination](https://lavalle.pl/planning/node325.html)
- [RHCR](https://arxiv.org/abs/2005.07371)
- [PIBT](https://arxiv.org/abs/1901.11282)
- [online pickup/delivery](https://arxiv.org/abs/1705.10868)
