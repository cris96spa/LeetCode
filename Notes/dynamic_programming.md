# Dynamic Programming

## Recognizing DP Problems

A problem is likely DP if it has both:

1. **Optimal substructure** -- the optimal solution contains optimal solutions to subproblems.
2. **Overlapping subproblems** -- the same subproblems are solved multiple times in a naive recursive approach.

**DP vs Greedy:** Greedy makes one locally optimal choice and never reconsiders. DP considers all choices and picks the best. If a greedy counterexample exists (a local choice leads to a globally suboptimal result), you need DP.

**DP vs Divide and Conquer:** Both decompose problems. The difference is overlap -- divide and conquer subproblems are independent (merge sort), DP subproblems recur (Fibonacci).

Common signals: "minimum/maximum," "count the number of ways," "is it possible," "longest/shortest."

---

## The DP Framework (SRTBOT)

| Step | Question | Example (House Robber) |
|------|----------|----------------------|
| **S**tate | What does `dp[i]` represent? | Max money robbing houses `0..i` |
| **R**ecurrence | How does it relate to prior states? | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` |
| **T**opo order | What order to fill the table? | Left to right, `i = 0..n-1` |
| **B**ase case | Simplest cases? | `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])` |
| **O**ptimize | Can we reduce space? | Only need `dp[i-1]` and `dp[i-2]` -> O(1) |
| **T**est | Verify on small input | `[2,7,9,3,1]` -> 12 |

---

## Pattern 1: Linear DP

Current state depends on a small window of previous states. Often Fibonacci-like.

### Climbing Stairs (LC 70)

```python
def climbStairs(n: int) -> int:
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    return prev1
```

**Time:** O(n) -- **Space:** O(1)

### House Robber (LC 198)

```python
def rob(nums: List[int]) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = current

    return prev1
```

**Time:** O(n) -- **Space:** O(1)

---

## Pattern 2: Kadane's Algorithm

Sliding window DP for contiguous subarray problems. Track the best ending at the current position.

### Maximum Subarray (LC 53)

```python
def maxSubArray(nums: List[int]) -> int:
    max_sum = curr_sum = nums[0]

    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)

    return max_sum
```

**Time:** O(n) -- **Space:** O(1)

The key insight: at each position, either extend the current subarray or start fresh. If `curr_sum` drops below the current element, starting over is better.

### Maximum Product Subarray (LC 152)

Track both max and min at each position because a negative times a negative can become the max.

```python
def maxProduct(nums: List[int]) -> int:
    result = max_prod = min_prod = nums[0]

    for num in nums[1:]:
        if num < 0:
            max_prod, min_prod = min_prod, max_prod

        max_prod = max(num, max_prod * num)
        min_prod = min(num, min_prod * num)
        result = max(result, max_prod)

    return result
```

**Time:** O(n) -- **Space:** O(1)

---

## Pattern 3: Grid DP

2D grid, usually moving right/down. State: `dp[i][j]` = answer at cell `(i, j)`.

### Unique Paths (LC 62)

```python
def uniquePaths(m: int, n: int) -> int:
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[-1]
```

**Time:** O(m * n) -- **Space:** O(n) (rolling array)

### Minimum Path Sum (LC 64)

```python
def minPathSum(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j-1]
            elif j == 0:
                grid[i][j] += grid[i-1][j]
            else:
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])
    return grid[-1][-1]
```

**Time:** O(m * n) -- **Space:** O(1) (modifies input in place)

---

## Pattern 4: String DP

Two strings -> 2D table where `dp[i][j]` relates prefixes `s1[0:i]` and `s2[0:j]`.

### Longest Common Subsequence (LC 1143)

```python
def longestCommonSubsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev = curr

    return prev[n]
```

**Time:** O(m * n) -- **Space:** O(n)

### Edit Distance (LC 72)

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # delete
                    dp[i][j-1],      # insert
                    dp[i-1][j-1]     # replace
                )

    return dp[m][n]
```

**Time:** O(m * n) -- **Space:** O(m * n) (can optimize to O(n) with rolling row)

---

## Pattern 5: Knapsack

### 0/1 Knapsack (Classic)

Each item used at most once. Space-optimized: iterate capacity backwards.

