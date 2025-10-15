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


class DataLoader:
    """Handles loading CSV data into pandas DataFrame"""

    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)

    def load(self) -> pd.DataFrame:
        """
        Load customer shopping data from CSV

        Returns:
            pd.DataFrame with columns: invoice_no, customer_id, gender, age,
            category, quantity, price, payment_method, invoice_date, shopping_mall
        """
        # TODO: Implement CSV loading with proper date parsing
        pass


class DataAggregator:
    """Performs aggregation and grouping operations on the data"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def count_by_gender(self) -> pd.Series:
        """
        Task 2: Count the population grouped by gender

        Returns:
            pd.Series with gender as index and counts as values
        """
        # TODO: Implement gender grouping and counting
        pass

    def total_sales_by_gender(self) -> pd.Series:
        """
        Task 3: Find total sales grouped by gender

        Returns:
            pd.Series with gender as index and total sales as values
        """
        # TODO: Implement sales aggregation by gender
        pass

    def most_used_payment_method(self) -> str:
        """
        Task 4: Find most used payment method

        Returns:
            String name of the most frequently used payment method
        """
        # TODO: Implement payment method frequency analysis
        pass

    def day_with_most_sales(self) -> str:
        """
        Task 5: Find day with the most sales

        Returns:
            Date string of the day with highest total sales
        """
        # TODO: Implement daily sales aggregation
        pass


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
