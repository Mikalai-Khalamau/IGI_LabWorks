# Lab 4, Task 2
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Interactive interface for Task 2.
Demonstrates: input validation, specific exception handling, repeat loop, polymorphic display.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from text_processor import AdvancedTextAnalyzer
from file_manager import FileManager

def get_valid_string(prompt: str) -> str:
    """Ensures non-empty string input."""
    while True:
        val = input(prompt).strip()
        if val: return val
        print("Input cannot be empty.")

def display_result(key: str, value):
    """Polymorphic display: formats output based on data type."""
    if isinstance(value, list):
        print(f"{key}: {value}")
    elif isinstance(value, dict):
        print(f"{key}:")
        for k, v in value.items(): print(f"{k}: {v}")
    else:
        print(f"{key}: {value}")

def run_task2():
    fm = FileManager()
    analyzer = None
    results = None
    out_path = None

    print("Task 2 | Variant 27: Text Analysis & Regex")

    while True:
        print("\nMenu:")
        print("1. Load & analyze text from file")
        print("2. Display full results")
        print("3. Save results to output file")
        print("4. Archive output file (ZIP)")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        try:
            if choice == '1':
                inp = get_valid_string("Enter input file path: ")
                text = fm.read_text(inp)
                analyzer = AdvancedTextAnalyzer(text)
                results = analyzer.analyze_all()
                print("Analysis completed successfully.")

            elif choice == '2':
                if not results:
                    print("Please analyze text first (Option 1).")
                    continue
                for k, v in results.items():
                    display_result(k, v)

            elif choice == '3':
                if not results:
                    print("Please analyze text first (Option 1).")
                    continue
                out_path = get_valid_string("Enter output file path: ")
                fm.save_results(out_path, results, analyzer.text)
                print(f"Results saved to '{out_path}'")

            elif choice == '4':
                if not out_path or not os.path.exists(out_path):
                    print("Save results first (Option 3).")
                    continue
                zip_path = os.path.splitext(out_path)[0] + ".zip"
                info = fm.archive_file(out_path, zip_path)
                print("Archive created successfully:")
                for line in info: print(f"   {line}")

            elif choice == '0':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid menu option.")

        except FileNotFoundError as fnf_err:
            print(f"File Error: {fnf_err}")
        except Exception as e:
            print(f"Critical Error: {e}")

        # Repeat loop
        again = input("\nReturn to menu? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    run_task2()