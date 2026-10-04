# Complexity Analysis

An algorithm is a procedure that takes *any* valid instance of a problem and produces the correct output. Two questions follow immediately: **is it correct?** and **how much does it cost?** This chapter is about the second question — how to reason about cost in a way that is independent of the machine, the language, and the particular input you happened to test on.

The goal is not mathematical rigor for its own sake. It is to develop the reflex of looking at a piece of code, or at a problem's constraints, and knowing within seconds whether an idea is fast enough to be worth writing.

---

## The RAM Model of Computation

To compare algorithms without running them, we need an abstract machine to count steps on. The standard choice is the **Random Access Machine (RAM)**:

- Each *simple* operation (`+`, `*`, `-`, `=`, `if`, a function call) takes exactly one step.
- Loops and subroutines are **not** simple operations. They are compositions of simple operations, and their cost depends on how many times they iterate.
- Each memory access takes one step, and memory is unlimited.

Under this model, the running time of an algorithm on an instance is the number of steps it executes. The model is *wrong* in almost every detail — multiplication costs more than addition, cache misses cost a hundred times more than cache hits — and yet it is extraordinarily useful, for the same reason a flat-Earth model is useful for planning a walk to the grocery store: the errors are irrelevant at the scale of the question being asked.

!!! warning "Python breaks the RAM model in sneaky places"
    The single most common source of complexity bugs in Python is a line that *looks* like one step but is secretly a loop:

    | Looks like one step | Actually costs | Why |
    |---|---|---|
    | `x in my_list` | $O(n)$ | linear scan |
    | `my_list.pop(0)`, `my_list.insert(0, x)` | $O(n)$ | shifts every element |
    | `arr[i:j]` | $O(j - i)$ | copies the slice |
    | `s + t` for strings | $O(\lvert s\rvert + \lvert t\rvert)$ | strings are immutable; a new one is built |
    | `min(arr)`, `max(arr)`, `sum(arr)` | $O(n)$ | scans everything |
    | `sorted(arr)` | $O(n \log n)$ | a full sort |
    | `list(d.keys())`, `set(arr)` | $O(n)$ | builds a new container |

    Apply the RAM model faithfully: **a built-in call is a subroutine, not a step.**

!!! tip "Take-Home Lesson"
    Algorithms can be understood and compared in a language- and machine-independent way. The RAM model gives us a common currency — the number of simple steps — for that comparison.

---

## Best, Worst, and Average Case

Running time depends on more than the input *size*. Sorting an already-sorted array may be much faster than sorting a reversed one. So for each size $n$ there is not one running time but a whole distribution of them, one per possible input.

Three numerical functions summarize that distribution:

- **Worst case** — the *maximum* number of steps over all inputs of size $n$.
- **Best case** — the *minimum* number of steps over all inputs of size $n$.
- **Average case** (or expected case) — the mean number of steps over some distribution of inputs of size $n$.

The worst case is almost always what we care about. The best case is typically meaningless (every algorithm is fast when the answer is at index 0). The average case is useful but requires assuming a probability distribution over inputs, which is hard to justify. The worst case is a *guarantee*: an adversary cannot make the algorithm slower than this.

!!! note "When average case *does* matter"
    Two important exceptions: hash tables ($O(1)$ expected, $O(n)$ worst) and randomized quicksort ($O(n \log n)$ expected, $O(n^2)$ worst). When the randomness is inside the *algorithm* (a random pivot, a randomly seeded hash function), not assumed about the input, the expected bound holds for **every** input — nearly as good as a worst-case guarantee. Python randomizes the pivot only if you do, and seeds hashes only for `str` and `bytes`: `hash(5) == 5`, so carefully chosen integer keys can still force collisions.

---

## The Big Oh Notation

Exact step counts are ugly. Selection sort might take $T(n) = \tfrac{1}{2}n^2 + \tfrac{3}{2}n - 4$ steps under one reasonable counting and $n^2 - n + 7$ under another. The difference is noise; what matters is that both grow like $n^2$. Big Oh notation is the tool for throwing away the noise.

