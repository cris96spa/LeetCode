from collections import defaultdict, deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Problem Statement:
        ------------------
        There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
        You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must
        take course bi first if you want to take course ai.

        Return the ordering of courses you should take to finish all courses. If there are many valid
        answers, return any of them. If it is impossible to finish all courses, return an empty array.

        Solution:
        ---------
        The problem can be solved using a topological sorting approach with the help of Kahn's algorithm.
        This involves:
        1. Building a directed graph using the prerequisites array.
        2. Maintaining an indegree array to track the number of prerequisites for each course.
        3. Initializing a queue with all courses that have no prerequisites (indegree of 0).
        4. Performing a BFS to process each course, appending it to the result list and reducing the
           indegree of its neighbors. Any neighbor with an indegree of 0 is added to the queue.
        5. If the result list contains all courses, return it. Otherwise, return an empty list, indicating
           a cycle in the graph and thus an impossible course schedule.

        Args:
            numCourses (int): The total number of courses.
            prerequisites (List[List[int]]): List of prerequisite pairs, where each pair [ai, bi] means
                                             course bi must be taken before course ai.

        Returns:
            List[int]: A valid ordering of courses to finish all courses, or an empty list if impossible.

        Examples:
        ---------
            Input: numCourses = 2, prerequisites = [[1,0]]
            Output: [0,1]

            Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
            Output: [0,2,1,3] or [0,1,2,3]

            Input: numCourses = 1, prerequisites = []
            Output: [0]

        Constraints:
        ------------
            1 <= numCourses <= 2000
            0 <= prerequisites.length <= numCourses * (numCourses - 1)
            prerequisites[i].length == 2
            0 <= ai, bi < numCourses
            ai != bi
            All the pairs [ai, bi] are distinct.
        """
        # Special case: no prerequisites
        if not prerequisites:
            return [i for i in range(numCourses)]

        # Build the adjacency list and indegree structure
        graph = defaultdict(list)
        indegree = [0] * numCourses

        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)
            indegree[course] += 1

        # Initialize the queue with courses that have no prerequisites
        queue = deque([i for i in range(numCourses) if indegree[i] == 0])

        # If no course has indegree 0, return an empty list (cycle exists)
        if not queue:
            return []

        result = []

        # Perform BFS
        while queue:
            course = queue.popleft()
            result.append(course)

            # Decrease the indegree of neighboring courses
            for neighbor in graph[course]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        # If we couldn't process all courses, return an empty list (cycle exists)
        return result if len(result) == numCourses else []
