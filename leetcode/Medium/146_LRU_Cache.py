from typing import Dict


class Node:
    """A Node in a doubly linked list."""

    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """Design and implement a Least Recently Used (LRU) cache.

    Problem Statement:
        Implement LRUCache(capacity) with get(key) and put(key, value) each running in O(1)
        average time. Evict the least recently used entry when capacity is exceeded.

    Approach:
        Combine a doubly linked list (to track usage order) with a hash map (for O(1) access).
        The head of the list is the most recently used; the tail is least recently used.
        On access or insert, move the node to the head. On eviction, remove from the tail.

    Complexity:
        Time: O(1) for both get and put.
        Space: O(capacity) for the cache storage.
    """

    def __init__(self, capacity: int):
        assert capacity > 0, "The LRU Capacity must be > 0"
        self.capacity = capacity
        self.cache: Dict[int, Node] = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            node.value = value
            self._add(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            node = Node(key, value)
            self.cache[key] = node
            self._add(node)

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add(self, node: Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
