"""
List initialization functions (manual input and generator).
"""

import random


def init_list_manual(size):
    """
    Initialize list with user manual input.

    Args:
        size (int): Number of elements to input

    Returns:
        list: List of float values entered by user

    Requirement 9: User input initialization method.
    """
    lst = []
    print(f"\nPlease enter {size} elements:")
    for i in range(size):
        while True:
            try:
                val = float(input(f"  Element {i + 1}: "))
                lst.append(val)
                break
            except ValueError:
                print("  Invalid input. Please enter a number.")
    return lst


def init_list_generator(size, min_val=-100, max_val=100):
    """
    Initialize list with random generator.

    Args:
        size (int): Number of elements to generate
        min_val (float): Minimum value for generator
        max_val (float): Maximum value for generator

    Returns:
        list: List of random float values

    Requirement 9: Generator initialization method.
    """
    lst = [random.uniform(min_val, max_val) for _ in range(size)]
    print(f"\nGenerated list ({size} elements, range [{min_val}, {max_val}]):")
    print(f"  {lst}")
    return lst
