# Lab 4, Task 5
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for NumPy matrix operations using OOP principles.
Implements Variant 27: insert first row after row with first minimum element,
calculate median of first row using two methods.
"""
import numpy as np
from typing import Tuple, Optional, Union
from stats_mixin import StatsMixin


class BaseMatrix:
    """Abstract-like base class for matrix operations."""
    _matrix_count: int = 0  # Static attribute: total instances created

    def __init__(self, rows: int, cols: int, seed: Optional[int] = None):
        if rows <= 0 or cols <= 0:
            raise ValueError("Matrix dimensions must be positive integers.")
        self._rows = rows
        self._cols = cols
        self._seed = seed
        self._data: Optional[np.ndarray] = None
        self._last_operation: str = "initialized"  # Dynamic attribute
        BaseMatrix._matrix_count += 1

    @property
    def data(self) -> Optional[np.ndarray]:
        """Property to access matrix data (read-only copy)."""
        return self._data.copy() if self._data is not None else None

    @property
    def shape(self) -> Tuple[int, int]:
        return (self._rows, self._cols)

    @property
    def last_operation(self) -> str:
        return self._last_operation

    def generate_random(self, low: int = -100, high: int = 100) -> np.ndarray:
        """Generate random integer matrix using NumPy random generator."""
        if self._seed is not None:
            np.random.seed(self._seed)
        self._data = np.random.randint(low, high + 1, size=(self._rows, self._cols))
        self._last_operation = f"generated({low},{high})"
        return self._data

    def set_data(self, values: Union[list, np.ndarray]) -> np.ndarray:
        """Set matrix data from external list/array with validation."""
        arr = np.asarray(values)
        if arr.shape != (self._rows, self._cols):
            raise ValueError(f"Shape mismatch: expected {self.shape}, got {arr.shape}")
        self._data = arr.astype(int)
        self._last_operation = "data_set"
        return self._data

    def __len__(self) -> int:
        return self._rows * self._cols if self._data is not None else 0

    def __str__(self) -> str:
        return f"BaseMatrix({self._rows}x{self._cols}, ops='{self._last_operation}')"

    def __repr__(self) -> str:
        return f"BaseMatrix(rows={self._rows}, cols={self._cols}, seed={self._seed})"

    @classmethod
    def get_instance_count(cls) -> int:
        """Class method: return total created matrix instances."""
        return cls._matrix_count

    @staticmethod
    def get_type_name() -> str:
        """Static method: return matrix type identifier."""
        return "BaseMatrix"


class Variant27Matrix(BaseMatrix, StatsMixin):
    """
    Implements Variant 27 task:
    1. Insert first row after the row containing first encountered minimum element.
    2. Calculate median of first row using two methods (standard + formula).
    """

    def __init__(self, rows: int, cols: int, seed: Optional[int] = None):
        super().__init__(rows, cols, seed)  # Inheritance chain via super()

    def find_min_position(self) -> Tuple[int, int]:
        """Find position (row, col) of first encountered minimum element."""
        if self._data is None:
            raise ValueError("Matrix data not initialized. Call generate_random() or set_data() first.")
        min_val = np.min(self._data)
        # Find first occurrence (row-major order)
        for i in range(self._rows):
            for j in range(self._cols):
                if self._data[i, j] == min_val:
                    return (i, j)
        return (0, 0)  # Fallback (should never reach)

    def insert_first_row_after_min(self) -> np.ndarray:
        """
        Insert a copy of the first row after the row containing first minimum element.
        Returns new matrix with shape (rows+1, cols).
        """
        if self._data is None:
            raise ValueError("Matrix data not initialized.")

        min_row, _ = self.find_min_position()
        first_row = self._data[0:1, :]  # Keep 2D shape

        # Insert first row after min_row
        self._data = np.insert(self._data, min_row + 1, first_row, axis=0)
        self._rows += 1  # Update internal dimension
        self._last_operation = f"inserted_row_after_min@({min_row},:)"
        return self._data

    def get_first_row_median(self) -> dict:
        """
        Calculate median of the first row using two methods.
        Returns dict with both results for comparison.
        """
        if self._data is None:
            raise ValueError("Matrix data not initialized.")

        first_row = self._data[0, :]
        return {
            "median_standard": round(self.median_standard(first_row), 4),
            "median_formula": round(self.median_formula(first_row), 4),
            "values": first_row.tolist(),
            "sorted": np.sort(first_row).tolist()
        }

    def get_statistics(self) -> dict:
        """Return comprehensive statistics for the entire matrix."""
        if self._data is None:
            raise ValueError("Matrix data not initialized.")

        flat = self._data.flatten()
        return {
            "shape": self._data.shape,
            "min": int(np.min(flat)),
            "max": int(np.max(flat)),
            "mean": round(self.mean_standard(flat), 4),
            "median_standard": round(self.median_standard(flat), 4),
            "median_formula": round(self.median_formula(flat), 4),
            "variance": round(self.variance_standard(flat), 4),
            "std": round(self.std_standard(flat), 4),
            "min_position": self.find_min_position()
        }

    def to_list(self) -> list:
        """Convert matrix to nested Python list for serialization."""
        return self._data.tolist() if self._data is not None else []

    @staticmethod
    def get_type_name() -> str:
        """Override static method: return specific type identifier."""
        return "Variant27Matrix"