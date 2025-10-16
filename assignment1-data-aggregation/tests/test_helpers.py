"""
Shared test utilities for Assignment 1

Test-specific validation helpers that are not part of production validation.

Note: DataFrame schema and type validation is handled by assignment1.validation
module, which is used directly by DataLoader. Tests verify validation by checking
that DataLoader.load() doesn't raise exceptions.
"""

import pandas as pd


def validate_series_structure(series: pd.Series, expected_index_name: str) -> None:
    """Validate common pd.Series properties

    Test-specific helper for validating aggregation method return values.

    Args:
        series: The Series to validate
        expected_index_name: Expected name of the Series index

    Raises:
        AssertionError: If validation fails

    Example:
        >>> result = aggregator.count_by_gender()
        >>> validate_series_structure(result, 'gender')
    """
    assert isinstance(series, pd.Series), \
        f"Expected pd.Series, got {type(series)}"
    assert series.index.name == expected_index_name, \
        f"Expected index name '{expected_index_name}', got '{series.index.name}'"
