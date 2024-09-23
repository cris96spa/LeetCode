 """
        Problem Description:
        You are given two arrays `nums1` and `nums2`, where `nums1` is a subset of `nums2`. For each element
        in `nums1`, the goal is to find the next greater element in `nums2`. The next greater element for a 
        number x in `nums2` is the first element to the right of x that is larger than x. If no such element exists, 
        return -1 for that number.

        Approach:
        - To solve this problem efficiently, we can use a stack and a dictionary to keep track of the next 
          greater element for each number in `nums2`. Instead of iterating over `nums2` multiple times (which 
          could lead to O(n^2) time complexity), we can process `nums2` in one pass.
        
        Solution Breakdown:
        1. We scan `nums2` from right to left. This ensures that when processing an element, all the potential 
           next greater elements to its right have already been processed and are available for comparison.
        
        2. We use a stack to maintain a decreasing sequence of elements from `nums2`. As we move through 
           the array, we pop elements from the stack that are smaller than the current element, because they 
           cannot be the next greater element for any element to the left.

        3. The top of the stack after the popping process will be the next greater element for the current 
           element in `nums2`. If the stack is empty, it means there is no greater element to the right, so 
           we store `-1`.

        4. For fast lookup, we store the next greater element for each number in a dictionary (`next_greater`), 
           where the key is the number and the value is its next greater element.

        5. Finally, for each element in `nums1`, we simply look up the precomputed next greater element 
           in the `next_greater` dictionary and return the result.
        
        Time Complexity:
        - Processing `nums2` takes O(n), where n is the length of `nums2`. For each element in `nums2`, 
          we perform a constant number of operations (push and pop), so overall the stack operations take O(n).
        - Constructing the result for `nums1` takes O(m), where m is the length of `nums1`.
        - Thus, the total time complexity is O(n + m).

        Space Complexity:
        - We use a dictionary to store the next greater element for each element in `nums2`, which takes O(n) space.
        - The stack can also take up to O(n) space in the worst case.
        """

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # Use a dict to keep the next greater for each element in nums2
        next_greater = {}  

        # Use a stack to keep the number, scanning nums2 in reverse order
        stack = []
        for num in reversed(nums2):
            # pop elements from the stack until the top is greater than num
            while stack and stack[-1] < num:
                stack.pop()
            # Get the next greater from the top of the stack
            next_greater[num] = stack[-1] if stack else -1
            
            # Push the current element on the stack
            stack.append(num)
        
        # Return the result for nums1 by looking up in the next_greater dictionary
        return [next_greater[num] for num in nums1]