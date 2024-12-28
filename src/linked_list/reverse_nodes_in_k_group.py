from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        dummy = ListNode()
        dummy.next = head
        prev = dummy
        while True:
            tail = prev
            for _ in range(k):
                tail = tail.next
                if not tail:
                    return dummy.next
            next_group = tail.next
            tail.next = None
            tail = prev.next
            prev.next = self.reverse(prev.next)
            tail.next = next_group
            prev = tail

    def reverse(self, node: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        while node:
            next_node = node.next
            node.next = prev
            prev = node
            node = next_node
        return prev
