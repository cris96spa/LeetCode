# Two Pointers & Sliding Window

## Pattern 1: Two Pointers - Opposite Direction

**When to Use:** Sorted arrays, pair-finding, palindrome checking, array partitioning.

### Template

```python
def two_pointer_opposite(arr):
    left, right = 0, len(arr) - 1
    
    while left < right:
        if condition:
            left += 1
        else:
            right -= 1
    
    return result
```

### Two Sum II (LC 167)

Find two numbers that sum to target in a **sorted** array.

```python
def twoSum(numbers: List[int], target: int) -> List[int]:
    left, right = 0, len(numbers) - 1
    
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        
        if curr_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    
    return []
```

**Time:** O(n) | **Space:** O(1)

### Valid Palindrome (LC 125)

```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

**Time:** O(n) | **Space:** O(1)

### 3Sum (LC 15)

Find all triplets that sum to 0.

```python
def threeSum(nums: List[int]) -> List[List[int]]:
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # Skip duplicates
        
        left, right = i + 1, len(nums) - 1
        target = -nums[i]
        
        while left < right:
            curr_sum = nums[left] + nums[right]
            
            if curr_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
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

**Time:** O(n^2) | **Space:** O(1) excluding output

Fix one element, two-pointer for the rest: reduces O(n^3) to O(n^2).

### Container With Most Water (LC 11)

Two vertical lines form a container. Maximize the water area.

```python
def maxArea(height: List[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        # Move the shorter line inward
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water
```

**Time:** O(n) | **Space:** O(1)

Moving the shorter line is correct because the width is shrinking, so the only way to get more area is a taller line.

### Trapping Rain Water (LC 42)

Two pointer O(1) space approach. Track left_max and right_max as you converge.

```python
def trap(height: List[int]) -> int:
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    
    return water
```

**Time:** O(n) | **Space:** O(1)

Water at each position = min(left_max, right_max) - height. By processing from the side with the smaller max, we know the other side has an equal or taller wall.

---

## Pattern 2: Two Pointers - Same Direction (Fast & Slow)

**When to Use:** Cycle detection, finding middle element, in-place array modification, removing duplicates.

### Template

```python
def fast_slow_pointers(arr):
    slow = fast = 0
    
    while fast < len(arr):
        if condition:
            arr[slow] = arr[fast]
            slow += 1
        fast += 1
    
    return slow
```

### Remove Duplicates (LC 26)

```python
def removeDuplicates(nums: List[int]) -> int:
    if not nums:
        return 0
    
    slow = 1
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[fast - 1]:
            nums[slow] = nums[fast]
            slow += 1
    
    return slow
```

**Time:** O(n) | **Space:** O(1)

### Linked List Cycle (LC 141)

Floyd's Tortoise and Hare.

```python
def hasCycle(head: ListNode) -> bool:
    if not head:
        return False
    
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False
```

**Time:** O(n) | **Space:** O(1)

---

## Pattern 3: Sliding Window - Fixed Size

**When to Use:** Subarray of exact size k, moving average, k consecutive elements.

### Template

```python
def sliding_window_fixed(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### Maximum Average Subarray (LC 643)

```python
def findMaxAverage(nums: List[int], k: int) -> float:
    curr_sum = sum(nums[:k])
    max_sum = curr_sum
    
    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, curr_sum)
    
    return max_sum / k
```

**Time:** O(n) | **Space:** O(1)

---

## Pattern 4: Sliding Window - Variable Size

**When to Use:** Longest/shortest subarray with a condition, at most k distinct elements.

### Template

```python
def sliding_window_variable(arr):
    left = 0
    result = 0
    window = {}  # Track window state
    
    for right in range(len(arr)):
        # Expand: add arr[right] to window
        window[arr[right]] = window.get(arr[right], 0) + 1
        
        # Contract: while window is invalid
        while not is_valid(window):
            window[arr[left]] -= 1
            if window[arr[left]] == 0:
                del window[arr[left]]
            left += 1
        
        # Update result
        result = max(result, right - left + 1)
    
    return result
```

### Longest Substring Without Repeating Characters (LC 3)

```python
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    max_len = 0
    char_set = set()
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**Time:** O(n) | **Space:** O(min(n, charset))

