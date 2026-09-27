# Bit Manipulation

An integer is two things at once: a number, and a fixed-length array of bits. Most code only uses the first view. Bit manipulation uses the second, and it gets two things in return:

1. **A compact set representation.** A 64-bit integer is a set over a 64-element universe, and union, intersection, and complement are single machine instructions.
2. **Free parallelism.** One `&` operates on every bit at once. Algorithms that process a whole word per step can be dozens of times faster than their element-by-element versions.

Bit tricks have a reputation for being clever puzzles. The goal of this chapter is to show that the handful you actually need all follow from a few simple facts about binary arithmetic, so that you can derive them rather than memorize them.

---

## Bits and Logarithms

There are $2$ bit strings of length 1, $4$ of length 2, and $2^w$ of length $w$. Turning that around: to give $n$ different things distinct labels, you need $w = \lceil \log_2 n \rceil$ bits. This one fact explains a lot:

- A number $n$ has $\lfloor \log_2 n \rfloor + 1$ bits, so **looping over the bits of $n$ costs $O(\log n)$**, not $O(1)$ and not $O(n)$.
- A set of $n$ items has $2^n$ subsets, and a subset is exactly an $n$-bit string: bit $i$ says whether item $i$ is in it. So **integers $0 \dots 2^n - 1$ are the subsets of $n$ items**.
- $\log_2$ of the number of possibilities is the number of yes/no questions needed to identify one of them — binary search, decision trees, and information-theoretic lower bounds are all the same idea.

---

## The Operators

| Operator | Meaning | $5$ op $3$ (`101` op `011`) |
|---|---|---|
| `a & b` | AND: 1 where **both** are 1 — set intersection | `001` = 1 |
| `a | b` | OR: 1 where **either** is 1 — set union | `111` = 7 |
| `a ^ b` | XOR: 1 where they **differ** — symmetric difference | `110` = 6 |
| `~a` | NOT: flip every bit — set complement | $-6$ in Python (see below) |
| `a << k` | shift left: multiply by $2^k$ | `5 << 1` = 10 |
| `a >> k` | shift right: floor-divide by $2^k$ | `5 >> 1` = 2 |

!!! warning "Precedence trap"
    In Python, comparison operators bind **tighter** than `&`, `|`, and `^`. So `x & 1 == 0` means `x & (1 == 0)`, which is `x & False`, which is always `0`. Always parenthesize: `(x & 1) == 0`.

### Negative numbers: two's complement

Hardware stores a $w$-bit signed integer so that ordinary addition "just works" modulo $2^w$. The representation of $-x$ is the bit pattern that, added to $x$, overflows to zero:

$$-x \equiv \sim x + 1 \pmod{2^w}$$

Why? $x + \sim x$ is all ones ($= 2^w - 1$), so $x + (\sim x + 1) = 2^w \equiv 0$. From this identity come two of the most useful tricks below.

**Python integers have unlimited width.** Conceptually, a negative Python int is two's complement with an *infinite* run of leading 1 bits. So `~5 == -6`, `-1` is "all ones forever," and `x >> k` on a negative `x` rounds toward $-\infty$. When a problem asks you to emulate 32-bit behavior, mask explicitly:

```python
MASK32 = 0xFFFF_FFFF


def to_signed32(x: int) -> int:
    """Interpret the low 32 bits of x as a signed 32-bit integer."""
    x &= MASK32
    return x - (1 << 32) if x >> 31 else x
```

---

## The Algebra of XOR

XOR is addition modulo 2 on each bit independently — addition **without carries**. That makes it behave like `+` in a group:

| Property | Identity |
|---|---|
| Identity element | $a \oplus 0 = a$ |
| Every element is its own inverse | $a \oplus a = 0$ |
| Commutative, associative | Order and grouping don't matter |
| Cancellation | $a \oplus b = c \iff a = b \oplus c$ |

**The key consequence:** XOR-ing a collection of values cancels every value that appears an even number of times. What survives is the XOR of the values appearing an odd number of times. This single fact solves a whole family of problems:

```python
from functools import reduce
from operator import xor


def single_number(nums: list[int]) -> int:
    """LC 136: every element appears twice except one."""
    return reduce(xor, nums, 0)


def missing_number(nums: list[int]) -> int:
    """LC 268: nums contains n distinct values from 0..n; find the absent one."""
    n = len(nums)
    return reduce(xor, range(n + 1), 0) ^ reduce(xor, nums, 0)
```

