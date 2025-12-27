# Graphs - Complete Mastery Guide

**Interview Frequency:** ⭐⭐⭐⭐⭐ (75% of Google interviews)  
**Google Frequency:** ⭐⭐⭐⭐⭐ (Almost guaranteed in onsite)  
**Mastery Time:** 10-12 hours

## Why Graphs are Critical for Google

Google's infrastructure is fundamentally graph-based:
- Web crawling (PageRank)
- Social networks (YouTube, Google+)
- Maps and navigation
- Knowledge graphs
- Dependency management

Graphs test:
- **Multiple solution approaches** (DFS vs BFS vs Union Find)
- **Space-time tradeoffs**
- **Edge case handling** (cycles, disconnected components)
- **Code quality** (clean traversal implementation)

---

## Graph Fundamentals

### Graph Representations

**1. Adjacency List (Most Common)**
```python
# Directed graph
graph = {
    0: [1, 2],
    1: [2],
    2: [0, 3],
    3: []
}

# Undirected graph (edges go both ways)
graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1, 3],
    3: [2]
}
```

**2. Adjacency Matrix**
```python
# graph[i][j] = 1 if edge from i to j
graph = [
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 0, 0, 0]
]
```

**3. Edge List**
```python
edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
```

**4. Matrix as Graph (Grid problems)**
```python
# Each cell is a node, edges to adjacent cells
grid = [
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1]
]
```

### When to Use Each

| Representation | Space | Check Edge | Get Neighbors | Use Case |
|---------------|-------|------------|---------------|----------|
| Adjacency List | O(V+E) | O(degree) | O(degree) | Sparse graphs (most interviews) |
| Adjacency Matrix | O(V²) | O(1) | O(V) | Dense graphs, edge queries |
| Edge List | O(E) | O(E) | O(E) | Simple algorithms (Kruskal's) |
| Matrix Grid | O(V) | O(1) | O(1) | 2D grid problems |

---

## Pattern 1: DFS (Depth-First Search)

**When to Use:**
- Exploring all paths
- Cycle detection
- Connected components
- Topological sort (directed acyclic graphs)
- Backtracking problems

### Template: Recursive DFS

```python
def dfs(graph, node, visited):
    if node in visited:
        return
    
    visited.add(node)
    
    # Process node
    print(node)
    
    # Explore neighbors
    for neighbor in graph[node]:
        dfs(graph, neighbor, visited)
```

### Template: Iterative DFS

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        print(node)  # Process
        
        # Add neighbors to stack
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

---

### Problem: Number of Islands (LC 200) ⭐⭐⭐⭐⭐

**Problem:** Count connected components of 1s in 2D grid.

```python
def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        # Boundary check and water check
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] == '0'):
            return
        
        # Mark as visited
        grid[r][c] = '0'
        
        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    
    return count
```

**Complexity:** O(rows × cols) time and space (recursion stack)

**Variations:**
- Return area of largest island
- Count islands with different shapes
- Return perimeter of islands

---

### Problem: Clone Graph (LC 133) ⭐⭐⭐⭐

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node: 'Node') -> 'Node':
    if not node:
        return None
    
    # Map original node to cloned node
    clones = {}
    
    def dfs(node):
        if node in clones:
            return clones[node]
        
        # Create clone
        clone = Node(node.val)
        clones[node] = clone
        
        # Clone neighbors
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
```

**Complexity:** O(V + E) time and space

---

## Pattern 2: BFS (Breadth-First Search)

**When to Use:**
- Shortest path (unweighted)
- Level-by-level traversal
- Minimum steps/moves
- "What's the closest X?"

### Template: BFS

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node)  # Process
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### Template: BFS with Levels

```python
def bfs_levels(graph, start):
    visited = set([start])
    queue = deque([(start, 0)])  # (node, level)
    
    while queue:
        node, level = queue.popleft()
        print(f"Node {node} at level {level}")
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))
```

---

### Problem: Shortest Path in Binary Matrix (LC 1090) ⭐⭐⭐⭐

**Problem:** Find shortest path from (0,0) to (n-1,n-1) in 8 directions.

```python
def shortestPathBinaryMatrix(grid: List[List[int]]) -> int:
    n = len(grid)
    
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    
    if n == 1:
        return 1
    
    # 8 directions
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), 
                  (0,1), (1,-1), (1,0), (1,1)]
    
    queue = deque([(0, 0, 1)])  # (row, col, distance)
    grid[0][0] = 1  # Mark visited
    
    while queue:
        r, c, dist = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if nr == n-1 and nc == n-1:
                return dist + 1
            
            if (0 <= nr < n and 0 <= nc < n and 
                grid[nr][nc] == 0):
                grid[nr][nc] = 1  # Mark visited
                queue.append((nr, nc, dist + 1))
    
    return -1
