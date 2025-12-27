# Trees - Complete Mastery Guide

**Interview Frequency:** ⭐⭐⭐⭐⭐ (85% of Google interviews)  
**Google Frequency:** ⭐⭐⭐⭐⭐ (Multiple tree problems in single interview)  
**Mastery Time:** 8-10 hours

## Why Trees are Google's Favorite

Trees appear everywhere at Google:
- File systems and directory structures
- DOM manipulation
- Database indexing (B-trees, B+ trees)
- Compiler expression trees
- Decision trees in ML

Trees test:
- **Recursion mastery** - most elegant solutions are recursive
- **Multiple traversal methods** - 6+ ways to traverse
- **Edge case handling** - null nodes, single nodes, skewed trees
- **Space-time tradeoffs** - recursive vs iterative

---

## Tree Fundamentals

### Binary Tree Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Tree Terminology

- **Root:** Top node with no parent
- **Leaf:** Node with no children
- **Height:** Longest path from node to leaf
- **Depth:** Path length from root to node
- **Level:** All nodes at same depth
- **Balanced:** Left and right subtree heights differ by at most 1

### Tree Types

**Binary Tree:** Each node has at most 2 children

**Binary Search Tree (BST):**
- Left subtree values < root
- Right subtree values > root
- All subtrees are also BSTs

**Complete Binary Tree:** All levels filled except possibly last, filled left-to-right

**Full Binary Tree:** Every node has 0 or 2 children

**Perfect Binary Tree:** All internal nodes have 2 children, all leaves at same level

---

## Pattern 1: Tree Traversals

### DFS Traversals (Recursive)

**Preorder: Root → Left → Right**
```python
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def preorder_iterative(root):
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Push right first (so left is processed first)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result
```

**Inorder: Left → Root → Right** (BST gives sorted order)
```python
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def inorder_iterative(root):
    result = []
    stack = []
    current = root
    
    while stack or current:
        # Go to leftmost node
        while current:
            stack.append(current)
            current = current.left
        
        # Process node
        current = stack.pop()
        result.append(current.val)
        
        # Move to right subtree
        current = current.right
    
    return result
```

**Postorder: Left → Right → Root**
```python
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]

def postorder_iterative(root):
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Push left first (so right is processed first)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    
    return result[::-1]  # Reverse for postorder
```

**Level Order (BFS):**
```python
from collections import deque

def levelOrder(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

**Complexity:** All traversals are O(n) time, O(h) space for recursive (O(n) worst case)

---

## Pattern 2: Tree Depth/Height Problems

### Maximum Depth (LC 104) ⭐⭐⭐⭐⭐

```python
def maxDepth(root: TreeNode) -> int:
    if not root:
        return 0
    
    left_depth = maxDepth(root.left)
    right_depth = maxDepth(root.right)
    
    return 1 + max(left_depth, right_depth)

# Iterative (BFS)
def maxDepth_iterative(root: TreeNode) -> int:
    if not root:
        return 0
    
    queue = deque([(root, 1)])
    max_depth = 0
    
    while queue:
        node, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    
    return max_depth
```

**Complexity:** O(n) time, O(h) space

---

### Diameter of Binary Tree (LC 543) ⭐⭐⭐⭐⭐

**Problem:** Longest path between any two nodes (may not pass through root).

```python
def diameterOfBinaryTree(root: TreeNode) -> int:
    diameter = 0
    
    def height(node):
        nonlocal diameter
        
        if not node:
            return 0
        
        left_height = height(node.left)
        right_height = height(node.right)
        
        # Update diameter: path through this node
        diameter = max(diameter, left_height + right_height)
        
        # Return height for parent
        return 1 + max(left_height, right_height)
    
    height(root)
    return diameter
```

**Key Pattern:** Use helper function to track global state while returning local result.

**Complexity:** O(n) time, O(h) space

---

## Pattern 3: Path Problems

### Path Sum (LC 112, 113, 437)

**LC 112: Has Path Sum**
```python
def hasPathSum(root: TreeNode, targetSum: int) -> bool:
    if not root:
        return False
    
    # Leaf node check
    if not root.left and not root.right:
        return root.val == targetSum
    
    # Recursively check subtrees
    remaining = targetSum - root.val
    return (hasPathSum(root.left, remaining) or 
            hasPathSum(root.right, remaining))
