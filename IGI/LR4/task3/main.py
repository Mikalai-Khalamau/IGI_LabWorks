# Lab 4, Task 3
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Interactive interface for Task 3: arcsin(x) Taylor series + statistics + visualization.
Demonstrates: input validation, specific exception handling, repeat loop, modular testing.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from series_core import ArcsinTaylorSeries
from plotter import Plotter


def get_valid_float(prompt: str, min_val: float = None, max_val: float = None) -> float:
    """Validates float input with optional range constraints."""
    while True:
        try:
            val = float(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return val
        except ValueError:
            print("Error: Please enter a valid number.")


def display_table(data: list):
    """Displays computation results as formatted console table."""
    print(f"{'x':>8} {'F_series':>12} {'F_math':>12} {'Error':>14} {'n':>4}")
    for row in data:
        print(f"{row['x']:8.4f} {row['F_series']:12.6f} {row['F_math']:12.6f} "
              f"{row['error']:14.2e} {row['n']:4d}")

def run_task3():
    """Main interactive loop for Task 3 testing."""
    calculator = None
    plotter = None
    output_file = "output/task3_arcsin_plot.png"

    print("Task 3 | Variant 27: arcsin(x) Taylor Series + Stats + Plot")

    while True:
        print("\nMENU:")
        print("1. Configure & compute arcsin series")
        print("2. Display results table")
        print("3. Show statistics (mean, median, mode, variance, std)")
        print("4. Create & display plot")
        print("5. Save plot to file")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        try:
            if choice == '1':
                print("\nSeries parameters (|x| < 1):")
                x_start = get_valid_float("  x_start (>= -0.99): ", min_val=-0.99, max_val=0.99)
                x_end = get_valid_float("  x_end (<= 0.99): ", min_val=x_start, max_val=0.99)
                step = get_valid_float("  step (e.g., 0.1): ", min_val=0.01)
                eps = get_valid_float("  eps (precision, e.g., 1e-6): ", min_val=1e-10, max_val=0.001)

                calculator = ArcsinTaylorSeries(x_start, x_end, step, eps)
                calculator.compute()
                plotter = Plotter(title=f"arcsin(x) Taylor Series (eps={eps})")
                print("Computation completed.")

            elif choice == '2':
                if not calculator:
                    print("Compute series first (Option 1).")
                    continue
                display_table(calculator.results)

            elif choice == '3':
                if not calculator:
                    print("Compute series first (Option 1).")
                    continue
                stats = calculator.get_statistics()
                print("\nStatistics for F_series values:")
                for k, v in stats.items():
                    print(f"{k}: {v}")

            elif choice == '4':
                if not calculator or not plotter:
                    print("Compute series first (Option 1).")
                    continue
                plotter.create_plot(calculator.results, series_label="arcsin Taylor", math_label="math.asin(x)")
                plotter.show_plot()

            elif choice == '5':
                if not plotter:
                    print("Create plot first (Option 4).")
                    continue
                filepath = input(f"Save path [default: {output_file}]: ").strip()
                if not filepath: filepath = output_file
                plotter.save_plot(filepath)

            elif choice == '0':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid menu option.")

        except ValueError as ve:
            print(f"Value Error: {ve}")
        except Exception as e:
            print(f"Critical Error: {e}")

        again = input("\nReturn to menu? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting program. Goodbye!")
            break


if __name__ == "__main__":
    run_task3()