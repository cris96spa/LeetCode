"""
Problem Description:
Given an integer array 'nums' of length n and an integer k, find the contiguous subarray of 
length k with the maximum average value. Return this maximum average value.

The problem accepts answers with a calculation error less than 10^-5.

Examples:
1. Input: nums = [1,12,-5,-6,50,3], k = 4
   Output: 12.75000
   Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75

2. Input: nums = [5], k = 1
   Output: 5.00000

Constraints:
- n == nums.length
- 1 <= k <= n <= 10^5
- -10^4 <= nums[i] <= 10^4

Solution Explanation:
1. We use a sliding window approach to efficiently calculate the sum of each k-length subarray.
2. First, we calculate the sum of the first k elements.
3. We then slide the window one element at a time, subtracting the element leaving the window 
   and adding the new element entering the window.
4. We keep track of the maximum sum encountered.
5. Finally, we return the maximum sum divided by k to get the maximum average.

This solution has a time complexity of O(n) where n is the length of nums, as we process each 
element once. The space complexity is O(1) as we only use a constant amount of extra space.
"""

class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        # Compute current sum up to k
        curr_sum = sum(nums[:k])
        max_sum = curr_sum

        # Compute successive sum in O(n) time
        for i in range(len(nums)-k):
            curr_sum = curr_sum - nums[i] + nums[i+k]
            max_sum = max(max_sum, curr_sum)

        return max_sum/k