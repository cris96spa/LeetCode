class Solution:
    """LeetCode 167. Two Sum II - Input Array Is Sorted.

    Problem:
        Given a 1-indexed array of integers `numbers` that is already sorted
        in non-decreasing order, find two numbers such that they add up to
        a specific `target`.

        Return the indices of the two numbers as a list [index1, index2],
        where index1 and index2 are 1-based.

    Key constraints:
        - Exactly one solution exists.
        - The same element may not be used twice.
        - The solution must use only constant extra space.

    Approach:
        Since the array is sorted, we can use two pointers:

            left  -> starts at the beginning
            right -> starts at the end

        At each step, compute:

            curr_sum = numbers[left] + numbers[right]

        There are three cases:

            1. curr_sum == target:
                We found the answer.

            2. curr_sum < target:
                The sum is too small, so we need a larger number.
                Move `left` one step to the right.

            3. curr_sum > target:
                The sum is too large, so we need a smaller number.
                Move `right` one step to the left.

        This works because the array is sorted.

    Complexity:
        Time:
            O(n), because each pointer moves at most n times.

        Space:
            O(1), because we only store a few variables.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left, right = 0, len(numbers) - 1

        while left < right:
            curr_sum = numbers[left] + numbers[right]

            if curr_sum == target:
                return [left + 1, right + 1]

            if curr_sum < target:
                left += 1
            else:
                right -= 1

        return []
