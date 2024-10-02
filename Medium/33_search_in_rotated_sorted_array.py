"""
Problem Description:

You are given a rotated, sorted array of distinct integers. The array was originally sorted in ascending order, 
but then rotated at an unknown pivot, meaning part of the array may still be in order, but the overall array is no 
longer fully sorted. 

Your task is to search for a specific target value within this array and return its index. If the target value is 
not present in the array, return -1.

### Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

### Example 2:
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

### Example 3:
Input: nums = [1], target = 0
Output: -1

### Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique.
- The array is sorted but possibly rotated.
- The solution must run in O(log n) time complexity.

Writeup:

We can solve this problem using a modified version of the binary search algorithm. Although the array is rotated,
one half of the array (either left or right) will always remain sorted at every step of the search. 

Key steps:
1. Identify which half of the array is sorted.
2. Check if the target lies within that sorted half.
3. If it does, adjust the binary search range to focus on that side.
4. If not, search the other half of the array.
5. Continue narrowing down the search range until the target is found or the search space is exhausted.

The algorithm efficiently searches for the target in O(log n) time by repeatedly halving the search space, taking 
advantage of the sorted sections of the array.
"""

from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        # Perform binary search while the search bounds are valid.
        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            # Determine which part of the array is sorted (left or right).
            if nums[left] <= nums[mid]:
                # This means the left side of the array is sorted.
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return -1
