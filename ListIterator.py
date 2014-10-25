# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None
            
class ListNodeIter:
    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return self

    def next(self):
        if not self.node:
            raise StopIteration
        current = self.node
        self.node = self.node.next
        return current
        
class Solution:
    # @param head, a ListNode
    # @return a ListNode
    def collector(self, generator):
        try:
            head = tail = generator.next()
        except:
            return None
        for node in generator:
            tail.next = tail = node
        tail.next = None
        return head
        
    def generator(self, head):
        for key, group in itertools.groupby(ListNodeIter(head), lambda node : node.val):
            yield group.next()
            
    def deleteDuplicates(self, head):
        return self.collector(self.generator(head))
