# Notebooks for Wordle Analysis

This directory contains Jupyter notebooks used for developing and analyzing the Wordle solver.

## [info_entropy.ipynb](info_entropy.ipynb)

This notebook explores the concept of **information entropy** and its application to Wordle.

### Understanding Information Entropy

**Information entropy**, introduced by Claude Shannon, _is a measure of the uncertainty or randomness in a set of possible outcomes_. In the context of Wordle, entropy quantifies the expected information you would gain from making a particular guess, based on how it partitions the remaining possible words.

In Wordle, each guess provides feedback that narrows down the list of possible answers. By choosing a word that maximizes the expected information gain (entropy), you can eliminate the largest number of potential words, leading you closer to the solution more efficiently.

**Key Concepts:**

- **Probability Distribution:** The likelihood of each possible outcome.
- **Expected Information Gain:** The average amount of information you expect to gain from a guess.

### Applying Entropy to Wordle

**How to Calculate Entropy for a Guess**

1.  **Possible Outcomes:** For each guess, consider all possible feedback patterns (e.g., positions of green, yellow, and gray letters).

2.  **Partitioning the Word List:** Each feedback pattern partitions the remaining possible words into subsets. Words that would produce the same feedback form a group.

3.  **Calculating Probabilities:** For each feedback pattern, calculate the probability that it will occur, based on the current list of possible answers.

4.  **Entropy Formula:**

$$
\large
\text { Entropy }=-\sum_i p_i \log _2 p_i
$$

where $\large p_i$ is the probability of the $\large i$-th feedback pattern.

## [wordle_solver.ipynb](wordle_solver.ipynb) and the `Wordle` Class

This notebook demonstrates how to use the `Wordle` class from the `wordle.utils` module to get suggestions for the next best word to play in Wordle.

### How the `Wordle` package works

The core of the solver is the `Wordle` class in `wordle/utils.py`. Here's a breakdown of how it works:

1.  **Initialization**:

- When you create an instance of the `Wordle` class, it loads the lists of possible Wordle answers and all allowed guess words.

2.  **Filtering Words**:

- The `find_words()` method is used to filter the list of possible answers based on your guesses. You provide the green, yellow, and gray letters and their positions.
- This method narrows down the `words` attribute of the `Wordle` instance.

3.  **Calculating Entropy and Choosing the Next Word**:
    - The `choose_word_to_play()` method is the main entry point for getting a word suggestion.
    - It calls `compute_entropy_words()` which iterates through all possible guess words to find the one with the highest entropy.
    - For each potential guess, it simulates the feedback pattern for all remaining possible answers (`simulate_feedback_pattern()`).
    - It then calculates the probability of each feedback pattern (`calculate_probabilities()`).
    - Using these probabilities, it computes the entropy for the guess word (`compute_entropy()`).
    - `choose_word_to_play()` also considers letter frequency to break ties and score words. It calculates a combined score based on entropy and letter frequency to suggest the best word to play next.

### Example Usage

```python
from wordle.utils import Wordle

# Initialize the Wordle helper
wordle_helper = Wordle()

# Find possible words based on your guesses
wordle_helper.find_words(
    green_letters="a",
    green_letter_positions=[1],
    yellow_letters="e",
    yellow_letter_positions=[3],
    gray_letters="s"
)

# Get the best words to play next
wordle_helper.choose_word_to_play()
```
