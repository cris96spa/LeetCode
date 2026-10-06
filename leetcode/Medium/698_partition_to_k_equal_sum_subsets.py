class Solution:
    """🎲 Partition to K Equal Sum Subsets.

    Problem:
    --------
    Given an integer array `nums` (positive values, possibly repeated) and an integer `k`,
    return whether `nums` can be divided into `k` non-empty subsets with equal sums. Every
    element must be used exactly once.

    Approach:
    ---------
    Each subset must sum to `target = sum(nums) // k`, so a necessary (not sufficient)
    condition is `sum(nums) % k == 0`; likewise no element may exceed `target`.

    Backtracking over the elements: keep `k` bucket sums and, for each element in turn,
    try placing it into each bucket.
    - Complete: every element is placed. No bucket exceeds `target` and the buckets sum to
      `k * target`, so each holds exactly `target` (and is non-empty, since `target > 0`).
    - Make move: add `nums[idx]` to a bucket, then recurse on `idx + 1`.
    - Unmake move: subtract it again. Return as soon as one branch succeeds.
    - Prune:
      - Skip a bucket that would overflow `target`.
      - Skip a bucket whose current sum was already tried for this element: buckets with
        equal sums are interchangeable, so placing the element there gives a symmetric state
        that fails the same way. In particular all empty buckets are equivalent, so the first
        element is tried in only one of them.
      - Sort `nums` in decreasing order: large elements have the fewest valid buckets, so
        dead ends surface near the root instead of deep in the tree.

    Complexity:
    -----------
    - Time: O(k^n) worst case, each of the n elements tried in up to k buckets; pruning cuts
      this sharply in practice. The O(n log n) sort is dominated.
    - Space: O(n * k) auxiliary, recursion depth n with a `seen` set of up to k sums per frame,
      plus O(n) for the sorted copy and O(k) for the buckets.
    """

    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        total_sum = sum(nums)
        if total_sum % k != 0:
            return False

        target = total_sum // k
        # Largest first, so dead ends are found near the root
        nums = sorted(nums, reverse=True)
        if nums[0] > target:
            return False

        buckets = [0] * k

        def place(idx: int) -> bool:
            """Try to place nums[idx] into one of the buckets."""
            if idx == len(nums):
                return True

            seen: set[int] = set()
            for bucket_idx in range(k):
                # Skip overflowing buckets and buckets equivalent to one already tried
                if buckets[bucket_idx] + nums[idx] > target or buckets[bucket_idx] in seen:
                    continue

                seen.add(buckets[bucket_idx])
                buckets[bucket_idx] += nums[idx]
                if place(idx + 1):
                    return True
                buckets[bucket_idx] -= nums[idx]

            return False

        return place(0)
