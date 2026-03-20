def task_3():
    """
    Main function for Task 3.
    Analyzes input string and counts lowercase letters and digits.
    """
    # Get input string from user
    string = input("Please, input string: ")

    # Initialize counters
    digits = 0
    letters = 0

    # Iterate through each character in string
    for s in string:
        if s.isdigit():
            digits += 1
        elif s.islower():
            letters += 1

    # Display results
    print_results(letters, digits, len(string))


def print_results(letters, digits, total_length):
    """
    Print the analysis results in formatted view.
    """
    print("Results")
    print(f"Total string length: {total_length}")
    print(f"Lowercase letters:   {letters}")
    print(f"Digits:              {digits}")
