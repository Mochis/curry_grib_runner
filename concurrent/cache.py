import threading


# Implements a cache using a dict() object
class Cache:
    def __init__(self):
        self.cache = dict()
        self.lock = threading.Lock()

    def put_value(self, key, value):
        self.lock.acquire()
        if key not in self.cache:
            self.cache[key] = value
        self.lock.release()

    def get_value(self, key):
        self.lock.acquire()
        value = self.cache.get(key, None)
        self.lock.release()
        return value
