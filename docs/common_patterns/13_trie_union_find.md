# Trie & Union Find

This chapter covers two specialized data structures. Neither is as general as a hash table or a balanced tree, but each does one job so well that it turns otherwise awkward problems into short, fast code:

- A **trie** stores a set of strings so that everything sharing a prefix shares storage and search effort. It answers prefix questions — "which words start with `pre`?" — in time proportional to the prefix, independent of how many words are stored.
- A **union-find** (disjoint set) structure maintains a partition of elements into groups under merging, answering "are these two in the same group?" in effectively constant time.

Both illustrate a recurring lesson of data structure design: when the obvious structures each make one of your operations fast and another slow, look for a structure that balances them.

---

## Part 1: Tries

### Why Another Dictionary?

Suppose you store a set of $n$ words and need to answer queries about a string $q$ of length $k$.

| Structure | Is $q$ a word? | Do any words start with $q$? | List words starting with $q$ |
|---|---|---|---|
| Hash set | $O(k)$ expected | $O(n \cdot k)$: check every word | $O(n \cdot k)$ |
| Sorted list + binary search | $O(k \log n)$ | $O(k \log n)$ | $O(k \log n + \text{output})$ |
| **Trie** | $O(k)$ | $O(k)$ | $O(k + \text{output size})$ |

A hash set is great at exact lookups but useless for prefixes: hashing scatters `car`, `card`, and `care` to unrelated buckets. A sorted list keeps words with a common prefix together, which is why it handles prefix queries — but every comparison costs up to $k$ character checks.

There's a subtler advantage too. Often queries arrive **incrementally**: first `c`, then `ca`, then `car`, each extending the last by one character (a user typing, a DFS extending a path on a board). A hash set must hash each new string from scratch, costing $O(k)$ per query. A trie just takes **one more step** from where the previous query ended: $O(1)$ per character.

### Structure

A trie is a tree in which each edge is labeled by a character, and the path from the root to a node spells out a string. Words with a common prefix share the path for that prefix and branch at their first differing character. Nodes that end a word are marked.

```text
             (root)
            /      \
           t        w
           |       / \
           h      a   h
           |      |   |
           e*     s*  e
          / \         |
         i   r        n*
         |   |
         r*  e*
                    words: the, their, there, was, when   (* = end of word)
```

Searching for $q$ walks down from the root following $q$'s characters. If an edge is missing, $q$ isn't in the set — and neither is any word with $q$ as a prefix. Otherwise, the search ends after exactly $|q|$ steps, no matter how many words are stored.

### Implementation (LC 208)

```python
class TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def _walk(self, s: str) -> TrieNode | None:
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

Each operation is $O(k)$ for a string of length $k$. Space is $O(\text{total characters inserted})$ in the worst case (no shared prefixes), and much less when prefixes overlap. A `dict` of children works for any alphabet; a fixed array of 26 slots is faster in compiled languages but wastes space on sparse nodes.

A compact alternative uses nested dictionaries directly, with a sentinel key marking word ends:

```python
def build_trie(words: list[str]) -> dict:
    root: dict = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w            # store the word itself: handy when you find it later
    return root
```

### Searching with Wildcards (LC 211)

When the query contains `.` (matches any single character), the walk branches: at a `.`, try every child. The trie still prunes aggressively — a branch dies the moment its prefix isn't present.

```python
class WordDictionary:
    def __init__(self) -> None:
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        def match(node: TrieNode, i: int) -> bool:
            if i == len(word):
                return node.is_word
            ch = word[i]
            if ch == ".":
                return any(match(child, i + 1) for child in node.children.values())
            child = node.children.get(ch)
            return child is not None and match(child, i + 1)

        return match(self.root, 0)
