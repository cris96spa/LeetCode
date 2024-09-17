"""
Problem Description:
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:

LRUCache(int capacity) Initializes the LRU cache with a positive size capacity.
int get(int key) Returns the value of the key if the key exists, otherwise returns -1.
void put(int key, int value) Updates the value of the key if the key exists. Otherwise, adds the key-value pair to the cache.
  If the number of keys exceeds the capacity from this operation, evict the least recently used key.
  
The functions get and put must each run in O(1) average time complexity.

Example:

Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]

Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation:
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // returns 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // returns -1 (not found)
lRUCache.get(3);    // returns 3
lRUCache.get(4);    // returns 4

Solution:
The LRU Cache is implemented using a combination of a double-linked list and a hash map (dictionary).
The dictionary stores the key-to-node mapping, and the double-linked list maintains the order of usage. 
The head of the list represents the most recently used item, while the tail holds the least recently used.

The 'get' operation:
  - When we access a key, if the key exists, we move the node associated with that key to the front of the list.
  - If the key does not exist, return -1.

The 'put' operation:
  - If the key already exists, we update the value and move the corresponding node to the front.
  - If the key does not exist, we create a new node. If the cache is full, we evict the least recently used node
    from the tail, remove it from the dictionary, and add the new node to the front.

Both operations are done in O(1) time due to the constant-time access in the dictionary and efficient list manipulations.

Constraints:
- 1 <= capacity <= 3000
- 0 <= key <= 10^4
- 0 <= value <= 10^5
- At most 2 * 10^5 calls will be made to get and put.

"""
from typing import Dict

class Node:
    """A Node in a double linked list"""
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        """
        Initialize the LRUCache with the given capacity.
        The cache is represented as a combination of a hash map (dictionary) and a double-linked list.
        """
        assert capacity > 0, "The LRU Capacity must be > 0"
        self.capacity = capacity
        self.cache: Dict[int, Node] = {}  # This holds the key-to-node mappings
        self.head = Node(0, 0)  # Dummy head of the double-linked list (most recently used node)
        self.tail = Node(0, 0)  # Dummy tail of the double-linked list (least recently used node)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        """
        Retrieve the value for the given key from the cache.
        If the key is found, move the associated node to the front (most recently used).
        If the key is not found, return -1.
        """
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """
        Insert or update the key-value pair in the cache.
        If the key already exists, update its value and move the node to the front.
        If the key is new and the cache is at full capacity, evict the least recently used node (from the tail).
        """
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            node.value = value
            self._add(node)
        else:
            if len(self.cache) >= self.capacity:
                # Evict the least recently used (LRU) node from the tail
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            # Create a new node and add it to the front
            node = Node(key, value)
            self.cache[key] = node
            self._add(node)

    def _remove(self, node: Node) -> None:
        """
        Remove a node from the double-linked list.
        """
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add(self, node: Node) -> None:
        """
        Add a node right after the head of the list (mark it as the most recently used).
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node