Formally, for functions $f, g$ from positive integers to positive reals:

| Notation | Meaning | Formal definition |
|---|---|---|
| $f(n) = O(g(n))$ | $g$ is an **upper bound** on $f$ | $\exists\, c, n_0$ such that $f(n) \le c \cdot g(n)$ for all $n \ge n_0$ |
| $f(n) = \Omega(g(n))$ | $g$ is a **lower bound** on $f$ | $\exists\, c, n_0$ such that $f(n) \ge c \cdot g(n)$ for all $n \ge n_0$ |
| $f(n) = \Theta(g(n))$ | $g$ is a **tight bound** on $f$ | $f(n) = O(g(n))$ **and** $f(n) = \Omega(g(n))$ |

Two details in the definition do all the work:

1. **The constant $c$** lets us ignore multiplicative factors. $1000n$ and $0.001n$ are both $\Theta(n)$.
2. **The threshold $n_0$** lets us ignore small inputs. We only care about behavior as $n$ grows large.

!!! info "In interviews, \"O\" usually means \"Θ\""
    Technically $3n = O(n^3)$ is true — $n^3$ is an upper bound on $3n$, just a very loose one. In everyday usage (and in interviews), when someone says an algorithm "is $O(n)$" they mean the tight bound $\Theta(n)$. Always give the tightest bound you can justify.

??? question "Stop and Think: Back to the definition"
    **Problem:** Is $2^{n+1} = \Theta(2^n)$? Is $2^{2n} = \Theta(2^n)$?

    **Solution:** For the first, $2^{n+1} = 2 \cdot 2^n$. Pick $c = 2$ and the upper bound holds; pick $c = 1$ and the lower bound holds. So yes, $2^{n+1} = \Theta(2^n)$ — adding a constant to an exponent multiplies by a constant.

    For the second, $2^{2n} = 4^n = 2^n \cdot 2^n$. For $2^{2n} \le c \cdot 2^n$ we would need $2^n \le c$ for all large $n$, which is impossible for any fixed $c$. So $2^{2n} \ne O(2^n)$. *Multiplying* an exponent changes the growth class. This is why $O(2^n)$ and $O(4^n)$ are genuinely different complexities, whereas $O(\log_2 n)$ and $O(\log_{10} n)$ are not.

!!! tip "Take-Home Lesson"
    Big Oh notation and worst-case analysis are *simplifications*, and deliberately so. They discard exactly the information that doesn't matter for choosing between algorithms, and keep exactly the information that does.

---

## Growth Rates and Dominance

Why are we allowed to be so cavalier about constants? Because the gap *between* growth classes is so enormous that constants become irrelevant. The table below assumes roughly $10^7$ simple operations per second, a realistic figure for pure Python (compiled languages are 10–100× faster, which shifts every row a little but changes none of the conclusions).

| $n$ | $\lg n$ | $n$ | $n \lg n$ | $n^2$ | $n^3$ | $2^n$ | $n!$ |
|---|---|---|---|---|---|---|---|
| 10 | < 1 µs | 1 µs | 3 µs | 10 µs | 100 µs | 100 µs | 0.36 s |
| 20 | < 1 µs | 2 µs | 9 µs | 40 µs | 0.8 ms | 0.1 s | 7,700 years |
| 30 | < 1 µs | 3 µs | 15 µs | 90 µs | 2.7 ms | 1.8 min | — |
| 50 | < 1 µs | 5 µs | 28 µs | 0.25 ms | 12.5 ms | 3.6 years | — |
| 100 | < 1 µs | 10 µs | 66 µs | 1 ms | 0.1 s | $10^{15}$ years | — |
| $10^3$ | 1 µs | 0.1 ms | 1 ms | 0.1 s | 1.7 min | — | — |
| $10^4$ | 1 µs | 1 ms | 13 ms | 10 s | 1.2 days | — | — |
| $10^5$ | 2 µs | 10 ms | 0.17 s | 17 min | 3 years | — | — |
| $10^6$ | 2 µs | 0.1 s | 2 s | 1.2 days | — | — | — |
| $10^9$ | 3 µs | 1.7 min | 50 min | 3,200 years | — | — | — |

