from heapq import heappop, heappush
from typing import List


class Solution:
    """Find the minimum cost to connect all points using Manhattan distance (MST).

    Problem Statement:
        Given points[i] = [xi, yi] on a 2D plane, the cost of connecting two points is their
        Manhattan distance |xi-xj| + |yi-yj|. Return the minimum cost to connect all points
        (minimum spanning tree).

    Approach:
        Prim's Algorithm: start from node 0, maintain a min-heap of (cost, node). Always
        expand the cheapest unvisited node, adding its edges to the heap. Stop once all n
        nodes are included.

    Complexity:
        Time: O(n^2 log n) — n nodes each examining n neighbors with heap operations.
        Space: O(n) for the heap and visited array.
    """

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n == 1:
            return 0

        min_cost = 0
        min_heap = [(0, 0)]
        visited = [False] * n
        edges_used = 0

        while edges_used < n:
            cost, current = heappop(min_heap)

            if visited[current]:
                continue

            visited[current] = True
            min_cost += cost
            edges_used += 1

            for next_point in range(n):
                if not visited[next_point]:
                    dist = abs(points[current][0] - points[next_point][0]) + abs(
                        points[current][1] - points[next_point][1]
                    )
                    heappush(min_heap, (dist, next_point))

        return min_cost
