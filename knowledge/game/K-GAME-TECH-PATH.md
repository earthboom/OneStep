---
id: K-GAME-TECH-PATH
title: Choose A-star or flow fields by query structure
summary: Choose search by graph costs, goal sharing and agent footprint. For scheduled multi-agent motion,
  model occupancy in time as well as space.
kind: reference
scope: Game development. For changing or shared routes, distinguish traversability from physical closure.
keywords: ["A*", "Dijkstra", "flow", "field", "navigation", "topology", "dynamic-obstacle", "door", "traversal", "reservation", "길찾기", "에이스타", "다익스트라", "플로필드", "bidirectional", "corridor", "radius", "clearance", "deadlock", "교행", "양방향", "반경", "통로", "교착", "경로장", "개체", "lifelong", "sustained", "inflow", "queue", "FIFO", "starvation", "overload", "throughput", "unlaned", "time-expanded", "지속", "유입", "개별", "무한", "대기", "차선", "없는", "지형", "시간", "확장", "예약", "과부하", "breadth-first search", "admissible heuristic", "consistent heuristic", "flow field", "time-expanded graph", "multi-agent path finding", "configuration space", "priority queue", "horizon pruning", "owned paths", "snapshot", "source destruction", "path order", "언리얼", "점유", "문 닫힘", "국소 회피"]
status: active
checked_at: '2026-11-11'
---
# Choose A-star or flow fields by query structure

## Guidance

Breadth-first search finds shortest paths on an unweighted graph. Dijkstra's algorithm expands lowest accumulated cost for nonnegative weights. A* orders by accumulated cost plus a heuristic. An admissible heuristic never overestimates remaining cost. If closed nodes cannot reopen, use a consistent heuristic for the usual graph-search optimality guarantee. For many agents sharing a goal, reverse search from that goal can produce a flow field of downhill choices. Respect directed edges, movement cost and each body's clearance.

## Applicability and exceptions

For changing or shared routes, distinguish traversability from physical closure. Block new routes first and drain existing traversals before closing a door. A time-expanded graph gives each state a location and time. Reserve vertex occupancy, opposing edges, footprint sweeps and final occupancy under a common clock. A bounded planning horizon can miss a route. Prune a corridor only when the graph proves that every feasible route crosses the relevant cut. In a priority queue, compact keys must preserve the full ordering, tie-breaks and range without overflow.

When a route is saved for replay or read on another thread, take an **owned snapshot** of each complete ordered path, including waits and the terminal state. A non-owning view into planner storage becomes invalid when its source is destroyed or reused. Publish only after copying the complete data. Destroy or mutate the source and compare every saved step and its order against the original. For an occupied door in Unreal, perform a separate gameplay check: update the route field for new entrants, preserve the traversing body's swept clearance until it exits, then close physical collision. A route field alone supplies no local avoidance. [C++ Core Guidelines — ownership and lifetime safety](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-ptr)

## Checks

Check reachability and cost against an independent shortest-path solution, including directed, blocked, reopened and narrow edges. For reservations audit simultaneous sweeps, swaps and terminal occupancy. Include a safe deadlock and a valid detour as controls. Compare complete paths and timing at equal offered demand before adopting optimizations.

## Evidence

Patel explains single-goal search and reusable destination fields. LaValle covers configuration space and coordinating fixed paths. The cited multi-agent papers have distinct graph and scheduling assumptions. Prior Unity and Unreal grid observations covered selected closures, radius constraints and finite scheduled routes. They leave arbitrary continuous geometry, lifelong fairness and production capacity open.

- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Amit Patel — Flow Field Pathfinding for Tower Defense](https://www.redblobgames.com/pathfinding/tower-defense/)
- [Li et al., corridor symmetry](https://mapf.info/index.php/Main.SKoen20k)
- [LaValle footprint/C-space](https://lavalle.pl/planning/node161.html)
- [fixed-path coordination](https://lavalle.pl/planning/node325.html)
- [RHCR](https://arxiv.org/abs/2005.07371)
- [PIBT](https://arxiv.org/abs/1901.11282)
- [online pickup/delivery](https://arxiv.org/abs/1705.10868)
