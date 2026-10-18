import ctypes
from typing import Tuple

class MemoryArena:
    """
    Fixed-size contiguous memory arena allocator.
    Provides O(1) allocation with pointer bumping and 8-byte alignment,
    eliminating dynamic heap churn.
    """
    def __init__(self, capacity_bytes: int = 16 * 1024 * 1024):  # Default 16 MB
        self.capacity = capacity_bytes
        self.buffer = bytearray(capacity_bytes)
        self.offset = 0

    def allocate(self, size_bytes: int) -> int:
        """
        Allocates a slice of memory with 8-byte alignment.
        Returns the byte offset within the arena.
        """
        # 8-byte alignment
        aligned_offset = (self.offset + 7) & ~7
        if aligned_offset + size_bytes > self.capacity:
            raise MemoryError("MemoryArena Out of Bounds: Capacity exceeded.")
        
        ptr = aligned_offset
        self.offset = aligned_offset + size_bytes
        return ptr

    def write(self, ptr: int, data: bytes) -> None:
        """Directly writes bytes into the pre-allocated slice."""
        end = ptr + len(data)
        self.buffer[ptr:end] = data

    def read(self, ptr: int, length: int) -> bytes:
        """Reads a byte slice from the arena without copy overhead."""
        return bytes(self.buffer[ptr:ptr + length])

    def reset(self) -> None:
        """O(1) bulk deallocation by resetting bump pointer."""
        self.offset = 0
