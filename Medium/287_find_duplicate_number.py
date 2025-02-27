from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        """
        Given an array of integers nums containing n + 1 integers where each integer
        is in the range [1, n] inclusive, there is only one repeated number in nums.

        Return this repeated number.

        Constraints:
        - You must solve the problem without modifying the array nums.
        - You must use only constant extra space.

        Approach:
        - We use Floyd's Cycle Detection Algorithm (also known as Tortoise and Hare Algorithm).
        - We initialize two pointers, slow and fast.
        - Move the slow pointer one step at a time and the fast pointer two steps at a time.
        - When they meet, a cycle is detected. Reset the slow pointer to the beginning.
        - Move both pointers one step at a time until they meet again, which gives the duplicate number.

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        # Use Floyd's algorithm to detect a cycle
        slow, fast = nums[0], nums[nums[0]]

        # Move fast pointer twice as fast as slow pointer
        while slow != fast:
            slow = nums[slow]
            fast = nums[nums[fast]]

        # Reset slow pointer to start
        slow = 0
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]

        return slow
