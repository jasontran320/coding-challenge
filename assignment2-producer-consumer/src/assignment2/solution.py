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

Number = Union[int, float]


class Container:
    """Generic container for storing numbers (integers and doubles)

    Thread-safe container with fixed capacity that supports both
    integers and floating-point numbers.

    Args:
        capacity: Maximum number of elements the container can hold
    """

    def __init__(self, capacity: int):
        """Initialize container with fixed capacity

        TODO: Set up a thread-safe container that can store numbers at specific indices
        """
        # TODO: Implement initialization
        pass

    def add(self, value: Number, index: int) -> None:
        """Add a number at specific index

        Args:
            value: Number (int or float) to add
            index: Position to add the value

        Raises:
            IndexError: If index is out of range

        TODO: Store the value at the given index in a thread-safe manner with validation
        """
        # TODO: Implement thread-safe add operation
        pass

    def get(self, index: int) -> Optional[Number]:
        """Get number at specific index

        Args:
            index: Position to retrieve from

        Returns:
            Number at index, or None if not set

        Raises:
            IndexError: If index is out of range

        TODO: Retrieve the value at the given index in a thread-safe manner with validation
        """
        # TODO: Implement thread-safe get operation
        pass

    def size(self) -> int:
        """Return current number of elements

        TODO: Return the count of items stored in the container (thread-safe)
        """
        # TODO: Return current size
        pass

    def __len__(self) -> int:
        """Return capacity (for len() calls)

        TODO: Return the maximum capacity of the container
        """
        # TODO: Return capacity
        pass


class BoundedQueue:
    """Thread-safe bounded queue for producer-consumer communication

    Task 3: Queue with half the capacity of source container

    Args:
        capacity: Maximum number of items the queue can hold
    """

    def __init__(self, capacity: int):
        """Initialize bounded queue with fixed capacity

        TODO: Set up a bounded queue with synchronization primitives for producer-consumer coordination
        """
        # TODO: Implement initialization
        pass

    def put(self, item: Number) -> None:
        """Task 4: Producer puts item into queue

        Blocks if queue is full. Notifies consumer when item is added.

        Args:
            item: Number to add to queue

        TODO: Add item to queue, blocking if full, and notify waiting consumers
        Note: Handle spurious wakeups properly
        """
        # TODO: Implement blocking put with notification
        pass

    def get(self) -> Optional[Number]:
        """Task 5: Consumer gets item from queue

        Blocks if queue is empty. Notifies producer when item is removed.
        Returns None when queue is finished and empty.

        Returns:
            Number from queue, or None if finished

        TODO: Remove and return item from queue, blocking if empty, and notify waiting producers
        Note: Handle graceful shutdown when producer is finished
        """
        # TODO: Implement blocking get with notification
        pass

    def is_full(self) -> bool:
        """Check if queue is at capacity

        TODO: Return whether the queue has reached its maximum capacity
        """
        # TODO: Implement is_full check
        pass

    def is_empty(self) -> bool:
        """Check if queue is empty

        TODO: Return whether the queue contains no items
        """
        # TODO: Implement is_empty check
        pass

    def mark_finished(self) -> None:
        """Signal that no more items will be produced

        TODO: Signal completion to waiting consumers so they can exit gracefully
        """
        # TODO: Implement mark_finished
        pass


class Producer(threading.Thread):
    """Task 4: Producer thread that reads from source container to queue

    Reads all numbers from source container and puts them into the queue.
    Notifies consumer when queue becomes full.

    Args:
        source: Container to read numbers from
        queue: BoundedQueue to write numbers to
        name: Thread name for debugging
    """

    def __init__(self, source: Container, queue: BoundedQueue, name: str = "Producer"):
        """Initialize producer thread

        TODO: Set up the producer thread with references to source and queue
        """
        # TODO: Implement initialization
        pass

    def run(self) -> None:
        """Read numbers from source container and put into queue

        TODO: Read all items from source and transfer them to the queue, then signal completion
        """
        # TODO: Implement producer logic
        pass


class Consumer(threading.Thread):
    """Task 5: Consumer thread that reads from queue to destination container

    Reads numbers from queue and writes them to destination container.
    Notifies producer when queue becomes empty.

    Args:
        queue: BoundedQueue to read numbers from
        destination: Container to write numbers to
        name: Thread name for debugging
    """

    def __init__(self, queue: BoundedQueue, destination: Container, name: str = "Consumer"):
        """Initialize consumer thread

        TODO: Set up the consumer thread with references to queue and destination
        """
        # TODO: Implement initialization
        pass

    def run(self) -> None:
        """Read numbers from queue and write to destination container

        TODO: Continuously read items from queue and write to destination until signaled to stop
        """
        # TODO: Implement consumer logic
        pass


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
