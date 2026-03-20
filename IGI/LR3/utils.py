"""
Utility functions, decorators, and input validation for Lab Work 3.
Provides reusable functions for safe user input and function logging.
"""

import functools


def task_info(title, description):
    """
    Decorator to display task information before execution.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{title}")
            print(f"{description}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_float_input(prompt):
    """
    Safely get float input from user with ValueError handling.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
        except KeyboardInterrupt:
            print("\nInput interrupted by user.")
            raise


def get_int_input(prompt):
    """
    Safely get integer input from user with ValueError handling.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")
        except KeyboardInterrupt:
            print("\nInput interrupted by user.")
            raise


def get_positive_int_input(prompt):
    """
    Safely get positive integer input from user.
    """
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Value must be positive (greater than 0).")
        except ValueError:
            print("Invalid input. Please enter an integer.")
        except KeyboardInterrupt:
            print("\nInput interrupted by user.")
            raise


def get_menu_choice(prompt, valid_options):
    """
    Safely get menu choice from user within valid options.
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        else:
            print(f"Invalid choice. Please select from: {', '.join(valid_options)}")
