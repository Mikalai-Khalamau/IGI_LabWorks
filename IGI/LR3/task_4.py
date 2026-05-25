from typing import List
import string

# Fixed text from task requirements
TEXT = (
    "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy "
    "and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and "
    "picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
)


def clean_word(word: str) -> str:
    """
    Remove punctuation from word and convert to lowercase.
    """
    # Strip punctuation from both ends of word
    return word.strip(string.punctuation).lower()


def task_4():
    """
    Main function for Task 4.

    Analyzes predefined text string :
    a) Count words and show words with odd number of letters
    b) Find shortest word starting with letter 'i'
    c) Show repetitive words
    """
    # Split text into words
    raw_words = TEXT.split()

    # Clean words (remove punctuation, convert to lowercase)
    words = [clean_word(w) for w in raw_words]

    # Filter out empty strings (from punctuation-only tokens)
    words = [w for w in words if w]

    # Task 4a: Words with odd number of letters
    odd_words = [w for w in words if len(w) % 2 == 1]

    # Task 4b: Shortest word starting with 'i'
    i_words = [w for w in words if w.startswith("i")]
    shortest_i_word = min(i_words, key=len) if i_words else None

    # Task 4c: Repetitive words (appear 2+ times)
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    repetitive_words = [w for w, count in word_counts.items() if count >= 2]

    # Display results
    print_results(len(words), odd_words, shortest_i_word, repetitive_words)


def print_results(
    words_count: int, odd_words: List[str], i_word: str, repetitive_words: List[str]
):
    """
    Print the analysis results in formatted view.
    """
    print("Results")

    # Part a
    print(f"\na) Total words in text: {words_count}")
    print(f"Words with odd length ({len(odd_words)}): {odd_words}")

    # Part b
    print(f"\nb) Shortest word starting with 'i': {i_word}")

    # Part c
    print(f"\nc) Repetitive words ({len(repetitive_words)}): {repetitive_words}")
