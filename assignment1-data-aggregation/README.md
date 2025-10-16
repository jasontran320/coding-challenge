# Assignment 1: Data Aggregation & Grouping

## Data Setup

This assignment uses the **Customer Shopping Data** CSV file.

### Dataset Location
The dataset file `customer_shopping_data.csv` should be placed in the `data/` directory:
```
assignment1-data-aggregation/data/customer_shopping_data.csv
```

### Why isn't the CSV in the repository?
The dataset is large (7.2MB) and has been excluded from version control to keep the repository lightweight.

### How to obtain the dataset
- Source: [customer_shopping_data.csv](https://drive.google.com/file/d/1GZHRdGvhK_e6qRyUFGIodGFLCHj-5U9b/view?usp=sharing)
- Or use your own customer shopping dataset with the required columns

### Required CSV Columns
- `invoice_no`
- `customer_id`
- `gender`
- `age`
- `category`
- `quantity`
- `price`
- `payment_method`
- `invoice_date`
- `shopping_mall`

## Running the Solution

From the `assignment1-data-aggregation/` directory (project root):

```bash
# Simple approach - use the convenience script
python run.py

# Or use the standard Python module approach
python -m src.assignment1
```

The solution will display results in the console and save a report to `output/report.txt`

## Running Tests

From the project root directory:

```bash
# Run tests
pytest assignment1-data-aggregation/tests/ -v
```
