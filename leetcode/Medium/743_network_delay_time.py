from collections import defaultdict
from heapq import heappop, heappush


class Solution:
    """Find the minimum time for all n nodes to receive a signal sent from node k.

    Problem Statement:
        Given a directed weighted graph of n nodes and travel times, send a signal from node k.
        Return the time it takes for all nodes to receive the signal, or -1 if impossible.

    Approach:
        Dijkstra's algorithm with a min-heap. Start from k with time 0, explore neighbors by
        expanding the shortest known path. Record shortest time to each node. If all n nodes
        are reached, return the maximum time; otherwise return -1.

    Complexity:
        Time: O((E + V) log V) where E = edges, V = nodes.
        Space: O(E + V) for the graph, heap, and shortest-time dict.
    """

    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((w, v))

        min_heap = [(0, k)]
        shortest_time: dict[int, int] = {}

        while min_heap:
            current_time, node = heappop(min_heap)
            if node in shortest_time:
                continue
            shortest_time[node] = current_time
            for time, neighbor in graph[node]:
                if neighbor not in shortest_time:
                    heappush(min_heap, (current_time + time, neighbor))

        return max(shortest_time.values()) if len(shortest_time) == n else -1
