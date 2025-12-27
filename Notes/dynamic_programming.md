# Dynamic Programming - Complete Mastery Guide

**Interview Frequency:** ⭐⭐⭐⭐⭐ (70% of Google interviews)  
**Difficulty Level:** High  
**Mastery Time:** 15-20 hours

## Why DP is Critical for Google

Dynamic Programming is the ultimate pattern recognition test. Google uses DP to evaluate:
- **Problem decomposition** - breaking complex problems into subproblems
- **State design** - identifying what information matters
- **Optimization thinking** - space/time tradeoffs
- **Code quality** - clean, readable recursive/iterative solutions

**Key Insight:** Most DP problems follow 10-15 core patterns. Master these, and you can solve 80%+ of DP questions.

---

## The DP Framework (SRTBOT)

Every DP problem can be solved with this systematic approach:

### **S - State Definition**
What does `dp[i]` or `dp[i][j]` represent?

### **R - Recurrence Relation**
How does `dp[i]` relate to previous states?

### **T - Base Cases**
What are the simplest cases we can solve directly?

### **B - Bottom-up or Top-down**
Which implementation approach to use?

### **O - Optimization**
Can we reduce space complexity?

### **T - Testing**
Verify with small examples

---

## Pattern 1: Linear DP (1D)

**Characteristics:**
- Single array `dp[i]`
- Current state depends on previous states
- Often Fibonacci-like recurrence

### **Problem: Climbing Stairs** (LC 70) ⭐⭐⭐⭐⭐

**Problem:** n stairs, can climb 1 or 2 steps. How many ways to reach top?

**Solution:**
```python
def climbStairs(n: int) -> int:
    # State: dp[i] = ways to reach step i
    # Base: dp[0] = 1, dp[1] = 1
    # Recurrence: dp[i] = dp[i-1] + dp[i-2]
    
    if n <= 1:
        return 1
    
    prev2, prev1 = 1, 1
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1
```

**Complexity:** O(n) time, O(1) space (optimized from O(n))

**Related:** Fibonacci, House Robber, Decode Ways

---

### **Problem: House Robber** (LC 198) ⭐⭐⭐⭐⭐

**Problem:** Rob houses in line, can't rob adjacent. Maximize money.

```python
def rob(nums: List[int]) -> int:
    # State: dp[i] = max money robbing houses 0..i
    # Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    #   Choice: rob house i (add to i-2) or skip (take i-1)
    
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

**Complexity:** O(n) time, O(1) space

**Variants:**
- LC 213: House Robber II (circular array)
- LC 337: House Robber III (binary tree)

---

## Pattern 2: Grid DP (2D)

**Characteristics:**
- 2D grid `dp[i][j]`
- Movement constraints (usually down/right)
- Path counting or optimization

### **Problem: Unique Paths** (LC 62) ⭐⭐⭐⭐

**Problem:** m×n grid, move only right/down. Count paths from top-left to bottom-right.

```python
def uniquePaths(m: int, n: int) -> int:
    # State: dp[i][j] = paths to cell (i,j)
    # Base: dp[0][j] = 1, dp[i][0] = 1 (single path along edges)
    # Recurrence: dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    # Space optimized: only need previous row
    dp = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]  # dp[j] already has dp[i-1][j]
    
    return dp[-1]
