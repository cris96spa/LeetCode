from collections import deque


class Solution:
    """Problem: Is Graph Bipartite?

    Given an undirected graph as an adjacency list, determine whether it is bipartite:
    that is, whether its nodes can be partitioned into two independent sets A and B
    such that every edge connects a node in A to a node in B.

    Example:
    Input: graph = [[1, 3], [0, 2], [1, 3], [0, 2]]
    Output: True
    Explanation: Partition the nodes into {0, 2} and {1, 3}.

    Input: graph = [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]
    Output: False
    Explanation: Nodes 0, 1 and 2 form a triangle, so no valid partition exists.

    Approach:
    - Two-color the graph with BFS: give the start node color 0 and each newly
      discovered neighbor the opposite color of the node that discovered it.
    - If an edge ever connects two nodes of the same color, the graph is not bipartite.
    - Start a new BFS from every uncolored node to handle disconnected components.

    Complexity:
    -----------
    - Time: O(|V| + |E|). Every node is enqueued once, and every edge is examined
      twice (once from each endpoint).
    - Space: O(|V|) for the colors array (which also tracks visited nodes) and the queue.
    """

    def isBipartite(self, graph: list[list[int]]) -> bool:
        n = len(graph)

        # -1 = uncolored (not yet visited), 0 / 1 = the two sets
        colors = [-1] * n

        def swap_colors(source_vertex: int) -> int:
            """Return the color opposite to the one assigned to source_vertex."""
            return int(not colors[source_vertex])

        for start in range(n):
            if colors[start] != -1:
                continue

            colors[start] = 0
            queue = deque([start])

            # BFS over the connected component containing start
            while queue:
                vertex = queue.popleft()

                for neighbor in graph[vertex]:
                    if colors[neighbor] == -1:  # undiscovered: assign the opposite color
                        colors[neighbor] = swap_colors(vertex)
                        queue.append(neighbor)
                    elif colors[neighbor] == colors[vertex]:  # same color on both ends of an edge
                        return False

        return True
