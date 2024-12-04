from typing import List
import collections


class Solution:
    """
    Problem Description:
    ---------------------
    You are given a list of airline tickets where `tickets[i] = [from_i, to_i]` represents the departure
    and arrival airports of one flight. Reconstruct the itinerary in order and return it.

    The itinerary must:
    - Begin with "JFK".
    - Use all the tickets exactly once.
    - Be the lexicographically smallest itinerary if multiple valid itineraries exist.

    Example:
    --------
    Input: [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    Output: ["JFK", "MUC", "LHR", "SFO", "SJC"]

    Approach:
    ---------
    The problem is solved using a depth-first search (DFS) combined with post-order traversal. This approach
    is based on Hierholzer's Algorithm for finding Eulerian paths in a directed graph. To ensure the smallest
    lexicographical order, destinations are sorted in reverse lexicographical order during graph construction
    and processed using a stack.

    Algorithm:
    ----------
    1. Build a directed graph using the given tickets, with each airport as a node and directed edges
       representing flights. The destinations for each airport are sorted in reverse lexicographical order.
    2. Perform a DFS traversal starting from "JFK".
    3. For each airport, recursively visit all its neighbors until no more edges remain.
    4. Append the airport to the itinerary list once all its neighbors are visited (post-order).
    5. Reverse the itinerary list at the end to obtain the correct order.

    Complexity Analysis:
    --------------------
    - Time Complexity:
      - Sorting tickets: O(E log E), where E is the number of tickets.
      - DFS traversal: O(V + E), where V is the number of unique airports (vertices) and E is the number of tickets (edges).
      Total: O(E log E) because E dominates V in typical cases.

    - Space Complexity:
      - Graph storage: O(E) for adjacency list.
      - Call stack depth: O(E) in the worst case due to recursion.
      Total: O(E).

    Parameters:
    -----------
    tickets : List[List[str]]
        A list of flight tickets where each ticket is represented as [from, to].

    Returns:
    --------
    List[str]
        The lexicographically smallest itinerary that uses all the tickets exactly once.
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
            """
            Depth-first search to build the itinerary.
            Parameters:
            -----------
            - source: (str) The current airport being visited.
            """
            while graph[source]:
                next_destination = graph[source].pop()
                dfs(next_destination)
            itinerary.append(source)

        # Start DFS from "JFK"
        dfs("JFK")

        # Reverse the itinerary to obtain the correct order
        return itinerary[::-1]
