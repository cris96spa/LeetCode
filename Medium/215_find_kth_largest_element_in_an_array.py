from heapq import heappush, heappop, heapify
from typing import List

class Solution:
    """
    Problem:
    Given an integer array `nums` and an integer `k`, return the kth largest element in the array.
    Note that it is the kth largest element in the sorted order, not the kth distinct element.

    The array may contain duplicates, and the elements can range between -10^4 and 10^4.
    The size of the array is constrained between 1 and 10^5.

    Approach:
    - We solve this problem using a min-heap of size `k`.
    - First, we initialize the heap with the first `k` elements of `nums`.
    - Then, for each of the remaining elements in the array, we check if it is larger than the
      smallest element in the heap (the root). If it is, we replace the root with the current element.
    - At the end, the root of the heap contains the kth largest element.

    This approach ensures that we maintain a heap of only `k` elements, optimizing the time complexity.

    Time Complexity:
    - Initial heap construction takes O(k).
    - For the remaining `n-k` elements, each insertion into the heap takes O(log k).
    - Therefore, the overall time complexity is O(n log k), where n is the length of `nums` and k is the given input.

    Space Complexity:
    - The space complexity is O(k) due to the heap size.

    Example 1:
    Input: nums = [3,2,1,5,6,4], k = 2
    Output: 5
    
    Example 2:
    Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
    Output: 4

    Constraints:
    - 1 <= k <= nums.length <= 10^5
    - -10^4 <= nums[i] <= 10^4
    """
    
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # Add the first k elements to the heap
        heap = nums[:k]
        heapify(heap)

        # Replace the root if a larger element is found
        for num in nums[k:]:
            if heap[0] < num:
                heappop(heap)
                heappush(heap, num)

        return heap[0]
