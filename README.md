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
   git clone https://github.com/jasontran320/coding-challenge.git
   cd coding-challenge
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

**Quick start:**
```bash
# Assignment 1
cd assignment1-data-aggregation
python run.py

# Assignment 2
cd assignment2-producer-consumer
python run.py
```

### Running Tests

**Important:** Run tests from the project root directory, specifying which assignment to test.

```bash
# Run Assignment 1 tests
pytest assignment1-data-aggregation/tests/ -v

# Run Assignment 2 tests
pytest assignment2-producer-consumer/tests/ -v
```

The project includes a `pytest.ini` configuration file that automatically sets up the Python path for both assignments.
