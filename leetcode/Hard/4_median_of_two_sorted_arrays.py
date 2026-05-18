from typing import List


class Solution:
    """Given two sorted arrays nums1 and nums2 of sizes m and n, return the median.

    We need O(log(m + n)), which suggests binary search.

    The idea is to find two split points such that:

        left_a <= right_b
        left_b <= right_a

    Conceptually, we split the merged sorted array into a left partition and a
    right partition.

    The left partition should contain:

        left_size = (m + n + 1) // 2

    elements. The +1 makes odd-length cases easier because the left partition
    contains the median element.

    If we choose split_a, the split in b is fixed:

        split_b = left_size - split_a

    because:

        split_a + split_b = left_size

    Once a valid partition is found:
        - if total length is odd, the median is max(left_a, left_b)
        - if total length is even, the median is the average of:
              max(left_a, left_b)
              min(right_a, right_b)

    If left_a > right_b, we took too many elements from a, so move left.
    Otherwise, we took too few elements from a, so move right.

    Time:  O(log(min(m, n)))
    Space: O(1)
    """

    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Binary search on the smaller array.
        if len(nums1) <= len(nums2):
            a, b = nums1, nums2
        else:
            a, b = nums2, nums1

        m, n = len(a), len(b)
        total = m + n
        left_size = (total + 1) // 2

        low, high = 0, m

        while low <= high:
            split_a = (low + high) // 2
            split_b = left_size - split_a

            left_a = float("-inf") if split_a == 0 else a[split_a - 1]
            right_a = float("inf") if split_a == m else a[split_a]

            left_b = float("-inf") if split_b == 0 else b[split_b - 1]
            right_b = float("inf") if split_b == n else b[split_b]

            if left_a <= right_b and left_b <= right_a:
                if total % 2 == 0:
                    return (max(left_a, left_b) + min(right_a, right_b)) / 2

                return float(max(left_a, left_b))

            elif left_a > right_b:
                high = split_a - 1
            else:
                low = split_a + 1

        raise ValueError("Input arrays must be sorted.")