```

**LC 113: All Paths with Sum**
```python
def pathSum(root: TreeNode, targetSum: int) -> List[List[int]]:
    result = []
    
    def dfs(node, remaining, path):
        if not node:
            return
        
        path.append(node.val)
        
        # Leaf node with target sum
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])  # Deep copy
        else:
            dfs(node.left, remaining - node.val, path)
            dfs(node.right, remaining - node.val, path)
        
        path.pop()  # Backtrack
    
    dfs(root, targetSum, [])
    return result
```

**LC 437: Path Sum III (not just root-to-leaf)**
```python
def pathSum(root: TreeNode, targetSum: int) -> int:
    # Prefix sum approach
    prefix_sum = {0: 1}  # sum -> count
    
    def dfs(node, curr_sum):
        if not node:
            return 0
        
        curr_sum += node.val
        count = prefix_sum.get(curr_sum - targetSum, 0)
        
        prefix_sum[curr_sum] = prefix_sum.get(curr_sum, 0) + 1
        
        count += dfs(node.left, curr_sum)
        count += dfs(node.right, curr_sum)
        
        prefix_sum[curr_sum] -= 1  # Backtrack
        
        return count
    
    return dfs(root, 0)
```

**Complexity:** O(n) time, O(n) space

---

## Pattern 4: Tree Construction

### Build Tree from Traversals

**LC 105: Preorder + Inorder**
```python
def buildTree(preorder: List[int], inorder: List[int]) -> TreeNode:
    if not preorder:
        return None
    
    # First element in preorder is root
    root_val = preorder[0]
    root = TreeNode(root_val)
    
    # Find root in inorder to split left/right
    mid = inorder.index(root_val)
    
    # Recursively build subtrees
    root.left = buildTree(preorder[1:mid+1], inorder[:mid])
    root.right = buildTree(preorder[mid+1:], inorder[mid+1:])
    
    return root
```

**Optimized with HashMap:**
```python
def buildTree(preorder: List[int], inorder: List[int]) -> TreeNode:
    inorder_map = {val: i for i, val in enumerate(inorder)}
    pre_idx = 0
    
    def build(left, right):
        nonlocal pre_idx
        
        if left > right:
            return None
        
        root_val = preorder[pre_idx]
        root = TreeNode(root_val)
        pre_idx += 1
        
        mid = inorder_map[root_val]
        
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        
        return root
    
    return build(0, len(inorder) - 1)
```

**Complexity:** O(n) time and space

---

## Pattern 5: Binary Search Tree Operations

### Validate BST (LC 98) ⭐⭐⭐⭐⭐

```python
def isValidBST(root: TreeNode) -> bool:
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        # Current node must be in range
        if not (min_val < node.val < max_val):
            return False
        
        # Check left subtree (max becomes current)
        # Check right subtree (min becomes current)
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))
```

**Inorder Approach (must be sorted):**
```python
def isValidBST(root: TreeNode) -> bool:
    prev = float('-inf')
    
    def inorder(node):
        nonlocal prev
        
        if not node:
            return True
        
        if not inorder(node.left):
            return False
        
        if node.val <= prev:
            return False
        prev = node.val
        
        return inorder(node.right)
    
    return inorder(root)
```

---

### Kth Smallest in BST (LC 230) ⭐⭐⭐⭐

```python
def kthSmallest(root: TreeNode, k: int) -> int:
    # Inorder traversal gives sorted order
    count = 0
    result = None
    
    def inorder(node):
        nonlocal count, result
        
        if not node or result is not None:
            return
        
        inorder(node.left)
        
        count += 1
        if count == k:
            result = node.val
            return
        
        inorder(node.right)
    
    inorder(root)
    return result
```

**Iterative:**
```python
def kthSmallest(root: TreeNode, k: int) -> int:
    stack = []
    current = root
    count = 0
    
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        count += 1
        
        if count == k:
            return current.val
        
        current = current.right
```

---

## Pattern 6: Lowest Common Ancestor

### LCA in Binary Tree (LC 236) ⭐⭐⭐⭐⭐

```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    # Base case
    if not root or root == p or root == q:
        return root
    
    # Search in subtrees
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    # If both found in different subtrees, root is LCA
    if left and right:
        return root
    
    # Return the non-null one
    return left if left else right
```

**LCA in BST (LC 235):**
```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    while root:
        # Both in left subtree
        if p.val < root.val and q.val < root.val:
            root = root.left
        # Both in right subtree
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            # Split point is LCA
            return root
