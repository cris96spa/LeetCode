# Stacks & Queues

## Stack Basics

LIFO (Last In, First Out). In Python, use a list:
```python
stack = []
stack.append(x)   # push
stack.pop()        # pop (raises IndexError if empty)
stack[-1]          # peek
len(stack) == 0    # is_empty
```

**When to use:** matching/pairing (parentheses, tags), undo/backtracking, DFS (explicit stack), expression evaluation, maintaining a running state that can be "unwound."

## Queue Basics

FIFO (First In, First Out). In Python, use `collections.deque`:
```python
from collections import deque
q = deque()
q.append(x)       # enqueue (right)
q.popleft()        # dequeue (left) - O(1)
q[0]               # peek front
```

Do NOT use `list.pop(0)` -- that's O(n). Always use deque for queues.

**When to use:** BFS, level-order traversal, order processing, sliding window (monotonic deque).

---

## Key Stack Problems

### Valid Parentheses (LC 20)

O(n) time, O(n) space:
```python
def isValid(s):
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in matching:
            if not stack or stack[-1] != matching[c]:
                return False
            stack.pop()
        else:
            stack.append(c)
    return len(stack) == 0
```

### Min Stack (LC 155)

O(1) for all operations. Store `(value, current_min)` pairs:
```python
class MinStack:
    def __init__(self):
        self.stack = []  # (val, min_so_far)
    
    def push(self, val):
        curr_min = min(val, self.stack[-1][1] if self.stack else val)
        self.stack.append((val, curr_min))
    
    def pop(self):
        self.stack.pop()
    
    def top(self):
        return self.stack[-1][0]
    
    def getMin(self):
        return self.stack[-1][1]
```

### Evaluate Reverse Polish Notation (LC 150)

O(n) time, O(n) space:
```python
def evalRPN(tokens):
    stack = []
    for t in tokens:
        if t in {'+', '-', '*', '/'}:
            b, a = stack.pop(), stack.pop()
            if t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            else: stack.append(int(a / b))  # truncate toward zero
        else:
            stack.append(int(t))
    return stack[0]
```

### Decode String (LC 394)

Input like `"3[a2[c]]"` -> `"accaccacc"`. O(n * max_k) time, O(n) space:
```python
def decodeString(s):
    stack = []
    curr_str = ""
    curr_num = 0
    for c in s:
        if c.isdigit():
            curr_num = curr_num * 10 + int(c)
        elif c == '[':
            stack.append((curr_str, curr_num))
            curr_str = ""
            curr_num = 0
        elif c == ']':
            prev_str, num = stack.pop()
            curr_str = prev_str + curr_str * num
        else:
            curr_str += c
    return curr_str
```

### Asteroid Collision (LC 735)

O(n) time, O(n) space:
```python
def asteroidCollision(asteroids):
    stack = []
    for a in asteroids:
        alive = True
        while alive and stack and a < 0 < stack[-1]:
            if stack[-1] < -a:
                stack.pop()
            elif stack[-1] == -a:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(a)
    return stack
```

### Basic Calculator II (LC 227)

Handles `+`, `-`, `*`, `/` with no parentheses. O(n) time, O(n) space:
```python
def calculate(s):
    stack = []
    num = 0
    op = '+'
    for i, c in enumerate(s):
        if c.isdigit():
            num = num * 10 + int(c)
        if c in '+-*/' or i == len(s) - 1:
            if op == '+':
                stack.append(num)
            elif op == '-':
                stack.append(-num)
            elif op == '*':
                stack.append(stack.pop() * num)
            elif op == '/':
                stack.append(int(stack.pop() / num))
            op = c
            num = 0
    return sum(stack)
```

### Basic Calculator (LC 224)

Handles `+`, `-`, and parentheses. O(n) time, O(n) space:
```python
def calculate(s):
    stack = []
    result = 0
    num = 0
    sign = 1
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == '+':
            result += sign * num
            num = 0
            sign = 1
        elif c == '-':
            result += sign * num
            num = 0
            sign = -1
        elif c == '(':
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1
        elif c == ')':
            result += sign * num
            num = 0
            result *= stack.pop()  # sign before paren
            result += stack.pop()  # result before paren
    result += sign * num
    return result
```

---

## Monotonic Stack

### Concept

A stack where elements are maintained in strictly increasing or decreasing order. When a new element violates the order, pop elements until the invariant is restored. The popped elements have found their "answer" (next greater, next smaller, etc.).

### When to Use

- "Next greater element" / "next smaller element"
- "Previous greater element" / "previous smaller element"
- Problems involving spans, rectangles, temperatures, stock prices
- Any time you need to find the nearest element satisfying some comparison

