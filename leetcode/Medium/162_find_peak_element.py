from typing import Callable


class Solution:
    """⛰️ Find Peak Element.

    Problem:
    --------
    Given an integer array `nums` where adjacent elements are distinct, return the index of
    any peak element, i.e. an element strictly greater than its neighbors. Treat
    `nums[-1] = nums[n] = -inf`. The algorithm must run in O(log n) time.

    Key Insight:
    ------------
    The array is not sorted, but the predicate `P(i) = nums[i] > nums[i + 1]` ("going
    downhill") still tells us which half contains a peak:
    - If `P(mid)` is False, we are going uphill, so a peak exists to the right of `mid`
      (the slope cannot rise forever, since `nums[n] = -inf`).
    - If `P(mid)` is True, a peak exists at `mid` or to its left.

    The predicate is not globally monotone, but the invariant "a peak exists in
    [low, high]" is preserved by every step, which is all binary search needs.

    Approach:
    ---------
    Run the `first_true` template over the half-open range [0, n - 1):
    - `mid < high <= n - 1`, so `nums[mid + 1]` is always in bounds.
    - If no index satisfies the predicate, the array is strictly increasing and the
      answer is `high = n - 1`, the last element.
    - For `n == 1` the loop never runs and the answer is 0.

    Complexity:
    -----------
    - Time: O(log n)
    - Space: O(1)
    """

    def findPeakElement(self, nums: list[int]) -> int:
        return self.first_true(nums, lambda idx: nums[idx] > nums[idx + 1])

    def first_true(self, nums: list[int], predicate: Callable[[int], bool]) -> int:
        low = 0
        high = len(nums) - 1

        while low < high:
            mid = (low + high) // 2
            if predicate(mid):
                high = mid
            else:
                low = mid + 1
        return low
