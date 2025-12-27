# Two Pointers & Sliding Window - Complete Guide

**Interview Frequency:** ⭐⭐⭐⭐⭐ (80% of Google interviews)  
**Google Frequency:** ⭐⭐⭐⭐⭐ (Multiple problems per interview)  
**Mastery Time:** 5-6 hours

## Why These Patterns are Essential

Two pointers and sliding window are **optimization techniques** that:
- Reduce O(n²) to O(n) or O(n log n)
- Minimize space complexity
- Enable elegant, readable solutions

**Google loves these because:**
- They test algorithmic thinking
- Multiple variations exist
- Real-world applications (streaming data, memory constraints)

---

## Pattern 1: Two Pointers - Opposite Direction

**When to Use:**
- Sorted array problems
- Pair-finding problems
- Palindrome checking
- Array partitioning

### Template

```python
def two_pointer_opposite(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        # Process current state
        if condition:
            # Move based on logic
            left += 1
        else:
            right -= 1
    
    return result
```

---

### Problem: Two Sum II (LC 167) ⭐⭐⭐⭐⭐

**Problem:** Find two numbers that sum to target in **sorted** array.

```python
def twoSum(numbers: List[int], target: int) -> List[int]:
    left, right = 0, len(numbers) - 1
    
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        
        if curr_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif curr_sum < target:
            left += 1  # Need larger sum
        else:
            right -= 1  # Need smaller sum
    
    return []
```

**Complexity:** O(n) time, O(1) space

**Key Insight:** Sorted array allows us to make directed decisions.

---

### Problem: Valid Palindrome (LC 125) ⭐⭐⭐⭐⭐

```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

**Complexity:** O(n) time, O(1) space

---

### Problem: 3Sum (LC 15) ⭐⭐⭐⭐⭐

**Problem:** Find all triplets that sum to 0.

```python
def threeSum(nums: List[int]) -> List[List[int]]:
    nums.sort()  # O(n log n)
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for first number
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Two pointer for remaining
        left, right = i + 1, len(nums) - 1
        target = -nums[i]
        
        while left < right:
            curr_sum = nums[left] + nums[right]
            
            if curr_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif curr_sum < target:
                left += 1
            else:
                right -= 1
    
    return result
```

**Complexity:** O(n²) time, O(1) space (excluding output)

**Pattern:** Fix one element, two-pointer for rest → reduces O(n³) to O(n²)

---

## Pattern 2: Two Pointers - Same Direction (Fast & Slow)

**When to Use:**
- Cycle detection
- Finding middle element
- In-place array modification
- Removing duplicates

### Template

```python
def fast_slow_pointers(arr):
    slow = fast = 0
    
    while fast < len(arr):
        # Fast pointer explores ahead
        if condition:
            arr[slow] = arr[fast]
            slow += 1
        fast += 1
    
    return slow  # New length or result
```

---

### Problem: Remove Duplicates (LC 26) ⭐⭐⭐⭐

```python
def removeDuplicates(nums: List[int]) -> int:
    if not nums:
        return 0
    
    slow = 1  # Position to place next unique
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[fast - 1]:
            nums[slow] = nums[fast]
            slow += 1
    
    return slow
```

**Complexity:** O(n) time, O(1) space

**Key Pattern:** Slow marks write position, fast explores.

---

### Problem: Linked List Cycle (LC 141) ⭐⭐⭐⭐⭐

**Floyd's Tortoise and Hare Algorithm:**

```python
def hasCycle(head: ListNode) -> bool:
    if not head:
        return False
    
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next       # Move 1 step
        fast = fast.next.next  # Move 2 steps
        
        if slow == fast:
            return True
    
    return False
```

**Complexity:** O(n) time, O(1) space

**Why it works:** In a cycle, fast will eventually catch slow.

---

## Pattern 3: Sliding Window - Fixed Size

**When to Use:**
- Subarray of size K
- Moving average
- K consecutive elements

### Template

```python
def sliding_window_fixed(arr, k):
    # Initialize window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

---

### Problem: Maximum Average Subarray (LC 643) ⭐⭐⭐⭐

```python
def findMaxAverage(nums: List[int], k: int) -> float:
    # Initial window
    curr_sum = sum(nums[:k])
    max_sum = curr_sum
    
    # Slide window
    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, curr_sum)
    
    return max_sum / k
```

**Complexity:** O(n) time, O(1) space

---

## Pattern 4: Sliding Window - Variable Size

**When to Use:**
- Longest/shortest subarray with condition
- At most K distinct elements
- Minimum window substring

### Template

```python
def sliding_window_variable(arr):
    left = 0
    result = 0
    window = {}  # Track window state
    
    for right in range(len(arr)):
        # Expand window
        window[arr[right]] = window.get(arr[right], 0) + 1
        
        # Contract window while invalid
        while not is_valid(window):
            window[arr[left]] -= 1
            if window[arr[left]] == 0:
                del window[arr[left]]
            left += 1
        
        # Update result
        result = max(result, right - left + 1)
    
    return result
```

---

### Problem: Longest Substring Without Repeating Characters (LC 3) ⭐⭐⭐⭐⭐

```python
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    max_len = 0
    char_set = set()
    
    for right in range(len(s)):
        # Shrink window until no duplicates
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character
        char_set.add(s[right])
        
        # Update max length
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Complexity:** O(n) time, O(min(n, charset)) space

**Alternative with Hash Map:**
```python
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    max_len = 0
    char_index = {}
    
    for right in range(len(s)):
        if s[right] in char_index:
            # Jump left pointer past duplicate
            left = max(left, char_index[s[right]] + 1)
        
        char_index[s[right]] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

---

### Problem: Minimum Window Substring (LC 76) ⭐⭐⭐⭐⭐

