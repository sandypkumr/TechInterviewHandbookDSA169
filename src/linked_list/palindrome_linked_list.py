from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        prev = None
        while slow:
            current = slow
            slow = slow.next
            current.next = prev
            prev = current
        while prev:
            if head.val != prev.val:
                return False
            head = head.next
            prev = prev.next
        return True
