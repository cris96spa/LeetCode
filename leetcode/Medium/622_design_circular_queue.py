class MyCircularQueue:
    """Design a circular queue (ring buffer) with fixed capacity.

    Problem Statement:
        Implement MyCircularQueue(k), a FIFO queue of capacity k whose last
        position wraps around to the first. Support enQueue, deQueue, Front,
        Rear, isEmpty and isFull. enQueue and deQueue return whether the
        operation succeeded; Front and Rear return -1 on an empty queue.

    Approach:
        Preallocate a buffer of size k and track two values: front, the index
        of the oldest element, and size, the number of stored elements.
        Every other position follows from them modulo k:
            - the rear element is at (front + size - 1) % k;
            - the next free slot is at (front + size) % k.

        enQueue writes into the next free slot and increments size. deQueue
        just advances front by one (mod k) and decrements size; the old value
        is left in the buffer and will be overwritten later.

        Keeping size instead of a rear pointer avoids the ambiguity of
        front == rear meaning either empty or full.

        Example with k = 4, after enQueue 1, 2, 3, 4, deQueue, enQueue 5:
            buffer = [5, 2, 3, 4], front = 1, size = 4
            Front() -> 2, Rear() -> buffer[(1 + 4 - 1) % 4] = 5

    Complexity:
        Time: O(1) for every operation.
        Space: O(k) for the buffer.
    """

    def __init__(self, k: int):
        self._buffer: list[int] = [0] * k
        # Points to the first element to be processed
        self._front = 0
        self._size = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False

        insert_idx = (self._front + self._size) % len(self._buffer)
        self._buffer[insert_idx] = value
        self._size += 1

        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False

        # The dequeued element, if needed, is self._buffer[self._front]
        self._front = (self._front + 1) % len(self._buffer)
        self._size -= 1

        return True

    def Front(self) -> int:
        if self.isEmpty():
            return -1
        return self._buffer[self._front]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self._buffer[(self._front + self._size - 1) % len(self._buffer)]

    def isEmpty(self) -> bool:
        return self._size == 0

    def isFull(self) -> bool:
        return self._size == len(self._buffer)
