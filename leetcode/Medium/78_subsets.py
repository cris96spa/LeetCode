class Solution:
    """Return all possible subsets (power set) of an integer array with unique elements.

    Problem Statement:
        Given an integer array nums of unique elements, return all possible subsets. The
        solution set must not contain duplicate subsets.

    Approach:
        Backtracking: at each step add the current path to results, then explore remaining
        elements by appending and recursing. After each recursive call, backtrack by popping.

    Complexity:
        Time: O(2^n * n) — 2^n subsets, each taking O(n) to copy.
        Space: O(n) for the recursion stack.
    """

    def subsets(self, nums: list[int]) -> list[list[int]]:
        results: list[list[int]] = []
        n = len(nums)

        def _backtrack(start: int, path: list[int]) -> None:
            results.append(path[:])
            if start == n:
                return
            for i in range(start, n):
                path.append(nums[i])
                _backtrack(i + 1, path)
                path.pop()

        _backtrack(0, [])
        return results
