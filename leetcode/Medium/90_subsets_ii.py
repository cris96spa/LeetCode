class Solution:
    """🎲 Subsets II.

    Problem:
    --------
    Given an integer array `nums` that may contain duplicates, return all possible subsets
    (the power set), in any order. The solution set must not contain duplicate subsets.

    Approach:
    ---------
    Backtracking as in Subsets (78): each node extends the candidate with an element after
    the last one picked, so every node of the tree is a distinct subset. Duplicates are
    pruned by sorting `nums` first, so equal values sit next to each other, and then picking
    only the first of a run of equal values at each position: skip `nums[idx]` when
    `idx > start_idx` and it equals `nums[idx - 1]`. A later copy at the same position would
    rebuild the subsets the first copy already produced.
    - Complete: every call is a valid subset, so record a copy on entry.
    - Make move: append `nums[idx]`, then recurse from `idx + 1`.
    - Unmake move: pop it.

    Complexity:
    -----------
    - Time: O(n * 2^n), at most 2^n subsets (all values distinct), each copied in O(n).
      The O(n log n) sort is dominated.
    - Space: O(n) auxiliary for the candidate and the recursion stack;
      O(n * 2^n) for the output.
    """

    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        results: list[list[int]] = []
        candidate: list[int] = []
        nums.sort()

        def backtrack(start_idx: int) -> None:
            results.append(candidate[:])

            for idx in range(start_idx, len(nums)):
                if idx > start_idx and nums[idx] == nums[idx - 1]:
                    continue

                candidate.append(nums[idx])
                backtrack(idx + 1)
                candidate.pop()

        backtrack(0)
        return results
