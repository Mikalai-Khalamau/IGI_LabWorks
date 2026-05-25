# Lab 4, Task 1
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for data storage, serialization (CSV, Pickle), and processing.
Demonstrates: inheritance, super(), mixins, polymorphism, dynamic attributes.
"""
import csv
import pickle
import os
from typing import Dict, List, Optional
from models import RationalNumber

class BaseStorage:
    """Abstract-like base class for storage operations."""
    def __init__(self):
        self.data: Dict[str, RationalNumber] = {}

    def add(self, key: str, num: int, den: int):
        raise NotImplementedError("Subclasses must implement add()")

    def get_all(self) -> Dict[str, RationalNumber]:
        return self.data.copy()

class SearchMixin:
    """Mixin providing search functionality."""
    def find_by_key(self, key: str) -> Optional[RationalNumber]:
        """Finds a rational number by its string key."""
        return self.data.get(key, None)

    def find_duplicates(self) -> List[str]:
        """Identifies equal rational numbers in the storage."""
        duplicates = []
        keys = list(self.data.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                if self.data[keys[i]] == self.data[keys[j]]:
                    duplicates.append(f"{keys[i]} == {keys[j]}")
        return duplicates

class SortMixin:
    """Mixin providing sorting and max-value functionality."""
    def sort_by_value(self, descending: bool = False) -> Dict[str, RationalNumber]:
        """Sorts dictionary items by rational number value."""
        sorted_items = sorted(self.data.items(), key=lambda item: item[1].to_float(), reverse=descending)
        return dict(sorted_items)

    def find_max(self) -> tuple:
        """Finds the key and value of the maximum rational number."""
        if not self.data:
            return None, None
        return max(self.data.items(), key=lambda item: item[1].to_float())

class RationalStorage(BaseStorage, SearchMixin, SortMixin):
    """Manages dictionary of RationalNumber objects and handles file I/O."""
    def __init__(self):
        super().__init__()  # Initializes base class
        self._last_operation = "init"  # Dynamic attribute example

    def add(self, key: str, num: int, den: int):
        self.data[key] = RationalNumber(num, den)
        self._last_operation = f"Added {key}"

    def save_csv(self, filepath: str):
        """Saves data to CSV file."""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Key", "Numerator", "Denominator"])
            for k, v in self.data.items():
                writer.writerow([k, v.numerator, v.denominator])

    def load_csv(self, filepath: str):
        """Loads data from CSV file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        self.data.clear()
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                self.data[row[0]] = RationalNumber(int(row[1]), int(row[2]))

    def save_pickle(self, filepath: str):
        """Serializes data using pickle."""
        with open(filepath, 'wb') as f:
            pickle.dump(self.data, f)

    def load_pickle(self, filepath: str):
        """Deserializes data using pickle."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Pickle file not found: {filepath}")
        with open(filepath, 'rb') as f:
            self.data = pickle.load(f)