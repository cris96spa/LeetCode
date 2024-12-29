# Bit Manipulation Cheatsheet

## **Introduction**

Bit manipulation involves using bitwise operators to solve problems efficiently by leveraging the binary representation of numbers. Common bitwise operators include:

| Operator    | Symbol | Description                     |
| ----------- | ------ | ------------------------------- |
| AND         | `&`    | Sets a bit if both bits are 1   |
| OR          | `\|`   | Sets a bit if at least one is 1 |
| XOR         | `^`    | Toggles a bit (1 if different)  |
| NOT         | `~`    | Flips bits                      |
| Left Shift  | `<<`   | Multiplies by 2 per shift       |
| Right Shift | `>>`   | Divides by 2 per shift          |

## **Common Bitwise Tricks**

### **1. Check if a number is odd or even**

- **Odd:** `num & 1 == 1`
- **Even:** `num & 1 == 0`

### **2. Get the \( i \)-th bit**

- Formula: `(num >> i) & 1`

### **3. Set the \( i \)-th bit**

- Formula: `num | (1 << i)`

### **4. Clear the \( i \)-th bit**

- Formula: `num & ~(1 << i)`

### **5. Toggle the \( i \)-th bit**

- Formula: `num ^ (1 << i)`

### **6. Count the number of 1s (Hamming weight)**

- Algorithm:
  ```python
  def hammingWeight(n):
      count = 0
      while n:
          n &= (n - 1)  # Remove the lowest set bit
          count += 1
      return count
  ```

### **7. Check if a number is a power of 2**

- Formula: `n > 0 and (n & (n - 1)) == 0`

### **8. Swap two numbers without a temporary variable**

- Formula:
  ```python
  a = a ^ b
  b = a ^ b
  a = a ^ b
  ```

## **Common Bit Manipulation Problems**

### **1. Single Number**

- **Problem:** Every element appears twice except one. Find the unique number.
- **Solution:** XOR all numbers. Duplicate numbers cancel out.
  ```python
  def singleNumber(nums):
      result = 0
      for num in nums:
          result ^= num
      return result
  ```

### **2. Single Number II**

- **Problem:** Every element appears three times except one. Find the unique number.
- **Solution:** Use `ones` and `twos` to track counts modulo 3.
  ```python
  def singleNumber(nums):
      ones, twos = 0, 0
      for num in nums:
          ones = (ones ^ num) & ~twos
          twos = (twos ^ num) & ~ones
      return ones
  ```

### **3. Subset Generation**

- **Problem:** Generate all subsets of a set.
- **Solution:** Use bit masking.
  ```python
  def subsets(nums):
      n = len(nums)
      result = []
      for mask in range(1 << n):
          subset = [nums[i] for i in range(n) if mask & (1 << i)]
          result.append(subset)
      return result
  ```

### **4. Reverse Bits**

- **Problem:** Reverse the bits of a number.
- **Solution:**
  ```python
  def reverseBits(n):
      result = 0
      for _ in range(32):
          result = (result << 1) | (n & 1)
          n >>= 1
      return result
  ```

### **5. Missing Number**

- **Problem:** Find the missing number in a range.
- **Solution:** XOR all indices and numbers. Missing number will remain.
  ```python
  def missingNumber(nums):
      n = len(nums)
      result = n  # Start with the maximum index
      for i, num in enumerate(nums):
          result ^= i ^ num
      return result
  ```

### **6. Bitwise AND of Numbers Range**

- **Problem:** Find the bitwise AND of all numbers in a range `[m, n]`.
- **Solution:** Remove the differing lower bits by right-shifting.
  ```python
  def rangeBitwiseAnd(m, n):
      shift = 0
      while m < n:
          m >>= 1
          n >>= 1
          shift += 1
      return m << shift
  ```

### **7. Power of Two**

- **Problem:** Check if a number is a power of two.
- **Solution:**
  ```python
  def isPowerOfTwo(n):
      return n > 0 and (n & (n - 1)) == 0
  ```

### **8. Find the Difference**

- **Problem:** Find the added letter in two strings.
- **Solution:** XOR all characters.
  ```python
  def findTheDifference(s, t):
      result = 0
      for char in s + t:
          result ^= ord(char)
      return chr(result)
  ```

## **Advanced Techniques**

### **1. Modular Arithmetic with Bits**

- **Use Case:** Handle counts like “numbers appearing three times.”
- Example for `k = 3`:
  ```python
  def singleNumber(nums):
      ones, twos = 0, 0
      for num in nums:
          ones = (ones ^ num) & ~twos
          twos = (twos ^ num) & ~ones
      return ones
  ```
- **Use Case:** Handle counts like “numbers appearing k times with k odd.”
- Example for `k = 5`:

  ```python
  state0, state1, state2 = 0, 0, 0
  for num in nums:
      new_state2 = (state2 ^ num) & ~state0 & ~state1
      new_state1 = (state1 ^ num) & ~state0 & ~state2
      state0 = (state0 ^ num) & ~state1 & ~state2
      state2, state1, state0 = new_state2, new_state1, state0
  # `state0` contains the unique number
  return state0

  ```

### **2. Gray Code Generation**

- **Problem:** Generate Gray Code sequence for `n` bits.
- **Solution:**
  ```python
  def grayCode(n):
      return [i ^ (i >> 1) for i in range(1 << n)]
  ```

## **Practice Problems**

### Easy:

- Number of 1 Bits
- Power of Two
- Find the Difference

### Medium:

- Subsets
- Single Number II
- Missing Number

### Hard:

- Maximum XOR of Two Numbers in an Array
- Bitwise AND of Numbers Range
- Reverse Bits

## **Tips and Tricks**

1. XOR is a powerful tool for toggling and identifying unique values.
2. Use masks like `1 << i` to isolate specific bits.
3. Combine bitwise operators with modular arithmetic for advanced counting problems.
4. Practice problems with edge cases to gain confidence.
