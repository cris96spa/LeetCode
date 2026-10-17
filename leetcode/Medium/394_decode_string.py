class Solution:
    """Decode a string encoded with the k[encoded_string] rule.

    Problem Statement:
        Given an encoded string s, return its decoded form. The encoding rule
        is k[encoded_string]: the encoded_string inside the brackets is
        repeated exactly k times. Encodings can be nested. The input is
        always valid, digits only appear as repeat counts, and 1 <= k <= 300.

    Example:
        s = "3[a]2[bc]"
        -> "aaabcbc"

        s = "3[a2[c]]"
        -> "accaccacc"

    Approach:
        Scan the string once, keeping the string being built in the current
        context (current) and the repeat count being parsed (num).

        - Digit: k can have up to 3 digits, so build it one digit at a time
          with num = 10 * num + digit (for "299": 2 -> 29 -> 299).
        - '[': opening a bracket starts a new context. Push the previous one
          as (current, num) on the stack, then reset both.
        - ']': closing a bracket ends the context. Pop (prefix, repeat) and
          set current = prefix + current * repeat.
        - Letter: append it to current.

        Trace on "3[a2[c]]":
            '3' -> num = 3
            '[' -> push ("", 3), current = ""
            'a' -> current = "a"
            '2' -> num = 2
            '[' -> push ("a", 2), current = ""
            'c' -> current = "c"
            ']' -> pop ("a", 2), current = "a" + "c" * 2 = "acc"
            ']' -> pop ("", 3), current = "" + "acc" * 3 = "accaccacc"

    Complexity:
        Time: O(n + m), where n is the length of s and m the length of the
            decoded output: the scan is linear, but building the output
            costs at least its length, which can far exceed n.
        Space: O(n + m), for the stack of contexts and the strings it holds.
    """

    def decodeString(self, s: str) -> str:
        stack: list[tuple[str, int]] = []
        current = ""
        num = 0

        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == "[":
                stack.append((current, num))
                current = ""
                num = 0
            elif ch == "]":
                prefix, repeat = stack.pop()
                current = prefix + current * repeat
            else:
                current += ch

        return current
