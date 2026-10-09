# Trees

Trees model **hierarchy**: a family tree, a file system, an organization chart, the parse of an expression, the decisions of a search. Whenever a problem talks about ancestors and descendants, parents and children, containment or dominance, there is probably a tree in it.

But the real reason trees deserve careful study is that they are the purest example of a **recursive object**. A binary tree is either empty, or a root together with two smaller binary trees. Almost every tree algorithm is written by trusting that definition: solve the problem for the two subtrees, then combine. If you become fluent at that one move, the vast majority of tree problems become short exercises.

---

## Recursion Is Induction

Recursion can feel like magic the first time you see it: the function calls itself on a smaller input and somehow gets the right answer. Mathematical induction can feel the same way: you assume the claim for smaller cases and somehow prove it for the general one. They feel alike because **they are the same thing**. A recursive function is correct if:

1. **Base case:** it returns the right answer on the smallest inputs (the empty tree, a leaf).
2. **Inductive step:** *assuming* the recursive calls return correct answers for the subtrees, the function combines them into the correct answer for the whole tree.

That's the entire method. You never trace the recursion all the way down; you trust the recursive calls exactly the way an inductive proof trusts the induction hypothesis.

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TreeNode:
    val: int = 0
    left: TreeNode | None = None
    right: TreeNode | None = None


def max_depth(root: TreeNode | None) -> int:
    """LC 104. Base: the empty tree has depth 0. Step: 1 + the deeper subtree."""
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

!!! tip "Take-Home Lesson"
    To write a tree function, answer two questions: *what should it return for an empty tree?* and *given correct answers for the left and right subtrees, how do I build the answer for the whole tree?* Don't trace the recursion; trust it.

### Strengthening the hypothesis

Sometimes the answers from the subtrees aren't *enough* to build the answer for the tree. Then the fix is the same as in an induction proof that gets stuck: **prove something stronger**. Make the recursive function return more information than the problem asked for.

**Balanced Binary Tree (LC 110).** A tree is height-balanced if every node's subtrees differ in height by at most one. The definition transcribes directly:

```python
def is_balanced_naive(root: TreeNode | None) -> bool:
    if root is None:
        return True
    return (abs(max_depth(root.left) - max_depth(root.right)) <= 1
            and is_balanced_naive(root.left) and is_balanced_naive(root.right))
```

It's correct, but every node recomputes the heights of its whole subtree, which is $O(n^2)$ on a path-shaped tree. The trouble is that the recursive call answers only "is this subtree balanced?", and the parent also needs its height. So return both. A convenient encoding returns the height, or $-1$ for "unbalanced":

```python
def is_balanced(root: TreeNode | None) -> bool:
    def height(node: TreeNode | None) -> int:
        """Height of node's subtree, or -1 if it isn't balanced."""
        if node is None:
            return 0
        lh, rh = height(node.left), height(node.right)
        if lh < 0 or rh < 0 or abs(lh - rh) > 1:
            return -1
        return 1 + max(lh, rh)

    return height(root) >= 0
```

The strengthened version is one pass, $O(n)$.

**Diameter of Binary Tree (LC 543).** The longest path between any two nodes either passes through the root or lies entirely inside one subtree. If it passes through a node, it's the deepest path down the left plus the deepest path down the right. So the recursive function returns **depth** (what the parent needs) while recording the best **diameter** seen (what the problem asks for):

```python
def diameter_of_binary_tree(root: TreeNode | None) -> int:
    best = 0

    def depth(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left, right = depth(node.left), depth(node.right)
        best = max(best, left + right)       # longest path bending at this node
        return 1 + max(left, right)          # longest path going down from here

    depth(root)
    return best
```

**Binary Tree Maximum Path Sum (LC 124)** has exactly the same shape, with sums instead of lengths — and one twist: a branch with a negative sum should be dropped, so each child contributes `max(0, gain)`.

