"""
Validation utilities for the Producer-Consumer Problem

This module provides shared validation functions used across multiple
components (Container, BoundedQueue, Producer, Consumer) to ensure
consistent type checking and data validation.
"""

from typing import Any


def is_valid_number(value: Any) -> bool:
    """Check if value is a valid Number (int or float)

    Args:
        value: Value to check

    Returns:
        True if value is int or float, False otherwise

    Note:
        Explicitly excludes bool type, even though bool is a subclass of int in Python.
        This prevents accidental acceptance of True/False as numeric values.

    Examples:
        >>> is_valid_number(42)
        True
        >>> is_valid_number(3.14)
        True
        >>> is_valid_number(True)
        False
        >>> is_valid_number("123")
        False
    """
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_positive_int(value: Any) -> bool:
    """Check if value is a positive integer

    Args:
        value: Value to check

    Returns:
        True if value is a positive integer, False otherwise

    Note:
        Returns False for non-integers, zero, negative numbers, and booleans.

    Examples:
        >>> is_positive_int(10)
        True
        >>> is_positive_int(0)
        False
        >>> is_positive_int(-5)
        False
        >>> is_positive_int("10")
        False
        >>> is_positive_int(True)
        False
    """
    return isinstance(value, int) and not isinstance(value, bool) and value > 0
