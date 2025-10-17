# Assignment 2: Producer-Consumer Problem

## Problem Statement

Implement the classic producer-consumer problem using Python threading.

### Tasks

1. **Create a source container** and populate it with integers and doubles
2. **Create a destination container** that can store both integers and doubles with the same capacity as the source container
3. **Create a queue** with half the capacity of the source container
4. **Implement a Producer** that will read numbers from the source container into the queue and notify the consumer when the queue is full
5. **Create a Consumer** that will read from the queue into the destination container and notify the producer when the queue is empty
6. **Write a test** to confirm the numbers from the source container have been copied to the destination container

## Architecture

```
Source Container → Producer → Bounded Queue → Consumer → Destination Container
                      ↓                           ↓
                   (notify)                   (notify)
```

**Components:**
- `Container`: Thread-safe storage for numbers (int/float)
- `BoundedQueue`: Fixed-capacity queue with blocking operations
- `Producer`: Thread that reads from source and writes to queue
- `Consumer`: Thread that reads from queue and writes to destination
- `ProducerConsumerCoordinator`: Manages the complete system

**Synchronization:**
- Uses `threading.Condition` for producer-consumer coordination
- Producer blocks when queue is full
- Consumer blocks when queue is empty

## Running the Solution

From the `assignment2-producer-consumer/` directory:

```bash
# Simple approach - use the convenience script
python run.py

# Or use the standard Python module approach (from src directory)
cd src
python -m assignment2.solution
```

## Running Tests

From the project root directory:

```bash
pytest assignment2-producer-consumer/tests/ -v
```

## Design Patterns

- **Producer-Consumer Pattern**: Classic concurrency pattern for decoupling production and consumption
- **Monitor Pattern**: Uses `threading.Condition` for synchronization
- **Thread-Safe Container**: Uses locks for concurrent access