```python
def max_path_sum(root: TreeNode) -> int:
    best = root.val

    def gain(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = max(0, gain(node.left))
        right = max(0, gain(node.right))
        best = max(best, node.val + left + right)   # path bending here
        return node.val + max(left, right)          # path continuing to the parent

    gain(root)
    return best
```

This **"return one thing, record another"** pattern is the single most important idea for hard tree problems. The value returned to the parent must describe a path that can be *extended* upward (so it can use only one branch); the value recorded globally can *bend* at the current node.

---

## Traversals

Visiting every node is the foundation of everything else. The three depth-first orders differ only in *when* the node itself is processed relative to its subtrees:

| Order | Sequence | Typical use |
|---|---|---|
| **Pre-order** | node, left, right | Copying or serializing a tree; top-down propagation |
| **In-order** | left, node, right | BST in sorted order |
| **Post-order** | left, right, node | Anything needing both subtrees' answers first: height, deletion, evaluation |

```python
def inorder(root: TreeNode | None) -> list[int]:
    out: list[int] = []

    def visit(node: TreeNode | None) -> None:
        if node:
            visit(node.left)
            out.append(node.val)       # move this line up for pre-order, down for post-order
            visit(node.right)

    visit(root)
    return out
```

All three are $O(n)$ time and $O(h)$ space for the recursion stack, where $h$ is the height.

### Iterative traversals

Recursion uses the call stack implicitly; an explicit stack does the same job and avoids Python's recursion limit on deep trees. Pre-order is simplest — push the right child before the left so the left is processed first:

```python
def preorder_iter(root: TreeNode | None) -> list[int]:
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out
```

In-order must first dive left as far as possible, remembering the path, then process and turn right:

```python
def inorder_iter(root: TreeNode | None) -> list[int]:
    out: list[int] = []
    stack: list[TreeNode] = []
    node = root
    while node or stack:
        while node:                   # dive left, remembering the path
            stack.append(node)
            node = node.left
        node = stack.pop()            # leftmost unvisited node
        out.append(node.val)
        node = node.right             # then its right subtree
    return out
```

Post-order is easiest as "reverse of a modified pre-order": visit node, right, left, then reverse the output.