```

**Complexity:** O(m×n) time, O(n) space (optimized from O(m×n))

**Pattern Recognition:** Any "count paths in grid" → grid DP

---

### **Problem: Minimum Path Sum** (LC 64) ⭐⭐⭐⭐

```python
def minPathSum(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    
    # Can modify grid in-place to save space
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

**Complexity:** O(m×n) time, O(1) space

---

## Pattern 3: String DP

**Characteristics:**
- Compare/match strings
- Often 2D DP with two strings
- Subsequence vs substring distinction

### **Problem: Longest Common Subsequence** (LC 1143) ⭐⭐⭐⭐⭐

**Problem:** Find length of longest common subsequence.

```python
def longestCommonSubsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    
    # State: dp[i][j] = LCS length of text1[0:i] and text2[0:j]
    # Recurrence:
    #   if text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
    #   else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

**Complexity:** O(m×n) time, O(m×n) space (can optimize to O(n))

**Space Optimization:**
```python
def longestCommonSubsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    
    # Only need current and previous row
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

**Complexity:** O(m×n) time, O(n) space

---

### **Problem: Edit Distance** (LC 72) ⭐⭐⭐⭐⭐

**Problem:** Minimum operations (insert, delete, replace) to convert word1 to word2.

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    
    # State: dp[i][j] = min ops to convert word1[0:i] to word2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # Delete from word1
                    dp[i][j-1],     # Insert into word1
                    dp[i-1][j-1]    # Replace
                )
    
    return dp[m][n]
```

**Complexity:** O(m×n) time, O(m×n) space

**Google Follow-up:** "Reconstruct the actual operations needed."

---

## Pattern 4: Knapsack Problems

**Characteristics:**
- Items with weight/value
- Capacity constraint
- Maximize value or count combinations

### **Problem: 0/1 Knapsack** (Classic)

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    
    # State: dp[i][w] = max value using items 0..i with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i-1][w]
            
            # Take item i-1 if fits
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]
```

**Space Optimized:**
```python
def knapsack(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # Traverse backwards to avoid using same item twice
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

**Complexity:** O(n×capacity) time, O(capacity) space

---

### **Problem: Coin Change** (LC 322) ⭐⭐⭐⭐⭐

**Problem:** Minimum coins to make amount (unbounded knapsack).

```python
def coinChange(coins: List[int], amount: int) -> int:
    # State: dp[i] = min coins to make amount i
    # Recurrence: dp[i] = min(dp[i - coin] + 1) for all coins
    
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 0 coins for amount 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Complexity:** O(amount × coins) time, O(amount) space

**Variant - Coin Change II (LC 518):** Count number of combinations

---

## Pattern 5: Longest Increasing Subsequence (LIS)

### **Problem: LIS** (LC 300) ⭐⭐⭐⭐⭐

**Approach 1: DP - O(n²)**
```python
def lengthOfLIS(nums: List[int]) -> int:
    if not nums:
        return 0
    
    # dp[i] = length of LIS ending at index i
    dp = [1] * len(nums)
    
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

**Approach 2: Binary Search - O(n log n)** (Google Expects This)
```python
def lengthOfLIS(nums: List[int]) -> int:
    from bisect import bisect_left
    
    # tails[i] = smallest tail element for LIS of length i+1
    tails = []
    
    for num in nums:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)
```

**Complexity:** O(n log n) time, O(n) space

---

## Pattern 6: State Machine DP

**Characteristics:**
- Finite states (buy, sell, cooldown)
- Transitions between states
- Often stock problems

### **Problem: Best Time to Buy/Sell Stock** (LC 121, 122, 123, 188, 309)

**LC 122: Multiple Transactions**
```python
def maxProfit(prices: List[int]) -> int:
    # State machine: hold stock or not
    # cash = max profit when not holding stock
    # hold = max profit when holding stock
    
    cash, hold = 0, -prices[0]
    
    for i in range(1, len(prices)):
        cash = max(cash, hold + prices[i])  # Sell
        hold = max(hold, cash - prices[i])  # Buy
    
    return cash
```

**LC 309: With Cooldown**
```python
def maxProfit(prices: List[int]) -> int:
    if len(prices) <= 1:
        return 0
    
    # Three states: hold, sold (just sold), rest (cooldown)
    hold = -prices[0]
    sold = 0
    rest = 0
    
    for i in range(1, len(prices)):
        prev_hold = hold
        prev_sold = sold
        prev_rest = rest
        
        hold = max(prev_hold, prev_rest - prices[i])
        sold = prev_hold + prices[i]
        rest = max(prev_rest, prev_sold)
    
    return max(sold, rest)
