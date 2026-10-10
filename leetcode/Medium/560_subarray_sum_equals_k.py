class Solution:
    """🧮 Subarray Sum Equals K.

    Problem:
    --------
    Given an integer array `nums` (values may be negative) and an integer `k`, return the
    number of non-empty contiguous subarrays whose sum equals `k`.

    Example (`nums = [1, 1, 1]`, `k = 2`, answer 2): `nums[0:2]` and `nums[1:3]`.

    Key Insight:
    ------------
    Let `P[j] = nums[0] + ... + nums[j - 1]` be the prefix sums, with `P[0] = 0` for the
    empty prefix. Every subarray sum is a difference of two prefix sums:

        sum(nums[i:j]) = P[j] - P[i]        for 0 <= i < j <= n

    So `sum(nums[i:j]) == k` iff `P[i] == P[j] - k`. Counting subarrays becomes counting
    **pairs of prefix sums**: for each end `j`, the number of subarrays ending there is
    the number of **earlier** prefixes `P[i]` (with `i < j`) equal to `P[j] - k`.

    Scan left to right with a hash map `freq[s]` = how many prefixes seen so far equal
    `s`. At each `j`, add `freq[P[j] - k]` to the answer, then record `P[j]`.

    Example (`nums = [1, 1, 1]`, `k = 2`):

          num   P[j]   P[j] - k   freq before          count
          1     1      -1         {0: 1}               0
          1     2       0         {0: 1, 1: 1}         1    (nums[0:2])
          1     3       1         {0: 1, 1: 1, 2: 1}   2    (nums[1:3])

    Why not a sliding window? Negative values break it: extending a window can lower its
    sum, so there's no rule for when to move the left end. Prefix sums work for any sign.

    Approach:
    ---------
    - `freq` starts as `{0: 1}`: the empty prefix `P[0] = 0`. Without it, subarrays that
      start at index 0 (where `P[j] == k`) are never counted.
    - Query **before** inserting the current prefix. That enforces `i < j`, so the
      subarray is non-empty. With `k = 0`, inserting first would count every `P[j]`
      against itself.
    - Store counts, not just presence: several earlier prefixes can share the same value
      (zeros or negatives), and each one starts a different subarray.

    Complexity:
    -----------
    - Time: O(n), one pass with O(1) expected hash operations
    - Space: O(n) for the prefix-sum counts
    """

    def subarraySum(self, nums: list[int], k: int) -> int:
        prefix_sum = 0
        count = 0
        # We keep track of the occurrences of each value we see
        # while computing the prefix sum
        freq = {0: 1}
        for num in nums:
            prefix_sum += num

            count += freq.get(prefix_sum - k, 0)
            freq[prefix_sum] = freq.get(prefix_sum, 0) + 1

        return count