Read it row by row and the lessons jump out:

- For $n = 10$, **everything is fast**. Small inputs never distinguish algorithms.
- $n!$ algorithms die at $n \approx 12$; $2^n$ algorithms at $n \approx 25$–$30$.
- Quadratic algorithms are fine up to a few thousand, painful at $10^5$, hopeless at $10^6$.
- $n \log n$ and linear algorithms stay practical on essentially any input that fits in memory.
- A logarithmic algorithm barely notices $n$ at all.

### The dominance pecking order

We say $g$ **dominates** $f$ (written $g \gg f$) when $f(n) = O(g(n))$ but not the other way around. The handful of classes that cover nearly every algorithm you will write, from fastest-growing to slowest:

$$
n! \gg 2^n \gg n^3 \gg n^2 \gg n \log n \gg n \gg \sqrt{n} \gg \log n \gg 1
$$

Filling in the gaps with some classes that show up in more advanced analyses:

$$
n! \gg c^n \gg n^3 \gg n^2 \gg n^{1+\epsilon} \gg n \log n \gg n \gg \sqrt{n} \gg \log^2 n \gg \log n \gg \log\log n \gg \alpha(n) \gg 1
$$

where $\alpha(n)$ is the inverse Ackermann function — the "practically constant" factor in Union-Find (see [Trie & Union Find](12_trie_union_find.md)).

| Class | Typical source |
|---|---|
| $1$ | Arithmetic, hash lookup, array indexing |
| $\log n$ | Halving the search space: binary search, balanced BST ops, heap push/pop |
| $n$ | Looking at each element a constant number of times |
| $n \log n$ | Sorting; $n$ operations on a heap or BST; divide-and-conquer with linear merge |
| $n^2$ | Looking at all **pairs**: nested loops, simple DP on two sequences |
| $n^3$ | Looking at all **triples**: Floyd–Warshall, interval DP, naive matrix multiplication |
| $2^n$ | Enumerating all **subsets** |
| $n!$ | Enumerating all **orderings** (permutations) |

!!! tip "Take-Home Lesson"
    A small set of growth classes suffices for almost every algorithm. Learn to recognize them by their *structure* — pairs, triples, subsets, orderings, halving — and you can estimate complexity before writing a line of code.

---

## Working with the Big Oh

The algebra of Big Oh reduces to two rules, plus one warning.

**Adding functions: the larger one wins.**

$$O(f(n)) + O(g(n)) = O(\max(f(n), g(n)))$$

Two consecutive loops over $n$ items is $O(n) + O(n) = O(n)$. A sort followed by a linear scan is $O(n \log n) + O(n) = O(n \log n)$. This is why we "drop non-dominant terms": $n^2 + n \log n + 100n = \Theta(n^2)$.

**Multiplying functions: they multiply.**

$$O(f(n)) \cdot O(g(n)) = O(f(n) \cdot g(n))$$

A loop running $n$ times whose body costs $O(\log n)$ is $O(n \log n)$. Multiplying by a positive *constant* does nothing: $O(c \cdot f(n)) = O(f(n))$.

**Warning: different inputs get different variables.**

```python
def common_elements(a: list[int], b: list[int]) -> list[int]:
    b_set = set(b)                        # O(len(b))
    return [x for x in a if x in b_set]   # O(len(a))
# Total: O(a + b), NOT O(n)


def all_pairs(a: list[int], b: list[int]) -> list[tuple[int, int]]:
    return [(x, y) for x in a for y in b]
# Total: O(a * b), NOT O(n^2)
```

