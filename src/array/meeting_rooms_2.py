"""

Given an array of meeting time intervals, where each interval is represented as [start, end], find the minimum number
of meeting rooms required to host all the meetings.

For example:

Input: [[0, 30], [5, 10], [15, 20]]
Output: 2

"""
from typing import List


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        if not intervals:
            return 0
        start_times = sorted([interval.start for interval in intervals])
        end_times = sorted([interval.end for interval in intervals])
        start_pointer = end_pointer = 0
        num_rooms = res = 0
        while start_pointer < len(start_times):
            if start_times[start_pointer] < end_times[end_pointer]:
                num_rooms += 1
                start_pointer += 1
            else:
                num_rooms -= 1
                end_pointer += 1
            res = max(res, num_rooms)
        return res