In `missing_number`, every present value appears twice across the two XORs and cancels; the missing one appears once. (The sum formula $n(n+1)/2 - \sum \text{nums}$ also works, but in fixed-width languages it can overflow; XOR cannot.)

### Addition from XOR and AND

Since XOR is addition without carries, and a carry occurs exactly where both bits are 1:

$$a + b = (a \oplus b) + 2 \cdot (a \mathbin{\&} b)$$

Repeating until there are no carries left gives addition using only bitwise operations (LC 371). In Python, the infinite-width integers mean negative numbers never run out of carries, so we must work within 32 bits:

```python
def get_sum(a: int, b: int) -> int:
    """LC 371: a + b without + or -, with 32-bit semantics."""
    while b & MASK32:
        a, b = a ^ b, (a & b) << 1
    return to_signed32(a)
```

---

## Single-Bit Operations

Everything here uses a **mask** with a single 1 at position $i$: `1 << i`.

```python
def get_bit(x: int, i: int) -> int:
    return (x >> i) & 1

def set_bit(x: int, i: int) -> int:
    return x | (1 << i)

def clear_bit(x: int, i: int) -> int:
    return x & ~(1 << i)

def toggle_bit(x: int, i: int) -> int:
    return x ^ (1 << i)
```

### The lowest set bit

Subtracting 1 from $x$ turns its lowest 1 bit into 0 and all the 0s below it into 1s (the borrow propagates up to the first 1):

```text
x      = 1011 0100
x - 1  = 1011 0011     lowest 1 became 0; trailing 0s became 1s
x & (x-1) = 1011 0000  -> lowest set bit REMOVED
```

And since $-x = \sim x + 1 = \sim(x - 1)$, the negation flips every bit *above* the lowest 1 while leaving it and the zeros below it intact:

```text
x      = 1011 0100
-x     = 0100 1100     (as two's complement)
x & -x = 0000 0100     -> lowest set bit ISOLATED
```

| Expression | Effect | Typical use |
|---|---|---|
| `x & (x - 1)` | Clears the lowest set bit | Popcount loop; power-of-two test |
| `x & -x` | Isolates the lowest set bit | Fenwick trees; splitting by a differing bit |
| `(x & (x - 1)) == 0` | True iff $x$ has at most one set bit | `x > 0 and (x & (x - 1)) == 0` tests powers of two |

### Counting bits

```python
def popcount(x: int) -> int:
    """Kernighan's method: one iteration per SET bit, not per bit."""
    count = 0
    while x:
        x &= x - 1
        count += 1
    return count
```

In practice use the built-ins: `x.bit_count()` (Python 3.10+) for the number of 1s, and `x.bit_length()` for the position of the highest 1 plus one — that is, $\lfloor \log_2 x \rfloor + 1$ for $x > 0$.

To count bits for **every** number from $0$ to $n$ (LC 338), don't call popcount $n$ times. Dropping the last bit of $i$ gives $i \gg 1$, whose answer is already known:

```python
def count_bits(n: int) -> list[int]:
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits
```

That's a tiny dynamic program: each answer is built from a smaller, already-solved one.

---

## Bit Vectors: Integers as Sets

When the universe is small and fixed — the 26 lowercase letters, the 9 digits of a Sudoku row, the $n \le 20$ items of a search problem — an integer is an excellent set.

| Set operation | Bit vector | Python `set` |
|---|---|---|
| $\{\}$, universe $U$ | `0`, `(1 << n) - 1` | `set()`, `set(range(n))` |
| $i \in S$ | `S >> i & 1` | `i in S` |
| $S \cup \{i\}$, $S \setminus \{i\}$ | `S | 1 << i`, `S & ~(1 << i)` | `S | {i}`, `S - {i}` |
| $S \cup T$, $S \cap T$, $S \setminus T$ | `S | T`, `S & T`, `S & ~T` | `S | T`, `S & T`, `S - T` |
| $S \subseteq T$ | `(S & ~T) == 0` | `S <= T` |
| $\lvert S \rvert$ | `S.bit_count()` | `len(S)` |
| Hashable key for memoization | Already an `int` | Needs `frozenset` |

