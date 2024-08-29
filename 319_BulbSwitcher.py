import math
class Solution:
    def bulbSwitch(self, n: int) -> int:
        if n==0 or n==1:
            return n
        on = n
        for i in range(2, n+1):
            on -= int(math.sqrt(i))
        return n
