import heapq


class Solution:
    """Return the k pairs with the smallest sums from two sorted arrays.

    Problem Statement:
        Given two integer arrays nums1 and nums2 sorted in non-decreasing
        order and an integer k, return the k pairs (u, v) with the smallest
        sums, where u comes from nums1 and v from nums2.

    Example:
        nums1 = [1, 7, 11], nums2 = [2, 4, 6], k = 3
        -> [[1, 2], [1, 4], [1, 6]]

    Approach:
        Brute force builds all n1 * n2 pairs and keeps the k smallest. With
        lengths up to 10^5 that is up to 10^10 pairs: infeasible.

        Picture the sums as a matrix M[i][j] = nums1[i] + nums2[j]. Since
        both arrays are sorted, every row and every column is non-decreasing:
        M[i][j] <= M[i][j + 1] and M[i][j] <= M[i + 1][j]. Each row is
        therefore a sorted list, and the task becomes merging n1 sorted
        lists and stopping after k elements, like Merge k Sorted Lists.

        A min-heap holds the next candidate of each row as (sum, i, j).
        Popping (i, j) emits a pair, and the only new candidate in that row
        is its successor (i, j + 1), so push it.

        The heap is seeded with the head of each row, (i, 0), but only for
        i < k: rows i >= k can never contribute, because the k heads
        M[0][0] <= ... <= M[k - 1][0] are already at least k pairs no larger
        than anything in row i.

        Trace on the example (heap seeded with (3, 0, 0), (9, 1, 0),
        (13, 2, 0)):
            pop (3, 0, 0) -> [1, 2], push (5, 0, 1)
            pop (5, 0, 1) -> [1, 4], push (7, 0, 2)
            pop (7, 0, 2) -> [1, 6], k pairs found

    Complexity:
        Time: O(k log k), heapify is O(min(n1, k)), then k pops each followed
            by at most one push, on a heap that never exceeds k entries.
        Space: O(k) for the heap, plus the output.
    """

    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        heap = [(num1 + nums2[0], i, 0) for i, num1 in enumerate(nums1[:k])]
        heapq.heapify(heap)
        result: list[list[int]] = []

        while heap and len(result) < k:
            _, i, j = heapq.heappop(heap)
            result.append([nums1[i], nums2[j]])
            if j + 1 < len(nums2):
                heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))

        return result
