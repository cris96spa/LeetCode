from collections import defaultdict
from heapq import heappop, heappush


class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        """
        Problem Statement:
        You are given a network of n nodes, labeled from 1 to n. You are also given `times`,
        a list of travel times as directed edges `times[i] = (ui, vi, wi)`, where `ui` is the
        source node, `vi` is the target node, and `wi` is the time it takes for a signal to
        travel from source to target.

        We will send a signal from a given node k. Return the minimum time it takes for all
        the n nodes to receive the signal. If it is impossible for all the n nodes to receive
        the signal, return -1.

        Constraints:
        - 1 <= k <= n <= 100
        - 1 <= times.length <= 6000
        - times[i].length == 3
        - 1 <= ui, vi <= n
        - ui != vi
        - 0 <= wi <= 100
        - All pairs (ui, vi) are unique.

        Example:
        Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
        Output: 2

        Approach:
        - The problem is modeled as finding the shortest path from a source node (k) to all
          other nodes in a weighted directed graph.
        - We use Dijkstra's algorithm with a priority queue (min-heap) to find the shortest
          paths efficiently.

        Steps:
        1. Represent the graph as an adjacency list for efficient traversal.
        2. Use a min-heap to store nodes along with their current accumulated time.
        3. Maintain a dictionary to store the shortest known time to reach each node.
        4. Process nodes from the min-heap, updating neighbors if a shorter path is found.
        5. After processing all reachable nodes, check if all nodes have been reached.
           If so, return the maximum time from the shortest path dictionary; otherwise, return -1.

        Time Complexity:
        - Building the graph: O(E), where E is the number of edges.
        - Dijkstra's algorithm: O((E + V) log V), where V is the number of nodes.
        - Total: O((E + V) log V)

        Space Complexity:
        - Adjacency list storage: O(E)
        - Heap and shortest path dictionary: O(V)
        - Total: O(E + V)

        """
        # Build the graph as an adjacency list
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((w, v))

        # Min-heap to store the current shortest paths
        min_heap = [(0, k)]  # (current time, current node)

        # Dictionary to store the shortest time to reach each node
        shortest_time = {}

        while min_heap:
            current_time, node = heappop(min_heap)

            # If the node is already visited, skip it
            if node in shortest_time:
                continue

            # Record the shortest time for the current node
            shortest_time[node] = current_time

            # Explore neighbors
            for time, neighbor in graph[node]:
                if neighbor not in shortest_time:
                    heappush(min_heap, (current_time + time, neighbor))

        # If all nodes are reached, return the maximum time; otherwise, return -1
        return max(shortest_time.values()) if len(shortest_time) == n else -1