Collapsing $a$ and $b$ into a single $n$ hides real information. If $a$ has 10 elements and $b$ has $10^6$, $O(a \cdot b)$ is perfectly fine while "$O(n^2)$" sounds alarming. The same applies to grids ($O(m \cdot n)$ for an $m \times n$ grid), graphs ($O(V + E)$), and strings with an alphabet ($O(n \cdot \Sigma)$).

---

## Reasoning About Efficiency

The fastest way to learn analysis is to do it on real code. Here are four classic examples, each teaching one technique.

### Selection sort: counting nested loops exactly

```python
def selection_sort(a: list[int]) -> None:
    n = len(a)
    for i in range(n):
        smallest = i
        for j in range(i + 1, n):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
```

The inner loop runs $n - i - 1$ times for each $i$. Summing:

$$
\sum_{i=0}^{n-1} (n - i - 1) = (n-1) + (n-2) + \cdots + 1 + 0 = \frac{n(n-1)}{2} = \Theta(n^2)
$$

A faster argument, useful when the exact sum is ugly: to show $\Theta(n^2)$, show both bounds. **Upper:** each loop runs at most $n$ times, so at most $n \cdot n = n^2$ steps. **Lower:** for the first $n/2$ values of $i$, the inner loop runs at least $n/2$ times, so at least $(n/2)(n/2) = n^2/4$ steps. Done — no summation formula required.

### Insertion sort: when best and worst case differ

```python
def insertion_sort(a: list[int]) -> None:
    for i in range(1, len(a)):
        j = i
        while j > 0 and a[j] < a[j - 1]:
            a[j], a[j - 1] = a[j - 1], a[j]
            j -= 1
```

The `while` loop stops as soon as the element is in place. On a sorted array it never iterates, so the total is $\Theta(n)$. On a reversed array it goes all the way to the front every time: $\Theta(n^2)$. The worst case is $\Theta(n^2)$, and that is what we report — but the gap explains why insertion sort is used inside Timsort for small or nearly-sorted runs.

!!! note "Counting what actually happens"
    For `while` loops, the number of iterations is not written in the code. You have to argue about it: *what quantity changes each iteration, and how far can it go?* Here, `j` decreases by one each step and cannot go below zero, so the inner loop runs at most $i$ times.

### String pattern matching: two variables, one loop nest

```python
def find_substring(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            return i
    return -1
```

The outer loop runs $n - m + 1$ times and the inner loop at most $m$ times, so the worst case is $O((n - m + 1) \cdot m) \le O(nm)$. Is that bound tight? Try `text = "aaaa...a"` and `pattern = "aa...ab"`: every alignment matches $m - 1$ characters before failing, so yes. Cleverer algorithms (KMP, Z-function, Rabin–Karp) bring this down to $O(n + m)$.

### Matrix multiplication: three nested loops

```python
def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    x, y, z = len(A), len(B), len(B[0])      # A is x*y, B is y*z
    C = [[0.0] * z for _ in range(x)]
    for i in range(x):
        for j in range(z):
            for k in range(y):
                C[i][j] += A[i][k] * B[k][j]
    return C
```

Three independent loops multiply: $\Theta(xyz)$, or $\Theta(n^3)$ for square matrices.

---

## Summations

Loops in code become summations in analysis. Two families of sums cover almost everything.

### Sums of powers: $\sum i^p = \Theta(n^{p+1})$

$$
\sum_{i=1}^{n} 1 = n \qquad \sum_{i=1}^{n} i = \frac{n(n+1)}{2} = \Theta(n^2) \qquad \sum_{i=1}^{n} i^2 = \Theta(n^3)
$$

The big-picture fact: summing a polynomial of degree $p$ gives a polynomial of degree $p + 1$. The constant ($\tfrac{1}{2}$, $\tfrac{1}{3}$, …) rarely matters.

### Geometric series: the "free lunch" of analysis

