from collections import defaultdict, deque
from typing import List


class Solution:
    """Find a valid course ordering to complete all courses given prerequisites.

    Problem Statement:
        Given numCourses and prerequisites where prerequisites[i] = [ai, bi] means bi must be
        taken before ai, return the ordering of courses to take. If impossible (cycle), return [].

    Approach:
        Topological sort using Kahn's algorithm (BFS). Build a directed graph and indegree array.
        Start with courses of indegree 0, process them and reduce neighbors' indegrees. If all
        courses are processed, return the order; otherwise there's a cycle.

    Complexity:
        Time: O(V + E) where V = numCourses and E = len(prerequisites).
        Space: O(V + E) for the graph and indegree array.
    """

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        if not prerequisites:
            return list(range(numCourses))

        graph = defaultdict(list)
        indegree = [0] * numCourses

        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)
            indegree[course] += 1

        queue = deque([i for i in range(numCourses) if indegree[i] == 0])
        if not queue:
            return []

        result = []
        while queue:
            course = queue.popleft()
            result.append(course)
            for neighbor in graph[course]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return result if len(result) == numCourses else []
