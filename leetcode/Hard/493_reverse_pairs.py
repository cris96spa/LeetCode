class Solution:
    """Count the reverse pairs in nums.

    Problem Statement:
        Given an integer array nums, return the number of reverse pairs.
        A reverse pair is a pair (i, j) such that:
            - 0 <= i < j < len(nums)
            - nums[i] > 2 * nums[j]

    Example:
        nums = [1, 3, 2, 3, 1]
        -> 2, the pairs (1, 4) and (3, 4)

        nums = [2, 4, 3, 5, 1]
        -> 3, the pairs (1, 4), (2, 4) and (3, 4)

    Approach:
        Sorting nums directly loses the index order that the i < j condition
        depends on. Merge sort keeps just enough of it: when merging two
        halves, every element of the left half has a smaller index than
        every element of the right half, whatever order each half is in.

        merge_count(lo, hi) sorts nums[lo:hi] in place and returns the number
        of reverse pairs inside it. Pairs either lie entirely in one half
        (counted by the recursive calls) or cross the midpoint (counted
        during the merge).

        To count crossing pairs, walk the sorted left half with i and keep a
        pointer k into the sorted right half, advancing it while
        nums[i] > 2 * nums[k]. Then every element in nums[mid:k] forms a
        pair with nums[i], adding k - mid to the count. Since nums[i] only
        grows as i advances, k never moves back, so counting is linear.

        The merge itself runs alongside with a separate pointer j, building
        the sorted range in a buffer that is copied back into nums[lo:hi].

    Complexity:
        Time: O(n log n), where n = len(nums). There are O(log n) levels of
            recursion and each level does O(n) work to count and merge.
        Space: O(n) for the merge buffer, plus O(log n) for the recursion
            stack.
    """

    def reversePairs(self, nums: list[int]) -> int:

        def merge_count(lo: int, hi: int) -> int:
            if hi - lo <= 1:
                return 0

            mid = (lo + hi) // 2
            count = merge_count(lo, mid) + merge_count(mid, hi)

            merged: list[int] = []
            i, j, k = lo, mid, mid
            while i < mid:
                if j < hi and nums[j] < nums[i]:
                    merged.append(nums[j])
                    j += 1
                else:
                    while k < hi and nums[i] > 2 * nums[k]:
                        k += 1
                    count += k - mid

                    merged.append(nums[i])
                    i += 1

            merged.extend(nums[j:hi])
            nums[lo:hi] = merged

            return count

        return merge_count(0, len(nums))
