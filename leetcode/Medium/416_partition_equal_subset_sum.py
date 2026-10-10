class Solution:
    """⚖️ Partition Equal Subset Sum.

    Problem:
    --------
    Given an integer array `nums` of positive values, return True if it can be split into
    two subsets with equal sums, False otherwise.

    - `[1, 5, 11, 5]` -> True: `{1, 5, 5}` and `{11}` both sum to 11.
    - `[1, 2, 3, 5]` -> False: the total, 11, is odd.

    Key Insight:
    ------------
    Every element goes into exactly one of the two subsets, so if one subset sums to `a`,
    the other sums to `total - a`. Hence:
    - If the split exists, `a = total - a`, so `a = total / 2`. An odd total is
      impossible right away.
    - If some subset sums to `total / 2`, put every other element in the complement: it
      sums to `total - total / 2 = total / 2` with no extra work.

    So the problem reduces to **subset sum** with target `m = total // 2`: finding one half
    is enough, because its complement is the other half.

    State: `S[i][j]` = can some subset of the first `i` elements sum to exactly `j`?
    Look at the `i`-th element `x = nums[i - 1]`. A subset of the first `i` elements
    summing to `j` either:
    - **leaves** `x`: it's a subset of the first `i - 1` elements summing to `j`;
    - **takes** `x` (only if `x <= j`): the rest is a subset of the first `i - 1`
      elements summing to `j - x`.

        S[i][j] = S[i-1][j] or S[i-1][j - x]

    Base case: with no elements, only the empty subset exists, so `S[0][0] = True` and
    `S[0][j] = False` for `j > 0`. The answer is `S[n][m]`.

    Example (`nums = [1, 5, 11, 5]`, `m = 11`, T = reachable):

          j       0  1  2  3  4  5  6  7  8  9  10 11
          none    T  .  .  .  .  .  .  .  .  .  .  .
          + 1     T  T  .  .  .  .  .  .  .  .  .  .
          + 5     T  T  .  .  .  T  T  .  .  .  .  .
          + 11    T  T  .  .  .  T  T  .  .  .  .  T
          + 5     T  T  .  .  .  T  T  .  .  .  T  T

    Each row is the row above, plus the row above shifted right by `x`. `S[3][11]` is
    already True (take the 11), so the answer is True.

    Approach:
    ---------
    Row `i` reads only row `i - 1`, so one array `state` of size `m + 1` suffices,
    overwritten in place one element at a time. The take branch reads `S[i-1][j - x]`, a
    cell to the **left** in the **previous** row, so `j` must go **downward**: then
    `state[j - x]` hasn't been updated for `x` yet and still holds row `i - 1`.

    Going upward would let `x` be used twice. In the example, on the row `+ 5` starting
    from `{0, 1}`: `state[5]` becomes True (0 + 5), then `state[10]` reads `state[5]` and
    becomes True as well, which means 10 = 5 + 5 with only one 5 seen so far.

    For `j < x` only "leave" is possible, so `state[j]` stays as it is and the loop stops
    at `x`.

    Complexity:
    -----------
    With `n = len(nums)` and `m = sum(nums) // 2`:
    - Time: O(n * m)
    - Space: O(m), down from O(n * m) for the full table
    """

    def canPartition(self, nums: list[int]) -> bool:
        total = sum(nums)

        # Check for necessary but not sufficient condition
        if total % 2:
            return False

        # Define our target
        m = total // 2

        def subset_sum(nums: list[int], target: int) -> bool:
            """Return whether some subset of nums sums to exactly target.

            Args:
                nums (list[int]): positive values to choose the subset from.
                target (int): the sum the subset must reach.

            Returns:
                True if such a subset exists, False otherwise.
            """
            n = len(nums)
            state = [True] + [False] * target

            for i in range(1, n + 1):
                x = nums[i - 1]
                for j in range(target, x - 1, -1):
                    # Can we pick?
                    if j >= x and state[j - x]:
                        state[j] = True

            return state[-1]

        return subset_sum(nums, m)
