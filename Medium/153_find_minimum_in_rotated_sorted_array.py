"""
Problem Description:

You are given an array `nums` of unique integers that is sorted in ascending order and then rotated at an unknown pivot. 
Your task is to find the minimum element in this rotated sorted array.

The array was originally sorted in ascending order, and it has been rotated between 1 and `n` times, where `n` is 
the length of the array. The goal is to find the minimum element in this rotated array in O(log n) time complexity.

### Example 1:
Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] and rotated 3 times.

### Example 2:
Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and rotated 4 times.

### Example 3:
Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and rotated 4 times.

### Constraints:
- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All the integers in `nums` are unique.
- The array is sorted and rotated between 1 and n times.

Solution:

To solve this problem in O(log n) time complexity, we can modify the binary search algorithm. 
The idea is to find the inflection point in the rotated array where the smallest element resides.

Key Steps:
1. Use two pointers `left` and `right` to represent the current bounds of the search space.
2. Calculate the middle index `mid`. Compare `nums[mid]` with `nums[right]`:
    - If `nums[mid]` is less than `nums[right]`, it means the smallest value is in the left half (including `mid`), so adjust `right`.
    - Otherwise, the smallest value is in the right half, so adjust `left`.
3. Continue narrowing the search space until `left` points to the minimum element.

By using binary search, we achieve the desired O(log n) time complexity.
"""

from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Initialize left and right pointers to represent the bounds of the array
        left, right = 0, len(nums) - 1
        
        # Perform binary search to find the minimum element
        while left < right:
            # Calculate the mid-point of the current search range
            mid = (left + right) // 2
            
            # Compare the mid element with the right element to decide which half to search
            if nums[mid] < nums[right]:
                # If nums[mid] is less than nums[right], the minimum must be in the left half (including mid)
                right = mid
            else:
                # Otherwise, the minimum must be in the right half, so move left to mid + 1
                left = mid + 1
    
        return nums[left]