```

### Word Search II (LC 212): Walking a Trie and a Grid Together

Find all dictionary words that can be traced on a letter grid by moving between adjacent cells. The naive approach runs a separate board search for each word — hopeless for thousands of words.

The key insight is the incremental-query advantage from above. A DFS on the board extends its current path by **one letter at a time**, so walk the trie **in lockstep** with it. Each board step is one trie step, and the moment the path's prefix is absent from the trie, that entire branch of the board search is abandoned. One DFS from each cell finds *all* words at once.

```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    root = build_trie(words)
    rows, cols = len(board), len(board[0])
    found: list[str] = []

    def dfs(r: int, c: int, parent: dict) -> None:
        ch = board[r][c]
        node = parent[ch]
        if "$" in node:
            found.append(node.pop("$"))        # report once, then forget it
        board[r][c] = "#"                      # mark as used on this path
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] in node:
                dfs(nr, nc, node)
        board[r][c] = ch                       # backtrack
        if not node:
            parent.pop(ch)                     # prune: nothing left below this prefix

    for r in range(rows):
        for c in range(cols):
            if board[r][c] in root:
                dfs(r, c, root)
    return found
```

Two refinements make a big difference in practice: removing each word from the trie once it's found (so it isn't reported twice), and **pruning** trie nodes that have become empty, so later searches don't walk into exhausted branches.

!!! tip "Take-Home Lesson"
    A trie lets a search that grows one character at a time take one step per character, and it lets you abandon a search as soon as the current prefix leads nowhere. Whenever a backtracking search builds strings and checks them against a dictionary, drive the search with a trie.

### More Trie Applications

- **Autocomplete / Search Suggestions** (LC 1268): walk to the prefix's node, then DFS (in alphabetical child order) to collect completions. For heavy traffic, cache the top suggestions at each node.
- **Replace Words** (LC 648): for each word, walk the trie and stop at the first node marked as a root word.
- **Longest Word in Dictionary** (LC 720): a word counts only if every prefix is also a word — a DFS that only descends through word-ending nodes.
- **Binary tries for XOR** (LC 421): store numbers as 32-bit strings, most significant bit first. To maximize `x ^ y`, walk the trie from the top, at each level preferring the child with the **opposite** bit of `x` — a greedy choice that's correct because a higher bit outweighs all lower bits combined.

```python
def find_maximum_xor(nums: list[int]) -> int:
    bits = max(nums).bit_length()
    root: dict = {}
    for x in nums:                            # insert every number, high bit first
        node = root
        for i in range(bits - 1, -1, -1):
            node = node.setdefault((x >> i) & 1, {})
    best = 0
    for x in nums:                            # greedily take the opposite bit when possible
        node, cur = root, 0
        for i in range(bits - 1, -1, -1):
            b = (x >> i) & 1
            if 1 - b in node:
                cur |= 1 << i
                node = node[1 - b]
            else:
                node = node[b]
        best = max(best, cur)
    return best
