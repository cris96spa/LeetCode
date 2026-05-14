from collections import Counter, deque
from heapq import heapify, heappop, heappush
from typing import List


class Solution:
    """Find the minimum number of CPU intervals to complete all tasks with cooling period n.

    Problem Statement:
        Given an array of CPU tasks labeled A-Z and a cooldown period n, each identical task
        must be separated by at least n intervals. CPU can be idle. Return the minimum total
        intervals required.

    Approach:
        Max-heap + waiting queue. Use a max-heap of (negative count, task). Each interval,
        pop the most frequent task, decrement count, and schedule it to re-enter the heap
        after n intervals. Track time for when waiting tasks become available.

    Complexity:
        Time: O(m log k) where m = number of tasks and k = number of unique tasks (<= 26).
        Space: O(k) for heap and queue.
    """

    def leastInterval(self, tasks: List[str], n: int) -> int:
        frequency_count = Counter(tasks)
        priority_queue = [(-count, task) for task, count in frequency_count.items()]
        heapify(priority_queue)

        waiting_queue: deque = deque()
        time = 0

        while priority_queue or waiting_queue:
            time += 1

            if priority_queue:
                count, task = heappop(priority_queue)
                count += 1
                if count:
                    waiting_queue.append((time + n, count, task))

            if waiting_queue and waiting_queue[0][0] == time:
                _, count, task = waiting_queue.popleft()
                heappush(priority_queue, (count, task))

        return time
