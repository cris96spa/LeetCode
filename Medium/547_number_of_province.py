"""
The solution provided is a union-find solution. The union-find data structure is used to keep track of the connected components in the graph.
Alternatively, we can solve this problem using a depth-first search (DFS) approach.
"""

from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """
        There are n cities. Some of them are connected, while some are not. If city a is
        connected directly with city b, and city b is connected directly with city c,
        then city a is connected indirectly with city c.

        A province is a group of directly or indirectly connected cities and no other cities
        outside of the group.

        You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city
        and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.

        Return the total number of provinces.

        Args:
            isConnected (List[List[int]]): An n x n adjacency matrix representing direct connections.

        Returns:
            int: The total number of provinces.
        """
        n = len(isConnected)
        root = [i for i in range(n)]  # Initialize the root node of each city
        rank = [1] * n  # Initialize the rank of each node
        count = n  # Start with each city as its own component

        def find(x):
            if root[x] != x:
                root[x] = find(root[x])  # Path compression
            return root[x]

        def union(x, y):
            nonlocal count
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                # Merge the smaller tree into the larger tree
                if rank[rootX] > rank[rootY]:
                    root[rootY] = rootX
                elif rank[rootX] < rank[rootY]:
                    root[rootX] = rootY
                else:
                    root[rootY] = rootX
                    rank[rootX] += 1
                count -= 1  # Decrement the count of components

        # Iterate through the upper triangle of the matrix
        for row in range(n):
            for col in range(row + 1, n):
                if isConnected[row][col] == 1:
                    union(row, col)

        return count


# Here is the solution using DFS
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """
        There are n cities. Some of them are connected, while some are not. If city a is
        connected directly with city b, and city b is connected directly with city c,
        then city a is connected indirectly with city c.

        A province is a group of directly or indirectly connected cities and no other cities
        outside of the group.

        You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city
        and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.

        Return the total number of provinces.

        Args:
            isConnected (List[List[int]]): An n x n adjacency matrix representing direct connections.

        Returns:
            int: The total number of provinces.
        """
        n = len(isConnected)
        visited = [False] * n
        count = 0

        def dfs(city):
            stack = [city]
            while stack:
                current = stack.pop()
                for neighbor in range(n):
                    if isConnected[current][neighbor] == 1 and not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)

        for city in range(n):
            if not visited[city]:
                count += 1
                visited[city] = True  # Mark as visited when starting a new province

        return count
