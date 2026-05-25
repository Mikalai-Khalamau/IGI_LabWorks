"""
List initialization functions (manual input and generator).
"""

import random


def init_list_manual(size):
    """
    Initialize list with user manual input.
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


<<<<<<< HEAD
def number_generator(size, min_val=-100, max_val=100):
    """
    Generator function with yield.
    """
    for _ in range(size):
        yield random.uniform(min_val, max_val)


def init_list_generator(size, min_val=-100, max_val=100):
    """
    Initialize list using the generator function.
    """
    gen = number_generator(size, min_val, max_val)
    lst = list(gen)

    print(f"\nGenerated list ({size} elements):")