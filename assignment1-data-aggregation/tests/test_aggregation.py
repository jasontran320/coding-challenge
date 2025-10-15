"""
Unit tests for Assignment 1: Data Aggregation

Run tests from project root:
    pytest assignment1-data-aggregation/tests/ -v
"""

import pytest
import pandas as pd

from assignment1.solution import DataLoader, DataAggregator, ReportGenerator

# Test data path
TEST_CSV_PATH = 'assignment1-data-aggregation/data/customer_shopping_data.csv'


class TestDataLoader:
    """Test CSV loading functionality"""

    def test_load_csv(self):
        """Test that CSV loads correctly"""
        loader = DataLoader(TEST_CSV_PATH)
        df = loader.load()

        # Check that we got a DataFrame
        assert isinstance(df, pd.DataFrame)
        # Check that it's not empty
        assert len(df) > 0
        print(f"[PASS] Loaded {len(df)} records")

    def test_column_names(self):
        """Test that columns match expected structure exactly"""
        loader = DataLoader(TEST_CSV_PATH)
        df = loader.load()

        expected_columns = [
            'invoice_no', 'customer_id', 'gender', 'age',
            'category', 'quantity', 'price', 'payment_method',
            'invoice_date', 'shopping_mall'
        ]

        # Check exact match (order and content)
        assert list(df.columns) == expected_columns, \
            f"Expected {expected_columns}, got {list(df.columns)}"

        print(f"[PASS] All {len(expected_columns)} columns match exactly")

    def test_data_types(self):
        """Test that data types support required operations"""
        loader = DataLoader(TEST_CSV_PATH)
        df = loader.load()

        # Columns for numeric calculations
        numeric_columns = ['quantity', 'price', 'age']
        for col in numeric_columns:
            assert pd.api.types.is_numeric_dtype(df[col]), \
                f"{col} must be numeric for calculations, got {df[col].dtype}"

        # Columns for grouping/aggregation (should be strings)
        categorical_columns = ['gender', 'payment_method', 'category', 'shopping_mall']
        for col in categorical_columns:
            assert pd.api.types.is_string_dtype(df[col]), \
                f"{col} must be string type for grouping, got {df[col].dtype}"

        # ID columns (should be strings)
        id_columns = ['invoice_no', 'customer_id']
        for col in id_columns:
            assert pd.api.types.is_string_dtype(df[col]), \
                f"{col} must be string type, got {df[col].dtype}"

        print(f"[PASS] All column types validated for their use cases")


class TestDataAggregator:
    """Test aggregation operations"""

    def test_count_by_gender(self):
        """Test gender population counting"""
        # TODO: Implement test with sample data
        pass

    def test_total_sales_by_gender(self):
        """Test sales aggregation by gender"""
        # TODO: Implement test with sample data
        pass

    def test_most_used_payment_method(self):
        """Test payment method frequency analysis"""
        # TODO: Implement test with sample data
        pass

    def test_day_with_most_sales(self):
        """Test daily sales aggregation"""
        # TODO: Implement test with sample data
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
