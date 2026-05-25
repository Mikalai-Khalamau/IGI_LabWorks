# Lab 4, Task 1
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Interactive module for testing Task 1.
Demonstrates: input validation, specific exception handling, repeat loop, polymorphism usage.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from storage import RationalStorage
from models import RationalNumber

def get_valid_int(prompt: str) -> int:
    """Validates user input to ensure it's an integer."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Error: Invalid input. Please enter an integer.")

def get_valid_float_or_str(prompt: str) -> str:
    """Validates non-empty string input."""
    while True:
            val = input(prompt).strip()
            if val:
                return val
            print("Error: Input cannot be empty.")

def display_info(obj):
    """Polymorphic function: displays info depending on object type."""
    if isinstance(obj, RationalNumber):
        print(f"Rational Info: {obj} (float: {obj.to_float():.4f})")
    elif isinstance(obj, str):
        print(f"Text: {obj}")
    else:
        print(f"Object: {repr(obj)}")

def run_task1():
    """Main interactive loop for Task 1."""
    storage = RationalStorage()
    filepath_csv = "rationals.csv"
    filepath_pickle = "rationals.pkl"

    print("Task 1 | Variant 27: Rational Numbers Dictionary")

    while True:
        print("\nMENU:")
        print("1. Add rational number")
        print("2. Save to CSV / Load from CSV")
        print("3. Save to Pickle / Load from Pickle")
        print("4. Find duplicates (equal numbers)")
        print("5. Find maximum number")
        print("6. Sort & display")
        print("7. Search by key")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        try:
            if choice == '1':
                key = get_valid_float_or_str("Enter key: ")
                num = get_valid_int("Enter numerator: ")
                den = get_valid_int("Enter denominator: ")
                storage.add(key, num, den)
                print(f"Added {key} = {storage.data[key]}")

            elif choice == '2':
                sub = input("Save (s) or Load (l)? ").strip().lower()
                if sub == 's':
                    storage.save_csv(filepath_csv)
                    print(f"Saved to {filepath_csv}")
                elif sub == 'l':
                    storage.load_csv(filepath_csv)
                    print(f"Loaded from {filepath_csv}")

            elif choice == '3':
                sub = input("Save (s) or Load (l)? ").strip().lower()
                if sub == 's':
                    storage.save_pickle(filepath_pickle)
                    print(f"Saved to {filepath_pickle}")
                elif sub == 'l':
                    storage.load_pickle(filepath_pickle)
                    print(f"Loaded from {filepath_pickle}")

            elif choice == '4':
                dups = storage.find_duplicates()
                if dups: print(f"Duplicates: {', '.join(dups)}")
                else: print("No duplicates found.")

            elif choice == '5':
                max_key, max_val = storage.find_max()
                if max_val:
                    print(f"Maximum: {max_key} = {max_val}")
                else: print("Storage is empty.")

            elif choice == '6':
                desc = input("Descending? (y/n): ").strip().lower() == 'y'
                sorted_data = storage.sort_by_value(descending=desc)
                for k, v in sorted_data.items():
                    print(f"{k}: {v}")

            elif choice == '7':
                key = get_valid_float_or_str("Enter key to search: ")
                res = storage.find_by_key(key)
                if res: display_info(res)
                else: print("Key not found.")

            elif choice == '0':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid menu option.")

        except Exception as e:
            print(f"Critical Error: {e}")

        # Repeat loop check
        again = input("\nRepeat menu? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    run_task1()