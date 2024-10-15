from typing import List


class Solution:
    """
    Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order,
    find two numbers such that they add up to a specific target number. Let these two numbers be
    `numbers[index1]` and `numbers[index2]` where 1 <= index1 < index2 <= numbers.length.

    Return the indices of the two numbers, `index1` and `index2`, added by one as an integer array
    [index1, index2] of length 2.

    The tests are generated such that there is exactly one solution. You may not use the same element twice.
    Your solution must use only constant extra space.

    Approach:
    ---------
    The solution uses a two-pointer approach:
    - Start with two pointers: one at the beginning (`start`) and one at the end (`end`) of the array.
    - Calculate the sum of the elements at the two pointers.
    - If the sum equals the target, return the 1-indexed positions of the two numbers.
    - If the sum is less than the target, increment the `start` pointer to try a larger value.
    - If the sum is greater than the target, decrement the `end` pointer to try a smaller value.
    - Repeat until the correct pair is found.
    - The solution operates in O(n) time complexity and uses O(1) additional space.
    """

    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        start, end = 0, len(numbers) - 1
        while start <= end:
            num_sum = numbers[start] + numbers[end]
            if num_sum == target:
                return [start + 1, end + 1]
            elif num_sum < target:
                start += 1
            else:
                end -= 1
