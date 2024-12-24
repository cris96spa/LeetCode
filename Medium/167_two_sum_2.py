from typing import List


class Solution:
    """
    Problem Statement:
    ------------------
    Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order,
    find two numbers such that they add up to a specific target number. Let these two numbers be
    `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

    Return the indices of the two numbers, `index1` and `index2`, added by one as an integer array
    `[index1, index2]` of length 2.

    The tests are generated such that there is exactly one solution, and the same element cannot be
    used twice.

    Constraints:
    ------------
    - 2 <= numbers.length <= 3 * 10^4
    - -1000 <= numbers[i] <= 1000
    - `numbers` is sorted in non-decreasing order.
    - -1000 <= target <= 1000
    - The tests are guaranteed to have exactly one solution.

    Solution:
    ---------
    This problem can be solved efficiently using the two-pointer technique because the input array
    is already sorted.

    Steps:
    1. Initialize two pointers, `left` at the start of the array and `right` at the end.
    2. Calculate the sum of the numbers at these two pointers.
    3. If the sum is greater than the target, decrement the `right` pointer to reduce the sum.
    4. If the sum is less than the target, increment the `left` pointer to increase the sum.
    5. If the sum equals the target, return the 1-indexed positions `[left + 1, right + 1]`.

    This approach ensures \(O(n)\) time complexity with \(O(1)\) extra space.
    """

    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """
        Finds two numbers in the sorted array `numbers` that add up to the `target`.

        Args:
            numbers (List[int]): A sorted array of integers.
            target (int): The target sum to achieve.

        Returns:
            List[int]: A 1-indexed list of the indices of the two numbers that add up to the target.
        """
        left, right = 0, len(numbers) - 1

        while left < right:
            _sum = numbers[left] + numbers[right]

            if _sum > target:
                right -= 1
            elif _sum < target:
                left += 1
            else:
                return [left + 1, right + 1]  # 1-indexed result

        # Guaranteed to have a solution; this line should never be reached.
        return []
