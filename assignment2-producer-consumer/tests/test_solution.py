"""
Unit tests for Assignment 2: Producer-Consumer Problem

Run tests from project root:
    pytest assignment2-producer-consumer/tests/ -v
"""

import pytest
import threading

from assignment2.solution import (
    Container, BoundedQueue, Producer, Consumer, ProducerConsumerCoordinator
)

# Test data path (if needed)
# For this assignment, we generate test data programmatically


class TestContainer:
    """Test Container class (Task 1 & 2)"""

    def test_container_creation(self):
        """Test creating container with specified capacity"""
        container = Container(10)
        assert len(container) == 10
        assert container.capacity == 10
        assert container.size() == 0

    def test_add_and_get(self):
        """Test adding and getting values"""
        container = Container(5)
        container.add(10)
        container.add(20)
        container.add(30)

        assert container.get(0) == 10
        assert container.get(1) == 20
        assert container.get(2) == 30
        assert container.size() == 3

    def test_mixed_types(self):
        """Test storing both integers and floats"""
        container = Container(5)
        container.add(42)
        container.add(3.14)
        container.add(100)
        container.add(2.718)

        assert container.get(0) == 42
        assert isinstance(container.get(0), int)
        assert container.get(1) == 3.14
        assert isinstance(container.get(1), float)
        assert container.size() == 4

    def test_add_when_full(self):
        """Test adding to full container raises ValueError"""
        container = Container(3)
        container.add(1)
        container.add(2)
        container.add(3)

        with pytest.raises(ValueError, match="Container is full"):
            container.add(4)

    def test_get_invalid_index(self):
        """Test getting with invalid index raises IndexError"""
        container = Container(5)
        container.add(10)

        with pytest.raises(IndexError):
            container.get(-1)
        with pytest.raises(IndexError):
            container.get(5)

    def test_thread_safety(self):
        """Test that concurrent add operations are thread-safe"""
        container = Container(100)

        def add_numbers(start, count):
            for i in range(count):
                container.add(start + i)

        # Create 10 threads, each adding 10 unique numbers
        threads = []
        for i in range(10):
            t = threading.Thread(target=add_numbers, args=(i * 10, 10))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Verify correct size
        assert container.size() == 100

        # Verify all values present (0-99) with no corruption
        values = [container.get(i) for i in range(100)]
        assert sorted(values) == list(range(100))


class TestBoundedQueue:
    """Test BoundedQueue class (Task 3)"""

    def test_queue_creation(self):
        """Test creating queue with capacity"""
        # TODO: Verify queue initializes with correct capacity and is empty
        pass

    def test_put_and_get(self):
        """Test putting and getting items"""
        # TODO: Verify items are retrieved in FIFO order
        pass

    def test_is_full(self):
        """Test queue full detection"""
        # TODO: Verify is_full() returns True when at capacity
        pass

    def test_blocking_when_full(self):
        """Test that put blocks when queue is full"""
        # TODO: Verify put() blocks when queue is full and unblocks when space available
        pass

    def test_blocking_when_empty(self):
        """Test that get blocks when queue is empty"""
        # TODO: Verify get() blocks when queue is empty and unblocks when item available
        pass

    def test_thread_safety(self):
        """Test that container is thread-safe"""
        # TODO: Verify concurrent add operations don't cause data corruption
        pass


class TestProducer:
    """Test Producer thread (Task 4)"""

    def test_producer_reads_all_items(self):
        """Test that producer reads all items from source"""
        # TODO: Verify producer transfers all items from source to queue
        pass


class TestConsumer:
    """Test Consumer thread (Task 5)"""

    def test_consumer_writes_all_items(self):
        """Test that consumer writes all items to destination"""
        # TODO: Verify consumer transfers all items from queue to destination
        pass


class TestProducerConsumer:
    """Test Producer and Consumer working together"""

    def test_simple_transfer(self):
        """Test transferring small amount of data"""
        # TODO: Verify complete transfer of small dataset (4 items)
        pass

    def test_large_transfer(self):
        """Test transferring large amount of data"""
        # TODO: Verify complete transfer of large dataset (100+ items) without deadlock
        pass

    def test_empty_transfer(self):
        """Test transferring empty amount of data"""
        # TODO: Verify complete transfer of empty dataset (0 items)
        pass

    def test_mixed_data_types(self):
        """Test transferring mixed integers and floats"""
        # TODO: Verify both int and float types are preserved during transfer
        pass


class TestCoordinator:
    """Test ProducerConsumerCoordinator (Complete System)"""

    def test_coordinator_setup(self):
        """Test that coordinator sets up all components correctly"""
        # TODO: Verify coordinator initializes all components with correct capacities
        pass

    def test_data_transfer_correctness(self):
        """Task 6: Test complete data transfer and verification"""
        # TODO: Verify end-to-end transfer completes successfully with all data matching
        pass

    def test_verification_method(self):
        """Test the verify() method"""
        # TODO: Verify the verify() method correctly detects successful transfers
        pass

    def test_order_preserved(self):
        """Test that order of elements is preserved"""
        # TODO: Verify elements appear in destination in same order as source
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
