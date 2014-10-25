class ListNode:
    def __init__(self, value):
        self.value = value
        self.pre = None
        self.next = None

class DoubleList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def remove(self, node):
        if node.pre == None and node.next == None:
            self.head = None
            self.tail = None
            return node
        if node.pre == None:
            node.next.pre = None
            self.head = node.next
            return node
        if node.next == None:
            node.pre.next = None
            self.tail = node.pre
            return node
        node.pre.next = node.next
        node.next.pre = node.pre
        return node
    
    def insert(self, node):
        node.pre = None
        node.next = None
        if self.tail == None:
            self.head = node
            self.tail = node
            return
        self.tail.next = node
        node.pre = self.tail
        self.tail = node
        
    def update(self, node):
        self.remove(node)
        self.insert(node)
    
    def pop(self):
        return self.remove(self.head)

class LRUCache:
    # @param capacity, an integer
    def __init__(self, capacity):
        self.capacity = capacity
        self.value_map = dict()
        self.double_list = DoubleList()

    # @return an integer
    def get(self, key):
        if key not in self.value_map:
            return -1
        
        value, node = self.value_map[key]
        self.double_list.update(node)
        return value
        

    # @param key, an integer
    # @param value, an integer
    # @return nothing
    def set(self, key, value):
        if key in self.value_map:
            self.value_map[key][0] = value
            self.double_list.update(self.value_map[key][1])
            return
        
        if len(self.value_map) == self.capacity:
            pop_key = self.double_list.pop().value
            self.value_map.pop(pop_key)

        node = ListNode(key)
        self.value_map[key] = [value, node]
        self.double_list.insert(node)