```python
def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

**Time:** O(n * capacity) -- **Space:** O(capacity)

### Coin Change (LC 322)

Unbounded knapsack (each coin reusable). Iterate capacity forwards.

```python
def coinChange(coins: List[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

**Time:** O(amount * len(coins)) -- **Space:** O(amount)

### Coin Change II (LC 518)

Count number of combinations (not permutations). Outer loop over coins, inner over amounts.

```python
def change(amount: int, coins: List[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:           # iterate coins first to avoid counting permutations
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]

    return dp[amount]
```

**Time:** O(amount * len(coins)) -- **Space:** O(amount)

The loop order matters: coins-first counts combinations `{1,1,2}`, amounts-first would also count `{1,2,1}` and `{2,1,1}`.

---

## Pattern 6: Longest Increasing Subsequence

### LIS (LC 300)

**O(n^2) DP:**

```python
def lengthOfLIS(nums: List[int]) -> int:
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**O(n log n) with binary search:**

Maintain `tails` where `tails[i]` is the smallest tail element for an increasing subsequence of length `i+1`.

```python
from bisect import bisect_left

def lengthOfLIS(nums: List[int]) -> int:
    tails = []
    for num in nums:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)
```

**Time:** O(n log n) -- **Space:** O(n)

---

## Pattern 7: State Machine DP

Finite states with defined transitions. Common in stock problems.

### Best Time to Buy and Sell Stock with Cooldown (LC 309)

Three states: `hold` (holding stock), `sold` (just sold), `rest` (cooldown/idle).

```python
def maxProfit(prices: List[int]) -> int:
    if len(prices) <= 1:
        return 0

    hold = -prices[0]
    sold = 0
    rest = 0

    for i in range(1, len(prices)):
        prev_hold, prev_sold, prev_rest = hold, sold, rest
        hold = max(prev_hold, prev_rest - prices[i])
        sold = prev_hold + prices[i]
        rest = max(prev_rest, prev_sold)

    return max(sold, rest)
```

**Time:** O(n) -- **Space:** O(1)

### Multiple Transactions (LC 122)

```python
def maxProfit(prices: List[int]) -> int:
    cash, hold = 0, -prices[0]
    for i in range(1, len(prices)):
        cash = max(cash, hold + prices[i])
        hold = max(hold, cash - prices[i])
    return cash
```

**Time:** O(n) -- **Space:** O(1)

---

## Pattern 8: Interval DP

Process subarrays/substrings of increasing length. State: `dp[i][j]` for substring `s[i..j]`.

### Longest Palindromic Substring (LC 5)

```python
def longestPalindrome(s: str) -> str:
    n = len(s)
    if n < 2:
        return s

    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    for i in range(n):
        dp[i][i] = True

    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start, max_len = i, 2

    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                start, max_len = i, length

    return s[start:start + max_len]
```

**Time:** O(n^2) -- **Space:** O(n^2)

---

## Pattern 9: Tree DP

DP on tree structures. Each node returns information to its parent. Typically post-order traversal.

### House Robber III (LC 337)

Each node returns a pair: `(max if robbed, max if not robbed)`.

```python
def rob(root: TreeNode) -> int:
    def dfs(node):
        if not node:
            return (0, 0)  # (rob_this, skip_this)

        left = dfs(node.left)
        right = dfs(node.right)

        # Rob this node: can't rob children
        rob_this = node.val + left[1] + right[1]
        # Skip this node: take best of each child
        skip_this = max(left) + max(right)

        return (rob_this, skip_this)

    return max(dfs(root))
```

**Time:** O(n) -- **Space:** O(h) where h is tree height (call stack)

---

## Space Optimization Techniques

### Rolling Array

When `dp[i]` only depends on `dp[i-1]` (and maybe `dp[i-2]`), keep only the needed rows.

```python
# Full table: O(m*n) space
dp = [[0] * (n+1) for _ in range(m+1)]

# Rolling: O(n) space
prev = [0] * (n+1)
for i in range(1, m+1):
    curr = [0] * (n+1)
    # fill curr using prev
    prev = curr
```

### Two Variables

When only `dp[i-1]` and `dp[i-2]` are needed:

```python
prev2, prev1 = base0, base1
for i in range(2, n+1):
    current = f(prev1, prev2)
    prev2 = prev1
    prev1 = current
```

### 1D Knapsack Trick

For 0/1 knapsack, iterate capacity backwards to prevent reusing items:
```python
for w in range(capacity, weight - 1, -1):  # backwards = 0/1
```

For unbounded knapsack, iterate forwards:
```python
for w in range(weight, capacity + 1):       # forwards = unbounded
```

---

## Complexity Reference Table

| Pattern | Typical Time | Optimized Space |
|---------|-------------|----------------|
| Linear DP | O(n) | O(1) |
| Kadane's | O(n) | O(1) |
| Grid DP | O(m * n) | O(n) or O(1) in-place |
| String DP (2 strings) | O(m * n) | O(n) |
| 0/1 Knapsack | O(n * W) | O(W) |
| LIS | O(n log n) | O(n) |
| State Machine | O(n * k) | O(k) states |
| Interval DP | O(n^2) to O(n^3) | O(n^2) |
| Tree DP | O(n) | O(h) call stack |

## Common Mistakes

1. **Wrong state definition.** `dp[i] = answer at index i` is too vague. Be precise: `dp[i] = max profit using items 0..i` or `dp[i] = number of ways to reach step i`.

2. **Off-by-one errors.** Use `dp` of size `n + 1` for cleaner base cases. Be careful with 0-indexed vs 1-indexed.

3. **Optimizing space too early.** First get the full DP table working, then reduce to rolling array.

4. **Forgetting base cases.** Always initialize `dp[0]` (and `dp[1]` if needed). Check empty input and single element.

5. **Wrong iteration order.** 0/1 knapsack space-optimized: iterate capacity backwards. Dependencies must be computed before they are used.

6. **Confusing combinations vs permutations in counting DP.** Coin Change II: loop coins outside, amounts inside for combinations. Reverse gives permutations.