Bit vectors are compact and every operation is a single word operation for $n \le 64$. Their weakness is sparse sets over large universes: listing the members of a nearly empty bit vector still means scanning all $n$ positions. For large, sparse universes, use a hash set.

!!! example "Bit vectors in practice"
    - **Valid Sudoku (LC 36):** one 9-bit mask per row, column, and box.
    - **Maximum Product of Word Lengths (LC 318):** precompute each word's 26-bit letter mask; two words share no letters iff `(mask1 & mask2) == 0`. That turns an $O(L)$ comparison into $O(1)$.
    - **Memoizing on a set of visited items:** a bitmask is a hashable `int`, so it works directly as a `dict` key or `lru_cache` argument.

### Word-level parallelism: bitsets as a speedup

Python's unbounded integers make a surprisingly powerful trick available. Take **Partition Equal Subset Sum (LC 416)**: can the numbers be split into two halves of equal sum? The standard DP tracks the set of reachable subset sums. Represent that set as the bits of one big integer — bit $s$ is 1 iff sum $s$ is reachable. Adding a number $x$ to every reachable sum is a *shift*:

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    reachable = 1                          # only sum 0 is reachable
    for x in nums:
        reachable |= reachable << x        # old sums, plus old sums + x
    return bool((reachable >> (total // 2)) & 1)
```

The DP is the same $O(n \cdot S)$ in principle, but each step processes $S$ sums with a handful of word-sized operations implemented in C, so it typically runs an order of magnitude or more faster than a list-of-booleans version.

---

## Generating Subsets

Every subset-search problem needs a systematic way to visit all $2^n$ subsets. Three orders are useful.

### Binary counting

Counting from $0$ to $2^n - 1$ visits every $n$-bit string exactly once, and hence every subset exactly once. This bijection between integers and subsets is the key to all subset-generation problems.

```python
def all_subsets(items: list[int]) -> list[list[int]]:
    n = len(items)
    return [
        [items[i] for i in range(n) if mask >> i & 1]
        for mask in range(1 << n)
    ]
```

**Time:** $O(n \cdot 2^n)$. Remember the practical limit from [Complexity Analysis](01_complexity_analysis.md): $2^{20} \approx 10^6$ is comfortable, $2^{30} \approx 10^9$ is not.

The bijection also gives **ranking** (subset → integer: set the bits of its members) and **unranking** (integer → subset: read off its bits). So "the next subset" is just `mask + 1`, and "a random subset" is `random.getrandbits(n)`.

### Gray code: minimum-change order

In a **Gray code**, consecutive subsets differ by exactly one element. That matters when the cost of evaluating a subset can be *updated* incrementally: moving to the next subset is then one insertion or deletion instead of a full recomputation.

The recursive construction is elegant: take the Gray code for $n - 1$ bits, follow it with a **reflected** (reversed) copy with bit $n-1$ set. The two halves meet at a single flipped bit, and the reflection guarantees the rest stays one-change-apart. The closed form is even shorter:

```python
def gray_code(n: int) -> list[int]:
    """LC 89: the i-th Gray code is i XOR (i >> 1)."""
    return [i ^ (i >> 1) for i in range(1 << n)]
```

### Submasks of a mask

To iterate over every subset of a given set `mask` (not of the whole universe), use `sub = (sub - 1) & mask`. Subtracting 1 decrements the number, and the `& mask` throws away bits outside `mask` — so this counts down through exactly the submasks, in decreasing order:

```python
def submasks(mask: int) -> list[int]:
    result = []
    sub = mask
    while True:
        result.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    return result
```

If you iterate over the submasks of *every* mask of $n$ bits, the total work is not $4^n$ but $3^n$: each element is independently either outside the mask, in the mask but not the submask, or in both. This bound is what makes "DP over subsets of subsets" feasible for $n \le 15$ or so.

!!! tip "Take-Home Lesson"
    Every subset of $\{0, \dots, n-1\}$ *is* an integer in $[0, 2^n)$. Once you internalize that, enumerating subsets is a `for` loop, a set of visited items is a dictionary key, and "all subsets" dynamic programming (see [Dynamic Programming](15_dynamic_programming.md)) is ordinary DP with integer states.

---

## Classic Problems

### Single Number III (LC 260): two unique elements

Every element appears twice except **two**, $a$ and $b$. XOR-ing everything gives $a \oplus b \ne 0$. Any set bit of $a \oplus b$ is a position where $a$ and $b$ differ — so it partitions the input into two groups, each containing exactly one of them (and pairs of duplicates, which stay together and cancel).

```python
def single_number_iii(nums: list[int]) -> list[int]:
    both = reduce(xor, nums, 0)
    diff = both & -both                  # any bit where a and b differ
    a = 0
    for x in nums:
        if x & diff:
            a ^= x
    return [a, both ^ a]
```

### Single Number II (LC 137): everything appears three times

XOR cancels pairs, not triples. Generalize instead: look at each bit position independently. Each triplicate contributes 0 or 3 to that position's count of 1s, so the count **modulo 3** is the unique element's bit.

```python
def single_number_ii(nums: list[int]) -> int:
    result = 0
    for i in range(32):
        if sum((x >> i) & 1 for x in nums) % 3:
            result |= 1 << i
    return to_signed32(result)
```

This works for any repetition count $k$: replace 3 with $k$. There is a slicker $O(1)$-state solution that encodes the count mod 3 in two bitmasks (`ones`, `twos`), but the counting version is easier to get right and to explain.

### Reverse bits (LC 190)

Shift bits out of the bottom of `n` and into the bottom of the result:

```python
def reverse_bits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

### Bitwise AND of a range (LC 201)

The AND of all integers in $[m, n]$ keeps only the **common binary prefix** of $m$ and $n$: below the first position where they differ, the range passes through both a 0 and a 1 in every lower bit. Strip low bits until they agree:

```python
def range_bitwise_and(m: int, n: int) -> int:
    shift = 0
    while m != n:
        m >>= 1
        n >>= 1
        shift += 1
    return m << shift
```

### Maximum XOR of two numbers (LC 421)

For each number, greedily prefer the opposite bit at each position from the top down. A binary trie over the bits answers "is there a number with this prefix?" in $O(\text{bits})$. See [Trie & Union Find](12_trie_union_find.md).

---

## Common Mistakes

1. **Operator precedence.** `x & 1 == 0`, `a ^ b > 0`, `mask & 1 << i` — in Python the first two are wrong (comparisons bind tighter than `&`/`^`); the third happens to be right (`<<` binds tighter than `&`). Parenthesize everything.

2. **Forgetting Python's infinite width.** `~x` is `-x - 1`, not a 32-bit complement. Negative numbers have infinitely many leading 1s, so loops like `while x: x >>= 1` never terminate for negative `x`. Mask with `0xFFFFFFFF` whenever a problem assumes fixed width.

3. **Assuming bit loops are $O(1)$.** Iterating over the bits of $n$ is $O(\log n)$. Iterating over all $2^n$ masks is exponential — respect the $n \le 20$ rule.

4. **Using a bit vector on a sparse, large universe.** A 10⁶-bit integer representing a 3-element set wastes memory and makes iteration slow. Use a `set`.

5. **Reaching for bit tricks when clarity is cheaper.** `x % 2` and `x // 2` are as fast as `x & 1` and `x >> 1` in Python, and read better. Use bits when they express the idea (sets, XOR cancellation, masks), not as micro-optimization.

---

## Practice Problems

| Problem | Idea |
|---|---|
| Single Number (LC 136) | XOR cancellation |
| Missing Number (LC 268) | XOR with the full range |
| Number of 1 Bits (LC 191) | `x & (x - 1)` |
| Counting Bits (LC 338) | `bits[i >> 1] + (i & 1)` |
| Reverse Bits (LC 190) | Shift out, shift in |
| Sum of Two Integers (LC 371) | XOR + carries, 32-bit masking |
| Single Number II (LC 137) | Per-bit count mod 3 |
| Single Number III (LC 260) | Split by a differing bit |
| Subsets (LC 78) | Binary counting |
| Gray Code (LC 89) | `i ^ (i >> 1)` |
| Bitwise AND of Numbers Range (LC 201) | Common prefix |
| Maximum Product of Word Lengths (LC 318) | Letter masks |
| Partition Equal Subset Sum (LC 416) | Bitset of reachable sums |
| Maximum XOR of Two Numbers (LC 421) | Binary trie, greedy by bit |
