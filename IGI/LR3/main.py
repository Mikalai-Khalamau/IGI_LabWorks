"""
Laboratory Work No. 3
Topic: Standard data types, collections, functions, modules
Author: Khalamau Mikalai Andreevich
Version: 1.0
Date: 2025-03-19
"""

from utils import task_info, get_menu_choice
from task_1 import task_1
from task_2 import task_2
from task_3 import task_3
from task_4 import task_4
from task_5 import task_5


@task_info(
    title="Task 1: Series Expansion",
    description="Calculate ln(1+x) using power series with specified accuracy",
)
def run_task1():
    """Wrapper function for Task 1 with decorator."""
    task_1()


@task_info(
    title="Task 2: Find Minimum",
    description="Find minimum number in sequence until 1 is entered",
)
def run_task2():
    """Wrapper function for Task 2 with decorator."""
    task_2()


@task_info(
    title="Task 3: String Analysis",
    description="Count lowercase letters and digits in input string",
)
def run_task3():
    """Wrapper function for Task 3 with decorator."""
    task_3()


@task_info(
    title="Task 4: Text Analysis",
    description="Analyze fixed text: odd-length words, shortest 'i' word, repetitive words",
)
def run_task4():
    """Wrapper function for Task 4 with decorator."""
    task_4()


@task_info(
    title="Task 5: List Processing",
    description="Find max modulo element and sum before last positive element",
)
def run_task5():
    """Wrapper function for Task 5 with decorator."""
    task_5()


# Main menu function


def print_menu():
    """Print the main menu with available options."""
    print("MAIN MENU")
    print("1. Task 1: Series Expansion (Variant 28)")
    print("2. Task 2: Find Minimum (Variant 28)")
    print("3. Task 3: String Analysis (Variant 28)")
    print("4. Task 4: Text Analysis (Variant 28)")
    print("5. Task 5: List Processing (Variant 3)")
    print("0. Exit Program")


def main():
    """
    Main function with menu loop for repeated execution.
    """

    print("Welcome to Laboratory Work 3!")

    while True:
        try:
            # Display menu
            print_menu()

            # Get user choice with validation (Requirement 11, 12)
            choice = get_menu_choice(
                "\nSelect task number (0-5): ", ["0", "1", "2", "3", "4", "5"]
            )

            # Execute selected task
            if choice == "1":
                run_task1()
            elif choice == "2":
                run_task2()
            elif choice == "3":
                run_task3()
            elif choice == "4":
                run_task4()
            elif choice == "5":
                run_task5()
            elif choice == "0":
                print("Thank you for using Laboratory Work 3!")
                print("Program ended successfully.")
                break

            # Prompt to continue
            print("\nTask completed!")
            continue_choice = get_menu_choice("Return to menu? (y/n): ", ["y", "n"])
            if continue_choice == "n":
                print("\nProgram ended by user.")
                break

        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user (Ctrl+C).")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
