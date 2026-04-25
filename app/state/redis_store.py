import time
import json
import threading


class RedisStore:
    """
    Lightweight Redis-like in-memory fallback store.
    Can later be replaced with real Redis without changing service logic.
    """

    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def set(self, key: str, value: dict, ttl: int = None):
        """
        Store a value with optional TTL (time to live in seconds)
        """
        with self.lock:
            expire_at = time.time() + ttl if ttl else None

            self.store[key] = {
                "value": value,
                "expire_at": expire_at
            }

    def get(self, key: str):
        """
        Retrieve value if not expired
        """
        with self.lock:
            item = self.store.get(key)

            if not item:
                return None

            # check expiry
            if item["expire_at"] and time.time() > item["expire_at"]:
                del self.store[key]
                return None

            return item["value"]

    def delete(self, key: str):
        """
        Remove key from store
        """
        with self.lock:
            if key in self.store:
                del self.store[key]

    def exists(self, key: str) -> bool:
        """
        Check if key exists and is not expired
        """
        return self.get(key) is not None

    def clear(self):
        """
        Clear all stored data (useful for tests)
        """
        with self.lock:
            self.store.clear()