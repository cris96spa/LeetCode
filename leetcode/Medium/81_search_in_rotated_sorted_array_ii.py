class Solution:
    """🔄 Search in Rotated Sorted Array II.

    Problem:
    --------
    Given an integer array `nums`, sorted in non-decreasing order and then rotated at an
    unknown pivot, and an integer `target`, return whether `target` is in `nums`. Unlike
    LC 33, values may repeat. Reduce the number of operations as much as possible.

    Key Insight:
    ------------
    With distinct values (LC 33), at least one half around `mid` is always sorted, and
    `nums[low] <= nums[mid]` tells us which one. A sorted half answers "is the target in
    here?" in O(1), so each step discards half the range: O(log n).

    Duplicates break the test, not the structure. One half is still sorted, but when
    `nums[low] == nums[mid] == nums[high]` we cannot tell which:
    - `[1, 0, 1, 1, 1]`: the pivot is in the left half.
    - `[1, 1, 1, 0, 1]`: the pivot is in the right half.
    Trusting `nums[low] <= nums[mid]` here can discard the half holding the target.

    Approach:
    ---------
    Binary search as in LC 33, plus one case:
    - `nums[mid] == target`: found.
    - `nums[low] == nums[mid] == nums[high]`: ambiguous. `nums[low]` and `nums[high]`
      equal `nums[mid]`, which is not the target, so drop both ends and retry with a new
      `mid`. The `continue` matters: without it the stale `mid` is compared against the
      shrunk range, and a one-element window steps `low` past the end of the array.
    - Otherwise one half is identifiably sorted: keep it if `target` lies in its range,
      else keep the other half.

    Complexity:
    -----------
    - Time: O(log n) when values are distinct, O(n) worst case. The O(n) is unavoidable:
      in `[1, 1, 1, 1, 0, 1, 1]` every probe of a `1` says nothing about where the `0` is,
      so any algorithm may have to inspect every position.
    - Space: O(1)
    """

    def search(self, nums: list[int], target: int) -> bool:
        low, high = 0, len(nums) - 1

        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target:
                return True

            # Both ends equal nums[mid] (not the target): drop them, recompute mid
            if nums[low] == nums[mid] == nums[high]:
                low, high = low + 1, high - 1
                continue

            if nums[low] <= nums[mid]:
                # [low, mid] is sorted
                if nums[low] <= target < nums[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                # [mid, high] is sorted
                if nums[mid] < target <= nums[high]:
                    low = mid + 1
                else:
                    high = mid - 1

        return False
