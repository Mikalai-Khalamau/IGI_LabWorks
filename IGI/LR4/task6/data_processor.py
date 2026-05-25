# Lab 4, Task 6
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for Pandas DataFrame operations with Sberbank Housing dataset.
Implements: Series creation, DataFrame manipulation, data extraction.
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional


class SberbankDataProcessor:
    """Class for processing Sberbank Housing dataset."""

    def __init__(self, data: Optional[pd.DataFrame] = None):
        """Initialize with optional DataFrame."""
        self._data = data
        self._original_data = None

    @property
    def data(self) -> Optional[pd.DataFrame]:
        """Getter for data property."""
        return self._data

    @data.setter
    def data(self, value: pd.DataFrame):
        """Setter for data with validation."""
        if not isinstance(value, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame")
        self._data = value

    def load_sample_data(self, n_samples: int = 100) -> pd.DataFrame:
        """
        Generate sample Sberbank Housing data for demonstration.
        In real scenario, load from CSV file.
        """
        np.random.seed(42)

        districts = ['Yuzhnoe Butovo', 'Severnoe Butovo', 'Yasenevo',
                     'Teply Stan', 'Obruchevsky', 'Cheryomushki']

        self._data = pd.DataFrame({
            'price': np.random.randint(5000000, 20000000, n_samples),
            'full_sq': np.random.randint(20, 120, n_samples),
            'floor': np.random.randint(1, 25, n_samples),
            'sub_area': np.random.choice(districts, n_samples),
            'life_sq': np.random.randint(10, 80, n_samples),
            'kitchen_sq': np.random.randint(5, 20, n_samples)
        })

        self._original_data = self._data.copy()
        return self._data

    def load_from_csv(self, filepath: str) -> pd.DataFrame:
        """Load data from CSV file."""
        try:
            self._data = pd.read_csv(filepath)
            self._original_data = self._data.copy()
            return self._data
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            print("Generating sample data instead...")
            return self.load_sample_data()
        except Exception as e:
            raise ValueError(f"Error loading CSV: {e}")

    def create_random_transactions_df(self, n: int = 5) -> pd.DataFrame:
        """
        ЗАДАНИЕ А: Create DataFrame from n random transactions.
        Keep columns: price, full_sq, floor.
        Reset index and save old index as separate column.
        """
        if self._data is None:
            raise ValueError("Data not initialized. Call load_sample_data() or load_from_csv() first.")

        if n > len(self._data):
            n = len(self._data)
            print(f"Requested {n} samples, but only {len(self._data)} available. Using all data.")

        # Select n random rows
        sample_df = self._data.sample(n=n, random_state=42)

        # Keep only required columns
        result_df = sample_df[['price', 'full_sq', 'floor']].copy()

        # Reset index and save old index as separate column
        result_df = result_df.reset_index(drop=False)
        result_df = result_df.rename(columns={'index': 'original_index'})

        return result_df

    def get_dataframe_info(self) -> Dict:
        """Get comprehensive information about DataFrame."""
        if self._data is None:
            raise ValueError("Data not initialized.")

        return {
            'shape': self._data.shape,
            'columns': list(self._data.columns),
            'dtypes': self._data.dtypes.to_dict(),
            'memory_usage': self._data.memory_usage(deep=True).sum(),
            'null_counts': self._data.isnull().sum().to_dict()
        }

    def display_sample(self, n: int = 5) -> None:
        """Display first n rows of DataFrame."""
        if self._data is not None:
            from IPython.display import display
            display(self._data.head(n))
        else:
            print("No data loaded.")

    def get_column_statistics(self, column_name: str) -> Dict:
        """Get statistical information for a specific column."""
        if self._data is None:
            raise ValueError("Data not initialized.")

        if column_name not in self._data.columns:
            raise ValueError(f"Column '{column_name}' not found in DataFrame.")

        col = self._data[column_name]
        return {
            'mean': col.mean() if pd.api.types.is_numeric_dtype(col) else None,
            'median': col.median() if pd.api.types.is_numeric_dtype(col) else None,
            'std': col.std() if pd.api.types.is_numeric_dtype(col) else None,
            'min': col.min(),
            'max': col.max(),
            'unique_count': col.nunique(),
            'null_count': col.isnull().sum()
        }