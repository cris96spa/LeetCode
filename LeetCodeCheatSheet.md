# LeetCode Patterns Cheat Sheet

## 1. Two Pointers

**Explanation:** The two pointers technique involves using two pointers to iterate through a data structure. It's often used with arrays or linked lists, especially when dealing with sorted data or when searching for pairs with a specific sum.

**Example Problem:** Find two numbers in a sorted array that add up to a target sum.

```python
def two_sum(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

## 2. Sliding Window

**Explanation:** The sliding window technique is used to perform operations on a specific window size of an array or string. It's particularly useful for problems involving subarrays or substrings.

**Example Problem:** Find the maximum sum subarray of a fixed size k.

```python
def max_sum_subarray(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    for i in range(k, len(nums)):
        window_sum = window_sum - nums[i-k] + nums[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

## 3. Fast and Slow Pointers (Floyd's Cycle Detection)

**Explanation:** This technique uses two pointers moving at different speeds to detect cycles in a linked list or to find a specific element in a cyclic structure.

**Example Problem:** Detect if a linked list has a cycle.

```python
def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    
    return False
```

## 4. Merge Intervals

**Explanation:** This pattern deals with problems involving overlapping intervals. It's useful for scheduling problems or when you need to merge overlapping ranges.

**Example Problem:** Merge overlapping intervals.

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])
    return merged
```

## 5. Binary Search

**Explanation:** Binary search is an efficient algorithm for searching a sorted array by repeatedly dividing the search interval in half.

**Example Problem:** Find the index of a target value in a sorted array.

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 6. DFS (Depth-First Search)

**Explanation:** DFS is a graph traversal algorithm that explores as far as possible along each branch before backtracking. It's useful for problems involving tree or graph traversal.

**Example Problem:** Traverse a graph using DFS.

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start)  # Process the node
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

## 7. BFS (Breadth-First Search)

**Explanation:** BFS is a graph traversal algorithm that explores all vertices at the present depth prior to moving on to vertices at the next depth level. It's often used for finding the shortest path in unweighted graphs.

**Example Problem:** Traverse a graph using BFS.

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        print(vertex)  # Process the node
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

## 8. Topological Sort

**Explanation:** Topological sorting is used for ordering tasks with dependencies. It's applicable to directed acyclic graphs (DAGs) and is often used in scheduling problems.

**Example Problem:** Perform a topological sort on a DAG.

```python
from collections import defaultdict

def topological_sort(graph):
    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        sorted_nodes.append(node)

    visited = set()
    sorted_nodes = []
    for node in graph:
        if node not in visited:
            dfs(node)
    return sorted_nodes[::-1]
```

## 9. Dynamic Programming

**Explanation:** Dynamic programming is a method for solving complex problems by breaking them down into simpler subproblems. It's often used for optimization problems.

**Example Problem:** Calculate the nth Fibonacci number.

```python
def fibonacci(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

## 10. Backtracking

**Explanation:** Backtracking is an algorithmic technique that considers searching every possible combination in order to solve a computational problem. It builds candidates for the solution incrementally and abandons a candidate as soon as it determines that the candidate cannot lead to a valid solution.

**Example Problem:** Generate all permutations of a list of numbers.

```python
def permutations(nums):
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # backtrack
    
    result = []
    backtrack(0)
    return result
```

## 11. Heap / Priority Queue

**Explanation:** A heap is a specialized tree-based data structure that satisfies the heap property. It's often used to implement priority queues and in algorithms where you need to repeatedly remove the smallest (or largest) element.

**Example Problem:** Find the k largest elements in an array.

```python
import heapq

def k_largest(nums, k):
    return heapq.nlargest(k, nums)
```

## 12. Trie

**Explanation:** A trie, also called a prefix tree, is a tree-like data structure used to store and retrieve strings. It's particularly useful for problems involving string searches or prefixes.

**Example Problem:** Implement a trie with insert and search operations.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
```

## 13. Union Find (Disjoint Set)

**Explanation:** Union Find is a data structure that keeps track of elements which are split into one or more disjoint sets. It has two primary operations: find and union. It's often used in graph algorithms to detect cycles or compute connected components.

**Example Problem:** Implement a Union Find data structure.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True
```

## 14. Bit Manipulation

**Explanation:** Bit manipulation involves applying bitwise operations to solve problems. It's often used for optimization or when dealing with binary representations of numbers.

**Example Problem:** Count the number of set bits (1s) in an integer.

```python
def count_set_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count
```

## 15. Greedy

**Explanation:** Greedy algorithms make the locally optimal choice at each step with the hope of finding a global optimum. They don't always yield the best solution, but for many problems they do.

**Example Problem:** Activity Selection Problem (maximize the number of activities that can be performed by a single person, assuming the person can only work on a single activity at a time).

```python
def activity_selection(start, finish):
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    selected = [activities[0]]
    for activity in activities[1:]:
        if activity[0] >= selected[-1][1]:
            selected.append(activity)
    return len(selected)
```