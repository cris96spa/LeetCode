# Combinatorics

Counting is the quiet partner of algorithm design. You count to know whether exhaustive search is feasible ($2^{20}$ subsets: yes; $20!$ permutations: no). You count to analyze algorithms (how many nodes does this search tree have?). Many problems simply *are* counting problems — "how many ways..." — usually solved with dynamic programming. And recognizing which combinatorial object a problem is really about is often the key step toward a solution.

This chapter collects the counting tools that come up again and again: the basic rules, the standard formulas and where they come from, the important number families, how to generate and index combinatorial objects, and the probability needed to reason about randomized algorithms.

---

## Modeling: Which Object Is This?

Most algorithmic problems are secretly about a handful of fundamental structures. The words in the problem statement are often a strong hint:

| Object | Keywords that suggest it | Typical count |
|---|---|---|
| **Permutation** | arrangement, ordering, tour, sequence, schedule, ranking | $n!$ |
| **Subset** | selection, group, committee, cluster, collection, packing | $2^n$, or $\binom{n}{k}$ |
| **Tree** | hierarchy, ancestor, dominance, taxonomy, nesting | Catalan numbers (binary trees) |
| **Graph** | network, relationship, connection, circuit, web | $2^{\binom{n}{2}}$ labeled graphs |
| **String** | text, pattern, label, sequence of symbols | $\lvert\Sigma\rvert^n$ |
| **Partition** | split into groups, clustering, coloring | Stirling / Bell numbers |

!!! tip "Take-Home Lesson"
    Modeling your problem in terms of well-defined structures — permutations, subsets, trees, graphs, strings — is the most important single step toward a solution. Once you know which object you're dealing with, you know how to count it, how to enumerate it, and which algorithms already exist for it.

---

## The Basic Counting Rules

Almost every counting argument is built from a few rules.

| Rule | Statement | Example |
|---|---|---|
| **Sum rule** | If choices come from disjoint cases, add the counts | A password is 4 or 5 digits: $10^4 + 10^5$ |
| **Product rule** | If a choice is a sequence of independent steps, multiply | A 3-letter code: $26^3$ |
| **Complement** | Count what you *don't* want, subtract from the total | Strings of length $n$ with at least one `a`: $26^n - 25^n$ |
| **Division rule** | If every outcome is counted exactly $k$ times, divide by $k$ | Seatings of $n$ people at a round table: $n!/n = (n-1)!$ |
| **Bijection** | If two sets can be matched one-to-one, they have the same size | Subsets of $n$ items ↔ $n$-bit strings: $2^n$ |
| **Inclusion–exclusion** | $\lvert A \cup B\rvert = \lvert A\rvert + \lvert B\rvert - \lvert A \cap B\rvert$ | Numbers $\le 100$ divisible by 2 or 3: $50 + 33 - 16 = 67$ |

