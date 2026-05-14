# Trees

## Fundamentals

### Binary Tree Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Terminology

- **Root:** Top node with no parent
- **Leaf:** Node with no children
- **Height:** Longest path from node to leaf
- **Depth:** Path length from root to node
- **Level:** All nodes at same depth
- **Balanced:** Left and right subtree heights differ by at most 1

### Tree Types

- **Binary Tree:** Each node has at most 2 children
- **Binary Search Tree (BST):** Left subtree values < root < right subtree values, recursively
- **Complete Binary Tree:** All levels filled except possibly last, filled left-to-right
- **Full Binary Tree:** Every node has 0 or 2 children
- **Perfect Binary Tree:** All internal nodes have 2 children, all leaves at same level

---

## Pattern 1: Traversals

### DFS Traversals (Recursive + Iterative)

**Preorder: Root -> Left -> Right**
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
        
        # Push right first so left is processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result
```

**Inorder: Left -> Root -> Right** (BST gives sorted order)
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
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        result.append(current.val)
        current = current.right
    
    return result
```

**Postorder: Left -> Right -> Root**
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

**Complexity:** All traversals are O(n) time, O(h) space for recursive (O(n) worst case for skewed trees).

---

## Pattern 2: Depth / Height Problems

### Maximum Depth (LC 104)

```python
def maxDepth(root: TreeNode) -> int:
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

**Time:** O(n) | **Space:** O(h)

### Diameter of Binary Tree (LC 543)

Longest path between any two nodes (may not pass through root).

```python
def diameterOfBinaryTree(root: TreeNode) -> int:
    diameter = 0
    
    def height(node):
        nonlocal diameter
        if not node:
            return 0
        
        left_height = height(node.left)
        right_height = height(node.right)
        
        diameter = max(diameter, left_height + right_height)
        return 1 + max(left_height, right_height)
    
    height(root)
    return diameter
```

**Time:** O(n) | **Space:** O(h)

**Key pattern:** Helper returns local result (height) while updating global state (diameter).

### Balanced Binary Tree (LC 110)

Check if height of left and right subtrees differ by at most 1, for every node. Bottom-up O(n) approach avoids redundant height calculations.

```python
def isBalanced(root: TreeNode) -> bool:
    def check(node):
        """Returns height if balanced, -1 if not."""
        if not node:
            return 0
        
        left = check(node.left)
        if left == -1:
            return -1
        
        right = check(node.right)
        if right == -1:
            return -1
        
        if abs(left - right) > 1:
            return -1
        
        return 1 + max(left, right)
    
    return check(root) != -1
```

**Time:** O(n) | **Space:** O(h)

---

## Pattern 3: Path Problems

### Path Sum (LC 112)

```python
def hasPathSum(root: TreeNode, targetSum: int) -> bool:
    if not root:
        return False
    
    if not root.left and not root.right:
        return root.val == targetSum
    
    remaining = targetSum - root.val
    return (hasPathSum(root.left, remaining) or
            hasPathSum(root.right, remaining))
```

### Path Sum II (LC 113) - All root-to-leaf paths with given sum

```python
def pathSum(root: TreeNode, targetSum: int) -> List[List[int]]:
    result = []
    
    def dfs(node, remaining, path):
        if not node:
            return
        
        path.append(node.val)
        
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])  # Deep copy
        else:
            dfs(node.left, remaining - node.val, path)
            dfs(node.right, remaining - node.val, path)
        
        path.pop()  # Backtrack
    
    dfs(root, targetSum, [])
    return result
```

### Path Sum III (LC 437) - Any path, not just root-to-leaf

```python
def pathSum(root: TreeNode, targetSum: int) -> int:
    prefix_sum = {0: 1}
    
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

**Time:** O(n) | **Space:** O(n)

---

## Pattern 4: Tree Construction

### Build Tree from Preorder + Inorder (LC 105)

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

**Time:** O(n) | **Space:** O(n)

---

## Pattern 5: BST Operations

### Validate BST (LC 98)

```python
def isValidBST(root: TreeNode) -> bool:
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if not (min_val < node.val < max_val):
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))
```

**Alternative -- inorder must be strictly increasing:**
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

### Kth Smallest in BST (LC 230)

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

**Time:** O(h + k) | **Space:** O(h)

