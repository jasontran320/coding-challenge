"""
Unit tests for Assignment 1: Data Aggregation

Run tests from project root:
    pytest assignment1-data-aggregation/tests/ -v
"""

import pytest

# TODO: Import solution classes when implemented
# from assignment1.solution import DataLoader, DataAggregator, ReportGenerator
# import pandas as pd  # Will be needed for test fixtures


class TestDataLoader:
    """Test CSV loading functionality"""

    def test_load_csv(self):
        """Test that CSV loads correctly"""
        # TODO: Implement test
        pass

    def test_column_names(self):
        """Test that all expected columns are present"""
        # TODO: Implement test
        pass

    def test_data_types(self):
        """Test that data types are correct"""
        # TODO: Implement test
        pass


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
