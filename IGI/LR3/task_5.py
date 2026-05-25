from utils import get_positive_int_input, get_menu_choice
from sequence_initialization import init_list_manual, init_list_generator


def task_5():
    """
    Main function for Task 5.

    Processes float list according to Variant 28:
    1) Find maximum modulo element
    2) Find sum of elements before last positive element
    """

    # Get list size from user
    size = get_positive_int_input("Enter list size: ")

    # Choose initialization method
    print("\nChoose initialization method:")
    print("1. Manual input (enter each element)")
    print("2. Random generator (automatic)")

    choice = get_menu_choice("    Enter choice (1 or 2): ", ["1", "2"])

    # Initialize list based on user choice
    if choice == "1":
        data_list = init_list_manual(size)
    else:
        data_list = list(init_list_generator(size))
    # Check if list is empty
    if not data_list:
        print("\nList is empty. Cannot process.")
        return

    # Display the list
    print(f"\nProcessing list: {data_list}")

    # Task 5a: Find maximum modulo element
    max_mod_value = max(data_list, key=abs)
    max_mod_index = data_list.index(max_mod_value)

    # Task 5b: Find sum before last positive element
    last_pos_index = -1
    for index, value in enumerate(data_list):
        if value > 0:
            last_pos_index = index

    # Calculate sum
    if last_pos_index != -1:
        sum_before_last_pos = sum(data_list[:last_pos_index])
    else:
        sum_before_last_pos = 0
        print("\nWarning: No positive elements found in list.")

    # Display results
    print_results(
        data_list, max_mod_value, max_mod_index, last_pos_index, sum_before_last_pos
    )


def print_results(
    data_list, max_mod_value, max_mod_index, last_pos_index, sum_before_last_pos
):
    """
    Print the processing results in formatted view.
    """
    print("Results")

    # Part 1: Maximum modulo element
    print("\n1) Maximum modulo element:")
    print(f"Value: {max_mod_value}")
    print(f"Module: {abs(max_mod_value)}")
    print(f"Index: {max_mod_index}")

    # Part 2: Sum before last positive element
    print("\n2) Sum before last positive element:")
    if last_pos_index != -1:
        print(f"Last positive element index: {last_pos_index}")
        print(f"Last positive element value: {data_list[last_pos_index]}")
        print(f"Sum of elements before it: {sum_before_last_pos}")
    else:
        print("No positive elements found")
        print(f"Sum: {sum_before_last_pos}")
