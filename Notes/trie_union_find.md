# Trie (Prefix Tree) & Union Find - Complete Guide

## Part 1: Trie (Prefix Tree)

**Interview Frequency:** ⭐⭐⭐ (35% of FAANG interviews)  
**Google Frequency:** ⭐⭐⭐⭐ (System design, autocomplete questions)  
**Mastery Time:** 3-4 hours

### What is a Trie?

A **Trie** (pronounced "try") is a tree data structure for storing strings where:
- Each node represents a character
- Paths from root to nodes form strings
- Efficient for prefix-based operations

**Use Cases:**
- Autocomplete systems
- Spell checkers
- IP routing (longest prefix matching)
- Phone dictionaries
- Word games (Boggle, Scrabble)

---

### Trie Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end_of_word = False
        # Optional: store word, frequency, etc.

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        \"\"\"Insert word into trie. O(m) where m = len(word)\"\"\"
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        \"\"\"Search for exact word. O(m)\"\"\"
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end_of_word
    
    def startsWith(self, prefix: str) -> bool:
        \"\"\"Check if any word starts with prefix. O(m)\"\"\"
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def delete(self, word: str) -> bool:
        \"\"\"Delete word from trie. O(m)\"\"\"
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
- Insert: O(m) time, O(m) space
- Search: O(m) time, O(1) space
- Prefix: O(m) time, O(1) space
- Space: O(ALPHABET_SIZE × N × M) worst case

---

### Problem: Implement Trie (LC 208) ⭐⭐⭐⭐⭐

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

---

### Problem: Word Search II (LC 212) ⭐⭐⭐⭐⭐

**Problem:** Find all words from dictionary in 2D board.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Store complete word

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
        
        # Found word
        if next_node.word:
            result.append(next_node.word)
            next_node.word = None  # Avoid duplicates
        
        # Mark visited
        board[r][c] = '#'
        
        # Explore neighbors
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, next_node)
        
        # Restore
        board[r][c] = char
        
        # Prune trie (optimization)
        if not next_node.children:
            del node.children[char]
    
    # Start DFS from each cell
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    
    return result
```

**Complexity:** O(M × N × 4^L) where L = max word length

**Key Optimization:** Prune trie nodes as words are found.

---

### Advanced: Autocomplete System

```python
class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.trie = {}
        self.current = self.trie
        self.current_sentence = ""
        
        # Build trie with frequencies
        for sentence, count in zip(sentences, times):
            self._add(sentence, count)
    
    def _add(self, sentence, count):
        node = self.trie
        for char in sentence:
            if char not in node:
                node[char] = {'#': {}}
            node = node[char]
        
        # Store frequency
        node['#']['count'] = node['#'].get('count', 0) + count
        node['#']['sentence'] = sentence
    
    def input(self, c: str) -> List[str]:
        if c == '#':
            # Save sentence
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
        
        # Collect all sentences with this prefix
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

## Part 2: Union Find (Disjoint Set Union)

**Interview Frequency:** ⭐⭐⭐⭐ (40% of Google interviews)  
**Google Frequency:** ⭐⭐⭐⭐⭐ (Graph connectivity, MST)  
**Mastery Time:** 3-4 hours

### What is Union Find?

**Union Find** tracks disjoint sets and supports:
- **Union:** Merge two sets
- **Find:** Determine which set an element belongs to
- **Connected:** Check if two elements are in same set

**Use Cases:**
- Network connectivity
- Kruskal's MST algorithm
- Cycle detection in undirected graphs
- Image processing (connected components)
- Social network friend groups

---

### Basic Implementation

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # Each node is its own parent
        self.rank = [1] * n           # Tree height for union by rank
        self.components = n           # Number of disjoint sets
    
    def find(self, x):
        \"\"\"Find root of x with path compression. O(α(n))\"\"\"
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        \"\"\"Union sets containing x and y. O(α(n))\"\"\"
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank: attach smaller tree to larger
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.rank[root_y] += self.rank[root_x]
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += self.rank[root_y]
        
        self.components -= 1
        return True
    
    def connected(self, x, y):
        \"\"\"Check if x and y are in same set. O(α(n))\"\"\"
        return self.find(x) == self.find(y)
    
    def count(self):
        \"\"\"Return number of disjoint sets. O(1)\"\"\"
        return self.components
```

**Complexity:** O(α(n)) ≈ O(1) amortized per operation, where α is inverse Ackermann function

**Why α(n)?**
- Path compression flattens tree
- Union by rank keeps trees balanced
- Combined: nearly constant time

---

### Problem: Number of Connected Components (LC 323) ⭐⭐⭐⭐⭐

```python
def countComponents(n: int, edges: List[List[int]]) -> int:
    uf = UnionFind(n)
    
    for a, b in edges:
        uf.union(a, b)
    
    return uf.count()
