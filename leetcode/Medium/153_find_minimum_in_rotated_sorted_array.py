from typing import List


class Solution:
    """Find the minimum element in a rotated sorted array in O(log n) time.

    Problem Statement:
        Given an array of unique integers sorted in ascending order and then rotated
        at an unknown pivot, find the minimum element.

    Approach:
        Use binary search. Compare nums[mid] with nums[right]:
        - If nums[mid] < nums[right], the minimum is in the left half (including mid).
        - Otherwise, the minimum is in the right half (excluding mid).
        Narrow the search until left == right, which is the minimum.

    Complexity:
        Time: O(log n).
        Space: O(1).
    """

    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] < nums[right]:
                right = mid
            else:
                left = mid + 1

        return nums[left]
