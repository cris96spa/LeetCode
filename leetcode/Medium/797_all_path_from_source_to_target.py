class Solution:
    """🎲 All Paths From Source to Target.

    Problem:
    --------
    Given a directed acyclic graph of `n` nodes labeled 0 to n - 1, where `graph[i]` lists
    the nodes reachable from node `i`, return all paths from node 0 to node n - 1, in any
    order.

    Approach:
    ---------
    Backtracking over the current path, starting from [0]. The graph is acyclic, so a path
    can never revisit a node and no visited set is needed.
    - Complete: when the current node is n - 1, record a copy of the path.
    - Make move: append an outgoing neighbor, then recurse from it.
    - Unmake move: pop it.

    A DAG has at most n(n - 1) / 2 edges, but the number of paths can be exponential: in the
    complete DAG (an edge i -> j for every i < j) each of the n - 2 inner nodes is either on
    a path or not, giving 2^(n - 2) paths from 0 to n - 1.

    Complexity:
    -----------
    - Time: O(n * 2^n), up to 2^(n - 2) paths, each copied in O(n).
    - Space: O(n) auxiliary for the path and the recursion stack; O(n * 2^n) for the output.
    """

    def allPathsSourceTarget(self, graph: list[list[int]]) -> list[list[int]]:
        results: list[list[int]] = []
        path: list[int] = [0]
        n = len(graph)

        def backtrack(node: int) -> None:
            if node == n - 1:
                results.append(path[:])
                return

            for adj in graph[node]:
                path.append(adj)
                backtrack(adj)
                path.pop()

        backtrack(0)
        return results
