"""
Unit tests for Assignment 2: Producer-Consumer Problem

Run tests from project root:
    pytest assignment2-producer-consumer/tests/ -v
"""

import pytest
import threading
import time

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
        queue = BoundedQueue(5)
        assert queue.capacity == 5
        assert queue.is_empty()
        assert not queue.is_full()

    def test_put_and_get_fifo(self):
        """Test FIFO ordering"""
        queue = BoundedQueue(3)
        queue.put(10)
        queue.put(20)
        queue.put(30)

        assert queue.get() == 10
        assert queue.get() == 20
        assert queue.get() == 30

    def test_is_full_and_empty(self):
        """Test full and empty detection"""
        queue = BoundedQueue(2)
        assert queue.is_empty()

        queue.put(1)
        assert not queue.is_empty()
        assert not queue.is_full()

        queue.put(2)
        assert queue.is_full()

        queue.get()
        assert not queue.is_full()

    def test_blocking_put(self):
        """Test that put blocks when queue is full"""
        queue = BoundedQueue(2)
        queue.put(1)
        queue.put(2)

        put_completed = []

        def blocking_put():
            queue.put(3)  # Should block
            put_completed.append(True)

        t = threading.Thread(target=blocking_put)
        t.start()

        # Give thread time to block
        time.sleep(0.1)
        assert len(put_completed) == 0  # Should still be blocked

        # Unblock by getting an item
        assert queue.get() == 1  # Get first item, makes space
        t.join(timeout=1.0)

        assert len(put_completed) == 1  # Should have completed
        # Queue now has [2, 3]
        assert queue.get() == 2
        assert queue.get() == 3

    def test_blocking_get(self):
        """Test that get blocks when queue is empty"""
        queue = BoundedQueue(2)

        result = []

        def blocking_get():
            item = queue.get()  # Should block
            result.append(item)

        t = threading.Thread(target=blocking_get)
        t.start()

        # Give thread time to block
        time.sleep(0.1)
        assert len(result) == 0  # Should still be blocked

        # Unblock by putting an item
        queue.put(42)
        t.join(timeout=1.0)

        assert result == [42]

    def test_graceful_shutdown(self):
        """Test mark_finished allows graceful shutdown"""
        queue = BoundedQueue(2)
        queue.put(1)
        queue.put(2)

        # Get items then mark finished
        assert queue.get() == 1
        assert queue.get() == 2

        queue.mark_finished()

        # Get on finished empty queue returns None
        assert queue.get() is None

        # Put on finished queue raises error
        with pytest.raises(RuntimeError):
            queue.put(3)

    def test_thread_safety(self):
        """Test concurrent operations don't corrupt data"""
        queue = BoundedQueue(5)
        results = []

        def putter():
            queue.put(1)
            queue.put(2)

        def getter():
            results.append(queue.get())
            results.append(queue.get())

        # Run put and get concurrently
        t1 = threading.Thread(target=putter)
        t2 = threading.Thread(target=getter)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Verify both items received correctly
        assert sorted(results) == [1, 2]


class TestProducer:
    """Test Producer thread (Task 4)"""

    def test_producer_transfers_all_items(self):
        """Test that producer transfers all items from source to queue"""
        # Setup: Create source with test data
        source = Container(5)
        source.add(10)
        source.add(20)
        source.add(30)
        source.add(40)
        source.add(50)

        # Create queue with smaller capacity to test blocking behavior
        queue = BoundedQueue(3)

        # Create and run producer
        producer = Producer(source, queue)
        producer.start()

        # Consume items to prevent deadlock
        results = []
        while True:
            item = queue.get()
            if item is None:  # Producer marked finished
                break
            results.append(item)

        producer.join()

        # Verify all items transferred in order
        assert results == [10, 20, 30, 40, 50]

    def test_producer_marks_queue_finished(self):
        """Test that producer marks queue as finished after transferring all items"""
        source = Container(3)
        source.add(1)
        source.add(2)
        source.add(3)

        queue = BoundedQueue(5)
        producer = Producer(source, queue)

        producer.start()
        producer.join()

        # Drain the queue
        assert queue.get() == 1
        assert queue.get() == 2
        assert queue.get() == 3

        # Queue should return None since it's finished and empty
        assert queue.get() is None

    def test_producer_auto_naming(self):
        """Test that producer auto-generates names when not provided"""
        source = Container(1)
        source.add(42)
        queue = BoundedQueue(1)

        # Create producers without explicit names
        producer1 = Producer(source, queue)
        producer2 = Producer(source, queue)
        producer3 = Producer(source, queue, name="CustomProducer")

        # Check auto-generated names
        assert "Producer-" in producer1.name
        assert "Producer-" in producer2.name
        assert producer1.name != producer2.name  # Should be unique

        # Check custom name preserved
        assert producer3.name == "CustomProducer"


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
