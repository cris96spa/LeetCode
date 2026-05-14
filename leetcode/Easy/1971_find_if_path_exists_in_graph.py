from collections import defaultdict


class Solution:
    """Determine if a valid path exists between two vertices in an undirected graph.

    Problem Statement:
        There is a bi-directional graph with n vertices labeled 0 to n-1. Edges
        are given as a 2D list where edges[i] = [u, v] represents a connection
        between u and v. Determine if there is a path from source to destination.

    Approach:
        Build an adjacency list from the edge list. Then run an iterative DFS
        using an explicit stack. Track visited nodes to avoid revisiting. If the
        destination is reached from any neighbor, return True immediately. If
        the stack is exhausted without reaching the destination, return False.

    Complexity:
        Time: O(V + E), where V is the number of vertices and E the number of
            edges. Each vertex and edge is visited at most once.
        Space: O(V) for the visited set and the DFS stack.
    """

    def validPath(
        self, n: int, edges: list[list[int]], source: int, destination: int
    ) -> bool:
        graph = defaultdict(list)
        for start, end in edges:
            graph[start].append(end)
            graph[end].append(start)

        visited = {i: False for i in range(n)}
        visited[source] = True
        stack = [source]

        while stack:
            curr_node = stack.pop()

            for next_node in graph[curr_node]:
                if next_node == destination:
                    return True

                if not visited[next_node]:
                    visited[next_node] = True
                    stack.append(next_node)

        return visited[destination]
