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

## [wordle_solver.ipynb](wordle_solver.ipynb) and the `Solver` class

This notebook is how the game is played day to day. It uses the `Solver` class from `wordle/solver.py` to suggest the next word and the `ScoreBoard` class from `wordle/scores.py` to record who won.

### How the `Solver` works

1.  **Initialization**:

- Creating a `Solver` loads the two bundled word lists from `wordle/data`: the possible answers and every allowed guess.

2.  **Filtering Words**:

- `find_words()` filters a word list by the green, yellow, and gray letters and their 1-indexed positions.
- The result is stored on the `words` attribute. Gray letters that also appear as green or yellow are ignored, because Wordle marks the surplus copies of a repeated letter gray.

3.  **Calculating Entropy and Choosing the Next Word**:
    - `choose_word_to_play()` is the main entry point. It returns a DataFrame of guesses ranked best first.
    - It calls `compute_entropy_words()`, which considers every allowed guess (or only the remaining candidates once few enough remain) and ranks them by entropy.
    - For each potential guess, `simulate_feedback_pattern()` works out the feedback every remaining candidate would produce, `calculate_probabilities()` turns those patterns into a distribution, and `compute_entropy()` scores it.
    - The entropy is multiplied by a letter-frequency score so that, among equally informative guesses, the one built from common letters wins.

### Example Usage

```python
from wordle import ScoreBoard, Solver

solver = Solver()
solver.find_words(
    green_letters="a",
    green_letter_positions=[1],
    yellow_letters="e",
    yellow_letter_positions=[3],
    gray_letters="s",
)
solver.choose_word_to_play()

board = ScoreBoard()
board.update()  # who won today?
print(board.commit_message(word=solver.answer))
```
