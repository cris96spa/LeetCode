class Solution:
    """🎲 Combinations.

    Problem:
    --------
    Given two integers `n` and `k`, return all possible combinations of `k` numbers chosen
    from the range [1, n], in any order.

    There are C(n, k) = n! / (k! (n - k)!) of them; for example, C(4, 2) = 6.

    Approach:
    ---------
    Backtracking over the "choose the next element" tree: each node extends the current
    candidate with a number larger than every number already in it, so each combination
    is generated exactly once, in increasing order.
    - Complete: when the candidate holds `k` numbers, record a copy.
    - Make move: append the next number, then recurse from the number after it.
    - Unmake move: pop it.
    - Prune: with `remaining = k - len(candidate)` numbers still to pick, the next number
      must leave at least `remaining - 1` larger ones after it, so the loop stops at
      index `n - remaining` instead of `n - 1`.

    Complexity:
    -----------
    - Time: O(k * C(n, k)), one O(k) copy per combination.
    - Space: O(k) auxiliary for the candidate and the recursion stack;
      O(k * C(n, k)) for the output.
    """

    def combine(self, n: int, k: int) -> list[list[int]]:
        results: list[list[int]] = []
        candidate: list[int] = []

        def backtrack(start: int) -> None:
            if len(candidate) == k:
                results.append(candidate[:])
                return

            remaining = k - len(candidate)
            for idx in range(start, n - remaining + 1):  # leave room for the remaining picks
                candidate.append(idx + 1)
                backtrack(idx + 1)
                candidate.pop()

        backtrack(0)
        return results
