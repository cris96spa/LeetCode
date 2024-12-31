from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Problem Statement:
        ------------------
        Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

        A subarray is a contiguous portion of an array. The solution must find the maximum sum
        that can be achieved by summing elements in a contiguous subarray.

        Approach:
        ---------
        This solution uses the Divide and Conquer approach:

        1. **Divide:**
           - Split the array into two halves at the midpoint.
           - Recursively find the maximum subarray sum in the left half and the right half.

        2. **Conquer:**
           - Find the maximum subarray sum that crosses the midpoint. This subarray must
             include elements from both halves.

        3. **Combine:**
           - The maximum subarray sum for the current portion of the array is the maximum
             of:
             - The maximum subarray sum in the left half.
             - The maximum subarray sum in the right half.
             - The cross-subarray sum.

        Complexity:
        -----------
        - **Time Complexity:** O(n log n), where n is the number of elements in `nums`.
          - Each level of recursion splits the array into two halves (log n levels).
          - At each level, finding the cross-sum takes O(n) time.
        - **Space Complexity:** O(log n), due to the recursive call stack.

        Examples:
        ---------
        Example 1:
        Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
        Output: 6
        Explanation: The subarray [4,-1,2,1] has the largest sum = 6.

        Example 2:
        Input: nums = [1]
        Output: 1
        Explanation: The subarray [1] has the largest sum = 1.

        Example 3:
        Input: nums = [5,4,-1,7,8]
        Output: 23
        Explanation: The subarray [5,4,-1,7,8] has the largest sum = 23.

        """

        def find_max_sum(left: int, right: int) -> int:
            # Base case
            if left == right:
                return nums[left]

            mid = (left + right) // 2

            # Recursively compute maximum subarray sums for left and right halves
            left_sum = find_max_sum(left, mid)
            right_sum = find_max_sum(mid + 1, right)

            # Compute the maximum cross-sum
            cross_sum = find_cross_sum(nums, left, mid, right)

            # Return the maximum of the three cases
            return max(left_sum, right_sum, cross_sum)

        def find_cross_sum(nums: List[int], left: int, mid: int, right: int) -> int:
            # Find maximum sum on the left side of the midpoint (inclusive)
            max_left = float("-inf")
            curr_sum = 0
            for i in range(mid, left - 1, -1):
                curr_sum += nums[i]
                max_left = max(curr_sum, max_left)

            # Find maximum sum on the right side of the midpoint
            max_right = float("-inf")
            curr_sum = 0
            for i in range(mid + 1, right + 1):
                curr_sum += nums[i]
                max_right = max(curr_sum, max_right)

            # Combine left and right sums
            # We care only about the cross-sum since left and right
            # sums are computed separately in the recursive calls
            return max_left + max_right

        return find_max_sum(0, len(nums) - 1)


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        This solution uses Kadane's Algorithm, a dynamic programming approach:

        1. Initialize two variables:
           - `curr_sum`: Tracks the sum of the current subarray.
           - `max_sum`: Tracks the maximum sum found so far.

        2. Iterate through the array:
           - At each step, decide whether to include the current element in the existing subarray or start a new subarray with the current element. Update `curr_sum` as:

             \( \text{curr\_sum} = \max(\text{num}, \text{curr\_sum} + \text{num}) \)

           - Update `max_sum` with the maximum of itself and `curr_sum`:

             \( \text{max\_sum} = \max(\text{max\_sum}, \text{curr\_sum}) \)

        3. Return `max_sum` at the end of the iteration.

        Complexity:
        -----------
        - **Time Complexity:** O(n), where n is the number of elements in `nums`.
          - The algorithm processes each element exactly once.
        - **Space Complexity:** O(1), as no additional space is used beyond a few variables.
        """
        # Initialize max and current sum
        max_sum, curr_sum = nums[0], nums[0]

        # Iterate through the array starting from the second element
        for num in nums[1:]:
            # Update current sum: include the current number in the subarray or start a new subarray
            curr_sum = max(num, curr_sum + num)
            # Update max sum
            max_sum = max(max_sum, curr_sum)

        return max_sum
