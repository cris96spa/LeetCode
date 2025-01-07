from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the
        two endpoints of the ith line are (i, 0) and (i, height[i]).

        Find two lines that together with the x-axis form a container, such that the container contains the most water.

        Return the maximum amount of water a container can store.

        Constraints:
        - n == height.length
        - 2 <= n <= 10^5
        - 0 <= height[i] <= 10^4

        Approach:
        - Use the two-pointer technique to calculate the container's area.
        - Start with the widest container and narrow the width by moving the pointer associated with the shorter line.
        - Update the maximum area at each step.

        Time Complexity: O(n) - Each line is visited once.
        Space Complexity: O(1) - No additional data structures are used.

        Args:
            height (List[int]): A list of integers representing heights of vertical lines.

        Returns:
            int: Maximum amount of water a container can store.
        """
        left, right = 0, len(height) - 1
        max_area = 0

        while left < right:
            # Calculate the current area
            curr_area = min(height[left], height[right]) * (right - left)

            # Update the maximum area if the current area is larger
            max_area = max(max_area, curr_area)

            # Move the pointer associated with the shorter line
            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1

        return max_area