---

## Pattern 6: Lowest Common Ancestor

### LCA in Binary Tree (LC 236)

```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    if not root or root == p or root == q:
        return root
    
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    if left and right:
        return root
    
    return left if left else right
```

**Time:** O(n) | **Space:** O(h)

### LCA in BST (LC 235)

```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

**Time:** O(h) | **Space:** O(1)

---

## Pattern 7: Serialize / Deserialize (LC 297)

```python
class Codec:
    def serialize(self, root):
        if not root:
            return "null"
        return (str(root.val) + "," +
                self.serialize(root.left) + "," +
                self.serialize(root.right))
    
    def deserialize(self, data):
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

**Time:** O(n) | **Space:** O(n)

---

## Tree Modification

### Invert Binary Tree (LC 226)

```python
def invertTree(root: TreeNode) -> TreeNode:
    if not root:
        return None
    
    root.left, root.right = root.right, root.left
    
    invertTree(root.left)
    invertTree(root.right)
    
    return root
```

**Time:** O(n) | **Space:** O(h)

### Subtree of Another Tree (LC 572)

```python
def isSubtree(root: TreeNode, subRoot: TreeNode) -> bool:
    if not root:
        return False
    
    if isSameTree(root, subRoot):
        return True
    
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)

def isSameTree(p: TreeNode, q: TreeNode) -> bool:
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val and
            isSameTree(p.left, q.left) and
            isSameTree(p.right, q.right))
```

**Time:** O(m * n) where m, n are sizes of each tree | **Space:** O(h)

---

## Level-Order Variations

### Zigzag Level Order (LC 103)

```python
def zigzagLevelOrder(root: TreeNode) -> List[List[int]]:
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level = []
        for _ in range(len(queue)):
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

### Right Side View (LC 199)

Take the last element at each level.

```python
def rightSideView(root: TreeNode) -> List[int]:
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            
            if i == level_size - 1:
                result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    return result
```

**Time:** O(n) | **Space:** O(n)

---

## Morris Traversal (O(1) Space Inorder)

Inorder traversal without a stack or recursion by temporarily threading the tree. Each node's in-order predecessor's right pointer is temporarily set to point back to the node.

```python
def morris_inorder(root: TreeNode) -> List[int]:
    result = []
    current = root
    
    while current:
        if not current.left:
            # No left subtree: visit and go right
            result.append(current.val)
            current = current.right
        else:
            # Find inorder predecessor (rightmost in left subtree)
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            
            if not predecessor.right:
                # Create thread: predecessor -> current
                predecessor.right = current
                current = current.left
            else:
                # Thread exists: left subtree done, visit and remove thread
                predecessor.right = None
                result.append(current.val)
                current = current.right
    
    return result
```

**Time:** O(n) | **Space:** O(1) (not counting output)

Each edge is traversed at most twice (once to create thread, once to remove it).

---

## N-ary Trees

Some problems use n-ary trees instead of binary trees. The patterns are identical -- just iterate over `node.children` instead of checking `node.left` / `node.right`.

```python
class NaryNode:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

def maxDepth(root: NaryNode) -> int:
    if not root:
        return 0
    if not root.children:
        return 1
    return 1 + max(maxDepth(child) for child in root.children)
```

---

## Common Mistakes

1. **Forgetting null checks** -- always test with `TreeNode(5)` (no children).

2. **Forgetting to backtrack** -- in path problems, pop after recursion.

3. **Modifying tree during traversal** -- be careful when asked to modify in-place.

4. **Stack overflow on deep trees** -- consider iterative for very deep trees.

5. **Confusing height vs depth** -- height is bottom-up (leaf = 0), depth is top-down (root = 0).

---

## Complexity Reference

| Operation | Time | Space |
|-----------|------|-------|
| Traversal (any) | O(n) | O(h) recursive, O(n) BFS |
| Search (BST) | O(h) | O(h) recursive, O(1) iterative |
| Height / Depth | O(n) | O(h) |
| LCA (binary tree) | O(n) | O(h) |
| LCA (BST) | O(h) | O(1) iterative |
| Level Order | O(n) | O(n) |
| Morris Traversal | O(n) | O(1) |

Where h = height: O(log n) balanced, O(n) worst case (skewed).
