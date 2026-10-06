# Stacks & Queues

A **container** is a data structure that stores items and hands them back **without regard to their content**. What distinguishes one container from another is the *order* in which items come back out:

- A **stack** returns the most recently inserted item: **last in, first out** (LIFO).
- A **queue** returns the least recently inserted item: **first in, first out** (FIFO).

That one decision — which item comes out next — turns out to shape entire families of algorithms. Stacks are the natural companion of recursion, nesting, and "the most recent unresolved thing." Queues are the natural companion of fairness, simulation, and exploring things in the order they were discovered. And when neither order is what you need, you want a priority queue, which retrieves by content after all (see [Heaps](10_heaps.md)).

---

## The Two Orders

**LIFO** shows up wherever things *nest*. People packed into a crowded elevator leave in LIFO order. Function calls return in LIFO order: the most recently called function finishes first. Parentheses close in LIFO order: the most recently opened one must close first. Undo histories, browser back buttons, and depth-first search all live on stacks.

**FIFO** shows up wherever things *wait their turn*. It is the fair order for serving requests: it minimizes the maximum time anyone waits. (Interestingly, the *average* waiting time is the same under FIFO and LIFO; what FIFO buys is that nobody is starved.) Breadth-first search, task schedulers, and buffered streams all live on queues.

!!! tip "Take-Home Lesson"
    If retrieval order doesn't matter to your algorithm, use a stack: it is the simplest and fastest container. Choose a queue when fairness or discovery order matters — most notably in breadth-first search, where FIFO order is exactly what makes shortest paths come out right.

### In Python

```python
from collections import deque

stack: list[int] = []
stack.append(1)          # push       O(1) amortized
stack.append(2)
top = stack[-1]          # peek       O(1)
stack.pop()              # pop        O(1)

queue: deque[int] = deque()
queue.append(1)          # enqueue    O(1)
queue.append(2)
front = queue[0]         # peek       O(1)
queue.popleft()          # dequeue    O(1)
```

!!! warning "Never use `list.pop(0)` as a queue"
    `list.pop(0)` shifts every remaining element: $O(n)$ per dequeue, $O(n^2)$ for a BFS over $n$ nodes. `deque.popleft()` is $O(1)$. This single substitution is the most common performance bug in Python BFS code.

---

## Implementing Containers

Both containers can be built on arrays or on linked lists; the question is whether you know a size bound in advance.

### A queue from two stacks (LC 232)

A stack reverses order; reversing twice restores it. Push onto an `inbox` stack. To dequeue, pop from an `outbox` stack — and when it's empty, pour the entire inbox into it, which reverses the inbox so its oldest element ends up on top.

```python
class MyQueue:
    def __init__(self) -> None:
        self.inbox: list[int] = []
        self.outbox: list[int] = []

    def push(self, x: int) -> None:
        self.inbox.append(x)

    def pop(self) -> int:
        self.peek()
        return self.outbox.pop()

    def peek(self) -> int:
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox[-1]

    def empty(self) -> bool:
        return not self.inbox and not self.outbox
```

