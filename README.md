# Level 2 Coding Challenge

This repository contains two programming challenges demonstrating different software engineering concepts.

## Structure

```
coding-challenge/
├── assignment1-data-aggregation/
├── assignment2-producer-consumer/
└── requirements.txt
```

## Assignments

- **Assignment 1:** Data Aggregation & Grouping
- **Assignment 2:** Producer-Consumer Problem

## Setup

### Prerequisites
- Python 3.8 or higher

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Level\ 2\ Coding\ Challenge\ 1
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Solutions

Each assignment has its own directory with specific instructions. See the README in each assignment folder for details.

### Running Tests

**Important:** Run all tests from the project root directory.

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run tests for specific assignment
pytest assignment1-data-aggregation/tests/ -v
```

The project includes a `pytest.ini` configuration file that automatically sets up the Python path.
