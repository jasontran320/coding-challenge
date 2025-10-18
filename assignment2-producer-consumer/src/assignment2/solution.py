"""
Assignment 2: Producer-Consumer Problem

Architecture:
- Container: Generic container for storing numbers (integers and doubles)
- BoundedQueue: Thread-safe queue with capacity limit
- Producer: Thread that reads from source and writes to queue
- Consumer: Thread that reads from queue and writes to destination
- ProducerConsumerCoordinator: Manages producer/consumer lifecycle
"""

import threading
from collections import deque
from typing import List, Union, Optional

from assignment2.validation import is_valid_number, is_positive_int

Number = Union[int, float]

class Container:
    """Generic container for storing numbers (integers and doubles)

    Thread-safe container with fixed capacity that supports both
    integers and floating-point numbers.

    Args:
        capacity: Maximum number of elements this container can hold

    Raises:
        TypeError: If capacity is not an integer
        ValueError: If capacity is not positive
    """

    def __init__(self, capacity: int):
        if not is_positive_int(capacity):
            raise ValueError(f"Capacity must be a positive integer, got {capacity}")

        self._lock = threading.Lock()
        self.capacity = capacity
        self._data = [None] * capacity
        self._size = 0
        
    def add(self, value: Number) -> None:
        """Add a number to the next available position

        Args:
            value: Number (int or float) to add

        Raises:
            ValueError: If container is full
            TypeError: If value is not a number
        """
        if not is_valid_number(value):
            raise TypeError(
                f"Container expects integer or float, "
                f"got {type(value).__name__}"
            )

        with self._lock:
            if self._size >= self.capacity:
                raise ValueError("Container is full")
            self._data[self._size] = value
            self._size += 1

    def get(self, index: int) -> Optional[Number]:
        """Get number at specific index

        Args:
            index: Position to retrieve from

        Returns:
            Number at index, or None if not set

        Raises:
            IndexError: If index is out of range

        """
        if not self._is_valid_index(index):
            raise IndexError(f"Index {index} out of range [0, {self.capacity})")
        
        with self._lock:
            return self._data[index]

    def size(self) -> int:
        """Return current number of elements (non-None values)

        Returns:
            Count of items currently stored in the container
        """
        with self._lock:
            return self._size

    def __len__(self) -> int:
        """Return capacity (for len() calls)

        Returns:
            Maximum capacity of the container
        """
        return self.capacity

    def _is_valid_index(self, index: int) -> bool:
        """Check if index is within container bounds"""
        return 0 <= index < self.capacity


class BoundedQueue:
    """Thread-safe bounded queue for producer-consumer communication

    Task 3: Queue with half the capacity of source container

    Args:
        capacity: Maximum number of items the queue can hold
    """

    def __init__(self, capacity: int):
        """Initialize bounded queue with fixed capacity"""
        if not is_positive_int(capacity):
            raise ValueError(f"Capacity must be a positive integer, got {capacity}")

        self.capacity = capacity
        self._data = deque(maxlen=capacity)
        self._condition = threading.Condition()
        self._finished = False

    def put(self, item: Number) -> None:
        """Task 4: Producer puts item into queue

        Blocks if queue is full. Notifies consumer when item is added.

        Args:
            item: Number to add to queue

        Raises:
            TypeError: If item is not a valid number
            RuntimeError: If queue is marked as finished

        Note:
            Blocks indefinitely until space is available.
            Consumer must call get() to free space.
        """
        if not is_valid_number(item):
            raise TypeError(
                f"Queue expects integer or float, "
                f"got {type(item).__name__}"
            )

        with self._condition:
            while self._is_full() and not self._finished:
                self._condition.wait()

            if self._finished:
                raise RuntimeError("Cannot add to finished queue")

            self._data.append(item)
            self._condition.notify()

    def get(self) -> Optional[Number]:
        """Task 5: Consumer gets item from queue

        Blocks if queue is empty. Notifies producer when item is removed.
        Returns None when queue is finished and empty.

        Returns:
            Number from queue, or None if finished

        Note:
            Blocks indefinitely until an item is available or queue is finished.
            Producer must call mark_finished() to allow graceful shutdown.
        """
        with self._condition:
            while self._is_empty() and not self._finished:
                self._condition.wait()

            if self._is_empty() and self._finished:
                return None

            item = self._data.popleft()
            self._condition.notify()
            return item
 
    def is_full(self) -> bool:
        """Check if queue is at capacity (thread-safe)

        Returns:
            True if queue is at maximum capacity, False otherwise
        """
        with self._condition:
            return self._is_full()

    def is_empty(self) -> bool:
        """Check if queue is empty (thread-safe)

        Returns:
            True if queue contains no items, False otherwise
        """
        with self._condition:
            return self._is_empty()

    def mark_finished(self) -> None:
        """Signal that no more items will be produced

        Notifies all waiting consumers to check finished status.
        """
        with self._condition:
            self._finished = True
            self._condition.notify_all()

    def _is_full(self) -> bool:
        """Internal check if queue is at capacity (assumes lock held)"""
        return len(self._data) >= self.capacity

    def _is_empty(self) -> bool:
        """Internal check if queue is empty (assumes lock held)"""
        return len(self._data) == 0


