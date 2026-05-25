# Lab 4, Task 5
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Interactive interface for Task 5: NumPy matrix operations, Variant 27.
Demonstrates: input validation, specific exception handling, repeat loop, modular testing.
"""
import sys
import os
from typing import Optional
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from matrix_core import Variant27Matrix, BaseMatrix


def get_valid_int(prompt: str, min_val: int = 1, max_val: int = 100) -> int:
    """Validate integer input within specified range."""
    while True:
        try:
            val = int(input(prompt).strip())
            if val < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if val > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return val
        except ValueError:
            print("Error: Please enter a valid integer.")


def get_valid_int_or_empty(prompt: str) -> Optional[int]:
    """Validate optional integer input (empty = None)."""
    while True:
        val = input(prompt).strip()
        if val == "":
            return None
        try:
            return int(val)
        except ValueError:
            print("Error: Please enter a valid integer or leave empty.")


def display_matrix(matrix: np.ndarray, title: str = "Matrix"):
    """Display NumPy array with formatting."""
    print(f"\n{title} (shape: {matrix.shape}):")
    for row in matrix:
        print("  " + "  ".join(f"{v:4d}" for v in row))


def display_statistics(stats: dict):
    """Display statistics dictionary in formatted way."""
    print("\nStatistics:")
    for key, value in stats.items():
        if isinstance(value, (list, tuple)) and len(value) <= 10:
            print(f"{key}: {value}")
        elif isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"{k}: {v}")
        else:
            print(f"{key}: {value}")


def run_task5():
    """Main interactive loop for Task 5 testing."""
    matrix = None

    print("Task 5 | Variant 27: NumPy Matrix Operations")
    print("Task: Insert first row after row with first min element; median (2 ways)")

    while True:
        print("\nMENU:")
        print("1. Create & generate random matrix")
        print("2. Set matrix data manually")
        print("3. Display current matrix")
        print("4. Find min element position")
        print("5. Insert first row after min row (Variant 27 task)")
        print("6. Calculate median of first row (2 methods)")
        print("7. Show full statistics")
        print("8. Test polymorphism & mixins")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        try:
            if choice == '1':
                print("\nMatrix parameters:")
                rows = get_valid_int("  Rows (1-50): ", min_val=1, max_val=50)
                cols = get_valid_int("  Columns (1-20): ", min_val=1, max_val=20)
                seed = get_valid_int_or_empty("  Random seed (optional, press Enter to skip): ")
                low = get_valid_int("  Min value: ", min_val=-1000, max_val=1000)
                high = get_valid_int("  Max value: ", min_val=low, max_val=1000)

                matrix = Variant27Matrix(rows, cols, seed)
                matrix.generate_random(low, high)
                print(f"Matrix generated: {matrix}")

            elif choice == '2':
                if not matrix:
                    print("Create matrix first (Option 1).")
                    continue
                print(f"\nEnter {matrix.shape[0]}x{matrix.shape[1]} integers (row by row):")
                data = []
                for i in range(matrix.shape[0]):
                    while True:
                        try:
                            row = list(map(int, input(f"  Row {i + 1}: ").strip().split()))
                            if len(row) != matrix.shape[1]:
                                print(f"Expected {matrix.shape[1]} values, got {len(row)}")
                                continue
                            data.append(row)
                            break
                        except ValueError:
                            print("Error: Please enter valid integers.")
                matrix.set_data(data)
                print("Data set successfully.")

            elif choice == '3':
                if not matrix or matrix.data is None:
                    print("Generate or set matrix data first.")
                    continue
                display_matrix(matrix.data, "Current Matrix")

            elif choice == '4':
                if not matrix or matrix.data is None:
                    print("Generate or set matrix data first.")
                    continue
                pos = matrix.find_min_position()
                min_val = matrix.data[pos[0], pos[1]]
                print(f"First minimum element: {min_val} at position row={pos[0]}, col={pos[1]}")

            elif choice == '5':
                if not matrix or matrix.data is None:
                    print("Generate or set matrix data first.")
                    continue
                print("\nInserting first row after row with first minimum...")
                new_data = matrix.insert_first_row_after_min()
                display_matrix(new_data, "Matrix After Insertion")
                print(f"Operation completed: {matrix.last_operation}")

            elif choice == '6':
                if not matrix or matrix.data is None:
                    print("Generate or set matrix data first.")
                    continue
                result = matrix.get_first_row_median()
                print(f"\nMEDIAN OF FIRST ROW:")
                print(f"Values: {result['values']}")
                print(f"Sorted: {result['sorted']}")
                print(f"Median (NumPy): {result['median_standard']}")
                print(f"Median (Formula): {result['median_formula']}")
                if abs(result['median_standard'] - result['median_formula']) < 1e-9:
                    print("Both methods match!")
                else:
                    print("Results differ - check implementation.")

            elif choice == '7':
                if not matrix or matrix.data is None:
                    print("Generate or set matrix data first.")
                    continue
                stats = matrix.get_statistics()
                display_statistics(stats)

            elif choice == '8':
                print("\nPOLYMORPHISM & MIXIN TEST:")
                # Test static method polymorphism
                print(f"Type name (static): {Variant27Matrix.get_type_name()}")
                print(f"Base type name: {BaseMatrix.get_type_name()}")
                # Test instance count
                print(f"Total matrices created: {BaseMatrix.get_instance_count()}")
                # Test mixin methods directly
                if matrix and matrix.data is not None:
                    test_data = [1, 3, 5, 7, 9]
                    print(f"Median test [1,3,5,7,9]:")
                    print(f"Standard: {matrix.median_standard(test_data)}")
                    print(f"Formula:  {matrix.median_formula(test_data)}")

            elif choice == '0':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid menu option.")

        except ValueError as ve:
            print(f"Value Error: {ve}")
        except IndexError as ie:
            print(f"Index Error: {ie}")
        except Exception as e:
            print(f"Critical Error: {type(e).__name__}: {e}")

        # Lab 3/4 Requirement: Repeat loop without exit
        again = input("\nReturn to menu? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting program. Goodbye!")
            break


if __name__ == "__main__":
    run_task5()