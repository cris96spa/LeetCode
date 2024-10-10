class Solution:
    """
    Problem:
    Given an array of integers nums sorted in non-decreasing order, find the starting and ending 
    position of a given target value. If the target is not found in the array, return [-1, -1].

    The algorithm must run in O(log n) time complexity.

    Example 1:
        Input: nums = [5,7,7,8,8,10], target = 8
        Output: [3,4]

    Example 2:
        Input: nums = [5,7,7,8,8,10], target = 6
        Output: [-1,-1]

    Example 3:
        Input: nums = [], target = 0
        Output: [-1,-1]

    Constraints:
    - 0 <= nums.length <= 10^5
    - -10^9 <= nums[i] <= 10^9
    - nums is a non-decreasing array.
    - -10^9 <= target <= 10^9

    Solution Approach:
    The problem requires finding the starting and ending positions of a target value in a sorted array. 
    We need an algorithm with O(log n) time complexity, which suggests a binary search approach.

    Approach:
    1. **Binary Search**: We perform two binary searches to find the leftmost and rightmost occurrences 
       of the target value. Both searches are performed with slight modifications:
       - The leftmost search narrows down to the left half when the target is found (`end = mid - 1`).
       - The rightmost search narrows down to the right half when the target is found (`start = mid + 1`).
    
    2. **Search Process**:
       - For each search, we maintain two pointers (`start` and `end`) and calculate the middle index (`mid`).
       - Depending on whether `nums[mid]` is less than or greater than the target, we adjust the `start` or `end` pointers.
       - If `nums[mid]` is equal to the target, we update the result to `mid` and continue searching to the left or right, depending on the search mode ('left' or 'right').

    3. **Return the Result**:
       - Once both the leftmost and rightmost indices are found, they are returned as a tuple (left, right).
       - If the target is not found in the array, both searches return `-1`.

    Time Complexity: O(log n) for both the left and right binary searches, making the overall complexity O(log n).

    Space Complexity: O(1) since the algorithm uses constant extra space.
    """

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def bin_search(nums: List[int], target: int, mode: str) -> int:
            start, end = 0, len(nums) - 1
            result = -1
            
            # Binary search loop
            while start <= end:
                mid = (start + end) // 2
                if nums[mid] < target:
                    start = mid + 1
                elif nums[mid] > target:
                    end = mid - 1
                else:
                    result = mid
                    if mode == 'left':
                        end = mid - 1  # Search on the left for the first occurrence
                    else:
                        start = mid + 1  # Search on the right for the last occurrence
            return result

        # Find the leftmost and rightmost positions of the target
        left = bin_search(nums, target, 'left')
        right = bin_search(nums, target, 'right')
        
        return [left, right]
