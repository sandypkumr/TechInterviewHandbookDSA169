from collections import deque
from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if k == 1:
            return nums
        n = len(nums)
        res = []
        max_deque = deque()
        for i in range(n):
            # Remove elements not in the window
            if max_deque and max_deque[0] < i - k + 1:
                max_deque.popleft()
            # Remove smaller elements in the window
            while max_deque and nums[max_deque[-1]] <= nums[i]:
                max_deque.pop()
            max_deque.append(i)
            # Append the maximum element of the current window
            if i >= k - 1:
                res.append(nums[max_deque[0]])
        return res