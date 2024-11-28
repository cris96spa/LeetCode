from collections import defaultdict


class Solution:
    def validPath(
        self, n: int, edges: list[list[int]], source: int, destination: int
    ) -> bool:
        """
        Determine if there is a valid path between source and destination in a bi-directional graph.

        Problem Description:
        There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1
        (inclusive). The edges in the graph are represented as a 2D integer array edges, where
        each edges[i] = [ui, vi] denotes a bi-directional edge between vertex ui and vertex vi.
        Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.

        You want to determine if there is a valid path that exists from vertex source to vertex destination.

        Parameters:
        n (int): The number of vertices in the graph.
        edges (List[List[int]]): A list of bi-directional edges in the graph.
        source (int): The starting vertex.
        destination (int): The target vertex.

        Returns:
        bool: True if there exists a valid path from source to destination, False otherwise.

        Approach:
        1. Build the graph using an adjacency list representation with `defaultdict`.
        2. Use Depth First Search (DFS) to explore the graph. In this implementation, an iterative
           DFS is performed using a stack.
        3. Keep track of visited nodes to prevent infinite loops and redundant processing.
        4. For each node popped from the stack, explore its neighbors. If any neighbor is the
           destination node, return True.
        5. If the stack is exhausted without finding the destination, return False.

        Complexity Analysis:
        - Time Complexity: O(V + E), where V is the number of vertices and E is the number of edges.
          This is due to the graph traversal where each vertex and edge is visited at most once.
        - Space Complexity: O(V), for storing the visited nodes and the stack.

        Example Usage:
        >>> sol = Solution()
        >>> n = 6
        >>> edges = [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]]
        >>> source = 0
        >>> destination = 5
        >>> sol.validPath(n, edges, source, destination)
        False
        """
        # First, we need to build the graph from the list of edges
        graph = defaultdict(list)
        for start, end in edges:
            graph[start].append(end)
            graph[end].append(start)

        # Now, we need to keep track of visited states
        visited = {i: False for i in range(n)}
        visited[source] = True

        # In order to perform a DFS we need a stack. This means that we can either
        # rely on an explicit one or, we can exploit the recursive function call that
        # implicitly uses a stack. Let's use an iterative approach with explicit stack management.
        stack = [source]

        while stack:
            # Get the node on the top of the stack
            curr_node = stack.pop()

            # We need to process now the nodes that are connected with the current one
            for next_node in graph[curr_node]:
                if next_node == destination:
                    return True

                if not visited[next_node]:
                    visited[next_node] = True
                    stack.append(next_node)

        return visited[destination]
