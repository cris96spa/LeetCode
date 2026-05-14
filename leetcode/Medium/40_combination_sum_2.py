from typing import List


class Solution:
    """Find all unique combinations in candidates that sum to target, each number used once.

    Problem Statement:
        Given a collection of candidate numbers and a target, find all unique combinations
        where the numbers sum to target. Each number may only be used once and the solution
        set must not contain duplicate combinations.

    Approach:
        Sort candidates, then use backtracking. Skip duplicates at the same recursion level
        (i > start and candidates[i] == candidates[i-1]). Prune when sum exceeds target.

    Complexity:
        Time: O(2^n) in the worst case for backtracking.
        Space: O(n) for the recursion stack.
    """

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        results: List[List[int]] = []
        candidates.sort()

        def _backtrack(start: int, path: List[int], curr_sum: int) -> None:
            if curr_sum == target:
                results.append(path[:])
                return
            for i in range(start, len(candidates)):
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                if curr_sum + candidates[i] > target:
                    break
                path.append(candidates[i])
                _backtrack(i + 1, path, curr_sum + candidates[i])
                path.pop()

        _backtrack(0, [], 0)
        return results
