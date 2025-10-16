"""
Test fixtures and sample data for Assignment 1 tests

This module centralizes all test data to keep test files focused on logic.
Each fixture is documented with its intended use case.
"""

import pandas as pd
import pytest


@pytest.fixture
def sample_data():
    """Standard fixture with known results for all aggregation methods

    Use case: Path testing with predictable outcomes

    Test Data Design:
        Total records: 5 transactions

        Gender distribution:
            - Male: 3 records (indices 0, 2, 4)
            - Female: 2 records (indices 1, 3)

        Payment methods:
            - Cash: 3 occurrences (indices 0, 2, 3)
            - Card: 2 occurrences (indices 1, 4)

        Daily sales breakdown:
            - 1/1/2023: 2 transactions, total sales = $400
            - 2/1/2023: 2 transactions, total sales = $650 (highest)
            - 3/1/2023: 1 transaction, total sales = $50

        Sales by gender:
            - Male: $700 total (2*100 + 3*150 + 1*50)
            - Female: $400 total (1*200 + 2*100)
    """
    return pd.DataFrame({
        'gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'quantity': [2, 1, 3, 2, 1],
        'price': [100.0, 200.0, 150.0, 100.0, 50.0],
        'payment_method': ['Cash', 'Card', 'Cash', 'Cash', 'Card'],
        'invoice_date': ['1/1/2023', '1/1/2023', '2/1/2023',
                         '2/1/2023', '3/1/2023']
    })


@pytest.fixture
def empty_dataframe():
    """Edge case: Empty DataFrame with correct schema

    Use case: Test aggregations handle empty data gracefully (e.g., no results after filtering)

    Expected results:
        - All aggregations should return empty Series/handle gracefully without crashing
    """
    return pd.DataFrame({
        'gender': pd.Series([], dtype='object'),
        'quantity': pd.Series([], dtype='int64'),
        'price': pd.Series([], dtype='float64'),
        'payment_method': pd.Series([], dtype='object'),
        'invoice_date': pd.Series([], dtype='object')
    })


@pytest.fixture
def tie_payment_methods():
    """Edge case: Ties with filtering for both payment methods and dates

    Use case: Test tie-breaking behavior in both most_used_payment_method()
             and day_with_most_sales() with invalid values and ties

    Test Data Design:
        Payment method frequency (for most_used_payment_method):
            - 'Credit Card': 3 occurrences (indices 0, 2, 4)
            - 'Cash': 3 occurrences (indices 1, 3, 5)
            - 'Debit Card': 3 occurrences (indices 6, 7, 8)
            - '  ' (whitespace): 2 occurrences (indices 9, 10) - filtered out
            - '' (empty): 1 occurrence (index 11) - filtered out
            Expected: 'Cash' (alphabetically first among tied valid values)

        Daily sales (for day_with_most_sales):
            - 15/1/2023: $300 sales (3 transactions × $100)
            - 10/1/2023: $300 sales (3 transactions × $100) - tied with 15/1/2023
            - 5/1/2023: $300 sales (3 transactions × $100) - tied with above
            - '2023-01-20': $200 sales - INVALID FORMAT (filtered out)
            - '  ': $100 sales - whitespace (filtered out)
            - '': $100 sales - empty string (filtered out)
            Expected: '5/1/2023' (chronologically earliest among tied valid dates)

    Expected results:
        - most_used_payment_method: 'Cash' (alphabetical tie-breaking)
        - day_with_most_sales: '5/1/2023' (chronological tie-breaking)
    """
    return pd.DataFrame({
        'payment_method': ['Credit Card', 'Cash', 'Credit Card', 'Cash', 'Credit Card',
                          'Cash', 'Debit Card', 'Debit Card', 'Debit Card', '  ', '  ', ''],
        'quantity': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'price': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0,
                 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
        'gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female',
                  'Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
        'invoice_date': ['15/1/2023', '15/1/2023', '15/1/2023',
                        '10/1/2023', '10/1/2023', '10/1/2023',
                        '5/1/2023', '5/1/2023', '5/1/2023',
                        '2023-01-20', '  ', '']
    })


@pytest.fixture
def data_with_bad_numeric():
    """Edge case: DataFrame with NaN and zero values in numeric columns

    Use case: Test handling missing/invalid numeric data

    Expected results:
        - pandas treats NaN in multiplication as NaN, but sum() ignores NaN
        - Zero values multiply correctly (0 * price = 0)
        - Male: (0*100) + (3*150) = 0 + 450 = 450
        - Female: (NaN*200) + (2*0) = 0 + 0 = 0
    """
    return pd.DataFrame({
        'gender': ['Male', 'Female', 'Male', 'Female'],
        'quantity': [0, float('nan'), 3, 2],
        'price': [100.0, 200.0, 150.0, 0.0],
        'payment_method': ['Cash', 'Card', 'Cash', 'Card'],
        'invoice_date': ['1/1/2023', '2/1/2023', '3/1/2023', '4/1/2023']
    })


@pytest.fixture
def data_with_bad_categorical():
    """Edge case: DataFrame with None, NaN, and empty strings in categorical columns

    Use case: Test handling missing/invalid categorical data

    Expected results:
        - pandas groups None/NaN together
        - Empty string '' is treated as a valid category
        - count_by_gender: Will have groups for 'Male', 'Female', '', and NaN
        - most_used_payment_method: Empty string '' is a valid payment method
        - day_with_most_sales: Empty/NaN dates are grouped separately
    """
    return pd.DataFrame({
        'gender': ['Male', None, 'Female', '', 'Male', float('nan')],
        'quantity': [1, 2, 3, 4, 5, 1],
        'price': [100.0, 200.0, 150.0, 100.0, 50.0, 100.0],
        'payment_method': ['Cash', '', 'Card', None, 'Cash', 'Card'],
        'invoice_date': ['1/1/2023', '', '2/1/2023', None, '3/1/2023', '4/1/2023']
    })
