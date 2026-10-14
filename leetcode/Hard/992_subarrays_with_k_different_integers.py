class Solution:
    """Count the subarrays of nums that contain exactly k distinct integers.

    Problem Statement:
        Given an integer array nums and an integer k, return the number of
        good subarrays of nums. A good subarray is a contiguous subarray
        containing exactly k different integers.

    Example:
        nums = [1, 2, 3, 1, 2], k = 3
        -> 6

        nums = [1, 2, 1, 2, 3], k = 2
        -> 7

        nums = [1, 2, 1, 3, 4], k = 3
        -> 3

    Approach:
        "Exactly k" is awkward for a sliding window: a window with too few
        distinct values may become valid by growing, while one with too many
        must shrink, so there is no single rule for moving the pointers.

        "At most k" is monotonic: if a window is valid, every window inside it
        is too. at_most_k keeps a count of each value in nums[left..right] and
        shrinks from left while the window has more than k distinct values.
        Once valid, every subarray ending at right and starting in
        [left, right] has at most k distinct values, adding
        right - left + 1 to the count.

        Subarrays with exactly k distinct values are those with at most k
        minus those with at most k - 1:
            exactly(k) = at_most_k(nums, k) - at_most_k(nums, k - 1)

    Complexity:
        Time: O(n), where n = len(nums). Each pass moves left and right at
            most n times.
        Space: O(k), the window holds at most k + 1 distinct values.
    """

    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:

        def at_most_k(nums: list[int], k: int) -> int:
            window: dict[int, int] = {}
            left = 0
            result = 0

            for right in range(len(nums)):
                window[nums[right]] = window.get(nums[right], 0) + 1

                # Is the current window valid?
                while len(window) > k:
                    window[nums[left]] -= 1
                    if window[nums[left]] == 0:
                        del window[nums[left]]
                    left += 1
                result += right - left + 1
            return result

        return at_most_k(nums, k) - at_most_k(nums, k - 1)