**Problem:** Find minimum window in s containing all characters of t.

```python
def minWindow(s: str, t: str) -> str:
    from collections import Counter
    
    if not s or not t:
        return ""
    
    # Count characters in t
    t_count = Counter(t)
    required = len(t_count)
    
    left = 0
    formed = 0
    window_counts = {}
    
    # (window_length, left, right)
    ans = (float('inf'), 0, 0)
    
    for right in range(len(s)):
        # Add character to window
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        # Check if this character satisfies requirement
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        # Contract window
        while left <= right and formed == required:
            char = s[left]
            
            # Update result
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
            
            # Remove leftmost character
            window_counts[char] -= 1
            if char in t_count and window_counts[char] < t_count[char]:
                formed -= 1
            
            left += 1
    
    return "" if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]
```

**Complexity:** O(|s| + |t|) time, O(|s| + |t|) space

---

## Pattern 5: Sliding Window with Deque

**When to Use:**
- Sliding window maximum/minimum
- Maintaining order within window

### Problem: Sliding Window Maximum (LC 239) ⭐⭐⭐⭐⭐

```python
from collections import deque

def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    if not nums:
        return []
    
    dq = deque()  # Store indices
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements (not useful)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Add to result when window is full
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

**Complexity:** O(n) time, O(k) space

**Key Idea:** Deque maintains indices in decreasing order of values.

---

## Advanced Patterns

### Pattern 6: Caterpillar Method

**Problem: Subarray Sum Equals K (LC 560)**

```python
def subarraySum(nums: List[int], k: int) -> int:
    # Prefix sum approach
    prefix_sum = {0: 1}
    curr_sum = 0
    count = 0
    
    for num in nums:
        curr_sum += num
        
        # Check if (curr_sum - k) exists
        if curr_sum - k in prefix_sum:
            count += prefix_sum[curr_sum - k]
        
        prefix_sum[curr_sum] = prefix_sum.get(curr_sum, 0) + 1
    
    return count
```

**Complexity:** O(n) time and space

---

## Google Interview Patterns

### 1. When to Use Each Pattern

| Problem Type | Pattern | Key Signal |
|-------------|---------|------------|
| Pair sum (sorted) | Two pointers opposite | "Sorted array" |
| Triplet sum | Fix + two pointers | "All triplets" |
| Remove duplicates | Fast/slow pointers | "In-place" |
| Cycle detection | Fast/slow pointers | "Linked list cycle" |
| Max subarray size K | Fixed window | "Exactly K elements" |
| Longest substring | Variable window | "Longest/shortest" |
| At most K distinct | Variable window | "At most K" |

### 2. Common Optimizations

**From O(n²) to O(n):**
```python
# ❌ O(n²): Nested loop
def max_subarray_slow(arr, k):
    max_sum = float('-inf')
    for i in range(len(arr) - k + 1):
        window_sum = sum(arr[i:i+k])
        max_sum = max(max_sum, window_sum)
    return max_sum

# ✅ O(n): Sliding window
def max_subarray_fast(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

---

## Master Checklist

### Two Pointers
- [ ] Opposite direction (sorted arrays)
- [ ] Same direction (fast/slow)
- [ ] Cycle detection (linked lists)
- [ ] In-place modification
- [ ] 3Sum and variants

### Sliding Window
- [ ] Fixed size window
- [ ] Variable size (longest/shortest)
- [ ] Window with hash map
- [ ] Window with deque (max/min)
- [ ] At most K distinct

### Skills
- [ ] Identify when to use which pattern
- [ ] Optimize from O(n²) to O(n)
- [ ] Handle edge cases (empty, single element)
- [ ] Explain time/space complexity

---

## Practice Roadmap

### Week 1: Two Pointers (10 problems)
- LC 167, 125, 344 (Opposite direction)
- LC 26, 27, 283 (Fast/slow)
- LC 15, 16, 18 (3Sum variants)
- LC 141, 142 (Cycle detection)

### Week 2: Sliding Window (10 problems)
- LC 643, 1343 (Fixed window)
- LC 3, 424, 1004 (Variable window)
- LC 76, 438, 567 (Minimum window)
- LC 239, 862 (Deque)

**Total:** 5-6 hours

---

## Common Mistakes

1. **Not initializing window correctly**
   ```python
   # ❌ Wrong
   for i in range(len(arr)):
       window_sum = sum(arr[i:i+k])
   
   # ✅ Correct
   window_sum = sum(arr[:k])
   for i in range(k, len(arr)):
       window_sum += arr[i] - arr[i-k]
   ```

2. **Infinite loop in while**
   ```python
   # ❌ Wrong
   while condition:
       # Forgot to update pointers
   
   # ✅ Correct
   while condition:
       left += 1  # or right -= 1
   ```

3. **Off-by-one in window size**
   ```python
   # Window size = right - left + 1
   max_len = max(max_len, right - left + 1)
   ```

4. **Not handling edge cases**
   - Empty array
   - K > array length
   - All elements same

---

## Time Complexity Reference

| Pattern | Time | Space |
|---------|------|-------|
| Two pointers | O(n) | O(1) |
| Fixed window | O(n) | O(1) |
| Variable window | O(n) | O(k) for hash map |
| Window with deque | O(n) | O(k) |

---

## Interview Template

```python
def solve_with_sliding_window(arr, condition):
    left = 0
    window_state = {}  # or set(), or int
    result = 0
    
    for right in range(len(arr)):
        # 1. Expand window: add arr[right]
        # Update window state
        
        # 2. Contract window: while invalid
        while not is_valid(window_state):
            # Remove arr[left]
            # Update window state
            left += 1
        
        # 3. Update result
        result = max(result, right - left + 1)
    
    return result
```

---

**Master these patterns, and you'll optimize solutions like a pro!**
