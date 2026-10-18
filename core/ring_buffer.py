from typing import Optional, Any, List

class LockFreeRingBuffer:
    """
    Lock-free bounded circular ring buffer.
    Uses bitwise power-of-two masking ((head) & (capacity - 1)) for O(1) modulo-free indexing.
    Eliminates mutex locks in high-frequency ingestion queues.
    """
    def __init__(self, power_of_two: int = 16):  # 2^16 = 65,536 elements
        self.capacity = 1 << power_of_two
        self.mask = self.capacity - 1
        self.buffer: List[Optional[Any]] = [None] * self.capacity
        self.head = 0  # Write sequence counter
        self.tail = 0  # Read sequence counter

    def enqueue(self, item: Any) -> bool:
        """Non-blocking atomic enqueue."""
        if (self.head - self.tail) >= self.capacity:
            return False  # Buffer full (backpressure signal)
        
        index = self.head & self.mask
        self.buffer[index] = item
        self.head += 1
        return True

    def dequeue(self) -> Optional[Any]:
        """Non-blocking atomic dequeue."""
        if self.head == self.tail:
            return None  # Buffer empty
        
        index = self.tail & self.mask
        item = self.buffer[index]
        self.buffer[index] = None
        self.tail += 1
        return item

    def size(self) -> int:
        return self.head - self.tail

    def is_empty(self) -> bool:
        return self.head == self.tail
