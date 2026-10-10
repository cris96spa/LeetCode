class Solution:
    """🔢 Combination Sum IV.

    Problem:
    --------
    Given distinct positive integers `nums` and an integer `target`, return the number of
    sequences of elements of `nums` (each usable any number of times) that sum to exactly
    `target`. LeetCode calls them "combinations", but **order matters**: `(1, 2)` and
    `(2, 1)` count separately.

    Example (`nums = [1, 2, 3]`, `target = 4`, answer 7):
    `(1, 1, 1, 1)`, `(1, 1, 2)`, `(1, 2, 1)`, `(2, 1, 1)`, `(2, 2)`, `(1, 3)`, `(3, 1)`.

    Key Insight:
    ------------
    This is **not** Coin Change II (LC 518) with a compressed table. There, the state
    `W[i][j]` decides the elements in a fixed order (all the 1s, then all the 2s, ...),
    which is exactly what makes `(1, 1, 2)` and `(1, 2, 1)` the same object. To count
    orderings, drop the element index entirely.

    State: `ways[j]` = number of ordered sequences summing to exactly `j`.

    Split on the **last** element `x` of the sequence: what comes before it is any
    sequence summing to `j - x`, and different last elements give different sequences.

        ways[j] = sum(ways[j - x] for x in nums if x <= j)

    Base case: `ways[0] = 1`, the empty sequence. The answer is `ways[target]`.

    This is Climbing Stairs (LC 70) with step sizes `nums`: the number of ways to reach
    step `j` is the sum over the size of the last step.

    Example (`nums = [1, 2, 3]`, `target = 4`):

          j        0  1  2  3  4
          ways[j]  1  1  2  4  7

    `ways[4] = ways[3] + ways[2] + ways[1] = 4 + 2 + 1`: the 4 sequences summing to 3
    followed by a 1, the 2 summing to 2 followed by a 2, and the 1 summing to 1 followed
    by a 3.

    Approach:
    ---------
    `ways[j]` needs every smaller total, each computed with **all** of `nums` already
    allowed. So totals go in the **outer** loop and `nums` in the inner one.

    Swapping the loops gives LC 518's loop (elements outer), which computes the
    unordered count instead: on this example it returns 4 (`1111`, `112`, `13`, `22`),
    because once the loop has moved past 1, no later 2 or 3 can be followed by a 1.

    Complexity:
    -----------
    With `n = len(nums)`:
    - Time: O(target * n)
    - Space: O(target)
    """

    def combinationSum4(self, nums: list[int], target: int) -> int:
        state: list[int] = [1] + [0] * target
        for j in range(target + 1):
            for num in nums:
                if j >= num:
                    state[j] += state[j - num]

        return state[-1]
