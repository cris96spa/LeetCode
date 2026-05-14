import collections
from typing import List


class Solution:
    """Reconstruct the lexicographically smallest flight itinerary starting from JFK.

    Problem Statement:
        Given a list of airline tickets [from_i, to_i], reconstruct the itinerary starting
        at "JFK" using all tickets exactly once. Return the lexicographically smallest
        valid itinerary.

    Approach:
        Hierholzer's Algorithm with DFS. Build an adjacency list sorted in reverse order so
        the lexicographically smallest destination is processed last (using pop). Post-order
        append to itinerary, then reverse.

    Complexity:
        Time: O(E log E) dominated by sorting.
        Space: O(E) for the graph and call stack.
    """

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # Initialize the directed graph as an adjacency list
        graph = collections.defaultdict(list)

        # Build the graph with destinations sorted in reverse lexicographical order
        for source, destination in sorted(tickets, reverse=True):
            graph[source].append(destination)

        # Itinerary to store the result
        itinerary = []

        def dfs(source: str):
            # Depth-first search to build the itinerary
            while graph[source]:
                next_destination = graph[source].pop()
                dfs(next_destination)
            itinerary.append(source)

        # Start DFS from "JFK"
        dfs("JFK")

        # Reverse the itinerary to obtain the correct order
        return itinerary[::-1]
