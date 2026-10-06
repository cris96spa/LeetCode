class Solution:
    """🎲 Permutations II.

    Problem:
    --------
    Given a collection of numbers `nums` that might contain duplicates, return all possible
    unique permutations, in any order.

    Approach:
    ---------
    Backtracking as in Permutations (46), with a `used` array marking which indices are in
    the current candidate. Duplicates are pruned by sorting `nums` first, so equal values
    sit next to each other, and then forcing equal values to be placed in index order:
    skip `nums[idx]` when it equals `nums[idx - 1]` and `nums[idx - 1]` is not used.
    In that case the previous copy was already tried at this position and backtracked,
    so placing this copy here would rebuild the same permutations.
    - Complete: when the candidate holds `len(nums)` numbers, record a copy.
    - Make move: mark `idx` as used and append `nums[idx]`, then recurse.
    - Unmake move: unmark `idx` and pop.

    Complexity:
    -----------
    - Time: O(n * n!), at most n! permutations (all values distinct), each built and copied
      in O(n). The O(n log n) sort is dominated.
    - Space: O(n) auxiliary for `used`, the candidate and the recursion stack;
      O(n * n!) for the output.
    """

    def permuteUnique(self, nums: list[int]) -> list[list[int]]:
        results: list[list[int]] = []
        candidate: list[int] = []
        used: list[bool] = [False] * len(nums)
        nums.sort()

        def backtrack() -> None:
            if len(candidate) == len(nums):
                results.append(candidate[:])
                return

            for idx in range(len(nums)):
                if used[idx]:
                    continue

                # Equal values go in index order: skip a copy whose previous copy is unused
                if idx > 0 and nums[idx] == nums[idx - 1] and not used[idx - 1]:
                    continue

                used[idx] = True
                candidate.append(nums[idx])
                backtrack()
                used[idx] = False
                candidate.pop()

        backtrack()
        return results
