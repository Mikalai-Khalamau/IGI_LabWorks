# Lab 4, Task 6
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Interactive interface for Task 6: Pandas operations with Sberbank Housing dataset.
Demonstrates: input validation, specific exception handling, repeat loop, modular testing.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import SberbankDataProcessor
from statistical_analysis import StatisticalAnalyzer

def get_valid_int(prompt: str, min_val: int = 1, max_val: int = 1000) -> int:
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

def display_dataframe(df, title: str = "DataFrame"):
    """Display DataFrame with formatting."""
    print(f"\n{title}")
    print(df.to_string())
    print(f"Shape: {df.shape}")
    print()

def display_dict(data: dict, indent: int = 0):
    """Recursively display dictionary with formatting."""
    prefix = "  " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            print(f"{prefix}{key}:")
            display_dict(value, indent + 1)
        elif isinstance(value, list) and len(value) <= 10:
            print(f"{prefix}{key}: {value}")
        else:
            print(f"{prefix}{key}: {value}")

def run_task6():
    """Main interactive loop for Task 6 testing."""
    processor = None
    analyzer = None

    print("Task 6 | Variant 27: Pandas - Sberbank Housing Dataset")

    while True:
        print("\nMENU:")
        print("1. Load/Generate sample data")
        print("2. ЗАДАНИЕ А: Create random transactions DataFrame (reset index)")
        print("3. Display DataFrame info")
        print("4. Display sample data")
        print("5. ЗАДАНИЕ Б: Analyze expensive vs cheap districts")
        print("6. Get detailed statistics")
        print("7. Get district statistics")
        print("8. Filter by district")
        print("9. Get top districts")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        try:
            if choice == '1':
                n_samples = get_valid_int("Number of samples (5-1000): ", min_val=5, max_val=1000)
                processor = SberbankDataProcessor()
                processor.load_sample_data(n_samples)
                analyzer = StatisticalAnalyzer(processor)
                print(f"Loaded {n_samples} sample transactions.")
                print(f"Columns: {list(processor.data.columns)}")

            elif choice == '2':
                if not processor:
                    print("Load data first (Option 1).")
                    continue
                n = get_valid_int("Number of random transactions (1-100): ", min_val=1, max_val=100)
                result_df = processor.create_random_transactions_df(n)
                display_dataframe(result_df, f"ЗАДАНИЕ А: Random {n} Transactions (Index Reset)")
                print("Columns: price, full_sq, floor")
                print("Index reset with original_index column saved")

            elif choice == '3':
                if not processor:
                    print("Load data first (Option 1).")
                    continue
                info = processor.get_dataframe_info()
                print("\nDATAFRAME INFORMATION:")
                display_dict(info)

            elif choice == '4':
                if not processor:
                    print("Load data first (Option 1).")
                    continue
                n = get_valid_int("Number of rows to display (1-20): ", min_val=1, max_val=20)
                display_dataframe(processor.data.head(n), "Sample Data")

            elif choice == '5':
                if not analyzer:
                    print("Load data first (Option 1).")
                    continue
                result = analyzer.analyze_expensive_vs_cheap_districts()
                print("\nЗАДАНИЕ Б: DISTRICT PRICE COMPARISON")
                print(f"Most expensive district: {result['most_expensive_district']}")
                print(f"Avg price per sqm: {result['most_expensive_price_per_sqm']} RUB")
                print(f"Cheapest district: {result['cheapest_district']}")
                print(f"Avg price per sqm: {result['cheapest_price_per_sqm']} RUB")
                print(f" RATIO: {result['ratio']} times")
                print("\nAll districts (avg price per sqm):")
                for district, price in result['all_districts_avg'].items():
                    print(f"{district}: {price} RUB/sqm")

            elif choice == '6':
                if not analyzer:
                    print("Load data first (Option 1).")
                    continue
                stats = analyzer.get_detailed_statistics()
                print("\nDETAILED STATISTICAL ANALYSIS:")
                display_dict(stats)

            elif choice == '7':
                if not analyzer:
                    print("Load data first (Option 1).")
                    continue
                district_stats = analyzer.get_district_statistics()
                display_dataframe(district_stats, "District Statistics")

            elif choice == '8':
                if not analyzer:
                    print("Load data first (Option 1).")
                    continue
                if processor.data is None:
                    print("No data loaded.")
                    continue
                districts = processor.data['sub_area'].unique()
                print(f"\nAvailable districts: {list(districts)}")
                district = input("Enter district name: ").strip()
                filtered = analyzer.filter_by_district(district)
                if len(filtered) > 0:
                    display_dataframe(filtered.head(10), f"Transactions in '{district}'")
                    print(f"Total transactions: {len(filtered)}")
                else:
                    print(f"No transactions found in '{district}'")

            elif choice == '9':
                if not analyzer:
                    print("Load data first (Option 1).")
                    continue
                n = get_valid_int("Number of top districts (1-10): ", min_val=1, max_val=10)
                print("\nSort by:")
                print("1. Price per sqm")
                print("2. Total price")
                sort_choice = input("Select: ").strip()
                by = 'price_per_sqm' if sort_choice == '1' else 'price'
                top = analyzer.get_top_districts(n, by)
                display_dataframe(top.to_frame(name=f'avg_{by}'), f"Top {n} Districts")

            elif choice == '0':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid menu option.")

        except ValueError as ve:
            print(f"Value Error: {ve}")
        except KeyError as ke:
            print(f"Key Error: {ke}")
        except Exception as e:
            print(f"Critical Error: {type(e).__name__}: {e}")

        # Repeat loop
        again = input("\nReturn to menu? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    run_task6()