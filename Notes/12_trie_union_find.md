# Trie & Union Find

## Part 1: Trie (Prefix Tree)

### What is a Trie

A trie (pronounced "try") is a tree where each node represents a character, and paths from root to nodes form strings. Efficient for prefix-based operations: autocomplete, spell checking, IP routing, word games.

### Implementation (TrieNode class)

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def delete(self, word: str) -> bool:
        def _delete(node, word, index):
            if index == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False
            
            should_delete = _delete(node.children[char], word, index + 1)
            
            if should_delete:
                del node.children[char]
                return not node.is_end_of_word and len(node.children) == 0
            
            return False
        
        return _delete(self.root, word, 0)
```

**Complexity:**
- Insert: O(m) time, O(m) space where m = word length
- Search: O(m) time, O(1) space
- Prefix check: O(m) time, O(1) space
- Total space: O(ALPHABET_SIZE x N x M) worst case

### Compact Implementation (dict-based)

```python
class Trie:
    def __init__(self):
        self.root = {}
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['$'] = True  # End marker
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        return '$' in node
    
    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node:
                return False
            node = node[char]
        return True
```

### Implement Trie (LC 208)

Solved by either implementation above.

### Add and Search Words (LC 211)

Supports wildcard `.` matching any single character. Use DFS when encountering `.`.

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return node.is_end_of_word
            
            if word[i] == '.':
                # Try all children
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                if word[i] not in node.children:
                    return False
                return dfs(node.children[word[i]], i + 1)
        
        return dfs(self.root, 0)
```

**Time:** O(m) for addWord, O(26^m) worst case for search with all dots (typically much better) | **Space:** O(m)

### Word Search II (LC 212)

Find all words from a dictionary in a 2D board.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Store complete word at end node

def findWords(board: List[List[str]], words: List[str]) -> List[str]:
    # Build trie
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word
    
    result = []
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c, node):
        char = board[r][c]
        
        if char not in node.children:
            return
        
        next_node = node.children[char]
        
        if next_node.word:
            result.append(next_node.word)
            next_node.word = None  # Avoid duplicates
        
        board[r][c] = '#'  # Mark visited
        
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, next_node)
        
        board[r][c] = char  # Restore
        
        # Prune trie (optimization)
        if not next_node.children:
            del node.children[char]
    
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    
    return result
```

**Time:** O(M x N x 4^L) where M x N = board size, L = max word length | **Space:** O(total characters in all words)

### Autocomplete System

```python
class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.trie = {}
        self.current = self.trie
        self.current_sentence = ""
        
        for sentence, count in zip(sentences, times):
            self._add(sentence, count)
    
    def _add(self, sentence, count):
        node = self.trie
        for char in sentence:
            if char not in node:
                node[char] = {'#': {}}
            node = node[char]
        node['#']['count'] = node['#'].get('count', 0) + count
        node['#']['sentence'] = sentence
    
    def input(self, c: str) -> List[str]:
        if c == '#':
            self._add(self.current_sentence, 1)
            self.current = self.trie
            self.current_sentence = ""
            return []
        
        self.current_sentence += c
        
        if c not in self.current:
            self.current['#'] = {}
            self.current = self.current['#']
            return []
        
        self.current = self.current[c]
        
        results = []
        
        def dfs(node):
            if '#' in node and 'sentence' in node['#']:
                results.append((node['#']['count'], node['#']['sentence']))
            for char in node:
                if char != '#':
                    dfs(node[char])
        
        dfs(self.current)
        
        # Sort by frequency (desc), then lexicographically
        results.sort(key=lambda x: (-x[0], x[1]))
        return [sentence for _, sentence in results[:3]]
```

---

## Part 2: Union Find (Disjoint Set)

### What is Union Find

Union Find tracks disjoint sets and supports:
- **Union:** Merge two sets
- **Find:** Determine which set an element belongs to
- **Connected:** Check if two elements are in the same set

Use cases: network connectivity, cycle detection in undirected graphs, connected components, Kruskal's MST.

### Implementation (path compression + union by rank)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n
        self.components = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.rank[root_y] += self.rank[root_x]
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += self.rank[root_y]
        
        self.components -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
    
    def count(self):
        return self.components
```

**Time:** O(a(n)) per operation, where a = inverse Ackermann function (effectively O(1) amortized)

**Space:** O(n)

### Size Tracking Variant

```python
class UnionFindWithSize:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        
        # Attach smaller to larger
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True
    
    def get_size(self, x):
        return self.size[self.find(x)]
```

### Connected Components (LC 323)

