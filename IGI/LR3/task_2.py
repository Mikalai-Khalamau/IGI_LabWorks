from utils import get_int_input


def task_2():
    """
    Main function for Task 2.
    Accepts integers from user and finds the minimum value.
    Loop terminates when user enters 1.
    """
    # Initialize empty list for storing numbers
    numbers = []

    print("Enter integers (enter 1 to finish):\n")

    # Input loop with validation
    while True:
        x = get_int_input(f"Enter number #{len(numbers) + 1}: ")

        # Check termination condition
        if x == 1:
            print("\nInput terminated by user (1 entered).")
            break

        # Add valid number to list
        numbers.append(x)

    # Process results
    if len(numbers) == 0:
        print("\nNo numbers were entered.")
    else:
        min_value = min(numbers)

        print("Results")
        print(f"Total numbers entered: {len(numbers)}")
        print(f"Minimum value: {min_value}")