class Producer(threading.Thread):
    """Task 4: Producer thread that reads from source container to queue

    Reads all numbers from source container and puts them into the queue.
    Notifies consumer when queue becomes full.

    Args:
        source: Container to read numbers from
        queue: BoundedQueue to write numbers to
        name: Thread name for debugging (auto-generated if not provided)
    """

    _counter = 0
    _counter_lock = threading.Lock()

    def __init__(self, source: Container, queue: BoundedQueue, name: str = None):
        """Initialize producer thread

        Args:
            source: Container to read numbers from
            queue: BoundedQueue to write numbers to
            name: Thread name for debugging (auto-generated as "Producer-N" if not provided)
        """
        if name is None:
            with Producer._counter_lock:
                Producer._counter += 1
                name = f"Producer-{Producer._counter}"

        super().__init__(name=name)
        self.source = source
        self.queue = queue

    def run(self) -> None:
        """Read numbers from source container and put into queue

        Transfers all items from source container to queue, then signals
        completion by calling mark_finished() on the queue.
        """
        for i in range(self.source.size()):
            item = self.source.get(i)
            self.queue.put(item)
        self.queue.mark_finished()

class Consumer(threading.Thread):
    """Task 5: Consumer thread that reads from queue to destination container

    Reads numbers from queue and writes them to destination container.
    Notifies producer when queue becomes empty.

    Args:
        queue: BoundedQueue to read numbers from
        destination: Container to write numbers to
        name: Thread name for debugging (auto-generated as "Consumer-N" if not provided)
    """

    _counter = 0
    _counter_lock = threading.Lock()

    def __init__(self, queue: BoundedQueue, destination: Container, name: str = None):
        """Initialize consumer thread

        Args:
            queue: BoundedQueue to read numbers from
            destination: Container to write numbers to
            name: Thread name for debugging (auto-generated as "Consumer-N" if not provided)
        """
        if name is None:
            with Consumer._counter_lock:
                Consumer._counter += 1
                name = f"Consumer-{Consumer._counter}"

        super().__init__(name=name)
        self.queue = queue
        self.destination = destination

    def run(self) -> None:
        """Read numbers from queue and write to destination container

        Continuously reads from queue until None is received (finished signal).
        """
        item = self.queue.get()
        while item is not None:
            self.destination.add(item)
            item = self.queue.get()


class ProducerConsumerCoordinator:
    """Coordinates the producer-consumer system

    Sets up all components (source, destination, queue, producer, consumer)
    and manages their lifecycle.

    Args:
        source_data: List of integers and doubles to process
    """

    def __init__(self, source_data: List[Number]):
        """Initialize the producer-consumer system

        Task 1: Create source container and populate with data
        Task 2: Create destination container with same capacity
        Task 3: Create queue with half capacity
        Task 4 & 5: Create producer and consumer threads

        TODO: Set up all components - source/destination containers, bounded queue, and threads
        """
        # TODO: Implement complete system setup
        pass

    def start(self) -> None:
        """Start producer and consumer threads

        TODO: Start both producer and consumer threads concurrently
        """
        # TODO: Start both threads
        pass

    def wait_completion(self) -> None:
        """Wait for both threads to complete

        TODO: Wait for both threads to finish their work
        """
        # TODO: Join both threads
        pass

    def verify(self) -> bool:
        """Task 6: Verify all numbers copied from source to destination

        Returns:
            True if all numbers match, False otherwise

        TODO: Compare source and destination containers to confirm all data transferred correctly
        """
        # TODO: Implement verification logic
        pass


def main():
    """Main entry point demonstrating the producer-consumer solution

    TODO: Create and run the complete producer-consumer system, then verify the results
    """
    # TODO: Wire up coordinator, execute transfer, and verify results
    pass


if __name__ == "__main__":
    main()