```python
def countComponents(n: int, edges: List[List[int]]) -> int:
    uf = UnionFind(n)
    
    for a, b in edges:
        uf.union(a, b)
    
    return uf.count()
```

**Time:** O(E x a(V)) ~= O(E) | **Space:** O(V)

### Redundant Connection (LC 684)

Find the edge that creates a cycle in an undirected graph.

```python
def findRedundantConnection(edges: List[List[int]]) -> List[int]:
    uf = UnionFind(len(edges) + 1)
    
    for a, b in edges:
        if not uf.union(a, b):
            return [a, b]  # Already connected = cycle
    
    return []
```

**Time:** O(E x a(V)) | **Space:** O(V)

### Graph Valid Tree (LC 261)

A graph is a valid tree if it has exactly n-1 edges and no cycles (equivalently: n-1 edges and all nodes connected).

```python
def validTree(n: int, edges: List[List[int]]) -> bool:
    if len(edges) != n - 1:
        return False
    
    uf = UnionFind(n)
    
    for a, b in edges:
        if not uf.union(a, b):
            return False  # Cycle detected
    
    return True
```

**Time:** O(E x a(V)) | **Space:** O(V)

### Accounts Merge (LC 721)

Merge accounts that share common emails.

```python
def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    email_to_id = {}
    uf = UnionFind(len(accounts))
    
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            else:
                email_to_id[email] = i
    
    # Group emails by root account
    root_to_emails = {}
    for email, acc_id in email_to_id.items():
        root = uf.find(acc_id)
        if root not in root_to_emails:
            root_to_emails[root] = []
        root_to_emails[root].append(email)
    
    result = []
    for root, emails in root_to_emails.items():
        name = accounts[root][0]
        result.append([name] + sorted(emails))
    
    return result
```

**Time:** O(N x K x a(N)) where K = avg emails per account | **Space:** O(N x K)

### Number of Islands with Union Find (LC 200)

```python
def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    
    def index(r, c):
        return r * cols + c
    
    uf = UnionFind(rows * cols)
    water = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '0':
                water += 1
            else:
                for dr, dc in [(0,1), (1,0)]:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                        grid[nr][nc] == '1'):
                        uf.union(index(r, c), index(nr, nc))
    
    return uf.count() - water
```

**Time:** O(M x N x a(M x N)) | **Space:** O(M x N)

### Kruskal's MST

Minimum Spanning Tree using Union Find: sort edges by weight, greedily add edges that don't form cycles.

```python
def kruskal_mst(n, edges):
    """
    n: number of vertices
    edges: list of (weight, u, v)
    Returns: (total_weight, mst_edges)
    """
    edges.sort()  # Sort by weight
    uf = UnionFind(n)
    
    total_weight = 0
    mst_edges = []
    
    for weight, u, v in edges:
        if uf.union(u, v):
            total_weight += weight
            mst_edges.append((u, v, weight))
            
            if len(mst_edges) == n - 1:
                break  # MST complete
    
    # Check if MST spans all vertices
    if len(mst_edges) != n - 1:
        return None  # Graph is not connected
    
    return total_weight, mst_edges
```

**Time:** O(E log E) for sorting + O(E x a(V)) for unions ~= O(E log E) | **Space:** O(V)

---

## Complexity Reference

| Operation | Time | Space |
|-----------|------|-------|
| Trie insert | O(m) | O(m) |
| Trie search / prefix | O(m) | O(1) |
| Trie delete | O(m) | O(m) recursion |
| Union Find (find/union) | O(a(n)) ~= O(1) | O(n) total |
| Kruskal's MST | O(E log E) | O(V) |

## Common Mistakes

### Trie

1. **Forgetting end marker** -- searching "ca" in a trie containing "cat" should return False. Always check `is_end_of_word` or the `$` marker.

2. **Not handling empty strings** -- decide upfront whether empty string is valid input.

3. **Memory leaks from not pruning** -- after deleting words, remove empty nodes to save space.

### Union Find

1. **Not using path compression** -- without it, find is O(n) worst case instead of O(a(n)).
   ```python
   # Wrong: O(n) per find
   def find(self, x):
       while self.parent[x] != x:
           x = self.parent[x]
       return x
   
   # Correct: O(a(n)) per find
   def find(self, x):
       if self.parent[x] != x:
           self.parent[x] = self.find(self.parent[x])
       return self.parent[x]
   ```

2. **Forgetting to check if already connected** -- `union` should return False when elements are already in the same set. This is critical for cycle detection.

3. **Off-by-one with node numbering** -- if nodes are 1-indexed, initialize UnionFind with `n+1`.
