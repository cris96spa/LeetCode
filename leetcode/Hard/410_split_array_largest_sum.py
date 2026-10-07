from typing import Callable


class Solution:
    """✂️ Split Array Largest Sum.

    Problem:
    --------
    Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty
    contiguous subarrays so that the largest subarray sum is as small as possible.
    Return that minimized largest sum.

    Key Insight:
    ------------
    Search on the answer instead of on the split. Let `P(t)` be "nums can be split into
    at most k subarrays, each with sum <= t". `P` is monotone in `t`: if a cap `t` works,
    any larger cap works too.

        t:    max(nums) ... ... ... sum(nums)
        P(t): F  F  F  T  T  T  T  T

    The answer is the first `t` where `P(t)` is True.

    Approach:
    ---------
    - Bounds: `t >= max(nums)`, because every element ends up in some subarray, and
      `t = sum(nums)` (one subarray) is always feasible.
    - Feasibility: go left to right and keep adding to the current subarray until the
      next element would push it past `t`, then start a new one. This greedy gives the
      fewest subarrays possible under cap `t`.
    - "At most k" is enough: since `n >= k`, a split with fewer pieces can be cut further
      until it has exactly `k`, and cutting never makes a sum larger.
    - Use the `first_true` template over [max(nums), sum(nums) + 1).

    Complexity:
    -----------
    - Time: O(n log S), where S = sum(nums) - max(nums) is the size of the search range;
      each of the O(log S) checks is O(n).
    - Space: O(1)
    """

    def splitArray(self, nums: list[int], k: int) -> int:

        def check_feasibility(t: int) -> bool:
            curr_sum = 0
            num_subarrays = 1
            for num in nums:
                if curr_sum + num > t:
                    num_subarrays += 1
                    curr_sum = 0
                curr_sum += num
            return num_subarrays <= k

        def first_true(low: int, high: int, pred: Callable[[int], bool]) -> int:
            while low < high:
                mid = (low + high) // 2
                if pred(mid):
                    high = mid
                else:
                    low = mid + 1
            return low

        return first_true(max(nums), sum(nums) + 1, check_feasibility)
