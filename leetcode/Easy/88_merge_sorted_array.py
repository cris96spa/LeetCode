from typing import List


class Solution:
    """Merge two sorted arrays into the first one, in place.

    Problem Statement:
        Given two integer arrays nums1 and nums2, sorted in non-decreasing
        order, and two integers m and n, the number of elements in nums1 and
        nums2 respectively, merge nums2 into nums1 as one array sorted in
        non-decreasing order. nums1 has length m + n: the first m elements are
        the ones to merge and the last n are zeros to be overwritten.

    Example:
        nums1 = [1, 2, 3, 0, 0, 0], m = 3
        nums2 = [2, 3, 6],          n = 3
        -> nums1 = [1, 2, 2, 3, 3, 6]

        nums1 = [1], m = 1
        nums2 = [],  n = 0
        -> nums1 = [1]

    Approach:
        This is the merge step of merge sort, done with O(1) extra space. With
        an O(n) buffer it is trivial: walk both arrays from the front, append
        the smaller of nums1[p1] and nums2[p2], and advance that pointer.

        To merge in place, use the free space at the end of nums1 and merge
        from the back: compare nums1[r1] and nums2[r2], write the larger one to
        nums1[w], and step that pointer back. This never overwrites an unread
        element of nums1, since w - r1 = r2 + 1 > 0 while nums2 has elements
        left. Once nums2 is exhausted, the remaining nums1[0..r1] are already in
        place, so the loop can stop.

    Complexity:
        Time: O(m + n), each element is written at most once.
        Space: O(1), only three pointers are used.
    """

    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        r1 = m - 1
        r2 = n - 1
        w = m + n - 1
        while r2 >= 0:
            if r1 >= 0 and nums1[r1] >= nums2[r2]:
                nums1[w] = nums1[r1]
                r1 -= 1
            else:
                nums1[w] = nums2[r2]
                r2 -= 1
            w -= 1
