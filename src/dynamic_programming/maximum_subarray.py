from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_sum = nums[0]
        current_sum = 0
        for i in range(len(nums)):
            if current_sum < 0:
                current_sum = 0
            current_sum = current_sum + nums[i]
            max_sum = max(max_sum, current_sum)
        return max_sum