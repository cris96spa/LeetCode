from collections import deque


class Solution:
    """Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1,
    find all possible paths from node 0 to node n - 1 and return them in any order.

    The graph is given as follows: graph[i] is a list of all nodes you can visit from node i
    (i.e., there is a directed edge from node i to node graph[i][j]).

    The Idea is to perform a DFS from the initial node and keep track of the path, until
    we reach the destination node. Once we reach the destination node, we add the path to the
    list of paths. This is a typical backtracking problem.

    In backtracking, there are three main steps:
    1. Place candidate: Choose a path to explore. In general, in this step some filtering can be applied as to
    reduce the number of paths to explore. In this case, we do not need to filter anything since we are
    dealing with a DAG.
    2. Explore: Explore the path. This is the recursive step where we explore the path and keep track of the
    current path.
    3. Unplace candidate: Once we have explored the path, we need to remove the last element from the path to revert
    the decision and explore other paths

    The time complexity of this algorithm is: O(2^N * N) where N is the number of nodes in the graph.
    There colud be at most `2^(N-1) - 1` possible paths in the graph. For each path, there could be at most N-2
    intermediate nodes. Therefore, the time complexity is O(2^(N-1)-1) * O(N) = O(2^N * N)

    The space complexity is O(N) since we are using a path list to keep track of the current path.
    However, apart from our algorithm, since at most we could have `2^(N−1)−1` paths as the results
    and each path can contain up to N nodes, we need extra O(2^N * N) space to store and return the results.

    """

    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        # The first thing we can notice is that we have a DAG. This means that,
        # we do not need to explicitly mark visited nodes since the direction of
        # edges and the absence of loops, will prevent to reach an already visited
        # node by construction

        def dfs(node):
            # Add the current node to the path
            path.append(node)

            # Add the path if we reach the destination
            if node == len(graph) - 1:
                paths.append(path.copy())

            for _next in graph[node]:
                dfs(_next)
                # Once a dfs is completed on the _next node, we can remove it from the path
                path.pop()

        paths = []
        path = []

        # Empty graph check
        if not graph or len(graph) == 0:
            return paths

        # Perform the dfs from the initial node
        dfs(0)

        return paths


""" This problem can be solved also using BFS which allow to find each path in order, from the shorter to the longer one.

"""


class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        if not graph or len(graph) == 0:
            return paths

        paths = []

        # Queue for BFS: each element is a path (list of nodes)
        queue = deque()
        queue.append([0])  # Start with a path containing only the source node

        while queue:
            # Extract the current path from the queue
            curr_path = queue.popleft()

            # The current node to be processed is the last element of curr_path
            curr_node = curr_path[-1]

            # We add the directly connected nodes to the path
            for _next in graph[curr_node]:
                # Add the next node to the next path
                next_path = curr_path.copy()
                next_path.append(_next)
                # If we find a path toward the destination, we add it to the list
                if _next == len(graph) - 1:
                    paths.append(next_path)
                else:
                    # Otherwise, we add the path to the queue
                    queue.append(next_path)
        return paths
