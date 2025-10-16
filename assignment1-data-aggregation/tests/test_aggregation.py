"""
Unit tests for Assignment 1: Data Aggregation

Run tests from project root:
    pytest assignment1-data-aggregation/tests/ -v
"""

import pytest
import pandas as pd

from assignment1.solution import DataLoader, DataAggregator, ReportGenerator
from .fixtures import (
    sample_data, empty_dataframe, tie_payment_methods,
    data_with_bad_numeric, data_with_bad_categorical
)
from .test_helpers import validate_series_structure

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
        """Test that DataLoader validates column schema"""
        loader = DataLoader(TEST_CSV_PATH)
        df = loader.load()

        # If load() succeeded, schema validation passed (no ValueError raised)
        # DataLoader already validates column names via validate_dataframe_schema()
        assert isinstance(df, pd.DataFrame)
        assert len(df.columns) == 10

        print(f"[PASS] Schema validation passed via DataLoader (10 columns)")

    def test_data_types(self):
        """Test that DataLoader validates data types"""
        loader = DataLoader(TEST_CSV_PATH)
        df = loader.load()

        # If load() succeeded, type validation passed (no ValueError raised)
        # DataLoader already validates types via validate_dataframe_types()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

        print(f"[PASS] Data type validation passed via DataLoader")


