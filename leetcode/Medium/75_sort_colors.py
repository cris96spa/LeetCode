class Solution:
    """Sort an array of 0s, 1s and 2s in place.

    Problem Statement:
        Given an array nums with n objects colored red, white or blue, sort
        them in place so that objects of the same color are adjacent, in the
        order red, white, blue. The integers 0, 1 and 2 represent red, white
        and blue. The library sort must not be used.

    Example:
        nums = [2, 0, 2, 1, 1, 0]
        -> [0, 0, 1, 1, 2, 2]

        nums = [2, 0, 1]
        -> [0, 1, 2]

    Approach:
        Any in-place comparison sort (e.g. heap sort) works in O(n log n),
        but with only three distinct values one pass is enough: this is the
        Dutch National Flag partition, using 1 as the pivot.

        Three pointers split the array into four regions:
            nums[:lt]     == 0
            nums[lt:i]    == 1
            nums[i:gt]    not yet seen
            nums[gt:]     == 2

        At each step, look at nums[i]:
            - 0: swap it into position lt, then advance lt and i. The value
              swapped back to i came from the 1s region (or is nums[i]
              itself), so it is already in place.
            - 1: already in place, advance i.
            - 2: shrink gt and swap nums[i] with nums[gt]. Do not advance i:
              the value swapped in comes from the unseen region and still
              needs to be checked.

        The loop stops when i meets gt, as no unseen elements are left.

        Trace on [2, 0, 2, 1, 1, 0] (lt, i, gt start at 0, 0, 6):
            2 -> swap with 0 at index 5: [0, 0, 2, 1, 1, 2], gt = 5
            0 -> in place:               lt = 1, i = 1
            0 -> in place:               lt = 2, i = 2
            2 -> swap with 1 at index 4: [0, 0, 1, 1, 2, 2], gt = 4
            1 -> i = 3
            1 -> i = 4 == gt, stop

    Complexity:
        Time: O(n), where n = len(nums). Every step either advances i or
            shrinks gt, so there are at most n steps.
        Space: O(1).
    """

    def sortColors(self, nums: list[int]) -> None:
        """Do not return anything, modify nums in-place instead."""
        lt, i, gt = 0, 0, len(nums)

        while i < gt:
            if nums[i] == 0:
                nums[i], nums[lt] = nums[lt], nums[i]
                lt += 1
                i += 1
            elif nums[i] == 1:
                i += 1
            else:
                gt -= 1
                nums[i], nums[gt] = nums[gt], nums[i]
