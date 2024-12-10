"""

We are given a list of employees, where each employee has a list of non-overlapping intervals representing their
working hours. These intervals are sorted by start time. We need to find the common free time intervals across all
employees.

The free time intervals are the time periods when all employees are not working.

Example:
    Input: [[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]
    Output: [[4, 6], [7, 9]]

    Explanation:
    The common free time intervals are [4, 6] and [7, 9].

"""

from typing import List

class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Solution:
    def employeeFreeTime(self, schedule: List[List[Interval]]) -> List[Interval]:
        if not schedule:
            return []
        intervals = sorted([interval for employee in schedule for interval in employee], key=lambda x: x.start)
        free_time = []
        end = intervals[0].end
        for i in range(1, len(intervals)):
            if intervals[i].start > end:
                free_time.append(Interval(end, intervals[i].start))
            end = max(intervals[i].end, end)
        return free_time