class Solution:
    """🎲 Combination Sum.

    Problem:
    --------
    Given an array of distinct integers `candidates` and an integer `target`, return all
    unique combinations of candidates that sum to `target`, in any order. Each candidate
    may be chosen an unlimited number of times.

    Approach:
    ---------
    Backtracking over the "choose the next element" tree, as in Combinations (77), except
    that the recursion restarts from the same index instead of the next one, so the current
    candidate can be reused. Never going back to an earlier index means each combination is
    built in non-decreasing order, so different orderings of it are never generated.
    - Complete: when the path sums to `target`, record a copy.
    - Make move: append `candidates[idx]`, then recurse from `idx`.
    - Unmake move: pop it.
    - Prune: with `candidates` sorted, once `sum_of_path + candidates[idx] > target` every
      later candidate is too large as well, so `break` instead of `continue`.

    Complexity:
    -----------
    Let m = min(candidates) and d = target // m, the maximum depth of the recursion.
    - Time: O(n^d) as a loose upper bound, with up to n branches per level and depth d;
      each valid combination is copied in O(d). The O(n log n) sort is dominated.
    - Space: O(d) auxiliary for the path and the recursion stack; the output depends on the
      number of valid combinations and their lengths.
    """

    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        results: list[list[int]] = []
        path: list[int] = []
        candidates.sort()

        def backtrack(start: int, sum_of_path: int) -> None:
            if sum_of_path == target:
                results.append(path[:])
                return

            for idx in range(start, len(candidates)):
                candidate = candidates[idx]

                # Sorted, so every later candidate overshoots as well
                if sum_of_path + candidate > target:
                    break

                sum_of_path += candidate
                path.append(candidate)
                backtrack(idx, sum_of_path)
                sum_of_path -= candidate
                path.pop()

        backtrack(start=0, sum_of_path=0)
        return results