```

**Complexity:** O(n²) time and space

**Key Pattern:** BFS guarantees shortest path in unweighted graphs

---

## Pattern 3: Topological Sort

**When to Use:**
- Dependency resolution (courses, build systems)
- Task scheduling with prerequisites
- Directed acyclic graphs (DAG)

### Method 1: Kahn's Algorithm (BFS-based)

```python
def topological_sort_kahn(n, edges):
    # Build graph and in-degree count
    graph = {i: [] for i in range(n)}
    in_degree = [0] * n
    
    for src, dst in edges:
        graph[src].append(dst)
        in_degree[dst] += 1
    
    # Start with nodes having in-degree 0
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If all nodes processed, no cycle
    return result if len(result) == n else []
```

**Complexity:** O(V + E) time, O(V) space

---

### Problem: Course Schedule (LC 207) ⭐⭐⭐⭐⭐

**Problem:** Can finish all courses given prerequisites?

```python
def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    # Build graph
    graph = {i: [] for i in range(numCourses)}
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0
    
    while queue:
        course = queue.popleft()
        count += 1
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return count == numCourses
```

**Complexity:** O(V + E) time, O(V) space

---

### Problem: Course Schedule II (LC 210) ⭐⭐⭐⭐⭐

```python
def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    graph = {i: [] for i in range(numCourses)}
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return order if len(order) == numCourses else []
```

---

## Pattern 4: Cycle Detection

### Undirected Graph - DFS

```python
def has_cycle_undirected(graph):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Back edge to non-parent
                return True
        
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node, -1):
                return True
    
    return False
```

### Directed Graph - DFS with Colors

```python
def has_cycle_directed(graph):
    # 0: white (unvisited), 1: gray (visiting), 2: black (done)
    color = {node: 0 for node in graph}
    
    def dfs(node):
        if color[node] == 1:  # Back edge (cycle)
            return True
        if color[node] == 2:  # Already processed
            return False
        
        color[node] = 1  # Mark as visiting
        
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        
        color[node] = 2  # Mark as done
        return False
    
    for node in graph:
        if color[node] == 0:
            if dfs(node):
                return True
    
    return False
```

---

## Pattern 5: Union Find (Disjoint Set)

**When to Use:**
- Dynamic connectivity
- Cycle detection (undirected graphs)
- Minimum spanning tree (Kruskal's)
- Connected components

### Implementation with Path Compression & Union by Rank

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n
        self.components = n
    
    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        
        if px == py:
            return False  # Already connected
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        self.rank[px] += self.rank[py]
        self.components -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Complexity:** O(α(n)) ≈ O(1) amortized per operation

---

### Problem: Number of Connected Components (LC 323) ⭐⭐⭐⭐

```python
def countComponents(n: int, edges: List[List[int]]) -> int:
    uf = UnionFind(n)
    
    for a, b in edges:
        uf.union(a, b)
    
    return uf.components
```

---

## Pattern 6: Shortest Path Algorithms

### Dijkstra's Algorithm (Weighted, Non-negative)

```python
import heapq