**Optimized with hash map** (jump left pointer directly):
```python
def lengthOfLongestSubstring(s: str) -> int:
    left = 0
    max_len = 0
    char_index = {}
    
    for right in range(len(s)):
        if s[right] in char_index:
            left = max(left, char_index[s[right]] + 1)
        
        char_index[s[right]] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

### Minimum Window Substring (LC 76)

Find minimum window in s containing all characters of t.

```python
def minWindow(s: str, t: str) -> str:
    from collections import Counter
    
    if not s or not t:
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    
    left = 0
    formed = 0
    window_counts = {}
    ans = (float('inf'), 0, 0)  # (length, left, right)
    
    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        
        while left <= right and formed == required:
            char = s[left]
            
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
            
            window_counts[char] -= 1
            if char in t_count and window_counts[char] < t_count[char]:
                formed -= 1
            
            left += 1
    
    return "" if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]
```

**Time:** O(|s| + |t|) | **Space:** O(|s| + |t|)

### Longest Repeating Character Replacement (LC 424)

Longest substring where you can replace at most k characters to make all characters the same.

```python
def characterReplacement(s: str, k: int) -> int:
    count = {}
    left = 0
    max_freq = 0  # Frequency of the most common char in current window
    result = 0
    
    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_freq = max(max_freq, count[s[right]])
        
        # Window size - max_freq = characters to replace
        # If > k, shrink window
        while (right - left + 1) - max_freq > k:
            count[s[left]] -= 1
            left += 1
        
        result = max(result, right - left + 1)
    
    return result
```

**Time:** O(n) | **Space:** O(1) (at most 26 characters)

Note: `max_freq` is never decremented when shrinking. This is correct because we only care about the maximum window size, and a smaller max_freq cannot produce a larger valid window.

### Subarrays with K Different Integers (LC 992)

Use the "at most K" trick: `exactly(K) = atMost(K) - atMost(K-1)`.

```python
def subarraysWithKDistinct(nums: List[int], k: int) -> int:
    def atMost(k):
        count = {}
        left = 0
        result = 0
        
        for right in range(len(nums)):
            count[nums[right]] = count.get(nums[right], 0) + 1
            
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            
            result += right - left + 1
        
        return result
    
    return atMost(k) - atMost(k - 1)
```

**Time:** O(n) | **Space:** O(k)

This trick works for any "exactly K" sliding window problem: convert to two "at most" problems.

---

## Pattern 5: Sliding Window with Deque

**When to Use:** Sliding window maximum/minimum.

### Sliding Window Maximum (LC 239)

```python
from collections import deque

def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    if not nums:
        return []
    
    dq = deque()  # Store indices, values in decreasing order
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements (they'll never be the max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result
```

**Time:** O(n) | **Space:** O(k)

---

## Prefix Sum (related technique)

### Subarray Sum Equals K (LC 560)

Not a sliding window (elements can be negative), but uses prefix sums with a hash map.

```python
def subarraySum(nums: List[int], k: int) -> int:
    prefix_sum = {0: 1}
    curr_sum = 0
    count = 0
    
    for num in nums:
        curr_sum += num
        
        if curr_sum - k in prefix_sum:
            count += prefix_sum[curr_sum - k]
        
        prefix_sum[curr_sum] = prefix_sum.get(curr_sum, 0) + 1
    
    return count
```

**Time:** O(n) | **Space:** O(n)

---

## Pattern Recognition Table

| Signal | Pattern |
|--------|---------|
| Sorted array, find pair | Two pointers (opposite) |
| Find triplets | Fix one + two pointers |
| In-place removal/dedup | Fast/slow pointers |
| Linked list cycle | Fast/slow pointers |
| Maximize area between lines | Two pointers (opposite) |
| Subarray of exact size k | Fixed sliding window |
| Longest/shortest subarray | Variable sliding window |
| "At most K distinct" | Variable sliding window |
| "Exactly K" | atMost(K) - atMost(K-1) |
| Sliding max/min | Deque (monotonic) |
| Subarray sum = k (with negatives) | Prefix sum + hash map |

## Complexity Reference

| Pattern | Time | Space |
|---------|------|-------|
| Two pointers (opposite) | O(n) | O(1) |
| Two pointers (fast/slow) | O(n) | O(1) |
| Fixed window | O(n) | O(1) |
| Variable window | O(n) | O(k) for hash map |
| Window with deque | O(n) | O(k) |
| Prefix sum | O(n) | O(n) |

## Common Mistakes

1. **Not initializing window correctly** -- compute the initial window before entering the slide loop.

2. **Infinite loop** -- forgetting to advance pointers inside the while loop.

3. **Off-by-one in window size** -- window size is `right - left + 1`.

4. **Not handling edge cases** -- empty array, k > array length, all elements same.

5. **Using sliding window with negative numbers** -- variable-size sliding window only works when elements are non-negative (or all positive). For negative numbers, use prefix sum.