### Template: Next Greater Element

For each element, find the next element to its right that is greater.

```python
def next_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices, monotonically decreasing values
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    return result
```

Stack invariant: values at indices in the stack are in **decreasing** order. When we find something greater, we pop and assign.

### Template: Next Smaller Element

```python
def next_smaller(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices, monotonically increasing values
    for i in range(n):
        while stack and nums[i] < nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    return result
```

### Template: Previous Smaller Element

```python
def prev_smaller(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices, monotonically increasing values
    for i in range(n):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        if stack:
            result[i] = nums[stack[-1]]
        stack.append(i)
    return result
```

Key difference from "next" pattern: the **current element** reads its answer from the stack top (instead of the popped element getting its answer from the current element).

### Daily Temperatures (LC 739)

"How many days until a warmer temperature?" -- classic next greater element.

O(n) time, O(n) space:
```python
def dailyTemperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []  # indices, decreasing temps
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    return result
```

### Next Greater Element I (LC 496)

Given `nums1` (subset of `nums2`), for each element in `nums1`, find its next greater in `nums2`.

O(n + m) time, O(n) space:
```python
def nextGreaterElement(nums1, nums2):
    next_greater = {}
    stack = []
    for num in nums2:
        while stack and num > stack[-1]:
            next_greater[stack.pop()] = num
        stack.append(num)
    return [next_greater.get(num, -1) for num in nums1]
```

### Next Greater Element II (LC 503) - Circular Array

Trick: iterate through the array twice (index `0` to `2n-1`) using `i % n`.

O(n) time, O(n) space:
```python
def nextGreaterElements(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(2 * n):
        while stack and nums[i % n] > nums[stack[-1]]:
            result[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)
    return result
```

### Largest Rectangle in Histogram (LC 84)

For each bar, find how far it can extend left and right (i.e., the nearest shorter bar on each side).

O(n) time, O(n) space:
```python
def largestRectangleArea(heights):
    stack = []  # indices, monotonically increasing heights
    max_area = 0
    heights.append(0)  # sentinel to flush remaining bars
    
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    heights.pop()  # restore input
    return max_area
```

**How it works:** The stack maintains indices of bars in increasing height order. When we encounter a shorter bar, we pop and compute the area with the popped bar's height. The width extends from the current stack top + 1 to the current index - 1.

### Trapping Rain Water (LC 42) - Stack Approach

O(n) time, O(n) space:
```python
def trap(heights):
    stack = []  # indices, decreasing heights
    water = 0
    for i, h in enumerate(heights):
        while stack and h > heights[stack[-1]]:
            bottom = heights[stack.pop()]
            if not stack:
                break
            width = i - stack[-1] - 1
            bounded_height = min(h, heights[stack[-1]]) - bottom
            water += width * bounded_height
        stack.append(i)
    return water
```

Note: the two-pointer approach (see `two_pointers_sliding_window.md`) is O(1) space and often preferred.

---

## Monotonic Queue (Deque)

### Sliding Window Maximum (LC 239)

Maintain a deque of indices where values are in **decreasing** order. The front of the deque is always the maximum for the current window.

O(n) time, O(k) space:
```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()  # indices, decreasing values
    result = []
    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Remove smaller elements (they'll never be the max)
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

See also: `two_pointers_sliding_window.md` for more sliding window patterns.

---

## Complexity Reference

| Operation     | Stack (list) | Queue (deque) |
|---------------|-------------|---------------|
| Push/Enqueue  | O(1) amort  | O(1)          |
| Pop/Dequeue   | O(1)        | O(1)          |
| Peek          | O(1)        | O(1)          |
| Search        | O(n)        | O(n)          |
| Space         | O(n)        | O(n)          |

Monotonic stack/queue: O(n) total time for processing n elements (each element pushed and popped at most once).

---

## Common Mistakes

- **Using list as queue:** `list.pop(0)` is O(n). Use `collections.deque`.
- **Empty stack access:** always check `if stack` before `stack[-1]` or `stack.pop()`.
- **Monotonic stack direction confusion:** "next greater" uses a decreasing stack; "next smaller" uses an increasing stack. Think about what you're keeping vs. popping.
- **Forgetting sentinel in histogram:** without appending 0, bars remaining in the stack at the end are never processed. Alternative: process the stack after the loop.
- **Integer division toward zero:** Python's `//` floors (rounds toward negative infinity). For calculator problems, use `int(a / b)` to truncate toward zero.
- **Not handling multi-digit numbers:** in expression evaluation, build the full number before processing.
