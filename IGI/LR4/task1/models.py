# Lab 4, Task 1
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module defining the RationalNumber class with OOP features.
Demonstrates: properties, getters/setters, magic methods, static/dynamic attributes.
"""
import math


class RationalNumber:
    """Represents a rational number with numerator and denominator."""

    # Static attribute: tracks total instances created
    _instances_count: int = 0

    def __init__(self, numerator: int, denominator: int):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self._numerator = numerator
        self._denominator = denominator
        self._reduce()
        RationalNumber._instances_count += 1

    def _reduce(self):
        """Reduces the fraction to its simplest form."""
        gcd = math.gcd(abs(self._numerator), abs(self._denominator))
        self._numerator //= gcd
        self._denominator //= gcd
        if self._denominator < 0:
            self._numerator *= -1
            self._denominator *= -1

    @property
    def numerator(self) -> int:
        return self._numerator

    @numerator.setter
    def numerator(self, value: int):
        self._numerator = value
        self._reduce()

    def get_numerator(self) -> int:
        """Classic getter method."""
        return self._numerator

    def set_numerator(self, value: int):
        """Classic setter method."""
        self.numerator = value

    @property
    def denominator(self) -> int:
        return self._denominator

    @denominator.setter
    def denominator(self, value: int):
        if value == 0:
            raise ValueError("Denominator cannot be zero.")
        self._denominator = value
        self._reduce()

    # Magic methods for polymorphism and comparison
    def __eq__(self, other):
        if isinstance(other, RationalNumber):
            return self.numerator == other.numerator and self.denominator == other.denominator
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, RationalNumber):
            return self.numerator * other.denominator < other.numerator * self.denominator
        return NotImplemented

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        return f"RationalNumber({self.numerator}, {self.denominator})"

    def to_float(self) -> float:
        """Converts rational number to float for sorting/comparison."""
        return self.numerator / self.denominator