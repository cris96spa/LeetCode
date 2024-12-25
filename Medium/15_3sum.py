from typing import List


class Solution:
    """
    Problem Statement:
    ------------------
    Given an integer array `nums`, return all the unique triplets [nums[i], nums[j], nums[k]] such that:
    - i != j, i != k, and j != k
    - nums[i] + nums[j] + nums[k] == 0

    Note:
    - The solution set must not contain duplicate triplets.

    Example:
    --------
        Input: nums = [-1, 0, 1, 2, -1, -4]
        Output: [[-1, -1, 2], [-1, 0, 1]]

        Explanation:
        nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0
        nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0
        nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0
        The distinct triplets are [-1, -1, 2] and [-1, 0, 1].
        The order of the output and the order of the triplets does not matter.

    Constraints:
    ------------
    - 3 <= nums.length <= 3000
    - -10^5 <= nums[i] <= 10^5

    Solution:
    ---------
    The problem can be efficiently solved using a sorted array and the two-pointer technique:
    1. **Sorting the Array**:
        - Sorting helps in efficiently skipping duplicates and simplifies the two-pointer approach.
    2. **Two-Pointer Search**:
        - For each element `nums[i]` (as the first number in the triplet), find pairs of numbers
          in the remaining array that sum to `-nums[i]`.
    3. **Avoid Duplicates**:
        - Skip duplicate elements while fixing the first element (`nums[i]`).
        - Similarly, skip duplicate elements for the second and third elements while adjusting pointers.
    4. **Time Complexity**:
        - Sorting: O(n log n)
        - Two-pointer traversal for each element: O(n^2)
        - Overall: O(n^2)
    """

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Finds all unique triplets in the array that sum to zero.

        Args:
            nums (List[int]): The input array of integers.

        Returns:
            List[List[int]]: A list of unique triplets where the sum of elements is zero.
        """
        # Sort the list to enable two-pointer technique and avoid duplicates
        nums.sort()
        results = []

        # Iterate over the array to fix the first element of the triplet
        for i in range(len(nums)):
            # Skip duplicates for the first element
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Use two pointers to find the remaining two elements
            target = -nums[i]
            left, right = i + 1, len(nums) - 1

            while left < right:
                curr_sum = nums[left] + nums[right]
                if curr_sum == target:
                    results.append([nums[i], nums[left], nums[right]])

                    # Skip duplicates for the second and third elements
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    # Move pointers inward
                    left += 1
                    right -= 1
                elif curr_sum < target:
                    # Increase the sum by moving the left pointer
                    left += 1
                else:
                    # Decrease the sum by moving the right pointer
                    right -= 1

        return results
