# 지형·이동 비용·동시 점유에 맞는 경로 탐색 선택하기

**K-GAME-TECH-PATH** · 그래프 비용, 공통 목표, 이동체 크기에 따라 탐색법을 고른다. 여러 개체의 이동을 예약할 때는 공간과 시간 점유를 함께 표현한다.

## 지침

너비 우선 탐색은 무가중 그래프에서 최단 경로를 구한다. 다익스트라는 비음수 가중치에서 누적 비용이 가장 작은 정점을 확장한다. A*는 누적 비용과 휴리스틱을 더해 순서를 정한다. 허용적 휴리스틱은 남은 비용을 과대평가하지 않는다. 닫힌 정점을 다시 열지 않는 그래프 탐색에서 일반적인 최적성을 유지하려면 일관된 휴리스틱을 쓴다. 다수가 같은 목적지로 가면 목표에서 역방향 탐색해 비용이 낮아지는 방향의 플로 필드를 만들 수 있다. 간선 방향, 비용, 몸체 통과 여유를 반영한다.

## 적용 조건과 예외

동적 경로나 공유 경로에서는 탐색 가능성과 실제 문 닫힘을 구분한다. 새 진입을 막고 기존 통행자가 빠진 뒤 닫는다. 시간 확장 그래프는 상태를 위치와 시각의 쌍으로 나타낸다. 같은 시계에서 정점 점유, 반대 방향 간선, 몸체 스윕, 도착점 점유를 예약한다. 제한된 탐색 기간은 더 늦은 경로를 놓칠 수 있다. 관련 단면을 모든 가능 경로가 통과한다는 그래프 근거가 있을 때만 통로 탐색을 가지치기한다. 우선순위 키를 압축할 때는 전체 순서, 동점 처리, 값 범위와 오버플로를 확인한다.

## 확인 방법

단방향·차단·재개방·협소 간선을 포함해 독립 최단 경로 풀이와 도달성·비용을 비교한다. 예약은 동시 스윕·자리 교환·종료 점유를 검사한다. 충돌 없는 교착과 유효 우회로를 대조 사례로 둔다. 최적화 전후에는 같은 요청 유입에서 전체 경로와 시간을 비교한다.

## 근거

Patel은 단일 목표 탐색과 목적지 기반 필드를, LaValle은 구성 공간과 고정 경로 조정을 설명한다. 인용한 다중 에이전트 연구는 각기 다른 그래프·스케줄 가정을 둔다. 과거 Unity와 Unreal 격자 관찰은 일부 폐쇄, 반경 제약, 유한 예약 경로를 확인했다. 임의의 연속 형상, 무한 시간 공정성, 실서비스 처리 용량은 확인하지 않았다.

- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Amit Patel — Flow Field Pathfinding for Tower Defense](https://www.redblobgames.com/pathfinding/tower-defense/)
- [Li et al., corridor symmetry](https://mapf.info/index.php/Main.SKoen20k)
- [LaValle footprint/C-space](https://lavalle.pl/planning/node161.html)
- [fixed-path coordination](https://lavalle.pl/planning/node325.html)
- [RHCR](https://arxiv.org/abs/2005.07371)
- [PIBT](https://arxiv.org/abs/1901.11282)
- [online pickup/delivery](https://arxiv.org/abs/1705.10868)

### owned paths

재생이나 다른 스레드의 읽기용 경로는 대기와 종료 상태를 포함한 전체 순서 경로의 **소유 스냅샷**으로 보관한다. 탐색기 저장소를 빌린 뷰는 원본이 파괴되거나 재사용되면 무효해진다. 전체 경로를 복사한 뒤 게시하고, 원본을 변경·파괴한 후에도 모든 스텝과 순서가 원래 값인지 검사한다. 언리얼의 점유 중인 문 닫힘은 별도로 검사한다. 새 진입자를 위한 경로장을 갱신하고 기존 통행자가 빠질 때까지 몸체 스윕 여유를 확보한 뒤 물리 충돌을 닫는다. 경로장만으로 국소 회피가 보장되지는 않는다. [C++ Core Guidelines — ownership and lifetime safety](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-ptr)
