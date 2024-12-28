from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Given a collection of candidate numbers (candidates) and a target number (target),
        find all unique combinations in candidates where the candidate numbers sum to target.

        Each number in candidates may only be used once in the combination.

        Note: The solution set must not contain duplicate combinations.

        Parameters:
        candidates (List[int]): A list of integers representing the candidate numbers.
        target (int): The target sum for the combinations.

        Returns:
        List[List[int]]: A list of unique combinations where the sum equals the target.

        Example:
        --------
        Input: candidates = [10,1,2,7,6,1,5], target = 8
        Output:
        [
          [1,1,6],
          [1,2,5],
          [1,7],
          [2,6]
        ]

        Example:
        --------
        Input: candidates = [2,5,2,1,2], target = 5
        Output:
        [
          [1,2,2],
          [5]
        ]

        Constraints:
        1 <= candidates.length <= 100
        1 <= candidates[i] <= 50
        1 <= target <= 30
        """
        results = []
        candidates.sort()

        def _backtrack(start: int, path: List[int], curr_sum: int):
            if curr_sum == target:
                results.append(path[:])
                return

            for i in range(start, len(candidates)):
                # Skip duplicates
                if i > start and candidates[i] == candidates[i - 1]:
                    continue

                # Stop the loop if the current sum exceeds the target
                if curr_sum + candidates[i] > target:
                    break

                path.append(candidates[i])
                _backtrack(i + 1, path, curr_sum + candidates[i])
                path.pop()

        _backtrack(0, [], 0)
        return results