(Morris traversal achieves $O(1)$ extra space by temporarily threading right pointers back to ancestors. It's clever, rarely necessary, and modifies the tree during the walk.)

### Level-Order Traversal (BFS)

Visiting nodes level by level uses a **queue** instead of a stack. Processing the queue in batches — one batch per level — gives per-level results:

```python
from collections import deque


def level_order(root: TreeNode | None) -> list[list[int]]:
    """LC 102."""
    if root is None:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):          # exactly the nodes of this level
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels
```

Many problems are one-line variations: the **right side view** (LC 199) is the last element of each level; **zigzag** order (LC 103) reverses every other level; **minimum depth** (LC 111) is the level of the first leaf BFS reaches — and BFS finds it without exploring deeper levels, which DFS can't promise.

---

## Top-Down vs. Bottom-Up

There are two ways to move information through a tree recursion, and recognizing which one a problem needs is half the solution.

**Top-down (pre-order):** pass information **down** as arguments — the depth so far, the sum so far, the allowed range of values. Each node receives context from its ancestors.

```python
def has_path_sum(root: TreeNode | None, target: int) -> bool:
    """LC 112: is there a root-to-leaf path summing to target?"""
    if root is None:
        return False
    remaining = target - root.val
    if root.left is None and root.right is None:
        return remaining == 0
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)
```

**Bottom-up (post-order):** return information **up** as results — height, subtree size, subtree sum, "is this subtree valid." Each node combines what its children report. `max_depth`, `is_balanced`, and `diameter` above are all bottom-up.

Some problems need both: pass the running state down, and collect results as the recursion unwinds. **Path Sum II** (LC 113) passes the current path down, appends at each node, and **undoes** the append on the way back up — the backtracking pattern (see [Combinatorial Search](14_combinatorial_search.md)).

**Path Sum III** (LC 437) counts downward paths (not necessarily from the root) summing to a target. Along any root-to-node path, this is exactly "count subarrays with sum $k$" — so it's solved with the prefix-sum-plus-hash-map idea from [Two Pointers & Sliding Window](04_two_pointers_sliding_window.md#prefix-sums), passing the prefix counts down and removing each prefix as the recursion leaves its node:

```python
def path_sum_iii(root: TreeNode | None, target: int) -> int:
    counts = {0: 1}                     # prefix sums on the current root-to-node path

    def dfs(node: TreeNode | None, prefix: int) -> int:
        if node is None:
            return 0
        prefix += node.val
        found = counts.get(prefix - target, 0)
        counts[prefix] = counts.get(prefix, 0) + 1
        found += dfs(node.left, prefix) + dfs(node.right, prefix)
        counts[prefix] -= 1             # leaving this node: its prefix is no longer on the path
        return found

    return dfs(root, 0)
```

---

## Binary Search Trees

Sorted arrays offer fast search ($O(\log n)$ by binary search) but slow updates ($O(n)$ to shift elements). Linked lists offer fast updates but slow search. Binary search needs quick access to the element in the middle of the remaining range — and a **binary search tree** provides it by storing the median of each range at the top, as a linked structure with two pointers per node.

> **BST property:** for every node $x$, all keys in $x$'s left subtree are less than $x$, and all keys in its right subtree are greater.

Note the word *all*. It's not enough for each node to be bigger than its left child: every key in the entire left subtree must be smaller.

### Search, minimum, successor

Search compares the key with the root and descends into the only subtree that could contain it. The minimum is the leftmost node; the maximum is the rightmost. All take $O(h)$.

```python
def search_bst(root: TreeNode | None, key: int) -> TreeNode | None:
    node = root
    while node and node.val != key:
        node = node.left if key < node.val else node.right
    return node


def insert_bst(root: TreeNode | None, key: int) -> TreeNode:
    """Insert where an unsuccessful search for key falls off the tree."""
    if root is None:
        return TreeNode(key)
    if key < root.val:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root
```

An **in-order traversal of a BST visits keys in sorted order** — this follows directly from the BST property, by induction. It makes the $k$-th smallest element (LC 230) an in-order traversal that stops after $k$ nodes, and validation a check that the in-order sequence is strictly increasing.

### Validation (LC 98)

The classic bug is to check only that each node is between its two children. That misses violations deeper down:

```text
      5
     / \
    1   6        each node is fine relative to its children,
       / \       but 3 is in 5's RIGHT subtree and 3 < 5
      3   7
```

The fix is to pass **bounds** down (top-down): every node in the right subtree of 5 must be greater than 5.

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    def valid(node: TreeNode | None, lo: float, hi: float) -> bool:
        if node is None:
            return True
        if not lo < node.val < hi:
            return False
        return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)

    return valid(root, float("-inf"), float("inf"))
```

### Deletion (LC 450)

Deleting a node has three cases:

1. **No children:** just remove it.
2. **One child:** replace it with that child. The child's subtree already sits entirely on the correct side of the parent, so the BST property survives.
3. **Two children:** the tricky case. Replace the node's key with its **in-order successor** — the smallest key in its right subtree, which is the leftmost node there. That successor has no left child, so deleting it from the right subtree falls into case 1 or 2.

```python
def delete_node(root: TreeNode | None, key: int) -> TreeNode | None:
    if root is None:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = delete_node(root.right, successor.val)
    return root