```

### Suffix Tries: Every Substring Is a Prefix

A **suffix trie** stores all suffixes of a string $S$. Its magic is a simple observation: **every substring of $S$ is a prefix of some suffix**. So "is $q$ a substring of $S$?" becomes a walk of $|q|$ steps from the root.

The catch: $S$ has $n$ suffixes of average length $n/2$, so the naive suffix trie has $\Theta(n^2)$ nodes. **Suffix trees** compress each unbranching path into a single edge labeled by a pair of indices into $S$, which brings the size down to $O(n)$, and clever algorithms build them in linear time. **Suffix arrays** — the sorted list of suffix start positions — offer most of the same power in a simpler, more memory-friendly package. You'll rarely implement either in an interview, but knowing they exist is valuable: they turn many quadratic string problems (longest repeated substring, longest common substring of two strings) into linear or near-linear ones.

---

## Part 2: Union-Find

### Dynamic Connectivity

Many problems maintain a **partition** of elements into disjoint groups — connected components of a growing graph, accounts belonging to the same person, variables forced equal — and repeatedly ask two things:

- **Find:** which group is $x$ in? (Equivalently: are $x$ and $y$ in the same group?)
- **Union:** merge the groups containing $x$ and $y$.

The two obvious representations each make one operation fast and the other slow:

| Representation | Same group? | Merge two groups |
|---|---|---|
| Label array: `group[x]` | $O(1)$ | $O(n)$: relabel one group's elements |
| Graph of the merges, traversed on demand | $O(n)$: run BFS/DFS | $O(1)$: add an edge |
| **Union-find** | $O(\alpha(n))$ amortized | $O(\alpha(n))$ amortized |

### Backward Trees

Union-find represents each group as a tree in which every node points to its **parent**, and the root names the group. There are no child pointers at all — just one `parent` array.

- **Find($x$):** follow parent pointers from $x$ until reaching a root (a node that is its own parent).
- **Union($x$, $y$):** find both roots; if they differ, make one root point to the other.

Both cost $O(\text{height})$, so everything depends on keeping the trees short. Two simple rules do that.

**Union by size.** Always hang the **smaller** tree under the root of the larger one. Every node in the smaller tree gets one step deeper; nobody in the larger tree does. Why does this keep trees short? A node gets deeper only when its tree is merged into one at least as large — so its tree's size at least **doubles** every time the node's depth increases. A size can double at most $\log_2 n$ times, so every tree has height $O(\log n)$.

**Path compression.** During a find, after locating the root, repoint every node on the path directly at it. Future finds on those nodes take one step.

With both rules, a sequence of $m$ operations costs $O(m \cdot \alpha(n))$, where $\alpha$ is the **inverse Ackermann function** — which grows so slowly that $\alpha(n) \le 4$ for any $n$ that could fit in this universe. For all practical purposes, union-find operations are constant time.

```python
class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:            # path compression
            next_x = self.parent[x]
            self.parent[x] = root
            x = next_x
        return root

    def union(self, x: int, y: int) -> bool:
        """Merge the groups of x and y. Return False if they were already together."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.size[rx] < self.size[ry]:        # union by size
            rx, ry = ry, rx
        self.parent[ry] = rx
        self.size[rx] += self.size[ry]
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
```

`union` returning whether a merge happened is a small design choice that pays off constantly: "this edge connected two already-connected vertices" is exactly what cycle detection and Kruskal's algorithm need to know.

### Applications

#### Components and cycles

- **Number of Connected Components** (LC 323) and **Number of Provinces** (LC 547): union every edge; the answer is `components`.
- **Redundant Connection** (LC 684): a tree plus one extra edge. Process edges in order; the first edge whose `union` returns `False` closes a cycle.
- **Graph Valid Tree** (LC 261): exactly $n - 1$ edges, and no `union` fails.

```python
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    uf = UnionFind(len(edges) + 1)
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    return []
```

#### Grouping by shared keys: Accounts Merge (LC 721)

Accounts sharing any email belong to the same person. Rather than comparing accounts pairwise, union each account with the **first account that claimed each email**. Then gather emails by root.

```python
def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    uf = UnionFind(len(accounts))
    owner: dict[str, int] = {}
    for i, (_, *emails) in enumerate(accounts):
        for email in emails:
            if email in owner:
                uf.union(i, owner[email])
            else:
                owner[email] = i
    groups: dict[int, list[str]] = {}
    for email, i in owner.items():
        groups.setdefault(uf.find(i), []).append(email)
    return [[accounts[root][0], *sorted(emails)] for root, emails in groups.items()]
```

#### Equivalence constraints: Satisfiability of Equality Equations (LC 990)

Given constraints like `a==b` and `b!=c`, decide whether they can all hold. Equality is an equivalence relation, so union all `==` pairs first; then every `!=` pair must lie in different groups.

```python
def equations_possible(equations: list[str]) -> bool:
    uf = UnionFind(26)
    idx = lambda ch: ord(ch) - ord("a")
    for eq in equations:
        if eq[1] == "=":
            uf.union(idx(eq[0]), idx(eq[3]))
    return all(not uf.connected(idx(eq[0]), idx(eq[3])) for eq in equations if eq[1] == "!")
```

#### Kruskal's minimum spanning tree

Sort edges by weight and add each one whose endpoints are in different components — the union-find test is exactly "would this edge close a cycle?" See [Graphs](12_graphs.md#kruskals-algorithm).

#### Online connectivity: Number of Islands II (LC 305)

Land cells appear one at a time on a grid; after each addition, report the number of islands. Re-running a flood fill after each addition costs $O(mn)$ per step. With union-find, each new cell starts as its own island and unions with its land neighbors: $O(\alpha(mn))$ per step.

This is where union-find truly beats BFS/DFS: when **edges arrive over time** and connectivity questions are interleaved with them.

### Union-Find vs. Traversal

| Situation | Better tool |
|---|---|
| Static graph, count or label components once | Either; DFS/BFS is just as fast and needs no extra structure |
| Edges arrive incrementally; queries interleaved | **Union-find** |
| Need actual paths, distances, or traversal order | **BFS / DFS** |
| Need to **delete** edges or split groups | Neither directly — union-find can't split. If all operations are known in advance, process them **in reverse**, turning deletions into unions |
| Directed reachability | **DFS / BFS** (union-find is for symmetric relations) |

---

## Common Mistakes

### Tries

1. **Confusing "prefix exists" with "word exists."** `starts_with("app")` can be true while `search("app")` is false. The end-of-word flag is what distinguishes them.

2. **Rebuilding strings during DFS.** Concatenating `path + ch` at each step costs $O(k)$ per step. Store the full word at its terminal node (as `build_trie` does), or keep a list and join only when reporting.

3. **Reporting duplicates in Word Search II.** A word reachable by two board paths is found twice unless you remove it from the trie (or use a set).

4. **Forgetting memory cost.** A trie with a node object per character can use far more memory than a hash set of the same words. Use it when you need prefix operations.

### Union-Find

1. **Comparing elements instead of roots.** `parent[x] == parent[y]` is not the same-group test; `find(x) == find(y)` is.

2. **Skipping union by size (or rank) and path compression.** Without them, a sequence of unions can build a linked list, and finds degrade to $O(n)$.

3. **Unioning non-roots.** `parent[x] = y` links $x$'s node, not $x$'s whole tree. Always link `find(x)` to `find(y)`.

4. **Mapping labels to indices.** For string or coordinate elements, maintain a `dict` from element to index, or implement the parent map itself as a `dict`.

5. **Expecting deletions to work.** Union-find merges only. For splits, reverse time or use a different structure.

---

## Practice Problems

| Problem | Structure / idea |
|---|---|
| Implement Trie (LC 208) | Basic trie |
| Design Add and Search Words (LC 211) | Trie + DFS on wildcards |
| Word Search II (LC 212) | Trie driving a grid DFS, with pruning |
| Replace Words (LC 648) | Shortest root prefix |
| Search Suggestions System (LC 1268) | Trie + DFS, or sort + binary search |
| Maximum XOR of Two Numbers (LC 421) | Binary trie, greedy by bit |
| Number of Connected Components (LC 323) | Union-find |
| Number of Provinces (LC 547) | Union-find on an adjacency matrix |
| Redundant Connection (LC 684) | First failed union |
| Graph Valid Tree (LC 261) | $n - 1$ edges and no cycle |
| Accounts Merge (LC 721) | Union by shared email |
| Satisfiability of Equality Equations (LC 990) | Union `==`, check `!=` |
| Longest Consecutive Sequence (LC 128) | Union neighbors (or a hash set) |
| Number of Islands II (LC 305) | Online union-find on a grid |
| Min Cost to Connect All Points (LC 1584) | Kruskal with union-find |