The **bijection** rule deserves special mention: much of combinatorial cleverness is finding a way to see an unfamiliar set as a familiar one in disguise. Stars and bars, below, is a bijection. So is the observation that subsets are binary strings (see [Bit Manipulation](04_bit_manipulation.md#generating-subsets)).

---

## Permutations and Combinations

| Choose $r$ from $n$... | Order matters | Order doesn't matter |
|---|---|---|
| **without repetition** | $P(n, r) = \dfrac{n!}{(n-r)!}$ | $\dbinom{n}{r} = \dfrac{n!}{r!\,(n-r)!}$ |
| **with repetition** | $n^r$ | $\dbinom{n + r - 1}{r}$ |

**Permutations without repetition.** By the product rule: $n$ choices for the first position, $n - 1$ for the second, ..., $n - r + 1$ for the last. Gold, silver, and bronze among 8 athletes: $8 \cdot 7 \cdot 6 = 336$.

**Combinations.** Each unordered selection of $r$ items appears $r!$ times among the ordered ones, so divide (the division rule): $\binom{n}{r} = P(n, r) / r!$. A 3-person committee from 10 people: $\binom{10}{3} = 120$.

**With repetition, ordered.** $r$ independent choices of $n$ options each: $n^r$. A 4-digit PIN: $10^4$.

**Multiset permutations.** Arrangements of $n$ items with $n_1$ identical copies of one kind, $n_2$ of another, ...: $\dfrac{n!}{n_1!\, n_2! \cdots n_k!}$. Swapping identical items doesn't create a new arrangement, so divide out those swaps. The letters of MISSISSIPPI (1 M, 4 I, 4 S, 2 P) have $\frac{11!}{1!\,4!\,4!\,2!} = 34{,}650$ arrangements.

### Stars and bars: combinations with repetition

How many ways to buy 5 donuts from 3 flavors? Write any purchase as a row of 5 stars (donuts) and 2 bars (dividers between flavors):

```text
★★|★|★★     =  2 of flavor A, 1 of flavor B, 2 of flavor C
★★★★★||     =  5 of flavor A
```

Every purchase is exactly one arrangement of 5 stars and 2 bars, and vice versa — a bijection. So the answer is the number of ways to choose which 2 of the 7 positions hold bars: $\binom{7}{2} = 21$. In general, $r$ items from $n$ types: $\binom{n + r - 1}{n - 1} = \binom{n + r - 1}{r}$.

The same argument counts the solutions of $x_1 + x_2 + \cdots + x_n = r$ in non-negative integers, which is how it appears in practice.

---

## Binomial Coefficients

$\binom{n}{k}$ is the most important family of counting numbers. Computing it from factorials is fine in Python (arbitrary precision), but in fixed-width languages the intermediate factorials overflow long before the answer does. The robust way is **Pascal's triangle**:

$$\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}, \qquad \binom{n}{0} = \binom{n}{n} = 1$$

**Why it's true** (a combinatorial proof, which is often clearer than algebra): fix one particular item. Every $k$-subset either **contains** it — then the other $k - 1$ items come from the remaining $n - 1$ — or it **doesn't** — then all $k$ come from the remaining $n - 1$. The cases don't overlap and cover everything, so add them. This is exactly the take-or-skip recurrence of [dynamic programming](15_dynamic_programming.md), and Pascal's triangle is its table.

```python
def pascal(n: int) -> list[list[int]]:
    rows = [[1]]
    for _ in range(n):
        prev = rows[-1]
        rows.append([1] + [prev[i] + prev[i + 1] for i in range(len(prev) - 1)] + [1])
    return rows
```

In Python, `math.comb(n, k)` computes a single coefficient exactly and quickly.

**Lattice paths.** The number of monotone paths through an $m \times n$ grid (LC 62, Unique Paths) is $\binom{m + n - 2}{m - 1}$: a path is a sequence of $m - 1$ downs and $n - 1$ rights, and choosing the positions of the downs determines it. The DP and the formula compute the same Pascal's triangle.

### Useful identities

| Identity | Formula | Why |
|---|---|---|
| Symmetry | $\binom{n}{k} = \binom{n}{n-k}$ | Choosing what to include = choosing what to exclude |
| Row sum | $\sum_k \binom{n}{k} = 2^n$ | Counting all subsets by size |
| Vandermonde | $\binom{m+n}{r} = \sum_k \binom{m}{k}\binom{n}{r-k}$ | Choose $r$ from two groups: $k$ from the first, the rest from the second |
| Hockey stick | $\sum_{i=r}^{n} \binom{i}{r} = \binom{n+1}{r+1}$ | Classify $(r+1)$-subsets of $\{0..n\}$ by their largest element |
| Binomial theorem | $(x + y)^n = \sum_k \binom{n}{k} x^k y^{n-k}$ | Choose which factors contribute an $x$ |

### Counting modulo a prime

When answers are huge, problems ask for them modulo $p = 10^9 + 7$. Precompute factorials and their inverses once; then each $\binom{n}{k}$ costs $O(1)$. Since $p$ is prime, Fermat's little theorem gives the inverse: $a^{-1} \equiv a^{p-2} \pmod p$.

```python
MOD = 10**9 + 7


def binomial_table(limit: int):
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (limit + 1)
    inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)     # Fermat inverse, O(log MOD)
    for i in range(limit, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def comb_mod(n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD

    return comb_mod
```

---

## Important Number Families

### Catalan numbers

$$C_0 = 1, \qquad C_{n} = \sum_{i=0}^{n-1} C_i \, C_{n-1-i}, \qquad C_n = \frac{1}{n+1}\binom{2n}{n}$$

Values: 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, ...

Catalan numbers count structures that **split into two independent smaller structures of the same kind**. For balanced parentheses: a string of $n$ pairs starts with `(` and its matching `)` encloses a balanced string of $i$ pairs, followed by a balanced string of the remaining $n - 1 - i$. Sum over $i$ — that's the recurrence. The same decomposition, "root plus left part plus right part," appears in all of these:

| Structure of size $n$ | Counted by $C_n$ |
|---|---|
| Balanced strings of $n$ pairs of parentheses (LC 22) | $C_n$ |
| Structurally distinct BSTs with $n$ keys (LC 96) | $C_n$ |
| Full binary trees with $n + 1$ leaves | $C_n$ |
| Ways to parenthesize a product of $n + 1$ factors | $C_n$ |
| Triangulations of a convex polygon with $n + 2$ sides | $C_n$ |
| Monotone lattice paths that never cross the diagonal | $C_n$ |

```python
def num_trees(n: int) -> int:
    """LC 96: C_n, via the root-splits-into-two recurrence."""
    catalan = [1] + [0] * n
    for m in range(1, n + 1):
        catalan[m] = sum(catalan[i] * catalan[m - 1 - i] for i in range(m))
    return catalan[n]
```

The closed form comes from the **reflection principle**: of the $\binom{2n}{n}$ lattice paths from $(0,0)$ to $(n,n)$, the ones that cross the diagonal can be put in bijection with all paths to $(n-1, n+1)$ — reflect each bad path after its first crossing — so the good ones number $\binom{2n}{n} - \binom{2n}{n+1} = \frac{1}{n+1}\binom{2n}{n}$.

### More families worth recognizing

| Family | Counts | Recurrence |
|---|---|---|
| **Fibonacci** $F_n$ | Tilings of a $1 \times n$ strip with $1 \times 1$ and $1 \times 2$ tiles; ways to climb $n$ stairs by 1s and 2s | $F_n = F_{n-1} + F_{n-2}$ |
| **Derangements** $D_n$ | Permutations with no fixed point | $D_n = (n - 1)(D_{n-1} + D_{n-2})$, $D_n \approx n!/e$ |
| **Stirling numbers (2nd kind)** $S(n, k)$ | Partitions of $n$ labeled items into $k$ non-empty groups | $S(n, k) = k\,S(n-1, k) + S(n-1, k-1)$ |
| **Bell numbers** $B_n$ | All partitions of $n$ labeled items | $B_n = \sum_k S(n, k)$ |
| **Integer partitions** $p(n)$ | Ways to write $n$ as an unordered sum of positive integers | Coin-change counting with coins $1 \dots n$ |

Each recurrence comes from asking **what happens to the last item**. For Stirling numbers: item $n$ either joins one of the $k$ groups formed by the others ($k \cdot S(n-1, k)$) or sits alone in a new group ($S(n-1, k-1)$). For derangements: item $n$ goes to some position $i$ ($n - 1$ choices); then either item $i$ goes to position $n$ (swap, leaving $D_{n-2}$) or it doesn't (effectively a derangement of $n - 1$). It's the same reasoning as a DP recurrence, because it *is* one.

---

## Generating and Indexing Combinatorial Objects

### Ranking and unranking

To enumerate, sample, or index a family of objects, it helps to put them in a fixed order and define two inverse functions:

- **rank**(object): its position in the order, from $0$ to $N - 1$.
- **unrank**(position): the object at that position.

With these, "the next object" is `unrank(rank(x) + 1)`, "a uniformly random object" is `unrank(random integer)`, and a set of objects can be stored as a bit vector over ranks.

For permutations in lexicographic order, the first element splits the $n!$ permutations into $n$ blocks of $(n-1)!$ each, so

$$\text{rank}(p) = (\text{index of } p_1 \text{ among remaining items}) \cdot (n - 1)! + \text{rank}(p_2, \ldots, p_n)$$

Unranking reverses this: divide by $(n - 1)!$ to find the first element, and recurse on the remainder. This is exactly **Permutation Sequence** (LC 60), the $k$-th permutation:

```python
from math import factorial


def get_permutation(n: int, k: int) -> str:
    """LC 60: the k-th (1-indexed) permutation of 1..n in lexicographic order."""
    items = [str(i) for i in range(1, n + 1)]
    k -= 1                                            # to a 0-indexed rank
    out = []
    for size in range(n, 0, -1):
        block = factorial(size - 1)                   # permutations per first choice
        i, k = divmod(k, block)
        out.append(items.pop(i))
    return "".join(out)


def rank_permutation(p: list[int]) -> int:
    items = sorted(p)
    rank = 0
    for i, x in enumerate(p):
        idx = items.index(x)
        rank += idx * factorial(len(p) - 1 - i)
        items.pop(idx)
    return rank
```

(The digits $i$ chosen along the way are the permutation's **factorial number system** representation.)

### Next permutation (LC 31)

To step to the next permutation in lexicographic order without ranking: find the longest non-increasing suffix — it's already the *last* arrangement of those elements. The element just before it, the **pivot**, must increase by as little as possible: swap it with the smallest suffix element larger than it, then reverse the suffix to make it the *first* arrangement.

```python
def next_permutation(nums: list[int]) -> None:
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1                                        # nums[i+1:] is non-increasing
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1                                    # smallest element > pivot in the suffix
        nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1:] = reversed(nums[i + 1:])             # suffix back to ascending order
```

Amortized $O(1)$ per step, and it handles duplicates correctly. This is how C++'s `std::next_permutation` works. Python's `itertools.permutations`, by contrast, permutes *positions*, so it repeats arrangements when the input contains duplicates.

### Random permutations: the Fisher–Yates shuffle

Generating a uniformly random permutation is a small problem that people often get wrong. The correct algorithm (LC 384) is two lines: for each position $i$ from left to right, swap in a random element from positions $i$ **through the end**.

```python
import random


def shuffle(a: list) -> None:
    for i in range(len(a) - 1):
        j = random.randint(i, len(a) - 1)            # i..n-1, NOT 0..n-1
        a[i], a[j] = a[j], a[i]
```

Why uniform? Position 0 receives each element with probability $1/n$; given that, position 1 receives each remaining element with probability $1/(n - 1)$; and so on. Every permutation arises with probability $\frac{1}{n} \cdot \frac{1}{n-1} \cdots = \frac{1}{n!}$.

??? question "Stop and Think: Why is the naive shuffle biased?"
    **Problem:** What's wrong with swapping each position with a random position from the **whole** array, `j = random.randint(0, n - 1)`?

    **Solution:** It makes $n$ independent choices of $n$ options, so it has $n^n$ equally likely execution paths. Each path produces one permutation, so a permutation's probability is (number of paths producing it)$/ n^n$. For the result to be uniform, each of the $n!$ permutations would need exactly $n^n / n!$ paths — but $n!$ doesn't divide $n^n$ for $n \ge 3$: the factor $n - 1$ of $n!$ shares no prime factor with $n^n$ (for $n = 3$: 6 doesn't divide 27). So some permutations must be more likely than others, no matter how good the random number generator is.

---

## The Pigeonhole Principle

> If $n$ items are placed into $m < n$ boxes, some box contains at least two items. More generally, some box contains at least $\lceil n / m \rceil$ items.

It sounds too obvious to be useful, but it proves existence without construction:

- **Find the Duplicate Number** (LC 287): $n + 1$ values from $\{1, \ldots, n\}$ must include a repeat. Treating the array as a function $i \mapsto \text{nums}[i]$, that repeat is the entrance to a cycle, found by [Floyd's algorithm](06_linked_lists.md#cycle-detection-floyds-tortoise-and-hare).
- **Maximum Gap** (LC 164): with $n$ numbers spanning a range $R$, some gap is at least $R/(n - 1)$, so the answer never lies inside a bucket of that width (see [Sorting](05_sorting.md#bucketing-in-interviews)).
- **Hashing:** with more keys than buckets, collisions are guaranteed; the question is only how many.
- **Prefix sums mod $k$:** among any $k + 1$ prefix sums, two agree modulo $k$, so some non-empty subarray has a sum divisible by $k$.

---

## Probability Essentials

Randomized algorithms (quicksort, hashing, sampling) are analyzed with a small amount of probability.

- A **sample space** is the set of possible outcomes; an **event** is a subset of it. With equally likely outcomes, $P(E) = |E| / |S|$ — probability is counting.
- **Complement:** $P(E) = 1 - P(\bar E)$, often the easier side to compute.
- **Union:** $P(A \cup B) = P(A) + P(B) - P(A \cap B)$.
- **Independence:** $A$ and $B$ are independent if $P(A \cap B) = P(A)\,P(B)$. Independent events let you multiply.
- **Conditional probability:** $P(A \mid B) = P(A \cap B) / P(B)$, and **Bayes' theorem** reverses it: $P(B \mid A) = P(A \mid B)\,P(B) / P(A)$.

**The birthday paradox.** With $n$ people and 365 days, the probability that all birthdays differ is $\prod_{i=0}^{n-1} (1 - i/365)$, which drops below $1/2$ at just $n = 23$. The same computation says that hashing about $\sqrt{m}$ keys into $m$ buckets already makes a collision likely — which is why hash tables must handle collisions rather than hope to avoid them.

### Linearity of expectation

The **expected value** of a random quantity is its probability-weighted average. The single most useful fact about it:

$$E[X + Y] = E[X] + E[Y] \qquad \text{always — even when } X \text{ and } Y \text{ are dependent.}$$

This lets you compute complicated expectations by breaking a quantity into simple **indicator** pieces (1 if something happens, 0 if not), whose expectations are just probabilities:

- **Fixed points of a random permutation:** position $i$ keeps its element with probability $1/n$. Summing over the $n$ positions, the expected number of fixed points is exactly 1 — for every $n$.
- **Coupon collector:** collecting all $n$ coupons, when each draw is uniformly random, takes $n\left(1 + \frac12 + \cdots + \frac1n\right) = n H_n \approx n \ln n$ draws on average. After $i$ distinct coupons, each draw is new with probability $(n - i)/n$, so that phase takes $n/(n - i)$ draws on average; add the phases.
- **Randomized quicksort:** elements $i$ and $j$ (in sorted order) are compared iff one of them is the first pivot chosen among $i, \ldots, j$, which has probability $2/(j - i + 1)$. Summing over all pairs gives about $2n \ln n$ comparisons.

### Sampling from a stream: reservoir sampling

To pick a uniformly random element from a stream of unknown length in one pass with $O(1)$ memory (LC 382, LC 398): keep the $i$-th element with probability $1/i$, replacing the current choice.

```python
def reservoir_sample(stream) -> object:
    chosen = None
    for i, x in enumerate(stream, start=1):
        if random.randrange(i) == 0:                  # probability 1/i
            chosen = x
    return chosen
```

**Why uniform?** Element $i$ is chosen at step $i$ with probability $1/i$, then survives each later step $j$ with probability $(j - 1)/j$. The product telescopes: $\frac{1}{i} \cdot \frac{i}{i+1} \cdot \frac{i+1}{i+2} \cdots \frac{n-1}{n} = \frac{1}{n}$.

**Weighted sampling** (LC 528): pick index $i$ with probability proportional to $w_i$. Build prefix sums of the weights, draw a uniform number in $[0, \text{total})$, and binary search for the first prefix sum exceeding it.

```python
import bisect
import itertools


class WeightedPicker:
    def __init__(self, weights: list[int]) -> None:
        self.prefix = list(itertools.accumulate(weights))

    def pick_index(self) -> int:
        target = random.random() * self.prefix[-1]
        return bisect.bisect_right(self.prefix, target)
```

---

## From Counts to Code

The counts above are exactly the sizes of the search spaces in [Combinatorial Search](13_combinatorial_search.md), which is why they give the running times of the corresponding algorithms:

| Object | Count | Generate with | Time to generate all |
|---|---|---|---|
| All subsets | $2^n$ | Choose-next backtracking, or bitmasks | $O(n \cdot 2^n)$ |
| $k$-subsets | $\binom{n}{k}$ | Choose-next backtracking with a size limit | $O(k \binom{n}{k})$ |
| Permutations | $n!$ | Backtracking with `used` flags, or next-permutation | $O(n \cdot n!)$ |
| Multiset permutations | $\frac{n!}{n_1! \cdots n_k!}$ | Sort + skip equal siblings | $O(n \cdot \text{count})$ |
| Balanced parentheses | $C_n \approx \frac{4^n}{n^{3/2}\sqrt{\pi}}$ | Backtracking with open/close counts | $O(n \cdot C_n)$ |
| Solutions of $x_1 + \cdots + x_n = r$ | $\binom{n+r-1}{r}$ | Unbounded-knapsack-style recursion | $O(n \cdot \text{count})$ |

When a problem only asks *how many*, don't generate — count with a formula or a DP.

---

## Common Mistakes

1. **Confusing ordered and unordered counts.** "How many ways to pick 3 people" ($\binom{n}{3}$) vs. "to pick a president, VP, and treasurer" ($P(n, 3)$). Ask whether swapping two choices produces a different outcome.

2. **Double counting.** Counting "at least one" as "pick one, then anything" overcounts outcomes with several. Use the complement, or inclusion–exclusion.

3. **Forgetting the modulus at every step.** Reduce after each multiplication and addition, not only at the end. And never *divide* modulo $p$ — multiply by the modular inverse.

4. **Overflowing factorials.** Irrelevant in Python, fatal in Java and C++. Use Pascal's triangle or modular arithmetic.

5. **The naive shuffle.** Swapping with a random position from the whole array is biased. Use Fisher–Yates: random position from $i$ to the end.

6. **Assuming independence.** Multiplying probabilities is valid only for independent events. Linearity of expectation, by contrast, never needs independence.

---

## Practice Problems

| Problem | Idea |
|---|---|
| Unique Paths (LC 62) | $\binom{m+n-2}{m-1}$ or Pascal DP |
| Pascal's Triangle (LC 118) | Pascal's rule |
| Unique Binary Search Trees (LC 96) | Catalan numbers |
| Generate Parentheses (LC 22) | Enumerate Catalan structures |
| Permutation Sequence (LC 60) | Unranking via factorials |
| Next Permutation (LC 31) | Pivot, swap, reverse suffix |
| Shuffle an Array (LC 384) | Fisher–Yates |
| Linked List Random Node (LC 382) | Reservoir sampling |
| Random Pick with Weight (LC 528) | Prefix sums + binary search |
| Find the Duplicate Number (LC 287) | Pigeonhole + cycle detection |
| Count Sorted Vowel Strings (LC 1641) | Stars and bars: $\binom{n+4}{4}$ |
| Count Vowels Permutation (LC 1220) | Counting DP |
| Number of Music Playlists (LC 920) | Counting DP with inclusion–exclusion flavor |
