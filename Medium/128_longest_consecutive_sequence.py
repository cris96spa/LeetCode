from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """
        Given an unsorted array of integers `nums`, return the length of the longest
        consecutive elements sequence.

        A consecutive sequence is defined as a sequence of numbers where each number
        in the sequence differs from the previous one by exactly 1.

        Constraints:
        - 0 <= nums.length <= 10^5
        - -10^9 <= nums[i] <= 10^9

        The algorithm must run in O(n) time complexity.

        Approach:
        - We first convert `nums` into a set to allow for O(1) lookups.
        - We iterate over each number in the set.
        - For each number, we check if it is the **smallest element in a sequence**
          (i.e., `n - 1` is not in the set).
        - If it is the start of a sequence, we incrementally check for consecutive
          numbers (`n + 1, n + 2, ...`) in the set and count the length.
        - We update `max_count` to track the longest consecutive sequence found.

        Complexity Analysis:
        - **Time Complexity: O(n)**
          - Insertion into a set and lookups are O(1).
          - Each number is processed only once.
        - **Space Complexity: O(n)**
          - A set is used to store unique elements.

        Edge Cases Considered:
        - An empty list (`nums = []`) should return `0`.
        - A list with all duplicate elements (`nums = [7,7,7]`) should return `1`.
        - A list with no consecutive numbers (`nums = [10, 100, 1000]`) should return `1`.
        - A long sequence (`nums = [1,2,3,4,5,6,7,8,9,10]`) should return `10`.

        Example:
        ```
        Input: nums = [100, 4, 200, 1, 3, 2]
        Output: 4
        Explanation: The longest consecutive sequence is [1, 2, 3, 4].
        ```

        Returns:
        - An integer representing the length of the longest consecutive sequence.
        """

        if not nums:
            return 0  # Edge case: empty list

        numbers = set(nums)  # Convert list to set for O(1) lookups
        max_count = 0

        for n in numbers:  # Iterate over set instead of list to avoid duplicates
            if (
                n - 1 not in numbers
            ):  # Only start counting if n is the smallest in sequence
                curr_count = 1
                next_num = n + 1

                while next_num in numbers:
                    next_num += 1
                    curr_count += 1

                max_count = max(max_count, curr_count)

        return max_count
