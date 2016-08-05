class ListNode:
    def __init__(self, value):
        self.key = value
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
    def __get__(self, key):
        if key not in self.value_map:
            return None
        
        value, node = self.value_map[key]
        self.double_list.update(node)
        return value
        
    # @param key, an integer
    # @param value, an integer
    # @return nothing
    def __set__(self, key, value):
        if key in self.value_map:
            self.value_map[key][0] = value
            self.double_list.update(self.value_map[key][1])
            return
        
        if len(self.value_map) == self.capacity:
            del_key = self.double_list.pop().key
            del value_map[del_key]

        node = ListNode(key)
        self.value_map[key] = [value, node]
        self.double_list.insert(node)
        
    def __delitem__(self, key):
        self.double_list.remove(value_map[key])
        del self.value_map[key]
        
class DoubleLRUCache:
    # @param capacity, an integer
    def __init__(self, capacity):
        self.cache1 = LRUCache(capacity)
        self.cache2 = LRUCache(capacity)

    # @return an integer
    def __get__(self, key):
        v1 = self.cache1[key]
        if v1:
            return v1
        v2 = self.cache2[key]
        if v2:
            del self.cache2[key]
            self.cache1[key] = v2            
            return v2
        return None

    def __set__(self, key, value):
        v1 = self.cahce1[key]
        if v1:
            self.cahce1[key] = value
            return
        v2 = self.cache2[key]
        if v2:
            del self.cache2[key]
            self.cache1[key] = value
            return
        self.cahce2[key] = value

class MultiLRUCache:
    # @param capacity, an integer
    def __init__(self, n, capacity):
        self.caches = [LRUCache(capacity) for i in range(n)]

    # @return an integer
    def __get__(self, key):
        for i in range(len(self.caches)):
            v = self.caches[i][key]
            if v:
                if i == 0:
                    return v
                else:
                    del self.caches[i][key]
                    self.caches[i - 1][key] = v
                    return v
        return None

    def __set__(self, key, value):
        for i in range(len(self.caches)):
            v = self.caches[i][key]
            if v:
                if i == 0:
                    self.caches[i][key] = value
                    return 
                else:
                    del self.caches[i][key]
                    self.caches[i-1][key] = value
                    return
        self.cahces[-1][key] = value

from functools import wraps
def memo(fn):
    @wraps(fn)
    def wrapper(*args):
        result = wrapper.cache[args]
        if result is None:
            result = fn(*args)
            wrapper.cache[args] = result
        return result
    wrapper.cache = DoubleLRUCache(1000)
    return wrapper
