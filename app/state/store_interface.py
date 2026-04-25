from abc import ABC, abstractmethod
from typing import Any, Optional


class StoreInterface(ABC):
    """
    Abstract interface for all storage backends.

    This allows swapping implementations:
    - InMemoryStore (for dev/testing)
    - RedisStore (for production scaling)
    """

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Store a value with optional TTL (time-to-live).
        """
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        """
        Retrieve value by key.
        Returns None if key does not exist or is expired.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Remove a key from storage.
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in storage.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear all stored data (useful for tests/reset).
        """
        pass