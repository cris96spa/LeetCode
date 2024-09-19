"""Problem Description:
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. 
All houses at this place are arranged in a circle. This means that the first house is the neighbor of the last one. 
Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent 
houses are broken into on the same night.

Given an integer array `nums` representing the amount of money of each house, the task is to return the maximum amount of 
money you can rob tonight without alerting the police. Since the houses are in a circle, this means that if you rob the 
first house, you cannot rob the last one, and vice versa. Therefore, the problem is reduced to two scenarios:
    1. Rob houses excluding the first one.
    2. Rob houses excluding the last one.
    
We then take the maximum result from these two cases to get the maximum possible amount of money that can be robbed.

Example Cases:
Example 1:
Input: nums = [2, 3, 2]
Output: 3
Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses. 
So, the best strategy is to rob house 2 for a total of 3.

Example 2:
Input: nums = [1, 2, 3, 1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3). Total amount you can rob = 1 + 3 = 4.

Example 3:
Input: nums = [1, 2, 3]
Output: 3

Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000
"""

from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        # Edge case: If there is only one house, rob it.
        if len(nums) == 1:
            return nums[0]
        
        # Consider two cases:
        # Case 1: Rob houses from the first one to the second-last one (exclude the last).
        # Case 2: Rob houses from the second one to the last one (exclude the first).
        # The final result is the maximum of the two cases.
        return max(self._get_max(nums[:-1]), self._get_max(nums[1:]), nums[0])

    def _get_max(self, nums):
        prev_rob = max_rob = 0
        
        # Dynamic programming approach: Iterate through the houses and keep track of the maximum money robbed.
        for curr in nums:
            temp = max(max_rob, prev_rob + curr)
            prev_rob = max_rob
            max_rob = temp
        
        return max_rob

# Example Test Cases
if __name__ == "__main__":
    solution = Solution()
    
    # Test Case 1
    nums1 = [2, 3, 2]
    print(f"Test Case 1: {solution.rob(nums1)}")  # Expected Output: 3
    
    # Test Case 2
    nums2 = [1, 2, 3, 1]
    print(f"Test Case 2: {solution.rob(nums2)}")  # Expected Output: 4
    
    # Test Case 3
    nums3 = [1, 2, 3]
    print(f"Test Case 3: {solution.rob(nums3)}")  # Expected Output: 3