A single `pop` can cost $O(n)$ when it triggers the pour. But each element is moved from inbox to outbox **at most once** in its lifetime — pushed once, poured once, popped once. So $n$ operations cost $O(n)$ in total: **$O(1)$ amortized** per operation. (This is the aggregate method from [Complexity Analysis](01_complexity_analysis.md#amortized-analysis).)

### A circular buffer (LC 622)

With a fixed capacity, a queue fits in an array whose ends wrap around. Keep the index of the front and the current size; the back is `(front + size) % capacity`.

```python
class CircularQueue:
    def __init__(self, capacity: int) -> None:
        self.buf = [0] * capacity
        self.front = 0
        self.size = 0

    def enqueue(self, x: int) -> bool:
        if self.size == len(self.buf):
            return False
        self.buf[(self.front + self.size) % len(self.buf)] = x
        self.size += 1
        return True

    def dequeue(self) -> int | None:
        if self.size == 0:
            return None
        x = self.buf[self.front]
        self.front = (self.front + 1) % len(self.buf)
        self.size -= 1
        return x
```

Circular buffers are how fixed-size queues are built in practice: no allocation after construction, excellent locality, and $O(1)$ everything. They're the natural structure for "last $k$ events" problems like moving averages and rate limiters.

---

## Stacks and Nesting

### Matching brackets (LC 20)

Why is a stack the right structure for checking brackets? Because the rule is exactly LIFO: a closing bracket must match **the most recently opened bracket that is still unclosed**. The stack holds the unclosed brackets, most recent on top.

```python
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack          # anything left open is an error
```

When there's only one bracket type, the stack degenerates into a **counter** (depth). For Longest Valid Parentheses (LC 32), push *indices* rather than characters, so that the distance between the current index and the index below the top gives the length of the valid run ending here.

### Nested state: Decode String (LC 394)

`"3[a2[c]]"` decodes to `"accaccacc"`. Each `[` begins a new, nested context; each `]` ends the current one and splices its result into the enclosing context. Push the enclosing context when entering, pop it when leaving:

```python
def decode_string(s: str) -> str:
    stack: list[tuple[str, int]] = []      # (text before '[', repeat count)
    current, num = "", 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            stack.append((current, num))
            current, num = "", 0
        elif ch == "]":
            prefix, repeat = stack.pop()
            current = prefix + current * repeat
        else:
            current += ch
    return current
```

This is exactly what a recursive-descent parser does implicitly with the call stack. Any recursive algorithm can be converted into an iterative one with an explicit stack of "saved contexts" — and vice versa.

### Expression evaluation

In **reverse Polish notation** (LC 150), operators follow their operands: `2 1 + 3 *` means $(2 + 1) \times 3$. A stack evaluates it directly — push numbers; on an operator, pop two operands and push the result. There's no need for parentheses or precedence rules, which is why stack machines (the JVM, CPython's bytecode interpreter) use it.

```python
def eval_rpn(tokens: list[str]) -> int:
    stack: list[int] = []
    for tok in tokens:
        if tok in {"+", "-", "*", "/"}:
            b, a = stack.pop(), stack.pop()
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))     # truncate toward zero
        else:
            stack.append(int(tok))
    return stack[0]
```

For ordinary **infix** expressions with `+ - * /` (LC 227), keep a stack of *terms* to be summed at the end. `+x` and `-x` push a new term; `*x` and `/x` bind tighter, so they modify the top term immediately:

```python
def calculate(s: str) -> int:
    stack: list[int] = []
    num, op = 0, "+"
    for i, ch in enumerate(s):
        if ch.isdigit():
            num = num * 10 + int(ch)
        if ch in "+-*/" or i == len(s) - 1:
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                stack.append(int(stack.pop() / num))
            num, op = 0, ch
    return sum(stack)
```

With parentheses (LC 224), push the running result and sign when you see `(`, and combine when you see `)` — the same "save the enclosing context" idea as Decode String.

---

## Augmented Stacks: Min Stack (LC 155)

Support `push`, `pop`, `top`, and `get_min`, all in $O(1)$.

The trouble with tracking a single minimum is that popping the minimum leaves you not knowing the next one. The fix exploits LIFO order: the elements *below* any stack entry never change while that entry is on the stack. So each entry can permanently record **the minimum of itself and everything below it**.

```python
class MinStack:
    def __init__(self) -> None:
        self.stack: list[tuple[int, int]] = []     # (value, min of stack up to here)

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def get_min(self) -> int:
        return self.stack[-1][1]
```

The idea generalizes to any associative aggregate (max, sum, gcd): augment each entry with the aggregate of the stack beneath it. Combined with the two-stacks queue above, it even gives a **queue** with $O(1)$ amortized min — an alternative to the monotonic deque.

---

## The Monotonic Stack

Many problems ask, for every element, about the **nearest element to one side that is larger (or smaller)**: the next warmer day, the previous taller building, the first smaller bar to the left. Brute force scans outward from each element: $O(n^2)$.

The monotonic stack answers all of these queries in a single $O(n)$ pass. Scan left to right, keeping a stack of indices whose values are **decreasing** from bottom to top. These are the elements still waiting for their "next greater" answer. When a new element $x$ arrives, every waiting element smaller than $x$ has just found its answer — $x$ — so pop them all. Then push $x$ to wait its turn.

```python
def next_greater(nums: list[int]) -> list[int]:
    """For each i, the next value to the right that is greater than nums[i], or -1."""
    answer = [-1] * len(nums)
    stack: list[int] = []                   # indices; nums[stack] decreasing
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            answer[stack.pop()] = x
        stack.append(i)
    return answer
```

**Why is this correct?** Two facts. First, the stack really is decreasing: before any index is pushed, every smaller value on top of the stack has been popped. Second, when $x$ pops an index $j$, $x$ is truly the *nearest* greater element to $j$'s right: every element between $j$ and $x$ was pushed on top of $j$ and was not greater than it (otherwise it would have popped $j$ itself).

**Complexity:** each index is pushed once and popped at most once, so the `while` loop runs at most $n$ times in total. $O(n)$ time, despite the nested loop.

### The four variants

| Question for each element | Scan direction | Keep stack | Pop while |
|---|---|---|---|
| Next greater (to the right) | left → right | decreasing | `nums[top] < x` |
| Next smaller (to the right) | left → right | increasing | `nums[top] > x` |
| Previous greater (to the left) | left → right | decreasing | `nums[top] <= x`; then the top is the answer |
| Previous smaller (to the left) | left → right | increasing | `nums[top] >= x`; then the top is the answer |

Two ways to read the same pass: the element being **popped** learns its *next* greater/smaller (it's the newcomer), and the **newcomer**, after popping, learns its *previous* greater/smaller (it's whatever remains on top).

**Circular arrays** (LC 503): iterate over indices $0 \dots 2n - 1$ and use `i % n`, pushing only during the first pass. **Daily Temperatures** (LC 739) records `i - popped_index` instead of a value.

### Largest rectangle in a histogram (LC 84)

The largest rectangle must be exactly as tall as *some* bar $i$ — the shortest bar it spans. For bar $i$, the widest such rectangle extends left and right until it hits a strictly shorter bar. So the answer for bar $i$ needs its **previous smaller** and **next smaller** elements, which one increasing stack provides:

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack: list[int] = []                     # indices; heights increasing
    best = 0
    for i, h in enumerate(heights + [0]):     # sentinel 0 flushes the stack
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1    # previous smaller bar
            best = max(best, height * (i - left - 1))   # i is the next smaller bar
        stack.append(i)
    return best
```

When a bar is popped, both of its boundaries are known at once: the newcomer `i` is the first bar to its right that's shorter, and the new stack top is the first bar to its left that's shorter. The appended sentinel `0` forces every remaining bar off the stack at the end. **Maximal Rectangle** (LC 85) reduces to this problem once per row of a binary matrix.

### Greedy with a monotonic stack

**Remove K Digits** (LC 402): delete $k$ digits from a number to make it as small as possible. Greedy insight: a digit followed by a *smaller* digit should be removed, since the smaller one then shifts into a more significant position. Scanning left to right with an increasing stack implements exactly that:

```python
def remove_k_digits(num: str, k: int) -> str:
    stack: list[str] = []
    for d in num:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    stack = stack[:len(stack) - k]            # still need removals: drop the largest tail
    return "".join(stack).lstrip("0") or "0"
```

The same pattern solves Remove Duplicate Letters (LC 316) and building the lexicographically smallest subsequence.

### Counting contributions

**Sum of Subarray Minimums** (LC 907): add up $\min$ over all $\Theta(n^2)$ subarrays. Flip the question: for each element, *in how many subarrays is it the minimum?* If $L$ is the distance to its previous smaller element and $R$ the distance to its next smaller-or-equal element, it is the minimum of exactly $L \cdot R$ subarrays (choose a start in $L$ ways, an end in $R$ ways). Both distances come from monotonic stacks, so the total is $O(n)$. (Breaking ties asymmetrically — strict on one side, non-strict on the other — ensures a subarray with repeated minimums is counted exactly once.)

!!! tip "Take-Home Lesson"
    When a problem asks about "the nearest larger/smaller element," or about every subarray's max/min, think monotonic stack. The key insight is that an element dominated by a newer one can never be the answer for anything that comes later — so it can be discarded forever.

---

## Queues in Algorithms

The queue's starring role is **breadth-first search**: vertices are explored in the order they're discovered, which guarantees that each is first reached by a shortest path. That story belongs to [Graphs](12_graphs.md) and [Trees](11_trees.md#level-order-traversal-bfs).

The **monotonic deque** is the queue-flavored sibling of the monotonic stack: it keeps candidates in decreasing order, evicts dominated ones from the back, and evicts expired ones from the front. It gives $O(n)$ sliding window maximum (LC 239) — see [Two Pointers & Sliding Window](04_two_pointers_sliding_window.md#sliding-window-maximum-lc-239).

---

## Common Mistakes

1. **`list.pop(0)` as a dequeue.** $O(n)$ per call. Use `collections.deque`.

2. **Popping or peeking an empty stack.** Check `if stack` first. In bracket matching, a closing bracket with an empty stack is invalid input, not a crash.

3. **Forgetting leftovers.** After the scan, a non-empty stack means unclosed brackets (LC 20) or elements that never found a next greater (they keep the default answer).

4. **Storing values when you need indices.** Monotonic stack problems usually need distances or positions (daily temperatures, histogram widths). Push indices; look values up.

5. **Wrong strictness in monotonic stacks.** `<` vs `<=` decides how equal elements are treated. Decide deliberately, especially in counting problems where duplicates can be double-counted.

6. **Integer division semantics.** Python's `//` rounds toward $-\infty$ (`-7 // 2 == -4`); many problems expect truncation toward zero. Use `int(a / b)`.

---

## Practice Problems

| Problem | Technique |
|---|---|
| Valid Parentheses (LC 20) | Stack of open brackets |
| Implement Queue using Stacks (LC 232) | Inbox / outbox, amortized $O(1)$ |
| Design Circular Queue (LC 622) | Array with wrap-around |
| Min Stack (LC 155) | Augmented entries |
| Evaluate Reverse Polish Notation (LC 150) | Operand stack |
| Basic Calculator II (LC 227) | Stack of terms |
| Basic Calculator (LC 224) | Save context on `(` |
| Decode String (LC 394) | Stack of enclosing contexts |
| Asteroid Collision (LC 735) | Stack simulation |
| Daily Temperatures (LC 739) | Next greater, store distance |
| Next Greater Element II (LC 503) | Circular: iterate twice |
| Online Stock Span (LC 901) | Previous greater, online |
| Largest Rectangle in Histogram (LC 84) | Previous / next smaller |
| Maximal Rectangle (LC 85) | Histogram per row |
| Remove K Digits (LC 402) | Greedy increasing stack |
| Sum of Subarray Minimums (LC 907) | Contribution counting |
