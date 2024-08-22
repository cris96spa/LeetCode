"""
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    You may assume that each input would have exactly one solution, and you may not use the same element twice.
    You can return the answer in any order.

    Example 1:

    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
    Example 2:

    Input: nums = [3,2,4], target = 6
    Output: [1,2]
    Example 3:

    Input: nums = [3,3], target = 6
    Output: [0,1]

    Constraints:

    2 <= nums.length <= 104
    -109 <= nums[i] <= 109
    -109 <= target <= 109
    Only one valid answer exists.
"""

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        sum_dict = {}
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in sum_dict:
                return [i, sum_dict[diff]]
            sum_dict[nums[i]] = i
            
        return []
    
    
"""
This function solves the "Two Sum" problem, where we need to find two distinct indices in an array such that the numbers at those indices add up to a given target.

The approach used is based on a dictionary (hashmap) to store the numbers encountered in the array along with their indices. Here's how it works:

1. We initialize an empty dictionary `sum_dict` which will be used to store the numbers and their corresponding indices as we iterate through the array.

2. We iterate through the `nums` array using a for loop:
   - For each element `nums[i]`, we calculate the difference between the target and the current element (`diff = target - nums[i]`).
   - We then check if this `diff` already exists in the dictionary:
     - If it does, it means we have found the two numbers whose sum equals the target. We return the current index `i` and the index of the previously stored number from the dictionary (`sum_dict[diff]`).
     - If it does not exist, we add the current number along with its index to the dictionary (`sum_dict[nums[i]] = i`).

3. The dictionary allows us to check in constant time whether the required complementary number (`diff`) exists, making the overall time complexity of the solution O(n), where n is the number of elements in the array.

4. If the loop completes without finding a solution, the function returns an empty list. However, given the problem constraints, this scenario will not occur as it is guaranteed that exactly one valid solution exists.
"""