```

---

## Pattern 7: Interval DP

**Characteristics:**
- Process intervals/subarrays
- Combine solutions from subintervals
- Often polynomial time

### **Problem: Longest Palindromic Substring** (LC 5) ⭐⭐⭐⭐⭐

```python
def longestPalindrome(s: str) -> str:
    n = len(s)
    if n < 2:
        return s
    
    # dp[i][j] = is s[i:j+1] palindrome?
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    
    # Base: single characters
    for i in range(n):
        dp[i][i] = True
    
    # Length 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start, max_len = i, 2
    
    # Length 3+
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                start, max_len = i, length
    
    return s[start:start + max_len]
```

**Complexity:** O(n²) time and space

---

## Master Checklist

### Fundamental Patterns (Must Know)
- [ ] 1D DP (Fibonacci, House Robber)
- [ ] 2D Grid DP (Unique Paths, Min Path Sum)
- [ ] String DP (LCS, Edit Distance)
- [ ] Knapsack (0/1, Unbounded)
- [ ] LIS (both O(n²) and O(n log n))

### Advanced Patterns
- [ ] State Machine DP
- [ ] Interval DP
- [ ] Tree DP
- [ ] Digit DP
- [ ] Bitmask DP

### Skills
- [ ] Identify DP problems in <2 minutes
- [ ] Define state correctly first time
- [ ] Write recurrence relation
- [ ] Optimize space complexity
- [ ] Handle edge cases

---

## Common Mistakes to Avoid

1. **Wrong State Definition**
   - ❌ `dp[i] = answer at index i` (too vague)
   - ✅ `dp[i] = max profit using first i items`

2. **Off-by-One Errors**
   - Be careful with 0-indexed vs 1-indexed
   - Use `len(dp) = n + 1` for cleaner base cases

3. **Space Optimization Too Early**
   - First solve with full DP table
   - Then optimize to rolling array

4. **Forgetting Base Cases**
   - Always initialize `dp[0]`, `dp[1]`
   - Check empty input, single element

5. **Iterating in Wrong Order**
   - For 0/1 knapsack optimization: iterate backwards
   - For dependencies: ensure previous states computed first

---

## Google Interview Tips

1. **Always Start with Brute Force**
   - State the recursive solution first
   - Identify overlapping subproblems
   - Transition to DP

2. **Communicate State Design**
   - "Let dp[i] represent..."
   - "This depends on dp[i-1] because..."

3. **Draw Small Examples**
   - Use 3×3 grid or length-4 array
   - Walk through DP table filling

4. **Discuss Optimizations**
   - Mention space optimization
   - Compare bottom-up vs top-down

5. **Handle Follow-ups**
   - "How to reconstruct solution?"
   - "What if constraints change?"

---

## Practice Roadmap

### Week 1: Foundations (15 problems)
- LC 70, 198, 213, 746 (1D DP)
- LC 62, 63, 64 (Grid DP)
- LC 139, 300 (Classic patterns)

### Week 2: Strings & Knapsack (15 problems)
- LC 1143, 72, 5, 516 (String DP)
- LC 322, 518, 416, 494 (Knapsack)

### Week 3: Advanced (15 problems)
- LC 121, 122, 123, 309, 188 (Stock problems)
- LC 53, 152, 1567 (Kadane variants)
- LC 10, 44, 97 (Pattern matching)

### Total: 45 problems, ~15-20 hours

---

## Time Complexity Quick Reference

| Pattern | Typical Complexity | Space |
|---------|-------------------|-------|
| 1D DP | O(n) | O(1) optimized |
| 2D Grid | O(m×n) | O(n) optimized |
| String (2 strings) | O(m×n) | O(n) optimized |
| Knapsack | O(n×W) | O(W) optimized |
| LIS | O(n log n) | O(n) |
| Interval DP | O(n²) - O(n³) | O(n²) |

---

**Key Takeaway:** DP is pattern recognition. Master these 7 patterns, and you can solve any DP problem Google gives you.

*Practice consistently, and DP will become your strongest skill.*
