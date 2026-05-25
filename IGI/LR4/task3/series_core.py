# Lab 4, Task 3
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for Taylor series computation of arcsin(x), statistical analysis, and OOP structure.
"""
import math
import time
from typing import List, Dict, Generator, Optional, Callable
from functools import wraps
from collections import Counter


# Lab 3 Requirement: Decorator for execution tracking
def execution_timer(func: Callable) -> Callable:
    """Decorator to measure and log execution time of computation functions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} executed in {end - start:.4f} seconds.")
        return result

    return wrapper


class BaseSeries:
    """Abstract-like base class for Taylor series."""
    _series_name: str = "Unknown"  # Static attribute

    def __init__(self, x_start: float, x_end: float, step: float, eps: float, max_iter: int = 500):
        self._x_start = x_start
        self._x_end = x_end
        self._step = step
        self._eps = eps
        self._max_iter = max_iter
        self._results: List[Dict] = []
        self._last_status: str = "initialized"  # Dynamic attribute

    @property
    def results(self) -> List[Dict]:
        return self._results.copy()

    @property
    def status(self) -> str:
        return self._last_status

    def get_bounds(self) -> tuple:
        return self._x_start, self._x_end

    def set_bounds(self, start: float, end: float):
        if start >= end:
            raise ValueError("Start must be strictly less than end.")
        self._x_start = start
        self._x_end = end

    def __len__(self) -> int:
        return len(self._results)

    def __str__(self) -> str:
        return f"{self._series_name}(x=[{self._x_start}:{self._x_end}], eps={self._eps})"

    def compute(self) -> List[Dict]:
        raise NotImplementedError("Subclasses must implement compute()")


# Generator for sequence initialization
def x_value_generator(start: float, end: float, step: float) -> Generator[float, None, None]:
    """Generator yielding x values from start to end with given step."""
    curr = start
    while curr <= end + 1e-9:
        yield round(curr, 4)
        curr += step


class StatsMixin:
    """Mixin providing statistical analysis of numeric sequences."""

    @staticmethod
    def mean(values: List[float]) -> float:
        """Arithmetic mean."""
        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def median(values: List[float]) -> float:
        """Median: standard implementation."""
        if not values: return 0.0
        s = sorted(values)
        n = len(s)
        return (s[n // 2 - 1] + s[n // 2]) / 2 if n % 2 == 0 else s[n // 2]

    @staticmethod
    def median_formula(values: List[float]) -> float:
        """Median: explicit formula implementation (Lab 3/4 requirement)."""
        if not values: return 0.0
        s = sorted(values)
        n = len(s)
        mid = (n - 1) / 2
        return (s[int(mid)] + s[int(mid) + 1]) / 2 if n % 2 == 0 else s[int(mid)]

    @staticmethod
    def mode(values: List[float]) -> Optional[float]:
        """Mode: most frequent value (rounded for float stability)."""
        if not values: return None
        rounded = [round(v, 4) for v in values]
        return Counter(rounded).most_common(1)[0][0]

    @staticmethod
    def variance(values: List[float], sample: bool = False) -> float:
        """Variance: sample (ddof=1) or population (ddof=0)."""
        if len(values) < 2 and sample: return 0.0
        m = StatsMixin.mean(values)
        ddof = 1 if sample else 0
        return sum((x - m) ** 2 for x in values) / (len(values) - ddof)

    @staticmethod
    def std(values: List[float], sample: bool = False) -> float:
        """Standard deviation: sqrt of variance."""
        return math.sqrt(StatsMixin.variance(values, sample))


class ArcsinTaylorSeries(BaseSeries, StatsMixin):
    """Implements Taylor series for arcsin(x)."""
    _series_name: str = "ArcsinTaylor"

    def __init__(self, x_start: float, x_end: float, step: float, eps: float, max_iter: int = 500):
        # arcsin domain: |x| < 1
        if x_start < -1 or x_end > 1:
            raise ValueError("arcsin(x) is defined for |x| < 1. Please use range within [-1, 1].")
        super().__init__(x_start, x_end, step, eps, max_iter)  # Inheritance chain

    @execution_timer  # Lab 3 decorator applied
    def compute(self) -> List[Dict]:
        """Computes arcsin series values for each x using generator-based initialization."""
        self._results = []
        for x in x_value_generator(self._x_start, self._x_end, self._step):
            series_val, n_terms = self._taylor_expansion(x, self._eps)
            math_val = math.asin(x)  # arcsin from math module
            self._results.append({
                "x": x,
                "F_series": round(series_val, 6),
                "F_math": round(math_val, 6),
                "error": round(abs(series_val - math_val), 8),
                "n": n_terms
            })
        self._last_status = "computed"
        return self._results

    def _taylor_expansion(self, x: float, eps: float) -> tuple:
        """
        Calculates Taylor series sum for arcsin(x).
        """
        term = x  # First term (n=0): x
        series_sum = term
        n = 1

        while abs(term) >= eps and n < self._max_iter:
            term *= ((2 * n - 1) ** 2) * (x ** 2) / (2 * n * (2 * n + 1))
            series_sum += term
            n += 1

        return series_sum, n

    def get_statistics(self) -> Dict[str, float]:
        """Computes statistics for the F_series sequence."""
        if not self._results: self.compute()
        values = [r["F_series"] for r in self._results]
        return {
            "mean": round(self.mean(values), 4),
            "median": round(self.median(values), 4),
            "median_formula": round(self.median_formula(values), 4),
            "mode": self.mode(values),
            "variance": round(self.variance(values), 4),
            "std": round(self.std(values), 4)
        }