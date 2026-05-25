# Lab 4, Task 5
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Mixin module providing statistical analysis methods for NumPy arrays.
Implements median calculation in two ways: standard function and formula programming.
"""
import numpy as np
from typing import Union, List


class StatsMixin:
    """Mixin class for statistical operations on 1D/2D NumPy arrays."""

    @staticmethod
    def mean_standard(values: Union[np.ndarray, List]) -> float:
        """Calculate arithmetic mean using NumPy standard function."""
        arr = np.asarray(values).flatten()
        return float(np.mean(arr))

    @staticmethod
    def mean_formula(values: Union[np.ndarray, List]) -> float:
        """Calculate arithmetic mean using explicit formula: sum/n."""
        arr = np.asarray(values).flatten()
        return float(np.sum(arr) / len(arr)) if len(arr) > 0 else 0.0

    @staticmethod
    def median_standard(values: Union[np.ndarray, List]) -> float:
        """Calculate median using NumPy standard function."""
        arr = np.asarray(values).flatten()
        return float(np.median(arr))

    @staticmethod
    def median_formula(values: Union[np.ndarray, List]) -> float:
        """
        Calculate median using explicit formula implementation.
        """
        arr = np.asarray(values).flatten()
        if len(arr) == 0:
            return 0.0
        sorted_arr = np.sort(arr)
        n = len(sorted_arr)
        if n % 2 == 1:
            return float(sorted_arr[n // 2])
        else:
            return float((sorted_arr[n // 2 - 1] + sorted_arr[n // 2]) / 2)

    @staticmethod
    def variance_standard(values: Union[np.ndarray, List], sample: bool = False) -> float:
        """Calculate variance using NumPy standard function."""
        arr = np.asarray(values).flatten()
        ddof = 1 if sample else 0
        return float(np.var(arr, ddof=ddof))

    @staticmethod
    def variance_formula(values: Union[np.ndarray, List], sample: bool = False) -> float:
        """Calculate variance using explicit formula: Σ(x - mean)² / (n - ddof)."""
        arr = np.asarray(values).flatten()
        if len(arr) == 0:
            return 0.0
        mean_val = StatsMixin.mean_formula(arr)
        ddof = 1 if sample else 0
        return float(np.sum((arr - mean_val) ** 2) / (len(arr) - ddof))

    @staticmethod
    def std_standard(values: Union[np.ndarray, List], sample: bool = False) -> float:
        """Calculate standard deviation using NumPy standard function."""
        return float(np.sqrt(StatsMixin.variance_standard(values, sample)))

    @staticmethod
    def std_formula(values: Union[np.ndarray, List], sample: bool = False) -> float:
        """Calculate standard deviation using explicit formula: sqrt(variance)."""
        return float(np.sqrt(StatsMixin.variance_formula(values, sample)))

    @staticmethod
    def corrcoef_standard(x: Union[np.ndarray, List], y: Union[np.ndarray, List]) -> float:
        """Calculate Pearson correlation coefficient using NumPy."""
        return float(np.corrcoef(np.asarray(x).flatten(), np.asarray(y).flatten())[0, 1])