```

**Complexity:** O(n) for binary tree, O(h) for BST

---

## Pattern 7: Serialize/Deserialize

### Serialize and Deserialize Binary Tree (LC 297) ⭐⭐⭐⭐⭐

```python
class Codec:
    def serialize(self, root):
        \"\"\"Encodes a tree to a single string.\"\"\"
        if not root:
            return "null"
        
        return (str(root.val) + "," + 
                self.serialize(root.left) + "," +
                self.serialize(root.right))
    
    def deserialize(self, data):
        \"\"\"Decodes your encoded data to tree.\"\"\"
        def build(vals):
            val = next(vals)
            
            if val == "null":
                return None
            
            node = TreeNode(int(val))
            node.left = build(vals)
            node.right = build(vals)
            
            return node
        
        vals = iter(data.split(","))
        return build(vals)
```

**BFS Approach:**
```python
class Codec:
    def serialize(self, root):
        if not root:
            return ""
        
        queue = deque([root])
        result = []
        
        while queue:
            node = queue.popleft()
            
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
        
        return ",".join(result)
    
    def deserialize(self, data):
        if not data:
            return None
        
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        queue = deque([root])
        i = 1
        
        while queue:
            node = queue.popleft()
            
            if vals[i] != "null":
                node.left = TreeNode(int(vals[i]))
                queue.append(node.left)
            i += 1
            
            if vals[i] != "null":
                node.right = TreeNode(int(vals[i]))
                queue.append(node.right)
            i += 1
        
        return root
```

---

## Google Interview Patterns

### 1. Tree Modification

**Invert Binary Tree (LC 226)** - Asked in Google phone screen
```python
def invertTree(root: TreeNode) -> TreeNode:
    if not root:
        return None
    
    # Swap children
    root.left, root.right = root.right, root.left
    
    # Recursively invert subtrees
    invertTree(root.left)
    invertTree(root.right)
    
    return root
```

### 2. Level-Order Variations

**Zigzag Level Order (LC 103)**
```python
def zigzagLevelOrder(root: TreeNode) -> List[List[int]]:
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        if not left_to_right:
            level.reverse()
        
        result.append(level)
        left_to_right = not left_to_right
    
    return result
```

---

## Master Checklist

### Fundamental Skills
- [ ] All 4 DFS traversals (recursive & iterative)
- [ ] BFS level-order traversal
- [ ] Calculate height/depth
- [ ] Validate BST
- [ ] Find LCA

### Advanced Skills
- [ ] Serialize/deserialize
- [ ] Build tree from traversals
- [ ] Path problems (all variants)
- [ ] BST operations (search, insert, delete)
- [ ] Tree to linked list conversion

### Pattern Recognition
- [ ] "Maximum/minimum path" → DFS with global variable
- [ ] "All paths" → DFS with backtracking
- [ ] "Level by level" → BFS
- [ ] "Is valid BST" → Inorder or min/max bounds
- [ ] "Lowest common ancestor" → Bottom-up DFS

---

## Practice Roadmap

### Week 1: Basics (15 problems)
- LC 104, 111, 543 (Height/depth)
- LC 226, 101, 572 (Tree structure)
- LC 94, 144, 145 (Traversals)
- LC 102, 103, 107 (Level order)

### Week 2: Advanced (15 problems)
- LC 98, 230, 235 (BST operations)
- LC 236, 1644 (LCA)
- LC 105, 106 (Tree construction)
- LC 112, 113, 437 (Path problems)
- LC 297 (Serialize)

**Total:** ~8-10 hours

---

## Common Mistakes

1. **Forgetting null checks**
   ```python
   # ❌ Wrong
   if node.left:
       process(node.left.val)
   
   # ✅ Correct
   if node and node.left:
       process(node.left.val)
   ```

2. **Not handling single-node trees**
   - Always test with `TreeNode(5)` (no children)

3. **Modifying tree during traversal**
   - Be careful when asked to modify in-place

4. **Stack overflow on deep trees**
   - Consider iterative for production code

5. **Forgetting to backtrack**
   - In path problems, pop after recursion

---

## Time Complexity Reference

| Operation | Time | Space |
|-----------|------|-------|
| Traversal (any) | O(n) | O(h) recursive, O(n) iterative |
| Search (BST) | O(h) | O(h) |
| Height | O(n) | O(h) |
| LCA | O(n) | O(h) |
| Level Order | O(n) | O(n) |

Where h = height (O(log n) balanced, O(n) worst case)

---

**Master trees, and you'll ace 85% of Google interviews!**