class TestDataAggregator:
    """Test aggregation operations with various data scenarios"""

    # ===== Happy Path Tests =====

    def test_count_by_gender(self, sample_data):
        """Test gender counting with standard data"""
        aggregator = DataAggregator(sample_data)
        result = aggregator.count_by_gender()

        validate_series_structure(result, 'gender')
        # Male has 3 records, Female has 2
        assert result['Male'] == 3
        assert result['Female'] == 2

        print(f"[PASS] Gender counts: Male={result['Male']}, Female={result['Female']}")

    def test_total_sales_by_gender(self, sample_data):
        """Test sales aggregation with standard data"""
        aggregator = DataAggregator(sample_data)
        result = aggregator.total_sales_by_gender()

        validate_series_structure(result, 'gender')
        # Male: (2*100) + (3*150) + (1*50) = 700
        # Female: (1*200) + (2*100) = 400
        assert result['Male'] == 700.0
        assert result['Female'] == 400.0

        print(f"[PASS] Total sales: Male=${result['Male']:.2f}, Female=${result['Female']:.2f}")

    def test_most_used_payment_method(self, sample_data):
        """Test payment method frequency with standard data"""
        aggregator = DataAggregator(sample_data)
        result = aggregator.most_used_payment_method()

        assert isinstance(result, str)
        assert result == 'Cash'  # Cash appears 3 times, Card 2 times

        print(f"[PASS] Most used payment method: {result}")

    def test_day_with_most_sales(self, sample_data):
        """Test daily sales aggregation with standard data"""
        aggregator = DataAggregator(sample_data)
        result = aggregator.day_with_most_sales()

        assert isinstance(result, str)
        # 2/1/2023 has $650 in sales (highest)
        assert result == '2/1/2023'

        print(f"[PASS] Day with most sales: {result}")

    # ===== Edge Case Tests =====

    def test_aggregations_with_empty_dataframe(self, empty_dataframe):
        """Test aggregations handle empty DataFrame gracefully"""
        aggregator = DataAggregator(empty_dataframe)

        # Count by gender - should return empty Series
        gender_counts = aggregator.count_by_gender()
        assert isinstance(gender_counts, pd.Series)
        assert len(gender_counts) == 0

        # Total sales by gender - should return empty Series
        sales_by_gender = aggregator.total_sales_by_gender()
        assert isinstance(sales_by_gender, pd.Series)
        assert len(sales_by_gender) == 0

        # Most used payment method - should return empty string
        payment_method = aggregator.most_used_payment_method()
        assert isinstance(payment_method, str)
        assert payment_method == ""

        # Day with most sales - should return empty string
        best_day = aggregator.day_with_most_sales()
        assert isinstance(best_day, str)
        assert best_day == ""

        print(f"[PASS] Empty DataFrame handled gracefully by all methods")

    def test_total_sales_with_bad_numeric_data(self, data_with_bad_numeric):
        """Test sales calculation with NaN and zero values in numeric columns"""
        aggregator = DataAggregator(data_with_bad_numeric)
        result = aggregator.total_sales_by_gender()

        validate_series_structure(result, 'gender')
        # Male: (0*100) + (3*150) = 0 + 450 = 450
        # Female: (NaN*200) + (2*0) = 0 + 0 = 0 (pandas sum() treats NaN as 0)
        assert result['Male'] == 450.0
        assert result['Female'] == 0.0

        print(f"[PASS] NaN and zero values handled correctly")

    def test_payment_method_tie(self, tie_payment_methods):
        """Test tie-breaking with filtering for both payment methods and dates

        This test validates that get_max_with_valid_index properly:
        1. Filters out empty/whitespace values
        2. Breaks ties alphabetically for payment methods
        3. Breaks ties chronologically for dates
        4. Filters out invalid date formats
        """
        aggregator = DataAggregator(tie_payment_methods)

        # Test most_used_payment_method with alphabetical tie-breaking
        payment_result = aggregator.most_used_payment_method()
        assert isinstance(payment_result, str)
        # Three methods tied at 3 occurrences: 'Cash', 'Credit Card', 'Debit Card'
        # Empty/whitespace filtered out, alphabetical order: 'Cash' comes first
        assert payment_result == 'Cash'
        print(f"[PASS] Payment method tie (alphabetical): {payment_result}")

        # Test day_with_most_sales with chronological tie-breaking
        date_result = aggregator.day_with_most_sales()
        assert isinstance(date_result, str)
        # Three dates tied at $300: '5/1/2023', '10/1/2023', '15/1/2023'
        # Invalid format '2023-01-20' and empty/whitespace filtered out
        # Chronological order: '5/1/2023' is earliest
        assert date_result == '5/1/2023'
        print(f"[PASS] Date tie (chronological): {date_result}")

        print(f"[PASS] Tie-breaking and filtering validated for both methods")

    def test_aggregations_with_bad_categorical_data(self, data_with_bad_categorical):
        """Test how None, NaN, and empty strings in categorical columns are handled"""
        aggregator = DataAggregator(data_with_bad_categorical)

        # Test count_by_gender with missing values
        gender_counts = aggregator.count_by_gender()
        validate_series_structure(gender_counts, 'gender')

        # Should have: Male=2, Female=1, ''=1 (NaN/None dropped)
        assert gender_counts['Male'] == 2
        assert gender_counts['Female'] == 1
        assert gender_counts[''] == 1  # Empty string is treated as valid category
        assert len(gender_counts) == 3  # Only 3 groups (NaN/None excluded)

        # Test total_sales_by_gender with bad categorical
        sales_by_gender = aggregator.total_sales_by_gender()
        validate_series_structure(sales_by_gender, 'gender')
        # Male: (1*100) + (5*50) = 350, Female: (3*150) = 450, '': (4*100) = 400
        assert sales_by_gender['Male'] == 350.0
        assert sales_by_gender['Female'] == 450.0
        assert sales_by_gender[''] == 400.0

        # Test most_used_payment_method with missing values
        # payment_method has: Cash=2, Card=2, ''=1, None=1
        # pandas drops None, so: Cash=2, Card=2, ''=1
        # With tie between Cash and Card, 'Card' comes first alphabetically
        payment_method = aggregator.most_used_payment_method()
        assert isinstance(payment_method, str)
        assert payment_method == 'Card'

        # Test day_with_most_sales with bad dates
        # Dates: '1/1/2023' (1*100=100), '' (2*200=400), '2/1/2023' (3*150=450),
        #        None (4*100=400), '3/1/2023' (5*50=250), '4/1/2023' (1*100=100)
        # Highest is '2/1/2023' with 450
        best_day = aggregator.day_with_most_sales()
        assert isinstance(best_day, str)
        assert best_day == '2/1/2023'

        print(f"[PASS] Bad categorical data handled correctly")


class TestReportGenerator:
    """Test report generation functionality"""

    def test_generate_report_with_data(self, sample_data):
        """Test report generation with standard data"""
        aggregator = DataAggregator(sample_data)
        results = {
            'gender_counts': aggregator.count_by_gender(),
            'sales_by_gender': aggregator.total_sales_by_gender(),
            'most_used_payment': aggregator.most_used_payment_method(),
            'best_sales_day': aggregator.day_with_most_sales()
        }

        report = ReportGenerator.generate_report(results)

        # Check that report is a string
        assert isinstance(report, str)
        # Check that report contains expected sections
        assert "CUSTOMER SHOPPING DATA ANALYSIS" in report
        assert "Task 2" in report
        assert "Task 3" in report
        assert "Task 4" in report
        assert "Task 5" in report
        # Check that report contains actual data
        assert "Male" in report
        assert "Female" in report
        assert "Cash" in report

        print(f"[PASS] Report generated successfully")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
