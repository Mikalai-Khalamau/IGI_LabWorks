import math
from utils import get_float_input

# Constants
MAX_ITERATIONS = 500


# Helper functions
def calculate_term(x, n):
    """
    Calculate the n-th term of the Taylor series for ln(1+x).
    """
    return ((-1) ** (n - 1)) * (x**n) / n


def print_results(x, n, fx, mfx, eps):
    """
    Print the calculation results in formatted view.
    """
    print("Results")
    print(f"x: {x}")
    print(f"n (iterations): {n}")
    print(f"F(x) (Series): {fx:.10f}")
    print(f"Math F(x): {mfx:.10f}")
    print(f"eps: {eps}")
    print(f"Error: {abs(fx - mfx):.10f}")


def task_1():
    """
    Main function for Task 1.
    Computes ln(1+x) using Taylor series expansion and compares
    the result with math.log() function.
    """
    # Safe input with validation
    x = get_float_input("Please, input x (recommended |x| < 1): ")
    eps = get_float_input("Please, input epsilon (accuracy): ")

    # Calculate using math module (reference value)
    try:
        mfx = math.log(1 + x)
    except ValueError:
        print("\nError: Cannot calculate log(1+x) for this x value")
        return

    # Calculate using series expansion
    fx = 0.0
    n = 1
    term = calculate_term(x, n)

    while abs(term) > eps and n < MAX_ITERATIONS:
        fx += term
        n += 1
        term = calculate_term(x, n)

    # Check if max iterations reached
    if n >= MAX_ITERATIONS:
        print(f"\nMaximum iterations ({MAX_ITERATIONS}) reached")
        print("Required accuracy may not be achieved.")

    # Print results
    print_results(x, n, fx, mfx, eps)
