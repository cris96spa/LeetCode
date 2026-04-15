"""
740. Delete and Earn

You are given an integer array nums. You want to maximize the number of
points you get by performing the following operation any number of times:

    Pick any nums[i] and delete it to earn nums[i] points. Afterwards,
    you must delete every element equal to nums[i] - 1 and every element
    equal to nums[i] + 1.

Return the maximum number of points you can earn by applying the above
operation some number of times.

Approach
--------
The key insight is *problem reduction*: if we aggregate each value's total
contribution (value * count), the decision of whether to "earn" a value
becomes identical to the House Robber problem — pick a value only if you
skip its adjacent neighbours.

A greedy strategy fails (e.g. [2, 2, 3, 3, 4]: picking 3 yields 6, but
picking 2 and 4 yields 8), so we need dynamic programming.

Two strategies are implemented and selected at runtime:

1. **Bucket DP** — iterate over every integer in [1, max(nums)].
   Time O(n + k), Space O(n), where k = max(nums).
   Best when the value range is dense relative to n.

2. **Sparse DP** — sort the unique values and only iterate over those.
   Time O(n + u·log u), Space O(n), where u = len(unique(nums)).
   Best when the value range is large but sparsely populated.

The heuristic `k <= 2n` picks bucket DP when the range is compact,
falling back to sparse DP otherwise.
"""
from collections import Counter
class Solution:
    def deleteAndEarn(self, nums: list[int]) -> int:        
        count = Counter(nums)
        n = len(nums)
        k = max(nums)
        u = len(count)
        
        # Heuristic: choose strategy based on density
        # If value range is not too large -> bucket DP
        if k <= n * 2:
            prev_2 = 0
            prev_1 = count[1] * 1
            
            for i in range(2, k + 1):
                curr = max(
                    prev_1,
                    prev_2 + count[i] * i
                )
                prev_2 = prev_1
                prev_1 = curr
            
            return prev_1
        
        # Otherwise -> sparse DP using sorted keys
        keys = sorted(count.keys())
        
        prev_2 = 0
        prev_1 = 0
        prev_key = None
        
        for key in keys:
            curr_value = key * count[key]
            
            if prev_key is not None and key == prev_key + 1:
                curr = max(prev_1, prev_2 + curr_value)
            else:
                curr = prev_1 + curr_value
            
            prev_2 = prev_1
            prev_1 = curr
            prev_key = key
        
        return prev_1