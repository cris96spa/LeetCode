# Graphs

## Representations

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
| Adjacency Matrix | O(V^2) | O(1) | O(V) | Dense graphs, edge queries |
| Edge List | O(E) | O(E) | O(E) | Simple algorithms (Kruskal's) |
| Matrix Grid | O(V) | O(1) | O(1) | 2D grid problems |

---

## DFS (Depth-First Search)

**When to Use:**
- Exploring all paths
- Cycle detection
- Connected components
- Topological sort (DAGs)
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
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

### Number of Islands (LC 200)

Count connected components of 1s in a 2D grid.

```python
def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] == '0'):
            return
        
        grid[r][c] = '0'  # Mark visited
        
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

**Time:** O(rows x cols) | **Space:** O(rows x cols) recursion stack worst case

### Clone Graph (LC 133)

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node: 'Node') -> 'Node':
    if not node:
        return None
    
    clones = {}
    
    def dfs(node):
        if node in clones:
            return clones[node]
        
        clone = Node(node.val)
        clones[node] = clone
        
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
```

**Time:** O(V + E) | **Space:** O(V)

---

## BFS (Breadth-First Search)

**When to Use:**
- Shortest path (unweighted)
- Level-by-level traversal
- Minimum steps/moves
- "What's the closest X?"

### Template: Standard BFS

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

### Shortest Path in Binary Matrix (LC 1091)

Find shortest path from (0,0) to (n-1,n-1) using 8 directions.

```python
def shortestPathBinaryMatrix(grid: List[List[int]]) -> int:
    n = len(grid)
    
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1
    
    if n == 1:
        return 1
    
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

**Time:** O(n^2) | **Space:** O(n^2)

BFS guarantees shortest path in unweighted graphs.

### Multi-source BFS / Rotting Oranges (LC 994)

Start BFS from all sources simultaneously. Add all starting nodes to the queue before processing.

```python
def orangesRotting(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    
    # Add all rotten oranges to queue at once
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    
    if fresh == 0:
        return 0
    
    minutes = 0
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] == 1):
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    
    return minutes - 1 if fresh == 0 else -1
```

**Time:** O(rows x cols) | **Space:** O(rows x cols)

---

## Topological Sort

**When to Use:**
- Dependency resolution (courses, build systems)
- Task scheduling with prerequisites
- Directed acyclic graphs (DAG)

### Kahn's Algorithm (BFS-based)

```python
def topological_sort_kahn(n, edges):
    graph = {i: [] for i in range(n)}
    in_degree = [0] * n
    
    for src, dst in edges:
        graph[src].append(dst)
        in_degree[dst] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == n else []  # Empty = cycle detected
```

**Time:** O(V + E) | **Space:** O(V)

### Course Schedule (LC 207)

Can you finish all courses given prerequisites?

```python
def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    graph = {i: [] for i in range(numCourses)}
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
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

**Time:** O(V + E) | **Space:** O(V)

### Course Schedule II (LC 210)

Return a valid ordering (or empty if impossible).

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

## Cycle Detection

### Undirected Graph (DFS with parent)

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

### Directed Graph (DFS with colors)

```python
def has_cycle_directed(graph):
    # 0: unvisited, 1: in current path, 2: fully processed
    color = {node: 0 for node in graph}
    
    def dfs(node):
        if color[node] == 1:  # Back edge (cycle)
            return True
        if color[node] == 2:  # Already processed
            return False
        
        color[node] = 1  # Mark as in-progress
        
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

## Shortest Path Algorithms

### Dijkstra's Algorithm (non-negative weights)

Use when all edge weights are non-negative.

```python
import heapq

def dijkstra(graph, start):
    # graph[node] = [(neighbor, weight), ...]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    pq = [(0, start)]  # (distance, node)
    
    while pq:
        curr_dist, node = heapq.heappop(pq)
        
        if curr_dist > distances[node]:
            continue  # Already found a shorter path
        
        for neighbor, weight in graph[node]:
            distance = curr_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
```

**Time:** O((V + E) log V) with binary heap | **Space:** O(V)

### Bellman-Ford (handles negative weights)

Use when edges can have negative weights. Also detects negative cycles.

```python
def bellman_ford(n, edges, start):
    """
    n: number of vertices
    edges: list of (u, v, weight)
    start: source vertex
    Returns distances dict, or None if negative cycle exists.
    """
    dist = [float('inf')] * n
    dist[start] = 0
    
    # Relax all edges V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    
    # Check for negative cycles (one more pass)
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # Negative cycle detected
    
    return dist
```

**Time:** O(V * E) | **Space:** O(V)

**Dijkstra vs Bellman-Ford:**
- Dijkstra: faster, but requires non-negative weights
- Bellman-Ford: slower, but handles negative weights and detects negative cycles

---

## Bipartite Graph Check (LC 785)

A graph is bipartite if nodes can be colored with 2 colors such that no adjacent nodes share a color. Use BFS coloring.

```python
def isBipartite(graph: List[List[int]]) -> bool:
    n = len(graph)
    color = [-1] * n  # -1 = uncolored
    
    for start in range(n):
        if color[start] != -1:
            continue
        
        queue = deque([start])
        color[start] = 0
        
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False  # Same color on adjacent nodes
    
    return True
```

**Time:** O(V + E) | **Space:** O(V)

---

## Grid Patterns

### 4-directional / 8-directional movement

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

**8-directional:**
```python
directions = [(-1,-1), (-1,0), (-1,1), (0,-1),
              (0,1), (1,-1), (1,0), (1,1)]
```

### Boundary Problems / Surrounded Regions (LC 130)

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

**Time:** O(rows x cols) | **Space:** O(rows x cols)

---

## Union Find

For Union Find (disjoint set) data structure, implementations, and problems, see [trie_union_find.md](trie_union_find.md).

---

## Pattern Recognition Table

| Signal | Pattern |
|--------|---------|
| "Shortest path" (unweighted) | BFS |
| "Shortest path" (weighted, non-negative) | Dijkstra |
| "Shortest path" (negative weights) | Bellman-Ford |
| "All paths" / "combinations" | DFS + backtracking |
| Prerequisites / dependencies | Topological sort |
| Connected components | DFS/BFS or Union Find |
| Cycle detection (undirected) | DFS with parent or Union Find |
| Cycle detection (directed) | DFS with colors |
| 2-colorable / bipartite | BFS coloring |
| Level-by-level | BFS |
| Grid traversal | DFS/BFS with directions array |
| Boundary-connected regions | DFS/BFS from edges |
| Multi-source spread | Multi-source BFS |

## Complexity Reference Table

| Algorithm | Time | Space |
|-----------|------|-------|
| DFS | O(V + E) | O(V) |
| BFS | O(V + E) | O(V) |
| Topological Sort | O(V + E) | O(V) |
| Dijkstra (binary heap) | O((V+E) log V) | O(V) |
| Bellman-Ford | O(V * E) | O(V) |
| Union Find (per op) | O(a(V)) ~= O(1) | O(V) |

## Common Mistakes

1. **Not marking nodes as visited** -- causes infinite loops. Mark when adding to queue (BFS) or at start of visit (DFS).

2. **Wrong graph representation** -- directed vs undirected. Check if edges are bidirectional.

3. **Modifying input carelessly** -- ask if you can modify the grid. Use extra space if needed.

4. **Forgetting disconnected components** -- loop through all nodes, not just one start node.

5. **Stack overflow in DFS** -- large graphs may need iterative approach.

6. **Using DFS for shortest path** -- BFS gives shortest path in unweighted graphs, not DFS.
