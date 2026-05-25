# Lab 4, Task 6
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for statistical analysis of Sberbank Housing dataset.
Implements: price per square meter analysis, district comparison.
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from data_processor import SberbankDataProcessor


class StatisticalAnalyzer:
    """Class for statistical analysis of housing data."""

    def __init__(self, processor: SberbankDataProcessor):
        """Initialize with data processor."""
        self._processor = processor

    @property
    def data(self) -> pd.DataFrame:
        """Get data from processor."""
        return self._processor.data

    def calculate_price_per_sqm(self) -> pd.Series:
        """Calculate price per square meter."""
        if self.data is None:
            raise ValueError("Data not initialized.")

        return self.data['price'] / self.data['full_sq']

    def get_district_statistics(self) -> pd.DataFrame:
        """Calculate statistics for each district (sub_area)."""
        if self.data is None:
            raise ValueError("Data not initialized.")

        # Calculate price per square meter
        price_per_sqm = self.calculate_price_per_sqm()

        # Group by district and calculate mean price per sqm
        district_stats = self.data.groupby('sub_area').agg({
            'price': ['mean', 'median', 'std', 'count'],
            'full_sq': 'mean'
        }).round(2)

        # Add price per sqm column
        district_stats[('price_per_sqm', 'mean')] = price_per_sqm.groupby(
            self.data['sub_area']
        ).mean().round(2)

        return district_stats

    def analyze_expensive_vs_cheap_districts(self) -> Dict:
        """
        ЗАДАНИЕ Б: Determine how many times the average price per square meter
        in the most expensive districts is greater than in the cheapest districts.
        """
        if self.data is None:
            raise ValueError("Data not initialized.")

        # Calculate price per square meter
        price_per_sqm = self.calculate_price_per_sqm()

        # Group by district and calculate average price per sqm
        district_avg_price = price_per_sqm.groupby(self.data['sub_area']).mean()

        # Find most expensive and cheapest districts
        most_expensive_district = district_avg_price.idxmax()
        cheapest_district = district_avg_price.idxmin()

        most_expensive_price = district_avg_price.max()
        cheapest_price = district_avg_price.min()

        # Calculate ratio
        ratio = most_expensive_price / cheapest_price

        return {
            'most_expensive_district': most_expensive_district,
            'most_expensive_price_per_sqm': round(most_expensive_price, 2),
            'cheapest_district': cheapest_district,
            'cheapest_price_per_sqm': round(cheapest_price, 2),
            'ratio': round(ratio, 2),
            'all_districts_avg': district_avg_price.round(2).to_dict()
        }

    def get_detailed_statistics(self) -> Dict:
        """Get comprehensive statistical analysis."""
        if self.data is None:
            raise ValueError("Data not initialized.")

        price_per_sqm = self.calculate_price_per_sqm()

        return {
            'general': {
                'total_transactions': len(self.data),
                'total_districts': self.data['sub_area'].nunique(),
                'avg_price': round(self.data['price'].mean(), 2),
                'median_price': round(self.data['price'].median(), 2),
                'avg_area': round(self.data['full_sq'].mean(), 2),
                'avg_price_per_sqm': round(price_per_sqm.mean(), 2),
                'median_price_per_sqm': round(price_per_sqm.median(), 2)
            },
            'price_per_sqm': {
                'mean': round(price_per_sqm.mean(), 2),
                'median': round(price_per_sqm.median(), 2),
                'std': round(price_per_sqm.std(), 2),
                'min': round(price_per_sqm.min(), 2),
                'max': round(price_per_sqm.max(), 2)
            },
            'district_comparison': self.analyze_expensive_vs_cheap_districts()
        }

    def filter_by_district(self, district_name: str) -> pd.DataFrame:
        """Filter data by specific district."""
        if self.data is None:
            raise ValueError("Data not initialized.")

        filtered = self.data[self.data['sub_area'] == district_name].copy()
        return filtered

    def get_top_districts(self, n: int = 5, by: str = 'price_per_sqm') -> pd.DataFrame:
        """Get top N districts by specified metric."""
        if self.data is None:
            raise ValueError("Data not initialized.")

        if by == 'price_per_sqm':
            price_per_sqm = self.calculate_price_per_sqm()
            district_avg = price_per_sqm.groupby(self.data['sub_area']).mean()
        elif by == 'price':
            district_avg = self.data.groupby('sub_area')['price'].mean()
        else:
            raise ValueError(f"Unknown metric: {by}")

        return district_avg.nlargest(n).round(2)