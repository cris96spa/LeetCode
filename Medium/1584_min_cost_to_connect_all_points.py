from typing import List, Tuple


class DisjointSets:
    """DisjointSets data structure to support Kruskal's algorithm."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """Finds the root of the set containing x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """Unites the sets containing x and y using union by rank."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            elif self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

    def connected(self, x: int, y: int) -> bool:
        """Checks if x and y are in the same set."""
        return self.find(x) == self.find(y)


class Solution:
    """
    Problem:
    You are given an array points representing integer coordinates of some points on a 2D-plane,
    where points[i] = [xi, yi].

    The cost of connecting two points [xi, yi] and [xj, yj] is the Manhattan distance between them:
    |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.

    Return the minimum cost to make all points connected. All points are connected if there is exactly
    one simple path between any two points.

    Approach:
    This solution uses Kruskal's algorithm to find the Minimum Spanning Tree (MST) of the graph formed
    by the points. The steps are as follows:
      1. Compute a fully connected graph where each edge represents the Manhattan distance between two points.
      2. Sort all edges by their weights (Manhattan distances).
      3. Use a DisjointSets (Union-Find) data structure to keep track of connected components.
      4. Iteratively add the smallest edge to the MST, ensuring no cycles are formed, until all points are connected.

    Algorithm:
    - Time Complexity:
        * Computing the graph: O(n^2), where n is the number of points.
        * Sorting edges: O(E log E), where E = n(n-1)/2 is the number of edges.
        * Kruskal's algorithm (union-find operations): O(E α(n)), where α is the inverse Ackermann function.
      Overall: O(n^2 log n), dominated by edge sorting.
    - Space Complexity: O(n^2) for the graph representation.
    """

    def _manhattan_distance(self, a: List[int], b: List[int]) -> int:
        """Computes the Manhattan distance between two points."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _compute_graph(self, points: List[List[int]]) -> List[Tuple[int, int, int]]:
        """Generates a fully connected graph with edges as (node_i, node_j, distance)."""
        n = len(points)
        graph = []
        for i in range(n):
            for j in range(i + 1, n):
                distance = self._manhattan_distance(points[i], points[j])
                graph.append((i, j, distance))
        return graph

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        """Finds the minimum cost to connect all points using Kruskal's algorithm."""
        n = len(points)

        # Edge case: Single point or two points
        if n == 1:
            return 0
        elif n == 2:
            return self._manhattan_distance(points[0], points[1])

        # Compute the fully connected weighted graph as a list of edges
        graph = self._compute_graph(points)

        # Sort edges by distance (weight)
        graph.sort(key=lambda edge: edge[2])

        # Kruskal's algorithm with DisjointSets
        min_cost = 0
        num_edges = 0
        ds = DisjointSets(n)

        for u, v, weight in graph:
            if not ds.connected(u, v):
                ds.union(u, v)
                min_cost += weight
                num_edges += 1

                # Stop when n-1 edges have been added
                if num_edges == n - 1:
                    break

        return min_cost
