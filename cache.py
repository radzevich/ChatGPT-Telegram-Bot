from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            # move the key to the end of the OrderedDict to indicate it was recently used
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            return None

    def set(self, key, value):
        # if key already exists in the cache, move it to the end
        if key in self.cache:
            self.cache.move_to_end(key)
        # if the cache is full, remove the least recently used key from the front of the OrderedDict
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        # add the new key-value pair to the end of the OrderedDict
        self.cache[key] = value