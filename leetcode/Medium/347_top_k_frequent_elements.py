import heapq


class Solution:
    """Return the k most frequent elements of an array.

    Problem Statement:
        Given an integer array nums and an integer k, return the k most
        frequent elements, in any order. 1 <= k <= number of distinct
        elements, and the answer is guaranteed to be unique, so ties at the
        k-th place never occur (e.g. [1, 1, 2, 2] with k = 1 is not a valid
        input).

    Example:
        nums = [1, 1, 1, 2, 2, 3], k = 2
        -> [1, 2]

    Approach:
        Count frequencies, then pick the top k among the m distinct values.
        Sorting them by count is O(m log m).

        A min-heap of size k does better: heap[0] is the least frequent of
        the current top k, so it is the one to replace. Heapify the first k
        (freq, value) pairs, then for each remaining pair whose frequency
        beats heap[0], swap it in with heapreplace. The heap ends up holding
        the k most frequent values.

        Bucket sort reaches O(n): frequencies are integers in [1, n], so put
        each value in buckets[freq] and read the buckets from n down until k
        values are collected:

            buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
            for num, freq in freq_count.items():
                buckets[freq].append(num)

            result: list[int] = []
            for freq in range(len(nums), 0, -1):
                for num in buckets[freq]:
                    result.append(num)
                    if len(result) == k:
                        return result

        In practice it is not worth it here: values lie in [-10^4, 10^4], so
        m <= 20001 and log k <= ~15 is effectively a constant, while the
        n + 1 buckets (up to 10^5 lists, mostly empty) cost more to allocate
        than the whole heap pass.

    Complexity:
        Time: O(n + m log k), counting is O(n) and each of the m - k
            remaining pairs costs at most one O(log k) heap operation.
        Space: O(m) for the counts.
    """

    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        freq_count: dict[int, int] = {}
        for num in nums:
            freq_count[num] = freq_count.get(num, 0) + 1

        freq_list = [(freq, num) for num, freq in freq_count.items()]

        heap = freq_list[:k]
        heapq.heapify(heap)

        for freq, num in freq_list[k:]:
            if freq > heap[0][0]:
                heapq.heapreplace(heap, (freq, num))

        return [num for _, num in heap]
