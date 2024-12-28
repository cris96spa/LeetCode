class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        """
        Given an integer array nums of unique elements, return all possible subsets (the power set).

        The solution set must not contain duplicate subsets. Return the solution in any order.

        Problem Statement:
        - Input: An integer array nums of unique elements.
        - Output: A list of all possible subsets (power set) of the input array.
        - Constraints:
            * 1 <= nums.length <= 10
            * -10 <= nums[i] <= 10
            * All numbers in nums are unique.

        Example 1:
        Input: nums = [1,2,3]
        Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

        Example 2:
        Input: nums = [0]
        Output: [[],[0]]

        Approach:
        - Use a backtracking algorithm to generate all subsets.
        - Maintain a current path to track the subset being constructed.
        - At each recursive call, add the current path to the results list.
        - Explore further elements by appending them to the current path and recursing.
        - After exploring, backtrack by removing the last element to restore the previous state.
        """
        results = []
        n = len(nums)

        def _backtrack(start: int, path: list[int]):
            # Add the current path to the powerset
            results.append(path[:])

            # End of DFS check
            if start == n:
                return

            # Consider the subset of all length from start to len(nums)
            for i in range(start, n):
                # Add current element to the path
                path.append(nums[i])

                # Recursive call
                _backtrack(i + 1, path)

                # Rollback to previous state
                path.pop()

        _backtrack(0, [])
        return results
