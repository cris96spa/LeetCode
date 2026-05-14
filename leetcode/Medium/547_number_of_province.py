from typing import List


class Solution:
    """Find the total number of provinces (connected components) among n cities.

    Problem Statement:
        Given an n x n adjacency matrix isConnected where isConnected[i][j] = 1 means city i
        and city j are directly connected, return the total number of provinces. A province is
        a group of directly or indirectly connected cities.

    Approach:
        Union-Find with path compression and rank-based merging. Start with each city as its
        own component. For each direct connection, union the two cities. The result is the
        number of remaining independent components.

    Complexity:
        Time: O(n^2 * alpha(n)) where alpha is the inverse Ackermann function (near O(1)).
        Space: O(n) for the root and rank arrays.
    """

    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        root = list(range(n))
        rank = [1] * n
        count = n

        def find(x):
            if root[x] != x:
                root[x] = find(root[x])
            return root[x]

        def union(x, y):
            nonlocal count
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                if rank[rootX] > rank[rootY]:
                    root[rootY] = rootX
                elif rank[rootX] < rank[rootY]:
                    root[rootX] = rootY
                else:
                    root[rootY] = rootX
                    rank[rootX] += 1
                count -= 1

        for row in range(n):
            for col in range(row + 1, n):
                if isConnected[row][col] == 1:
                    union(row, col)

        return count
