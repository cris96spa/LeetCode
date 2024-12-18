class Solution:
    def singleNumber(nums):
        """
        Given an integer array nums where every element appears three times except for one, which appears exactly once,
        find the single element and return it.

        You must implement a solution with a linear runtime complexity and use only constant extra space.

        Problem Explanation:
        - All elements in the array appear exactly three times except one unique element that appears once.
        - The task is to identify this unique element efficiently.

        Solution Explanation:
        - Use bit manipulation to track the count of each bit across all numbers.
        - Maintain two variables, `ones` and `twos`, to represent bits appearing exactly once and twice respectively.
        - For each number in the array:
          - Update `ones` to hold bits that have appeared once, excluding those appearing in `twos`.
          - Update `twos` to hold bits that have appeared twice, excluding those appearing in `ones`.
          - If a bit appears three times, it is cleared from both `ones` and `twos`.
        - At the end of the iteration, `ones` will hold the unique number.

        Example:
        Input: nums = [2, 2, 3, 2]
        Output: 3

        Input: nums = [0, 1, 0, 1, 0, 1, 99]
        Output: 99

        Constraints:
        - 1 <= nums.length <= 3 * 10^4
        - -2^31 <= nums[i] <= 2^31 - 1
        - Each element in nums appears exactly three times except for one element which appears once.

        Complexity:
        - Time Complexity: O(n), where n is the length of the array, as the array is traversed once.
        - Space Complexity: O(1), as only two integer variables are used.

        Parameters:
        nums (List[int]): List of integers where each element appears three times except one.

        Returns:
        int: The single element that appears exactly once.
        """
        ones, twos = 0, 0
        for num in nums:
            # Update ones with current number, considering twos
            ones = (ones ^ num) & ~twos
            # Update twos with current number, considering ones
            twos = (twos ^ num) & ~ones
        return ones
