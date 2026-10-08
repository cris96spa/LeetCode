from bisect import bisect_left


class Solution:
    """📈 Longest Increasing Subsequence.

    Problem:
    --------
    Given an integer array `nums`, return the length of the longest strictly increasing
    subsequence. A subsequence is obtained by deleting some or no elements without
    changing the order of the rest.

    Key Insight:
    ------------
    O(n^2) baselines:
    - `D[i] = 1 + max(D[j] for j < i if nums[j] < nums[i])`: the LIS ending at `i`.
    - LCS (LC 1143) of `nums` with `sorted(set(nums))`: a common subsequence is
      increasing (it follows the sorted copy) and strictly so (no duplicates there).

    Both waste work: for each length we only care about the **smallest possible tail**.
    A subsequence ending lower is at least as easy to extend later. So keep

        tails[k] = smallest tail of any increasing subsequence of length k + 1 so far

    `tails` is strictly increasing: a subsequence of length k + 2 has a length-(k + 1)
    prefix ending below its own tail, so `tails[k] < tails[k + 1]`. That makes it
    binary-searchable.

    Approach:
    ---------
    For each `x`, let `pos = bisect_left(tails, x)`, the first index with
    `tails[pos] >= x`:
    - `tails[pos - 1] < x`, so `x` extends a subsequence of length `pos` into one of
      length `pos + 1`. It cannot extend anything longer: those all end at `>= x`.
    - `pos == len(tails)`: `x` beats every tail and creates a new, longer length.
    - Otherwise `x <= tails[pos]`, so `x` is the new smallest tail for length `pos + 1`.
      No other entry changes.

    `bisect_left` keeps the increase strict: an `x` equal to a tail replaces it instead
    of extending it. `bisect_right` would compute the longest *non-decreasing*
    subsequence.

    Example (`nums = [10, 9, 2, 5, 3, 7, 101, 18]`, answer 4):

          x     pos   tails
          10    0     [10]
          9     0     [9]
          2     0     [2]
          5     1     [2, 5]
          3     1     [2, 3]
          7     2     [2, 3, 7]
          101   3     [2, 3, 7, 101]
          18    3     [2, 3, 7, 18]

    `tails` is *not* itself an LIS, only its length is meaningful: `[3, 4, 1]` ends with
    `tails = [1, 4]`. To recover an actual subsequence, store indices in `tails` and, for
    each `x`, a parent pointer to the index at `tails[pos - 1]`.

    Complexity:
    -----------
    - Time: O(n log n), one binary search per element
    - Space: O(n)
    """

    def lengthOfLIS(self, nums: list[int]) -> int:
        tails: list[int] = []
        for x in nums:
            pos = bisect_left(tails, x)
            if pos == len(tails):
                tails.append(x)
            else:
                tails[pos] = x
        return len(tails)
