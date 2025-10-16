"""
Assignment 1: Data Aggregation and Grouping using Pandas

Architecture:
- DataLoader: Reads CSV into pandas DataFrame
- DataAggregator: Performs grouping and aggregation operations
- ReportGenerator: Formats and displays results

Design Pattern: Strategy pattern for different aggregation strategies
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from .validation import validate_dataframe_schema, validate_dataframe_types, get_max_with_valid_index

# Expected date format in customer shopping data CSV
# Format: Day/Month/Year (e.g., '15/1/2023', '31/12/2022')
DEFAULT_DATE_FORMAT = '%d/%m/%Y'


class DataLoader:
    """Handles loading CSV data into pandas DataFrame

    Args:
        csv_path (str): Path to the CSV file containing customer shopping data

    Example:
        >>> loader = DataLoader('data/customer_shopping_data.csv')
        >>> df = loader.load()
        >>> print(df.shape)
        (99457, 10)
    """

    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)

    def load(self) -> pd.DataFrame:
        """Load customer shopping data from CSV file

        Validates file existence, schema, and data types before returning.

        Returns:
            pd.DataFrame: DataFrame with columns:
                - invoice_no: Unique invoice identifier
                - customer_id: Unique customer identifier
                - gender: Customer gender (Male/Female)
                - age: Customer age
                - category: Product category
                - quantity: Number of items purchased
                - price: Price per item
                - payment_method: Payment method used
                - invoice_date: Date of purchase
                - shopping_mall: Shopping mall location

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV has incorrect schema or data types

        Example:
            >>> loader = DataLoader('data/customer_shopping_data.csv')
            >>> df = loader.load()
            >>> df.columns.tolist()
            ['invoice_no', 'customer_id', 'gender', 'age', 'category',
             'quantity', 'price', 'payment_method', 'invoice_date', 'shopping_mall']
        """
        # Validate file exists
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        # Load CSV data
        df = pd.read_csv(self.csv_path)

        # Validate schema and data types using validation logic
        validate_dataframe_schema(df)
        validate_dataframe_types(df)

        return df


class DataAggregator:
    """Performs aggregation and grouping operations on customer shopping data

    This class provides methods to analyze customer shopping patterns through
    various grouping and aggregation operations using pandas.

    Args:
        df (pd.DataFrame): DataFrame containing customer shopping records.
            Should be loaded via DataLoader.load() to ensure proper schema
            and data types.

    Example:
        >>> loader = DataLoader('data/customer_shopping_data.csv')
        >>> df = loader.load()
        >>> aggregator = DataAggregator(df)
        >>> gender_counts = aggregator.count_by_gender()
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def count_by_gender(self) -> pd.Series:
        """Count the number of customers grouped by gender

        Groups the dataset by gender and returns the count of records
        for each gender category.

        Returns:
            pd.Series: Series with gender as index and count as values.
                Index name is 'gender', values are integer counts.

        Example:
            >>> result = aggregator.count_by_gender()
            >>> result
            gender
            Female    5234
            Male      4766
            dtype: int64
        """
        return self.df.groupby("gender").size()
        

    def total_sales_by_gender(self) -> pd.Series:
        """Calculate total sales amount grouped by gender

        Computes total sales (quantity × price) for each transaction,
        then aggregates by gender to find total revenue per gender.

        Returns:
            pd.Series: Series with gender as index and total sales as values.
                Index name is 'gender', values are float (sales amounts).

        Example:
            >>> result = aggregator.total_sales_by_gender()
            >>> result
            gender
            Female    2456789.50
            Male      1823456.75
            dtype: float64
        """
        total_sales = self.df['quantity'] * self.df['price']
        return total_sales.groupby(self.df['gender']).sum()

    def most_used_payment_method(self) -> str:
        """Find the most frequently used payment method

        Groups transactions by payment method and identifies which
        payment method appears most often in the dataset.

        Returns:
            str: Name of the most frequently used payment method
                (e.g., 'Cash', 'Credit Card', 'Debit Card').
                Returns empty string if DataFrame is empty or no valid
                payment methods found.

        Example:
            >>> result = aggregator.most_used_payment_method()
            >>> result
            'Cash'

        Note:
            - Filters out empty/whitespace-only payment method values
              before determining the most used method.
            - In case of a tie, returns the first payment method
              encountered in alphabetical order.
        """
        # Group by payment method and get counts
        payment_counts = self.df.groupby("payment_method").size()
        return get_max_with_valid_index(payment_counts)

    def day_with_most_sales(self) -> str:
        """Find the date with the highest total sales revenue

        Calculates total sales (quantity × price) for each transaction,
        groups by date, and identifies the day with maximum total revenue.

        Returns:
            str: Date string of the day with highest total sales
                (format matches the invoice_date column format).
                Returns empty string if DataFrame is empty or no valid
                dates found.

        Example:
            >>> result = aggregator.day_with_most_sales()
            >>> result
            '3/8/2022'

        Note:
            - Filters out empty/whitespace-only date values before
              determining the day with most sales.
            - In case of a tie, returns the earliest date chronologically.
        """
        total_sales = self.df['quantity'] * self.df['price']
        daily_sales = total_sales.groupby(self.df['invoice_date']).sum()

        # Use chronological sort for dates (earliest first when tied)
        return get_max_with_valid_index(
            daily_sales,
            sort_key=lambda x: datetime.strptime(x, DEFAULT_DATE_FORMAT)
        )


class ReportGenerator:
    """Formats and displays aggregation results"""

    @staticmethod
    def generate_report(results: Dict[str, Any]) -> str:
        """
        Generate formatted report from aggregation results

        Args:
            results: Dictionary containing all aggregation results

        Returns:
            Formatted string report
        """
        # TODO: Implement report formatting
        pass


def main():
    """Main entry point for the data aggregation solution"""

    # TODO: Wire up all components
    # 1. Load data
    # 2. Perform all aggregations
    # 3. Generate report
    # 4. Display results

    pass


if __name__ == "__main__":
    main()
