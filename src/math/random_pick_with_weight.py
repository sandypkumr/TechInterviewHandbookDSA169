from random import random
from typing import List


class Solution:

    def __init__(self, w: List[int]):
        self.prefix_sum = [0]
        for weight in w:
            self.prefix_sum.append(self.prefix_sum[-1] + weight)

    def pickIndex(self) -> int:
        target = self.prefix_sum[-1] * random()
        left, right = 0, len(self.prefix_sum) - 1
        while left < right:
            mid = left + (right - left) // 2
            if self.prefix_sum[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left - 1