def dijkstra(graph, start):
    # graph[node] = [(neighbor, weight), ...]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Min heap: (distance, node)
    pq = [(0, start)]
    
    while pq:
        curr_dist, node = heapq.heappop(pq)
        
        if curr_dist > distances[node]:
            continue
        
        for neighbor, weight in graph[node]:
            distance = curr_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
```

**Complexity:** O((V + E) log V) with binary heap

---

## Google Interview Patterns

### 1. Matrix as Graph (Very Common)

**4-directional movement:**
```python
def solve_grid(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(0,1), (1,0), (0,-1), (-1,0)]  # right, down, left, up
    
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols
    
    def dfs(r, c):
        if not is_valid(r, c) or grid[r][c] == 0:
            return
        
        grid[r][c] = 0  # Mark visited
        
        for dr, dc in directions:
            dfs(r + dr, c + dc)
```

**8-directional movement:**
```python
directions = [(-1,-1), (-1,0), (-1,1), (0,-1), 
              (0,1), (1,-1), (1,0), (1,1)]
```

### 2. Boundary Problems

**Problem: Surrounded Regions (LC 130)**
```python
def solve(board: List[List[str]]) -> None:
    if not board:
        return
    
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != 'O'):
            return
        
        board[r][c] = 'T'  # Temporary mark
        
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            dfs(r + dr, c + dc)
    
    # Mark boundary-connected 'O's
    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)
    
    # Flip: O -> X, T -> O
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'O':
                board[r][c] = 'X'
            elif board[r][c] == 'T':
                board[r][c] = 'O'
```

---

## Master Checklist

### Fundamental Skills
- [ ] Implement DFS (recursive & iterative)
- [ ] Implement BFS with queue
- [ ] Build graph from edge list
- [ ] Detect cycles (directed & undirected)
- [ ] Topological sort (Kahn's & DFS)

### Advanced Skills
- [ ] Union Find with optimizations
- [ ] Dijkstra's algorithm
- [ ] Matrix traversal patterns
- [ ] Bipartite graph check
- [ ] Strongly connected components

### Problem Recognition
- [ ] Shortest path → BFS (unweighted) or Dijkstra
- [ ] All paths/combinations → DFS + backtracking
- [ ] Prerequisites/dependencies → Topological sort
- [ ] Connected components → DFS/BFS or Union Find
- [ ] Minimum spanning tree → Kruskal's or Prim's

---

## Practice Roadmap

### Week 1: Fundamentals (12 problems)
- LC 200, 695 (Islands - DFS on matrix)
- LC 133, 797 (Clone, All Paths - DFS)
- LC 207, 210 (Course Schedule - Topo sort)
- LC 323, 547 (Connected Components)

### Week 2: Advanced (12 problems)
- LC 130, 417 (Boundary problems)
- LC 1091, 286 (BFS shortest path)
- LC 684, 685 (Redundant Connection - Union Find)
- LC 743, 787 (Dijkstra variations)

**Total:** ~10-12 hours

---

## Common Mistakes

1. **Not marking nodes as visited**
   - Causes infinite loops
   - Mark when adding to queue (BFS) or at start (DFS)

2. **Wrong graph representation**
   - Directed vs undirected
   - Check if edge is bidirectional

3. **Modifying input carelessly**
   - Ask if you can modify grid
   - Use extra space if needed

4. **Forgetting disconnected components**
   - Loop through all nodes, not just start

5. **Stack overflow in DFS**
   - Large graphs may need iterative approach

---

**Time Complexity Cheat Sheet:**

| Algorithm | Time | Space |
|-----------|------|-------|
| DFS | O(V + E) | O(V) |
| BFS | O(V + E) | O(V) |
| Topological Sort | O(V + E) | O(V) |
| Union Find | O(α(V)) per op | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |

**Master these patterns, and graphs will become your strength!**
