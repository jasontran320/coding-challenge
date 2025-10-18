"""
Data validation utilities for customer shopping data

This module provides reusable validation functions for DataFrame schema and types.

All validation functions raise ValueError for production use. Tests can catch
and convert to AssertionError if needed, or use them directly.
"""

import pandas as pd
from typing import List, Optional, Callable, Any
from datetime import datetime

# Expected schema for customer shopping data CSV
EXPECTED_COLUMNS = {
    'invoice_no', 'customer_id', 'gender', 'age', 'category',
    'quantity', 'price', 'payment_method', 'invoice_date', 'shopping_mall'
}

# Column type expectations
NUMERIC_COLUMNS = ['quantity', 'price', 'age']
STRING_COLUMNS = ['gender', 'payment_method', 'category', 'shopping_mall',
                  'invoice_no', 'customer_id']


def validate_numeric_columns(df: pd.DataFrame, columns: List[str]) -> None:
    """Validate that specified columns are numeric types

    Args:
        df: DataFrame to validate
        columns: List of column names that should be numeric

    Raises:
        ValueError: If any column is not numeric

    Example:
        >>> validate_numeric_columns(df, ['quantity', 'price', 'age'])
    """
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(
                f"Column '{col}' must be numeric for calculations, got {df[col].dtype}"
            )


def validate_string_columns(df: pd.DataFrame, columns: List[str]) -> None:
    """Validate that specified columns are string types

    Args:
        df: DataFrame to validate
        columns: List of column names that should be strings

    Raises:
        ValueError: If any column is not string type

    Example:
        >>> validate_string_columns(df, ['gender', 'payment_method'])
    """
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")
        if not pd.api.types.is_string_dtype(df[col]):
            raise ValueError(
                f"Column '{col}' must be string type, got {df[col].dtype}"
            )


def validate_dataframe_schema(df: pd.DataFrame) -> None:
    """Validate that DataFrame has all required columns for customer shopping data

    This function checks that all required columns are present. Column order is
    not validated as the code accesses columns by name, not position.

    Args:
        df: DataFrame to validate

    Raises:
        ValueError: If DataFrame is missing required columns

    Example:
        >>> df = pd.read_csv('data.csv')
        >>> validate_dataframe_schema(df)
    """
    actual_columns = set(df.columns)

    # Check for missing columns
    missing_columns = EXPECTED_COLUMNS - actual_columns
    if missing_columns:
        raise ValueError(
            f"DataFrame missing required columns: {sorted(missing_columns)}"
        )


def validate_dataframe_types(df: pd.DataFrame) -> None:
    """Validate that DataFrame columns have appropriate data types

    Validates that numeric columns (quantity, price, age) are numeric types
    and categorical columns (gender, payment_method, etc.) are string types.

    Args:
        df: DataFrame to validate

    Raises:
        ValueError: If any column has incorrect data type

    Example:
        >>> df = pd.read_csv('data.csv')
        >>> validate_dataframe_types(df)
    """
    # Use shared validation functions
    validate_numeric_columns(df, NUMERIC_COLUMNS)
    validate_string_columns(df, STRING_COLUMNS)


def _filter_sortable_indices(indices: pd.Index, sort_key: Optional[Callable[[str], Any]] = None) -> List[str]:
    """Filter indices to only valid values, optionally testing against sort_key

    Args:
        indices: Index values to filter
        sort_key: Optional function to test each index value against.
                  If None, only filters empty/whitespace values.

    Returns:
        List[str]: Valid indices (non-empty/whitespace, and if sort_key provided,
                   those that successfully pass through sort_key without raising exceptions)
    """
    valid = []
    for idx in indices:
        # Always filter empty/whitespace-only values
        if str(idx).strip() == '':
            continue

        # If sort_key provided, test if index can be processed
        if sort_key is not None:
            try:
                sort_key(idx)
                valid.append(idx)
            except (ValueError, TypeError, AttributeError):
                # Skip indices that can't be processed by sort_key
                continue
        else:
            # No sort_key, just keep non-empty values
            valid.append(idx)

    return valid


def get_max_with_valid_index(
    series: pd.Series,
    sort_key: Optional[Callable[[str], Any]] = None
) -> str:
    """Find the index with maximum value, filtering out invalid string indices

    Helper function for aggregation methods that return the most common/highest
    categorical value. Filters out empty/whitespace-only index values and handles
    ties deterministically.

    Args:
        series: Series with string index and numeric values (e.g., counts or sums)
        sort_key: Optional function to transform index values for sorting ties.
                  Used when ties need custom ordering (e.g., chronological for dates).
                  If None, ties are broken alphabetically (default).
                  Indices that raise exceptions when passed to sort_key are filtered out.

    Returns:
        str: Index value with maximum, or empty string if no valid indices exist.
            When tied, returns first by sort order (alphabetical or by sort_key).

    Examples:
        >>> # Alphabetical tie-breaking (default for categories like payment methods)
        >>> counts = pd.Series({'Cash': 100, '': 50, 'Credit Card': 100})
        >>> get_max_with_valid_index(counts)
        'Cash'  # Filters out '', 'Cash' comes before 'Credit Card' alphabetically

        >>> # Chronological tie-breaking for dates - gracefully handles invalid dates
        >>> from datetime import datetime
        >>> sales = pd.Series({'5/8/2022': 1000, '3/8/2022': 1000, '2023-01-02': 1000})
        >>> get_max_with_valid_index(sales, sort_key=lambda x: datetime.strptime(x, '%m/%d/%Y'))
        '3/8/2022'  # Invalid format '2023-01-02' filtered out, earliest valid date returned
    """
    # Filter to only valid indices (handles both empty/whitespace AND invalid sort_key values)
    valid_indices = _filter_sortable_indices(series.index, sort_key)

    if len(valid_indices) == 0:
        return ""

    # Work with filtered series
    valid_series = series[valid_indices]

    # Find max value from valid indices only
    max_value = valid_series.max()
    ties = valid_series[valid_series == max_value]

    # Return early if no ties to judge
    if len(ties) == 1:
        return ties.index[0]

    # Multiple ties - break tie by sorting
    if sort_key is not None:
        # All indices already validated by _filter_sortable_indices
        sorted_indices = sorted(ties.index, key=sort_key)
        return sorted_indices[0]
    else:
        # Default: alphabetical tie-breaking
        return ties.sort_index().index[0]