```

### How good are binary search trees?

Every operation costs $O(h)$. The height $h$ ranges from $\log_2 n$ (perfectly balanced) to $n$ (a path) — and which one you get depends entirely on the **insertion order**, which the data structure doesn't control. Insert keys in sorted order, a very common situation, and each new key becomes the right child of the previous one: the BST degenerates into a linked list with $O(n)$ operations.

If the keys arrive in **random** order, the tree is good: the average depth of a node is about $2 \ln n \approx 1.39 \log_2 n$ — only 39% more than in a perfectly balanced tree — and the height is $O(\log n)$ with high probability. (The analysis is the same as for randomized quicksort: the root of a random BST plays the role of the first pivot.) But "random order" is an assumption about the user, not a guarantee.

**Balanced search trees** (AVL trees, red–black trees, B-trees, skip lists) restructure themselves slightly on each update to guarantee $h = O(\log n)$, so every operation is $O(\log n)$ in the worst case. You should know they exist and what they guarantee; you will almost never need to implement one. For algorithm analysis, assume a balanced tree is available as a black box.

!!! note "Balanced trees in Python"
    Python has no balanced BST in its standard library. The usual substitutes: `bisect` on a sorted list (fast search, $O(n)$ insert — often fine in practice because the shifting is a fast `memmove`), `heapq` if you only need the minimum, or the third-party `sortedcontainers.SortedList` ($O(\log n)$-ish everything), which LeetCode makes available.

!!! tip "Take-Home Lesson"
    Picking the *wrong* data structure can be disastrous — an unbalanced BST on sorted input is a linked list in disguise. Picking the *very best* one is usually less critical, because several good choices perform similarly. Aim first to avoid the disaster.

??? question "Stop and Think: Sorting with a search tree"
    **Problem:** You have a balanced BST supporting insert, delete, search, minimum, maximum, successor, and predecessor, each in $O(\log n)$. How can you sort $n$ numbers in $O(n \log n)$ using only (a) insert and in-order traversal? (b) minimum, successor, and insert? (c) minimum, insert, and delete?

    **Solution:** Every version begins by inserting all $n$ items: $O(n \log n)$. Then:

    - (a) An in-order traversal lists the keys in sorted order: $O(n)$.
    - (b) Start at the minimum and call successor $n - 1$ times: $O(n \log n)$.
    - (c) Repeatedly find and delete the minimum: $O(n \log n)$. This is heapsort's strategy, with a tree standing in for the heap.

    In every case, building the structure is the bottleneck. And (c) shows that a balanced BST can do everything a priority queue can.

---

## Lowest Common Ancestor

The **lowest common ancestor** (LCA) of nodes $p$ and $q$ is the deepest node that has both of them as descendants (a node counts as its own descendant).

**In a BST (LC 235)**, the BST property steers the search. If both $p$ and $q$ are smaller than the current node, the LCA is in the left subtree; if both are larger, it's in the right. Otherwise they split here (or one of them *is* here), so this is the LCA.

```python
def lca_bst(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    node = root
    while True:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node
```

**In a general binary tree (LC 236)**, there are no values to steer by, so ask each subtree bottom-up: *does it contain $p$ or $q$?* The recursive function returns $p$ or $q$ if it finds one, the LCA if it finds both, and `None` otherwise.

```python
def lca(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    if root is None or root is p or root is q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:           # p and q found in different subtrees: we're the split point
        return root
    return left or right         # pass up whichever was found (or None)
```

Why is it correct when $p$ is an ancestor of $q$? The recursion returns $p$ as soon as it reaches $p$, without looking for $q$ below it. That's the right answer: $q$ is guaranteed to exist in the tree, and if it isn't found elsewhere, it must be under $p$.

---

## Building and Serializing Trees

### Why one traversal isn't enough

The pre-order sequence `[1, 2, 3]` could come from five different three-node trees. A single traversal loses the shape. Two traversals can pin it down: **pre-order + in-order** determine a binary tree with distinct values uniquely. Pre-order tells you the root (its first element); finding that root in the in-order sequence splits everything else into the left and right subtrees (LC 105).

```python
def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    index = {v: i for i, v in enumerate(inorder)}
    next_pre = 0

    def build(lo: int, hi: int) -> TreeNode | None:
        """Build the subtree whose in-order values are inorder[lo:hi]."""
        nonlocal next_pre
        if lo >= hi:
            return None
        root = TreeNode(preorder[next_pre])
        next_pre += 1
        mid = index[root.val]
        root.left = build(lo, mid)          # left subtree comes next in pre-order
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(inorder))
```

The hash map avoids an $O(n)$ search for each root, making the whole construction $O(n)$. (Pre-order + post-order is *not* enough in general: a node with a single child can't tell whether it's a left or right child.)

### Serialization (LC 297)

To write a tree to a string and read it back, a single traversal *is* enough — if you also record the **empty subtrees**. With null markers, the pre-order sequence describes the shape completely:

```python
def serialize(root: TreeNode | None) -> str:
    out: list[str] = []

    def walk(node: TreeNode | None) -> None:
        if node is None:
            out.append("#")
            return
        out.append(str(node.val))
        walk(node.left)
        walk(node.right)

    walk(root)
    return ",".join(out)


def deserialize(data: str) -> TreeNode | None:
    tokens = iter(data.split(","))

    def build() -> TreeNode | None:
        tok = next(tokens)
        if tok == "#":
            return None
        node = TreeNode(int(tok))
        node.left = build()
        node.right = build()
        return node

    return build()
```

The deserializer reads tokens in exactly the order the serializer wrote them, so no indices or lengths are needed. Serialization also gives a neat solution for finding duplicate subtrees (LC 652): two subtrees are identical exactly when their serializations are equal.

---

## Common Mistakes

1. **Checking only immediate children for BST validity.** Pass bounds down, or check that the in-order sequence is strictly increasing.

2. **Recomputing heights at every node.** Calling `max_depth` inside another recursion makes the algorithm $O(n^2)$ on skewed trees. Return the height alongside the other result.

3. **Confusing "returned" and "recorded" values.** In diameter and max-path-sum problems, the parent can only extend a one-branch path; the bent path through a node is a candidate answer, not a return value.

4. **Forgetting the backtracking step.** When passing a mutable path or counter down, undo the change after the recursive calls return.

5. **Leaf vs. `None` confusion.** "Root-to-leaf" means stopping at nodes with no children, not at `None` — otherwise a node with one child counts as a path end.

6. **Deep recursion.** A 10⁵-node skewed tree exceeds Python's default recursion limit. Use an explicit stack or BFS when depth can be large.

7. **Assuming a BST is balanced.** $O(\log n)$ holds only for balanced trees. Sorted insertions produce $O(n)$ height.

---

## Practice Problems

| Problem | Idea |
|---|---|
| Maximum Depth of Binary Tree (LC 104) | Bottom-up height |
| Invert Binary Tree (LC 226) | Swap children recursively |
| Same Tree (LC 100) / Subtree of Another Tree (LC 572) | Simultaneous recursion |
| Binary Tree Level Order Traversal (LC 102) | BFS in batches |
| Binary Tree Right Side View (LC 199) | Last node per level |
| Balanced Binary Tree (LC 110) | Return height or −1 |
| Diameter of Binary Tree (LC 543) | Return depth, record diameter |
| Binary Tree Maximum Path Sum (LC 124) | Return gain, record bent path |
| Path Sum II (LC 113) | Top-down with backtracking |
| Path Sum III (LC 437) | Prefix sums on the root path |
| Validate Binary Search Tree (LC 98) | Bounds passed down |
| Kth Smallest Element in a BST (LC 230) | In-order, stop at $k$ |
| Delete Node in a BST (LC 450) | Successor replacement |
| Lowest Common Ancestor of a BST (LC 235) | Steer by values |
| Lowest Common Ancestor of a Binary Tree (LC 236) | Bottom-up search |
| Construct Tree from Preorder and Inorder (LC 105) | Root from pre-order, split by in-order |
| Serialize and Deserialize Binary Tree (LC 297) | Pre-order with null markers |
| Count Good Nodes in Binary Tree (LC 1448) | Top-down running max |
