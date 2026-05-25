# Lab 4, Task 4
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Interactive interface for Task 4: Regular Hexagon visualization.
Demonstrates: input validation, specific exception handling, repeat loop, modular testing.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from figures import RegularHexagon, GeometricFigure, FigureColor
from renderer import FigureRenderer


def get_valid_float(prompt: str, min_val: float = 0.01, max_val: float = 100.0) -> float:
    """Validates float input within specified range."""
    while True:
        try:
            val = float(input(prompt).strip())
            if val < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if val > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return val
        except ValueError:
            print("Error: Please enter a valid number.")


def get_valid_color(prompt: str) -> str:
    """Validates color input against allowed list."""
    valid = FigureColor._valid_colors
    while True:
        val = input(f"{prompt} {valid}: ").strip().lower()
        if val in valid:
            return val
        print(f"Invalid color. Choose from: {valid}")


def get_valid_string(prompt: str, allow_empty: bool = True) -> str:
    """Validates non-empty string input (optional)."""
    while True:
        val = input(prompt).strip()
        if val or allow_empty:
            return val
        print("Input cannot be empty.")


def run_task4():
    """Main interactive loop for Task 4 testing."""
    hexagon = None
    renderer = None
    output_file = "output/task4_hexagon.png"

    print("Task 4 | Variant 27: Regular Hexagon Visualization")
    print("Requirements: ABC, inheritance, @property, mixins, matplotlib, file I/O")

    while True:
        print("\nMENU:")
        print("1. Create regular hexagon")
        print("2. Display figure info")
        print("3. Draw & display figure")
        print("4. Save figure to file")
        print("5. Test polymorphism & mixins")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        try:
            if choice == '1':
                print("\nHexagon parameters:")
                side = get_valid_float("  Side length (a): ", min_val=0.1, max_val=50.0)
                color = get_valid_color("  Color")
                label = get_valid_string("  Label text (optional): ", allow_empty=True)

                hexagon = RegularHexagon(side, color)
                hexagon.label = label
                renderer = FigureRenderer(title=f"{hexagon.get_name()} Visualization")
                print(f"Created: {hexagon}")

            elif choice == '2':
                if not hexagon:
                    print("Create hexagon first (Option 1).")
                    continue
                print("\nFigure information:")
                print(f"Name: {hexagon.get_name()}")
                print(f"Formatted: {hexagon.get_formatted_info()}")
                print(f"Parameters: {hexagon.get_parameters()}")
                print(f"Area: {hexagon.area():.4f}")
                print(f"Vertices: {hexagon.get_vertices()}")
                print(f"Dict export: {hexagon.to_dict()}")

            elif choice == '3':
                if not hexagon or not renderer:
                    print("Create hexagon first (Option 1).")
                    continue
                renderer.draw_hexagon(hexagon.get_vertices(),
                                      hexagon.color_obj.color,
                                      hexagon.label)
                renderer.show_plot()

            elif choice == '4':
                if not renderer:
                    print("Draw figure first (Option 3).")
                    continue
                filepath = input(f"Save path [default: {output_file}]: ").strip()
                if not filepath:
                    filepath = output_file
                if renderer.save_plot(filepath):
                    print(f"Saved successfully.")
                renderer.close()

            elif choice == '5':
                print("\nPOLYMORPHISM & MIXIN TEST:")
                # Test polymorphic behavior
                figures: list[GeometricFigure] = []
                if hexagon:
                    figures.append(hexagon)
                for fig in figures:
                    # Polymorphic calls
                    print(f"str(): {str(fig)}")
                    print(f"area(): {fig.area():.2f}")
                    print(f"get_formatted_info(): {fig.get_formatted_info()}")
                    print(f"to_dict() keys: {list(fig.to_dict().keys())}")
                # Test static/class methods
                print(f"Total figures created: {GeometricFigure.get_figures_count()}")
                print(f"Figure name (static): {RegularHexagon.get_name()}")

            elif choice == '0':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid menu option.")

        except ValueError as ve:
            print(f"Value Error: {ve}")
        except Exception as e:
            print(f"Critical Error: {e}")

        # Lab 3/4 Requirement: Repeat loop without exit
        again = input("\nReturn to menu? (y/n): ").strip().lower()
        if again != 'y':
            print("Exiting program. Goodbye!")
            break


if __name__ == "__main__":
    run_task4()