"""Check stored graph counterexamples; this is not a game or plugin test."""

import heapq
import json
from pathlib import Path


def check(case):
    outgoing, incoming = {}, {}
    for source, target, cost in case["edges"]:
        assert cost >= 0
        outgoing.setdefault(source, []).append((target, cost))
        incoming.setdefault(target, []).append((source, cost))

    # Reverse search preserves each original directed edge's cost.
    distance, successor = {case["goal"]: 0}, {}
    frontier = [(0, case["goal"])]
    while frontier:
        current_cost, current = heapq.heappop(frontier)
        if current_cost != distance[current]:
            continue
        for previous, edge_cost in incoming.get(current, []):
            candidate = current_cost + edge_cost
            if candidate < distance.get(previous, float("inf")):
                distance[previous] = candidate
                successor[previous] = current
                heapq.heappush(frontier, (candidate, previous))

    start = case["start"]
    naive = min(outgoing[start], key=lambda edge: distance[edge[0]])
    best = min(outgoing[start], key=lambda edge: edge[1] + distance[edge[0]])
    naive_cost = naive[1] + distance[naive[0]]
    best_cost = best[1] + distance[best[0]]
    assert distance[start] == best_cost == case["expected_cost"]
    assert best[0] == successor[start] == case["expected_next"]
    if "naive_expected_cost" in case:
        assert naive_cost == case["naive_expected_cost"] > best_cost

    current, seen, actual_tree_cost = start, set(), 0
    while current != case["goal"]:
        assert current not in seen
        seen.add(current)
        next_node = successor[current]
        actual_tree_cost += next(cost for node, cost in outgoing[current] if node == next_node)
        current = next_node
    assert actual_tree_cost == best_cost

    current, seen = start, set()
    while current != case["goal"] and current not in seen:
        seen.add(current)
        current = min(outgoing[current], key=lambda edge: edge[1] + distance[edge[0]])[0]
    arbitrary_tie_cycles = current != case["goal"]
    if case["id"] == "zero-cost-tie":
        assert arbitrary_tie_cycles
    return dict(case=case["id"], naive_cost=naive_cost, optimal_cost=best_cost,
                next_hop=successor[start], tree_terminates=True,
                arbitrary_argmin_tie_cycles=arbitrary_tie_cycles)


if __name__ == "__main__":
    cases = json.loads(Path(__file__).with_name("weighted-flow-cases.json").read_text(encoding="utf-8"))
    print(json.dumps({"passed": len(cases["graphs"]), "cases": [check(c) for c in cases["graphs"]],
                      "limit": "Graph arithmetic and termination only; no game/runtime execution."}, indent=2))
