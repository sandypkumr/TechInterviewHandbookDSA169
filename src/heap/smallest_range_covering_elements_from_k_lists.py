import heapq
from typing import List


class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        heap = []
        max_val = float('-inf')
        for i, num in enumerate(nums):
            heap.append((num[0], i, 0))
            max_val = max(max_val, num[0])
        heapq.heapify(heap)
        start, end = float('-inf'), float('inf')
        while len(heap) == len(nums):
            val, i, j = heapq.heappop(heap)
            if max_val - val < end - start:
                start, end = val, max_val
            if j + 1 < len(nums[i]):
                heapq.heappush(heap, (nums[i][j + 1], i, j + 1))
                max_val = max(max_val, nums[i][j + 1])
        return [start, end]