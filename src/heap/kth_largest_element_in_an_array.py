from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        min_val, max_val = min(nums), max(nums)
        count = [0] * (max_val - min_val + 1)
        for num in nums:
            count[num - min_val] += 1
        for i in range(max_val, min_val - 1, -1):
            k -= count[i - min_val]
            if k <= 0:
                return i