$$
\sum_{i=0}^{n} a^i = \frac{a^{n+1} - 1}{a - 1}
$$

- If $a > 1$ the sum is dominated by its **largest term**: $1 + 2 + 4 + \cdots + 2^k = 2^{k+1} - 1 < 2 \cdot 2^k$.
- If $a < 1$ the sum is bounded by a **constant**: $1 + \tfrac{1}{2} + \tfrac{1}{4} + \cdots < 2$, no matter how many terms.

This is one of the most powerful tools in analysis: *a sum of a logarithmic number of geometrically shrinking terms costs only as much as the largest term*. It is the reason why:

- Appending to a dynamic array is $O(1)$ amortized (the resize costs $1 + 2 + 4 + \cdots + n < 2n$).
- Building a heap bottom-up (`heapq.heapify`) is $O(n)$, not $O(n \log n)$.
- A recursion that does $O(n)$ work and then recurses on *one* half (quickselect, on average) is $O(n)$ total: $n + n/2 + n/4 + \cdots < 2n$.

### The harmonic series: where the log comes from

$$
H(n) = \sum_{i=1}^{n} \frac{1}{i} = 1 + \frac{1}{2} + \frac{1}{3} + \cdots + \frac{1}{n} = \Theta(\log n)
$$

When a $\log n$ appears unexpectedly in an analysis, the harmonic series is usually why. A classic example:

```python
def count_divisor_pairs(n: int) -> int:
    count = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):   # multiples of i: n / i of them
            count += 1
    return count
```

This looks like it might be quadratic, but the inner loop runs $n / i$ times, so the total is $\sum_{i=1}^{n} n/i = n \cdot H(n) = \Theta(n \log n)$. The same shape appears in the Sieve of Eratosthenes (which is even better, $\Theta(n \log \log n)$, because it only iterates over primes $i$).

---

## Logarithms

A logarithm is an inverse exponential: $b^x = y \iff x = \log_b y$. Exponentials grow terrifyingly fast; logarithms grow refreshingly slowly. $\log_2(10^9) \approx 30$.

!!! tip "Take-Home Lesson"
    Logarithms arise whenever things are repeatedly **halved** or **doubled**. If you see a quantity multiplied or divided by a constant at each step, expect a log.

**Binary search.** Each comparison discards half of the remaining candidates. The number of steps is the number of times you can halve $n$ before reaching 1, which is exactly $\log_2 n$. Twenty comparisons find any item among a million.

**Trees.** A binary tree of height $h$ has at most $2^h$ leaves. So a tree holding $n$ leaves must have height at least $\log_2 n$ — and a *balanced* tree achieves it. Short trees can hold an enormous number of items, which is why trees underlie so many fast data structures. A $d$-ary tree has height $\log_d n$.

**Bits.** There are $2^w$ bit strings of length $w$. To give $n$ items distinct labels you need $w = \lceil \log_2 n \rceil$ bits. This is why an integer $n$ has $\Theta(\log n)$ digits, and why iterating over the bits of $n$ costs $O(\log n)$.

**Fast exponentiation.** Computing $a^n$ by $n - 1$ multiplications is wasteful. Since $a^n = (a^{n/2})^2$ for even $n$ and $a \cdot (a^{\lfloor n/2 \rfloor})^2$ for odd $n$, we halve the exponent with at most two multiplications:

```python
def fast_pow(a: int, n: int, mod: int | None = None) -> int:
    """Compute a**n (optionally modulo mod) in O(log n) multiplications."""
    result = 1
    while n > 0:
        if n & 1:                 # current bit of n is set
            result *= a
            if mod:
                result %= mod
        a *= a                    # a, a^2, a^4, a^8, ...
        if mod:
            a %= mod
        n >>= 1
    return result
```

