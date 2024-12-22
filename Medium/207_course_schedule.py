from collections import defaultdict


class Solution:
    """
    Problem: Can you finish all courses given the prerequisites?

    There are a total of `numCourses` courses labeled from 0 to `numCourses - 1`.
    Each course may have prerequisites, represented as pairs [a, b] where to take course `a`,
    you must first complete course `b`. Determine if it is possible to finish all courses.

    Example:
    Input: numCourses = 2, prerequisites = [[1, 0]]
    Output: True
    Explanation: To take course 1 you must first complete course 0. This is possible.

    Input: numCourses = 2, prerequisites = [[1, 0], [0, 1]]
    Output: False
    Explanation: To take course 1 you must complete course 0, and vice versa. This forms a cycle.

    Approach:
    - Use a graph (adjacency list) to represent course dependencies.
    - Perform Depth-First Search (DFS) to detect cycles.
      - Mark nodes as:
        0: Unvisited
        1: In progress (currently being processed in the stack)
        2: Fully processed
      - If a node is encountered in the "in-progress" state, a cycle exists.
    - Run the DFS for all courses to handle disconnected components.
    """

    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        # Build the adjacency list for the graph
        graph = defaultdict(list)
        for course, pre in prerequisites:
            graph[pre].append(course)

        # Track the state of each course: 0 = unvisited, 1 = in progress, 2 = processed
        visited = [0] * numCourses

        def dfs(course: int) -> bool:
            """
            Perform a DFS to check for cycles.
            Returns False if a cycle is detected, otherwise True.
            """
            if visited[course] == 1:  # Cycle detected
                return False
            if visited[course] == 2:  # Already processed
                return True

            # Mark the course as in progress
            visited[course] = 1

            # Visit all dependent courses
            for neighbor in graph[course]:
                if not dfs(neighbor):
                    return False

            # Mark the course as processed
            visited[course] = 2
            return True

        # Run DFS for each course
        for course in range(numCourses):
            if not dfs(course):
                return False

        return True
