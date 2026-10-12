class Solution:
    """🌧️ Trapping Rain Water.

    Problem:
    --------
    Given `n` non-negative integers representing an elevation map where each bar has
    width 1, compute how much water it can trap after raining.

    Example (`height = [0, 1, 0, 1]`, answer 1): one unit sits at index 2.

    Key Insight:
    ------------
    The water above index `i` is set by the shorter of the tallest bars on each side:

        water[i] = min(max(height[:i + 1]), max(height[i:])) - height[i]

    Scanning left to right we know `left_max`, but not whether a tall enough barrier
    exists on the right. Two pointers fix that: move the side with the **smaller** bar.
    If `height[lo] < height[hi]`, there is a bar at least as tall as `left_max` at or
    right of `hi` (when `lo` passed the bar that set `left_max`, it was shorter than the
    `hi` bar back then, and `hi` only moves left). So the right side never limits
    position `lo`, regardless of what is in the middle, and:

        water[lo] = left_max - height[lo]

    The right side is symmetric.

    Example (`height = [2, 0, 5, 1, 3]`):

          lo  hi  side    max  water
          0   4   left    2    0
          1   4   left    2    2
          2   4   right   3    0
          2   3   right   3    2      total = 4

    Approach:
    ---------
    - Update the running max **before** adding water, so a new tallest bar adds 0.
    - On ties move either side; `else` moves `hi`.

    Complexity:
    -----------
    - Time: O(n), each index is visited once
    - Space: O(1), only the two pointers and running maxima
    """

    def trap(self, height: list[int]) -> int:
        lo: int = 0
        hi: int = len(height) - 1
        total_water: int = 0

        left_max = 0
        right_max = 0

        while lo < hi:
            if height[lo] < height[hi]:
                left_max = max(left_max, height[lo])
                total_water += left_max - height[lo]
                lo += 1
            else:
                right_max = max(right_max, height[hi])
                total_water += right_max - height[hi]
                hi -= 1

        return total_water
