from typing import Optional, Tuple, List, Any

class RobinHoodHashMap:
    """
    Robin Hood Open-Addressing Hash Map.
    Minimizes probe sequence variance, keeping lookups tightly bounded to O(1).
    Stores entries in contiguous flat arrays for CPU cache spatial locality.
    """
    def __init__(self, power_of_two: int = 17):  # 2^17 = 131,072 slots
        self.capacity = 1 << power_of_two
        self.mask = self.capacity - 1
        self.keys: List[Optional[str]] = [None] * self.capacity
        self.values: List[Optional[Any]] = [None] * self.capacity
        self.dist: List[int] = [-1] * self.capacity
        self.count = 0

    def _hash(self, key: str) -> int:
        # FNV-1a fast 64-bit non-cryptographic hash
        h = 14695981039346656037
        for char in key.encode('utf-8'):
            h ^= char
            h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
        return h & self.mask

    def put(self, key: str, value: Any) -> bool:
        idx = self._hash(key)
        d = 0
        curr_key = key
        curr_val = value

        while True:
            # Slot empty
            if self.keys[idx] is None:
                self.keys[idx] = curr_key
                self.values[idx] = curr_val
                self.dist[idx] = d
                self.count += 1
                return True

            # Existing key update
            if self.keys[idx] == curr_key:
                self.values[idx] = curr_val
                return True

            # Robin Hood: steal from the rich
            if self.dist[idx] < d:
                # Swap current with richer slot
                curr_key, self.keys[idx] = self.keys[idx], curr_key
                curr_val, self.values[idx] = self.values[idx], curr_val
                d, self.dist[idx] = self.dist[idx], d

            idx = (idx + 1) & self.mask
            d += 1
            if d > 128:  # Maximum probe bound guard
                raise OverflowError("Hash table probe distance exceeded safe bounds.")

    def get(self, key: str) -> Optional[Any]:
        idx = self._hash(key)
        d = 0

        while True:
            if self.keys[idx] is None or d > self.dist[idx]:
                return None
            if self.keys[idx] == key:
                return self.values[idx]
            idx = (idx + 1) & self.mask
            d += 1
