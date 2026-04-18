# Bit Manipulation

## Operators & XOR Properties

### Operator Table

| Operator | Symbol | Description | Example (5, 3) |
|---|---|---|---|
| AND | `&` | 1 if both bits are 1 | `5 & 3 = 1` (101 & 011 = 001) |
| OR | `\|` | 1 if at least one bit is 1 | `5 \| 3 = 7` (101 \| 011 = 111) |
| XOR | `^` | 1 if bits differ | `5 ^ 3 = 6` (101 ^ 011 = 110) |
| NOT | `~` | Flip all bits | `~5 = -6` (in Python) |
| Left Shift | `<<` | Shift bits left, fill with 0 | `5 << 1 = 10` |
| Right Shift | `>>` | Shift bits right | `5 >> 1 = 2` |

### XOR Properties

These come up constantly. Know them cold.

| Property | Expression | Why It Matters |
|---|---|---|
| Self-inverse | `a ^ a = 0` | Duplicate cancellation |
| Identity | `a ^ 0 = a` | XOR with 0 is no-op |
| Commutative | `a ^ b = b ^ a` | Order doesn't matter |
| Associative | `(a ^ b) ^ c = a ^ (b ^ c)` | Can regroup freely |

Consequence: XOR of a list where every element appears twice except one leaves the unique element.

### Two's Complement

Negative numbers are stored as two's complement: `-x` is represented as `~x + 1`.
This means `x & (-x)` isolates the lowest set bit (see below).

---

## Common Tricks

### Check, Set, Clear, Toggle a Bit

```python
# Check if i-th bit is set
(num >> i) & 1

# Set the i-th bit
num | (1 << i)

# Clear the i-th bit
num & ~(1 << i)

# Toggle the i-th bit
num ^ (1 << i)
```

### Lowest Set Bit

```python
# Isolate lowest set bit
lowest = x & (-x)
# Example: x = 12 (1100) -> lowest = 4 (0100)

# Remove lowest set bit
x = x & (x - 1)
# Example: x = 12 (1100) -> 8 (1000)
```

`x & (x - 1)` is the foundation of many tricks: counting bits, checking power of 2.

### Power of 2

A power of 2 has exactly one set bit. Removing it gives 0.

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

**Time:** O(1). **Space:** O(1).

### Check Odd/Even

```python
is_odd = (num & 1) == 1
is_even = (num & 1) == 0
```

### Count Set Bits (Hamming Weight)

```python
def count_bits(n):
    count = 0
    while n:
        n &= (n - 1)  # remove lowest set bit
        count += 1
    return count
```

**Time:** O(k) where k = number of set bits. **Space:** O(1).

### Swap Without Temp Variable

```python
a = a ^ b
b = a ^ b  # now b = original a
a = a ^ b  # now a = original b
```

---

## Bitmask Subset Enumeration

Use an integer as a bitmask to represent a subset of n elements. Bit `i` being set means element `i` is included.

### Generate All Subsets

```python
def subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result
```

**Why it works:** There are 2^n possible subsets. Each integer from 0 to 2^n - 1 has a unique binary representation that maps to a unique subset.

**Time:** O(n * 2^n). **Space:** O(n) per subset.

### Iterate All Submasks of a Mask

Given a bitmask `mask`, enumerate all its submasks (subsets of the set bits in `mask`):

```python
sub = mask
while sub > 0:
    # process sub
    sub = (sub - 1) & mask
# don't forget to process sub = 0 (empty set) if needed
```

This runs in O(2^k) where k is the number of set bits in `mask`. Useful in bitmask DP problems.

---

## Key Problems

### Single Number (LC 136)

Every element appears twice except one. XOR all -- duplicates cancel.

```python
def singleNumber(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
```

**Time:** O(n). **Space:** O(1).

### Single Number II (LC 137)

Every element appears three times except one. Track bit counts modulo 3 using two state variables.

```python
def singleNumber(nums):
    ones, twos = 0, 0
    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones
    return ones
```

**Time:** O(n). **Space:** O(1).

**Intuition:** `ones` holds bits that have appeared 1 mod 3 times, `twos` holds bits at 2 mod 3. When a bit hits 3, both reset to 0.

### Missing Number (LC 268)

Array of n numbers from 0..n with one missing. XOR indices with values.

```python
def missingNumber(nums):
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
```

**Time:** O(n). **Space:** O(1).

### Reverse Bits (LC 190)

Reverse all 32 bits of a number.

```python
def reverseBits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

**Time:** O(1) -- always 32 iterations. **Space:** O(1).

### Find the Difference (LC 389)

String t is string s with one extra character. XOR all characters.

```python
def findTheDifference(s, t):
    result = 0
    for char in s + t:
        result ^= ord(char)
    return chr(result)
```

**Time:** O(n). **Space:** O(1).

### Bitwise AND of Numbers Range (LC 201)

Find AND of all numbers in [m, n]. Right-shift both until they match -- the common prefix is the answer.

```python
def rangeBitwiseAnd(m, n):
    shift = 0
    while m < n:
        m >>= 1
        n >>= 1
        shift += 1
    return m << shift
```

**Time:** O(log n). **Space:** O(1).

**Intuition:** Any bit position where m and n differ will have both 0 and 1 in the range, so AND produces 0 for that bit. Only the common high-bit prefix survives.

### Gray Code (LC 89)

Generate n-bit Gray code sequence where consecutive numbers differ by one bit.

```python
def grayCode(n):
    return [i ^ (i >> 1) for i in range(1 << n)]
```

**Time:** O(2^n). **Space:** O(1) excluding output.

---

## Python-Specific Notes

1. **Arbitrary precision integers.** Python ints have unlimited bits, so there's no overflow. But this means `~x` returns `-(x+1)`, not a fixed-width complement.

2. **No unsigned right shift.** Python's `>>` always does arithmetic shift (sign-extending). To simulate 32-bit unsigned behavior:
   ```python
   # Treat as 32-bit unsigned
   result = n & 0xFFFFFFFF
   ```

3. **bin() and bit_count().** `bin(x)` gives the binary string. Python 3.10+ has `int.bit_count()` for popcount:
   ```python
   x = 13
   bin(x)          # '0b1101'
   x.bit_count()   # 3
   ```

4. **Negative number masking.** When a problem expects 32-bit integers, mask with `0xFFFFFFFF`:
   ```python
   # Convert Python's arbitrary-precision negative to 32-bit representation
   if result > 0x7FFFFFFF:
       result -= 0x100000000
   ```

---

## Complexity Notes

| Operation | Time | Space |
|---|---|---|
| Single bitwise op (AND, OR, XOR, shift) | O(1) | O(1) |
| Count set bits | O(k), k = set bits | O(1) |
| Enumerate all subsets of n elements | O(n * 2^n) | O(n) |
| Enumerate submasks of a mask | O(2^k), k = set bits | O(1) |
| XOR of n elements | O(n) | O(1) |

Bit manipulation solutions typically achieve O(1) space, which is their main advantage over hash-based approaches.
