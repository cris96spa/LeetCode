class Solution:
    """
    Problem Description:
    ---------------------
    Given an array `nums` of distinct integers, return all the possible permutations of the array.
    You can return the answer in any order.

    Approach:
    ---------
    This solution uses a backtracking approach to generate all permutations of the input list `nums`.

    Steps:
    1. Use a helper function `backtrack` to construct permutations step by step.
    2. Use a `used` array to keep track of elements already included in the current permutation to avoid duplicates.
    3. At each step, iterate through all elements in `nums`:
       - If the element is not used, include it in the current path, mark it as used, and recurse.
       - After recursion, remove the element from the current path and mark it as unused to explore other possibilities.
    4. When the path length equals the length of `nums`, it represents a valid permutation, so append a copy of the path to the results.

    Complexity:
    -----------
    - Time Complexity: O(n * n!), where n is the length of `nums`.
      - There are n! permutations, and for each permutation, we perform O(n) work.
    - Space Complexity: O(n * n!) due to result storage and recursion stack.

    Example:
    --------
    Input: nums = [1, 2, 3]
    Output: [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """

    def permute(self, nums: list[int]) -> list[list[int]]:
        results = []
        used = [False] * len(nums)  # To track used elements

        def backtrack(path: list[int]) -> None:
            # Exit condition: path contains all elements
            if len(path) == len(nums):
                results.append(path[:])  # Append a copy of path
                return

            # Iterate through the elements
            for i in range(len(nums)):
                if not used[i]:  # Check if the element is used
                    # Make a choice
                    path.append(nums[i])
                    used[i] = True

                    # Recurse
                    backtrack(path)

                    # Undo the choice
                    path.pop()
                    used[i] = False

        # Start backtracking
        backtrack([])

        return results
