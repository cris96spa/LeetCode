from heapq import heappush, heappop, heapify
from collections import Counter, deque
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Given an array of CPU tasks labeled with letters from A to Z and an integer n,
        return the minimum number of CPU intervals required to complete all tasks,
        ensuring that the same task appears at least 'n' intervals apart.

        Args:
        tasks (List[str]): A list of task labels.
        n (int): The cooling period between two identical tasks.

        Returns:
        int: The minimum number of CPU intervals required.

        Complexity Analysis:
        - Building the max heap: O(k log k), where k is the number of unique tasks.
        - Running the scheduling loop: O(m log k), where m is the number of tasks.
        - Overall: O(m log k), where k ≤ 26 (constant in practice).
        """

        # Step 1: Count frequency of tasks
        frequency_count = Counter(tasks)

        # Step 2: Use a max heap to store task frequencies
        priority_queue = [(-count, task) for task, count in frequency_count.items()]
        heapify(priority_queue)

        # Step 3: Use a queue to track waiting tasks
        waiting_queue = deque()

        time = 0
        while priority_queue or waiting_queue:
            time += 1

            if priority_queue:
                count, task = heappop(priority_queue)
                count += 1  # Reduce the count since the task was executed
                if count:
                    waiting_queue.append(
                        (time + n, count, task)
                    )  # Track when task can be reinserted

            # Check if a task is ready to be pushed back into the priority queue
            if waiting_queue and waiting_queue[0][0] == time:
                _, count, task = waiting_queue.popleft()
                heappush(priority_queue, (count, task))

        return time
