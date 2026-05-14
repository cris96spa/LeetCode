# Combinatorics Reference

## Formulas at a Glance

| Concept | Order Matters? | Repetition? | Formula | Example |
|---|---|---|---|---|
| Permutation | Yes | No | P(n,r) = n!/(n-r)! | Arrange 3 of 5 people: 60 |
| Permutation | Yes | Yes | n^r | 3-digit PIN, digits 0-9: 1000 |
| Combination | No | No | C(n,r) = n!/(r!(n-r)!) | Choose 3 of 5 people: 10 |
| Combination | No | Yes | C(n+r-1, r) | 3 scoops from 5 flavors: 35 |

---

## Permutations

### Without Repetition: P(n, r) = n! / (n-r)!

Choose r items from n, order matters, no reuse.

**Intuition:** n choices for the first slot, n-1 for the second, ..., n-r+1 for the last.

**Example:** How many ways to award gold/silver/bronze to 8 athletes?
P(8, 3) = 8 * 7 * 6 = 336.

Special case: P(n, n) = n! (arrange all n items).

### With Repetition: n^r

Choose r items from n, order matters, reuse allowed.

**Intuition:** n independent choices, each with n options.

**Example:** 4-digit PIN using digits 0-9: 10^4 = 10,000.

### Permutations of a Multiset: n! / (n1! * n2! * ... * nk!)

Arrange n items where some are identical.

**Intuition:** Start with n! total arrangements, then divide out the indistinguishable rearrangements within each group.

**Example:** Arrangements of MISSISSIPPI (11 letters: 1M, 4I, 4S, 2P):
11! / (1! * 4! * 4! * 2!) = 34,650.

---

## Combinations

### Without Repetition: C(n, r) = n! / (r!(n-r)!)

Choose r items from n, order does not matter, no reuse.

**Intuition:** Take the permutation count P(n,r) and divide by r! to remove ordering.

**Example:** Choose a 3-person committee from 10 people: C(10,3) = 120.

### With Repetition (Stars and Bars): C(n+r-1, r)

Choose r items from n types, order does not matter, reuse allowed.

**Intuition:** Equivalent to placing r identical balls into n distinct bins. The r balls are "stars" and n-1 dividers are "bars".

**Example:** Buy 5 donuts from 3 flavors: C(3+5-1, 5) = C(7, 5) = 21.

---

## Key Identities

| Identity | Formula | Intuition |
|---|---|---|
| Symmetry | C(n,r) = C(n, n-r) | Choosing r to include = choosing n-r to exclude |
| Pascal's Rule | C(n,r) = C(n-1,r-1) + C(n-1,r) | Element n is either in the subset or not |
| Sum of row | C(n,0) + C(n,1) + ... + C(n,n) = 2^n | Total number of subsets of n elements |
| Vandermonde | C(m+n, r) = sum of C(m,k)*C(n,r-k) | Choose r items from two groups |
| Hockey stick | C(r,r) + C(r+1,r) + ... + C(n,r) = C(n+1,r+1) | Sum along a diagonal of Pascal's triangle |

**Pascal's Rule** is particularly useful in DP -- it gives the recurrence for computing C(n,r) without factorials:

```python
# Build Pascal's triangle for C(n, r) values
def build_pascal(n):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1
        for j in range(1, i + 1):
            dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
    return dp
```

---

## Connection to Coding Patterns

| Math Concept | Count | Coding Pattern | Key Mechanism |
|---|---|---|---|
| All subsets | 2^n | Backtracking with start index, or bitmask | Include/exclude each element |
| Permutations | n! | Backtracking with visited array | Try each unused element at each position |
| Combinations C(n,r) | C(n,r) | Backtracking with start index, stop at size r | Same as subsets but with length constraint |
| Stars and bars | C(n+r-1, r) | Unbounded knapsack / coin change DP | Each "type" can be used multiple times |
| Multiset permutations | n!/(n1!...nk!) | Backtracking, sort + skip duplicates | Avoid counting identical arrangements |

This is why complexity analysis of backtracking problems maps directly to combinatorial formulas:
- Subsets: O(n * 2^n) because there are 2^n subsets.
- Permutations: O(n * n!) because there are n! permutations.
- Combinations of size k: O(k * C(n,k)).

---

## Catalan Numbers

**Formula:** C_n = C(2n, n) / (n + 1)

**Recurrence:** C_0 = 1, C_n = sum of C_i * C_{n-1-i} for i in 0..n-1

**First values:** 1, 1, 2, 5, 14, 42, 132, 429, 1430

Catalan numbers appear whenever a problem involves recursively splitting something into two parts:

| Problem | n | C_n counts |
|---|---|---|
| Balanced parentheses | pairs | valid arrangements |
| Distinct BSTs | nodes | structurally unique trees (LC 96) |
| Triangulations | polygon sides - 2 | ways to triangulate |
| Full binary trees | internal nodes | distinct trees |
| Dyck paths | steps | paths that don't cross below diagonal |
| Matrix chain multiplication | matrices - 1 | ways to parenthesize |

```python
# Compute n-th Catalan number with DP
def catalan(n):
    if n <= 1:
        return 1
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        for j in range(i):
            dp[i] += dp[j] * dp[i - 1 - j]
    return dp[n]
```

---

## Pigeonhole Principle

**Statement:** If n items are placed into m containers and n > m, at least one container has more than one item.

Sounds trivial, but it's the key insight for several problems:

- **Find the Duplicate Number (LC 287):** n+1 numbers in range [1, n]. By pigeonhole, at least one value repeats. This justifies the Floyd's cycle detection approach.
- **Existence arguments:** Proving that a collision/duplicate must exist without finding it directly.
- **Generalized form:** If n items go into m containers, some container has at least ceil(n/m) items. Useful for bounding worst cases.
