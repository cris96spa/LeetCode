from typing import Callable, List


class Solution:
    """
    Evaluate an arithmetic expression written in Reverse Polish Notation.

    Plan
    ----
    Use a stack to process the tokens from left to right.

    - If the current token is a number, push it onto the stack.
    - If the current token is an operator, pop the top two numbers
      from the stack, apply the operator in the correct order, and
      push the result back onto the stack.
    - At the end of the scan, the stack contains exactly one value:
      the final result.

    Why a stack works
    -----------------
    In Reverse Polish Notation, every operator applies to the most
    recent two operands that have not yet been used. A stack is the
    natural data structure for this because it gives direct access
    to the most recently inserted values.

    For an operator:
    - The first popped value is the right operand.
    - The second popped value is the left operand.

    This order matters for subtraction and division.

    Example:
    tokens = ["2", "1", "+", "3", "*"]

    Process:
    - push 2
    - push 1
    - '+' => pop 1 and 2, compute 2 + 1 = 3, push 3
    - push 3
    - '*' => pop 3 and 3, compute 3 * 3 = 9, push 9

    Final result: 9

    Division
    --------
    The problem requires division to truncate toward zero.
    In Python, using // would floor the result for negative numbers,
    so we compute the sign separately and divide absolute values.

    Time Complexity
    ---------------
    O(n), where n is the number of tokens.
    Each token is processed exactly once, and each stack operation
    takes O(1) time.

    Space Complexity
    ----------------
    O(n) in the worst case, when many operands are stored in the stack
    before being reduced by operators.
    """

    def __init__(self):
        self.operation_mapping: dict[str, Callable[[int, int], int]] = {
            "+": self._sum,
            "-": self._subtract,
            "*": self._multiply,
            "/": self._divide,
        }

    def _sum(self, a: int, b: int) -> int:
        return a + b

    def _subtract(self, a: int, b: int) -> int:
        return a - b

    def _multiply(self, a: int, b: int) -> int:
        return a * b

    def _divide(self, a: int, b: int) -> int:
        sign = -1 if (a < 0) ^ (b < 0) else 1
        return sign * (abs(a) // abs(b))

    def _is_operator(self, elem: str) -> bool:
        return elem in self.operation_mapping

    def evalRPN(self, tokens: List[str]) -> int:
        stack = []

        for elem in tokens:
            if self._is_operator(elem):
                # Pop right operand first, then left operand
                b = stack.pop()
                a = stack.pop()
                result = self.operation_mapping[elem](a, b)
                stack.append(result)
            else:
                stack.append(int(elem))

        return stack.pop()