```

**Complexity:** O(E × α(V)) ≈ O(E)

---

### Problem: Redundant Connection (LC 684) ⭐⭐⭐⭐⭐

**Problem:** Find edge that creates cycle in undirected graph.

```python
def findRedundantConnection(edges: List[List[int]]) -> List[int]:
    uf = UnionFind(len(edges) + 1)
    
    for a, b in edges:
        # If already connected, this edge creates cycle
        if not uf.union(a, b):
            return [a, b]
    
    return []
```

**Complexity:** O(E × α(V))

---

### Problem: Number of Islands (LC 200) with Union Find

```python
def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    
    # Map 2D to 1D
    def index(r, c):
        return r * cols + c
    
    uf = UnionFind(rows * cols)
    
    # Count water cells to subtract
    water = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '0':
                water += 1
            else:
                # Connect to adjacent land cells
                for dr, dc in [(0,1), (1,0)]:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols and
                        grid[nr][nc] == '1'):
                        uf.union(index(r, c), index(nr, nc))
    
    return uf.count() - water
```

---

### Problem: Accounts Merge (LC 721) ⭐⭐⭐⭐⭐

**Problem:** Merge accounts with common emails.

```python
def accountsMerge(accounts: List[List[str]]) -> List[List[str]]:
    # Map email to account index
    email_to_id = {}
    uf = UnionFind(len(accounts))
    
    # Union accounts with common emails
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
    
    # Format result
    result = []
    for root, emails in root_to_emails.items():
        name = accounts[root][0]
        result.append([name] + sorted(emails))
    
    return result
```

**Complexity:** O(N × K × α(N)) where K = avg emails per account

---

### Advanced: Union Find with Size Tracking

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

---

## Comparison: When to Use What

| Problem Type | Trie | Union Find |
|-------------|------|------------|
| Prefix search | ✅ | ❌ |
| Autocomplete | ✅ | ❌ |
| Connected components | ❌ | ✅ |
| Cycle detection | ❌ | ✅ |
| String matching | ✅ | ❌ |
| Dynamic connectivity | ❌ | ✅ |

---

## Master Checklist

### Trie
- [ ] Implement basic Trie (insert, search, prefix)
- [ ] Solve Word Search II
- [ ] Understand space-time tradeoffs
- [ ] Handle deletion correctly
- [ ] Implement autocomplete

### Union Find
- [ ] Implement with path compression
- [ ] Implement with union by rank/size
- [ ] Detect cycles
- [ ] Count components
- [ ] Solve MST with Kruskal's

---

## Practice Problems

### Trie (8 problems)
1. LC 208 - Implement Trie ⭐⭐⭐⭐⭐
2. LC 212 - Word Search II ⭐⭐⭐⭐⭐
3. LC 211 - Add and Search Word ⭐⭐⭐⭐
4. LC 648 - Replace Words ⭐⭐⭐
5. LC 677 - Map Sum Pairs ⭐⭐⭐
6. LC 720 - Longest Word ⭐⭐⭐
7. LC 1804 - Implement Trie II ⭐⭐⭐⭐
8. LC 1268 - Search Suggestions ⭐⭐⭐⭐

### Union Find (10 problems)
1. LC 323 - Number of Components ⭐⭐⭐⭐⭐
2. LC 684 - Redundant Connection ⭐⭐⭐⭐⭐
3. LC 685 - Redundant Connection II ⭐⭐⭐⭐⭐
4. LC 547 - Number of Provinces ⭐⭐⭐⭐
5. LC 721 - Accounts Merge ⭐⭐⭐⭐⭐
6. LC 737 - Sentence Similarity II ⭐⭐⭐⭐
7. LC 990 - Satisfiability ⭐⭐⭐⭐
8. LC 1101 - Earliest Connection ⭐⭐⭐⭐
9. LC 1579 - Remove Max Edges ⭐⭐⭐⭐⭐
10. LC 1584 - Min Cost to Connect Points ⭐⭐⭐⭐⭐

**Total Time:** 6-8 hours combined

---

## Common Mistakes

### Trie
1. **Forgetting end marker**
   ```python
   # ❌ Wrong: "cat" in trie but searching "ca" returns True
   
   # ✅ Correct: Use is_end_of_word flag
   ```

2. **Not handling empty strings**

3. **Memory leaks from not pruning**

### Union Find
1. **Not using path compression**
   ```python
   # ❌ O(n) per find
   def find(self, x):
       while self.parent[x] != x:
           x = self.parent[x]
       return x
   
   # ✅ O(α(n)) per find
   def find(self, x):
       if self.parent[x] != x:
           self.parent[x] = self.find(self.parent[x])
       return self.parent[x]
   ```

2. **Forgetting to check if already connected**
   ```python
   def union(self, x, y):
       root_x, root_y = self.find(x), self.find(y)
       if root_x == root_y:
           return False  # Important!
       # ... rest of union
   ```

---

**Master these data structures for specialized problem domains!**
