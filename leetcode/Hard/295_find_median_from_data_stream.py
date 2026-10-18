import heapq


class MedianFinder:
    """Maintain the median of a stream of numbers.

    Problem Statement:
        Implement MedianFinder with addNum(num), which adds an integer from
        the stream, and findMedian(), which returns the median of all
        numbers so far: the middle element if their count is odd, or the
        mean of the two middle elements if it is even.

    Example:
        addNum(1), addNum(2) -> findMedian() = 1.5
        addNum(3)            -> findMedian() = 2.0

    Approach:
        Keeping every number in a sorted list makes findMedian O(1), but
        each insertion costs O(n): binary search finds the slot, then the
        tail has to shift (re-sorting from scratch would be O(n log n)).

        The median only depends on the boundary between the smaller and the
        larger half, so split the numbers into two heaps:
            - low: a max-heap of the smaller half, whose top is its largest;
            - high: a min-heap of the larger half, whose top is its smallest.
        Invariants: every element of low <= every element of high, and
        len(low) == len(high) or len(low) == len(high) + 1. The median is
        then -low[0] (odd count) or the mean of both tops (even count).

        Python's heapq is a min-heap, so low stores negated values.

        addNum restores both invariants in two steps:
            - push num into low and pop low's largest into high. Whichever
              of the two was larger ends up in high, so the ordering holds;
            - if high is now longer than low, move high's smallest back to
              low to restore the size balance.

        Trace on 2, 3, 4:
            add 2: low = [2], high = []
            add 3: 3 goes through low into high: low = [2], high = [3]
            add 4: 4 goes through low into high, high is longer, 3 moves
                   back: low = [3, 2], high = [4] -> median 3

    Complexity:
        Time: O(log n) for addNum, at most three heap operations; O(1) for
            findMedian.
        Space: O(n) for the two heaps.

    Follow-ups:
        All numbers in [0, 100]: replace the heaps with a counting array.
        addNum is counts[num] += 1, O(1). findMedian walks the 101 counters
        to find the values at ranks (n - 1) // 2 and n // 2 (the same rank
        when n is odd), which is O(101) = O(1). Space is O(1).

            counts = [0] * 101

            def kth(r: int) -> int:  # value at 0-based rank r
                seen = 0
                for value, count in enumerate(counts):
                    seen += count
                    if seen > r:
                        return value

            median = (kth((n - 1) // 2) + kth(n // 2)) / 2

        99% of numbers in [0, 100]: keep the counting array for in-range
        numbers and store the outliers in two sorted lists, `below` (< 0)
        and `above` (> 100). A rank r falls in `below` if r < len(below),
        in the counters if it is less than len(below) plus the in-range
        total, and in `above` otherwise. With at most 1% of numbers outside
        the range, the middle ranks land in the counters, so findMedian
        stays O(1). Inserting an outlier with insort costs O(outliers), but
        only 1% of the numbers pay it.

            counts = [0] * 101
            in_range = 0
            below: list[int] = []
            above: list[int] = []

            def add(num: int) -> None:
                if num < 0:
                    bisect.insort(below, num)
                elif num > 100:
                    bisect.insort(above, num)
                else:
                    counts[num] += 1
                    in_range += 1

            def kth(r: int) -> int:  # value at 0-based rank r
                if r < len(below):
                    return below[r]
                r -= len(below)
                if r >= in_range:
                    return above[r - in_range]
                seen = 0
                for value, count in enumerate(counts):
                    seen += count
                    if seen > r:
                        return value

            median = (kth((n - 1) // 2) + kth(n // 2)) / 2
    """

    def __init__(self):
        # Max-heap (negated) of the smaller half; holds the extra element
        # when the count is odd
        self._low: list[int] = []
        # Min-heap of the larger half
        self._high: list[int] = []

    def addNum(self, num: int) -> None:
        low_highest = -heapq.heappushpop(self._low, -num)
        heapq.heappush(self._high, low_highest)

        if len(self._high) > len(self._low):
            high_lowest = heapq.heappop(self._high)
            heapq.heappush(self._low, -high_lowest)

    def findMedian(self) -> float:
        if len(self._low) == len(self._high):
            return (-self._low[0] + self._high[0]) / 2
        return -self._low[0]
