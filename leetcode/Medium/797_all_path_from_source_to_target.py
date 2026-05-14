from typing import List


class Solution:
    """Find all possible paths from node 0 to node n-1 in a directed acyclic graph.

    Problem Statement:
        Given a DAG of n nodes labeled 0 to n-1, find all paths from node 0 to node n-1.
        graph[i] is a list of nodes reachable from node i.

    Approach:
        DFS with backtracking. Build the current path as we recurse; when the destination
        is reached, record the path. After exploring each neighbor, pop it to backtrack.

    Complexity:
        Time: O(2^n * n) — up to 2^(n-1) paths each of length up to n.
        Space: O(n) for the current path stack plus O(2^n * n) for the result.
    """

    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        paths: List[List[int]] = []
        path: List[int] = []

        if not graph:
            return paths

        def dfs(node: int) -> None:
            path.append(node)
            if node == len(graph) - 1:
                paths.append(path.copy())
            for next_node in graph[node]:
                dfs(next_node)
                path.pop()

        dfs(0)
        return paths