(Python's built-in `pow(a, n, mod)` does exactly this.)

### Properties worth memorizing

| Identity | Consequence |
|---|---|
| $\log_a(xy) = \log_a x + \log_a y$ | Log of a product is a sum of logs |
| $\log_a n^b = b \log_a n$ | $\log(n^2) = 2 \log n = \Theta(\log n)$ |
| $\log_a n = \dfrac{\log_b n}{\log_b a}$ | **The base does not matter**: changing it is a constant factor |
| $\log(n!) = \Theta(n \log n)$ | Why comparison sorting needs $\Omega(n \log n)$ comparisons |

The base-change rule is why we write $O(\log n)$ without a base. But note that the base *inside* an exponent matters: $2^{\log_2 n} = n$ whereas $2^{\log_4 n} = \sqrt{n}$.

---

## Recurrences and Divide and Conquer

Recursive algorithms are analyzed with **recurrence relations**, which express the cost on an input of size $n$ in terms of the cost on smaller inputs.

| Recurrence | Solution | Example |
|---|---|---|
| $T(n) = T(n-1) + O(1)$ | $O(n)$ | Recursive linear scan, factorial |
| $T(n) = T(n-1) + O(n)$ | $O(n^2)$ | Selection sort as recursion; quicksort worst case |
| $T(n) = T(n/2) + O(1)$ | $O(\log n)$ | Binary search |
| $T(n) = T(n/2) + O(n)$ | $O(n)$ | Quickselect (expected) — geometric series |
| $T(n) = 2T(n/2) + O(1)$ | $O(n)$ | Tree traversal |
| $T(n) = 2T(n/2) + O(n)$ | $O(n \log n)$ | Merge sort |
| $T(n) = 2T(n-1) + O(1)$ | $O(2^n)$ | Naive Fibonacci (roughly), subset enumeration |

### The master theorem

For recurrences of the form $T(n) = a\,T(n/b) + f(n)$ — split into $a$ subproblems of size $n/b$, then combine in $f(n)$ time — picture the **recursion tree**. Level $i$ has $a^i$ nodes, each of size $n/b^i$. The tree has $\log_b n$ levels and $a^{\log_b n} = n^{\log_b a}$ leaves. The answer depends on where the work concentrates:

| Case | Condition | Result | Intuition |
|---|---|---|---|
| 1 | $f(n) = O(n^{\log_b a - \epsilon})$ | $\Theta(n^{\log_b a})$ | **Leaves dominate**: too many subproblems |
| 2 | $f(n) = \Theta(n^{\log_b a})$ | $\Theta(n^{\log_b a} \log n)$ | **Every level costs the same**: multiply by the depth |
| 3 | $f(n) = \Omega(n^{\log_b a + \epsilon})$ | $\Theta(f(n))$ | **Root dominates**: the combine step is the bottleneck |

| Algorithm | $a$, $b$, $f(n)$ | $n^{\log_b a}$ | Case | Result |
|---|---|---|---|---|
| Binary search | 1, 2, $1$ | $1$ | 2 | $\Theta(\log n)$ |
| Merge sort | 2, 2, $n$ | $n$ | 2 | $\Theta(n \log n)$ |
| Tree traversal | 2, 2, $1$ | $n$ | 1 | $\Theta(n)$ |
| Karatsuba multiplication | 3, 2, $n$ | $n^{1.585}$ | 1 | $\Theta(n^{1.585})$ |
| Strassen | 7, 2, $n^2$ | $n^{2.807}$ | 1 | $\Theta(n^{2.807})$ |

!!! note "Divide as evenly as possible"
    Fast exponentiation and merge sort both work because they split the problem into halves. A split of $n - 1$ and $1$ (as in quicksort with a bad pivot) turns $T(n) = 2T(n/2) + n$ into $T(n) = T(n-1) + n = \Theta(n^2)$. Balance is what makes divide and conquer fast.

---

## Amortized Analysis

Sometimes a single operation can be expensive, but expensive operations are *rare enough* that the average over any sequence is cheap. The **amortized cost** is the total cost of a sequence of operations divided by its length, in the worst case over all sequences. Unlike average-case analysis, no probability is involved — it is a worst-case guarantee on the *total*.

### Dynamic arrays

A Python `list` stores its elements in a contiguous block with some spare capacity. When `append` finds the block full, it allocates a larger block and copies everything over — an $O(n)$ operation. Is `append` therefore $O(n)$?

Suppose the capacity doubles on each resize. Over $n$ appends, resizes happen at sizes $1, 2, 4, \dots, n$, copying

$$1 + 2 + 4 + \cdots + n < 2n$$

elements in total — a geometric series. Adding the $n$ ordinary writes, $n$ appends cost less than $3n$ steps: **$O(1)$ amortized** per append. (CPython grows by roughly 12.5% rather than 100%, but any constant growth factor $> 1$ gives a geometric series and the same conclusion. Growing by a constant *amount* would not: $k + 2k + 3k + \cdots$ is quadratic.)

### Aggregate counting: "each element is touched a constant number of times"

The most useful amortized argument in practice is simple bookkeeping: instead of bounding each loop iteration, bound how many times **each element** can be processed over the entire run.

```python
def next_greater(nums: list[int]) -> list[int]:
    result = [-1] * len(nums)
    stack: list[int] = []                   # indices, decreasing values
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            result[stack.pop()] = x
        stack.append(i)
    return result
```

A `while` inside a `for` looks quadratic. But every index is pushed exactly once and popped at most once, so across the *whole* run the `while` loop body executes at most $n$ times. Total: $O(n)$. The same argument proves that sliding-window two-pointer algorithms are linear: `left` and `right` each move forward at most $n$ times.

!!! tip "Take-Home Lesson"
    When a nested loop looks quadratic, ask: *can the inner loop really run $n$ times on every outer iteration, or is it consuming a shared budget?* If each element can be pushed, popped, or passed over only once, the total is linear.

---

## Space Complexity

Space is analyzed with the same tools. Two conventions to be explicit about:

- **Auxiliary space** is the extra memory beyond the input. When people say "$O(1)$ space," they mean auxiliary space.
- **Output space** is usually not counted — returning a list of $n$ answers doesn't make an algorithm "use $O(n)$ space" in the usual sense.

### The call stack counts

Each active recursive call holds a stack frame. Recursion depth $d$ costs $O(d)$ space even if the function allocates nothing.

| Recursion | Depth | Space |
|---|---|---|
| Binary search (recursive) | $\log n$ | $O(\log n)$ |
| DFS on a balanced tree | $\log n$ | $O(\log n)$ |
| DFS on a skewed tree / linked list | $n$ | $O(n)$ |
| DFS on a graph | up to $V$ | $O(V)$ |
| Quicksort (recurse on the smaller side, loop on the larger) | $\log n$ | $O(\log n)$ |

!!! warning "Python's recursion limit"
    CPython's default recursion limit is 1000. A recursive DFS on a path graph or a degenerate tree of 10,000 nodes raises `RecursionError`. Either raise the limit with `sys.setrecursionlimit`, or convert the recursion into an explicit stack — which is always possible and uses the same asymptotic space.

---

## The Python Cost Model

Knowing the cost of built-in operations is as important as knowing the algorithm. All figures are for CPython.

| Container | Operation | Cost |
|---|---|---|
| `list` | index `a[i]`, assign `a[i] = x`, `len(a)` | $O(1)$ |
| | `append(x)`, `pop()` | $O(1)$ amortized |
| | `pop(0)`, `insert(0, x)`, `insert(i, x)`, `del a[i]` | $O(n)$ |
| | `x in a`, `a.index(x)`, `a.count(x)`, `a.remove(x)` | $O(n)$ |
| | slice `a[i:j]`, `a.copy()`, `a + b` | $O(j-i)$, $O(n)$, $O(n + m)$ |
| | `a.sort()`, `sorted(a)` | $O(n \log n)$ |
| `dict` / `set` | `d[k]`, `k in d`, `d[k] = v`, `del d[k]`, `s.add(x)` | $O(1)$ average, $O(n)$ worst |
| | iteration, copy | $O(n)$ |
| | `s & t`, `s | t` | $O(\min(n, m))$, $O(n + m)$ |
| `collections.deque` | `append`, `appendleft`, `pop`, `popleft` | $O(1)$ |
| | index `q[i]` | $O(n)$ (fast only near the ends) |
| `heapq` | `heappush`, `heappop` | $O(\log n)$ |
| | `heapify` | $O(n)$ |
| | `h[0]` (peek) | $O(1)$ |
| `str` | index, `len` | $O(1)$ |
| | `s + t`, slicing, `s.replace`, `s.split` | $O(n)$ |
| | `"".join(parts)` | $O(\text{total length})$ |
| `int` | arithmetic on "small" integers | $O(1)$ |
| | arithmetic on $k$-digit integers | grows with $k$ (arbitrary precision) |

---

## Estimation: From Constraints to Complexity

On LeetCode, the constraints *tell you* the intended complexity. Budget roughly $10^7$–$10^8$ simple operations for Python in a one- or two-second time limit, and read the table backwards:

| Constraint | Largest feasible complexity | Typical techniques |
|---|---|---|
| $n \le 10$ | $O(n!)$, $O(n \cdot n!)$ | Permutations, brute force |
| $n \le 20$ | $O(2^n)$, $O(n \cdot 2^n)$ | Subsets, bitmask DP, backtracking |
| $n \le 40$ | $O(2^{n/2})$ | Meet in the middle |
| $n \le 500$ | $O(n^3)$ | Floyd–Warshall, interval DP |
| $n \le 5{,}000$ | $O(n^2)$ | 2-D DP, all pairs |
| $n \le 10^5$–$10^6$ | $O(n \log n)$ or $O(n)$ | Sorting, heaps, binary search, two pointers, hashing |
| $n \le 10^9$ or more | $O(\log n)$, $O(\sqrt{n})$, $O(1)$ | Binary search on the answer, math |

Estimation is also a sanity check for your own design. If you have derived an $O(n^2)$ algorithm and $n = 10^5$, stop: you need a better idea, not a better implementation.

!!! tip "Take-Home Lesson"
    Programs working on large inputs must run in linear or near-linear time. Once you commit to that requirement, the constraint itself usually points toward the right technique.

---

## Common Mistakes

1. **Confusing additive and multiplicative progress.**
   ```python
   i = 1
   while i < n:
       i += 2      # O(n): additive steps
   i = 1
   while i < n:
       i *= 2      # O(log n): multiplicative steps
   ```

2. **Hidden linear work inside a loop.** `pop(0)`, `x in list`, slicing, and string concatenation inside a loop turn $O(n)$ into $O(n^2)$. Use `deque`, `set`, index arithmetic, and `"".join`, respectively.

3. **Slicing in recursion.** `solve(arr[1:])` copies the array at every level: $O(n)$ extra per call, $O(n^2)$ total for $n$ levels. Pass indices instead.

4. **Forgetting the call stack.** A recursive solution with no explicit data structures still uses $O(\text{depth})$ space.

5. **Assuming nested loops mean $O(n^2)$.** The inner loop may share a budget with the outer one (amortized $O(n)$) or shrink geometrically (harmonic, $O(n \log n)$). Count what actually happens.

6. **Reporting $O(n)$ for a two-input problem.** Use $O(m + n)$, $O(V + E)$, $O(m \cdot n)$ — every independent size gets its own variable.

7. **Treating hash operations as always $O(1)$.** They are $O(1)$ *expected*. Also, hashing a key costs time proportional to the key: hashing a string of length $k$ is $O(k)$, and using a `tuple` of length $k$ as a dict key is $O(k)$ per lookup.
