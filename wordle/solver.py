"""Entropy-based Wordle solver.

The :class:`Solver` filters candidate words from the feedback of previous
guesses and ranks the next guess by expected information gain (entropy).
"""

import math
from collections import Counter
from importlib import resources

import pandas as pd

WORD_LENGTH = 5


def load_word_list(name: str) -> list[str]:
    """Load a bundled word list from ``wordle/data``.

    Args:
        name: File name inside the package data directory, e.g. ``"answers.txt"``.

    Returns:
        Lower-case words, one per non-empty line.
    """
    text = resources.files("wordle.data").joinpath(name).read_text(encoding="utf-8")
    return [line.strip().lower() for line in text.splitlines() if line.strip()]


class Solver:
    """Suggest Wordle guesses using information entropy.

    Attributes:
        answers: Words that can be the daily answer (the smaller list).
        possible_words: Every word Wordle accepts as a guess (the larger list).
        words: Candidates still consistent with the feedback given to
            :meth:`find_words`. Empty until ``find_words`` has been called.
        top_entropy_words: Mapping of guess -> entropy for the best guesses found
            by the last call to :meth:`compute_entropy_words`.
    """

    def __init__(self) -> None:
        self.answers = load_word_list("answers.txt")
        self.possible_words = load_word_list("possible_words.txt")
        self.words: list[str] = []
        self.top_entropy_words: dict[str, float] = {}

    @property
    def answer(self) -> str | None:
        """The solved word, or ``None`` unless exactly one candidate remains."""
        return self.words[0] if len(self.words) == 1 else None

    # ------------------------------------------------------------------ filtering
    def find_words(
        self,
        green_letters: str,
        green_letter_positions: list[int],
        yellow_letters: str,
        yellow_letter_positions: list[int],
        gray_letters: str,
        answer_word_list: bool = True,
    ) -> list[str]:
        """Return the words consistent with green, yellow and gray feedback.

        Positions are 1-indexed to match how the game board reads. A letter that
        appears in both the gray string and the green or yellow strings is
        treated as known-present: Wordle marks repeated letters gray once the
        answer's copies are used up, so gray is only evidence about that tile,
        never about the letter as a whole.

        Args:
            green_letters: Letters in the correct position.
            green_letter_positions: Position of each green letter, same order.
            yellow_letters: Letters in the word but in the wrong position.
            yellow_letter_positions: Position each yellow letter was guessed at.
            gray_letters: Letters marked absent.
            answer_word_list: Filter the answers list when ``True``, otherwise
                the full possible-words list.

        Returns:
            The remaining candidate words. Also stored on :attr:`words`.
        """
        green_letters = green_letters.lower()
        yellow_letters = yellow_letters.lower()
        gray_letters = gray_letters.lower()

        if len(green_letters) != len(green_letter_positions):
            raise ValueError(
                "green_letters and green_letter_positions differ in length"
            )
        if len(yellow_letters) != len(yellow_letter_positions):
            raise ValueError(
                "yellow_letters and yellow_letter_positions differ in length"
            )

        green = list(zip(green_letters, (p - 1 for p in green_letter_positions)))
        yellow = list(zip(yellow_letters, (p - 1 for p in yellow_letter_positions)))
        required = set(yellow_letters)
        excluded = set(gray_letters) - set(green_letters) - set(yellow_letters)

        source = self.answers if answer_word_list else self.possible_words
        self.words = [
            word
            for word in source
            if not (excluded & set(word))
            and required <= set(word)
            and all(word[pos] != letter for letter, pos in yellow)
            and all(word[pos] == letter for letter, pos in green)
        ]
        return self.words

    # ------------------------------------------------------------------- entropy
    def simulate_feedback_pattern(self, word_played: str) -> dict[str, tuple[str, ...]]:
        """Feedback each remaining candidate would give for ``word_played``.

        Handles repeated letters the way Wordle does: greens are assigned first,
        then each remaining guess letter is yellow only while unmatched copies of
        it remain in the secret word.

        Returns:
            Mapping of candidate word -> pattern of ``"green"``, ``"yellow"`` and
            ``"gray"`` for each position.
        """
        feedback_pattern = {}
        for secret in self.words:
            pattern = [None] * WORD_LENGTH
            secret_letters = list(secret)
            guess_letters = list(word_played)
            for i, (g, s) in enumerate(zip(guess_letters, secret_letters)):
                if g == s:
                    pattern[i] = "green"
                    secret_letters[i] = None
                    guess_letters[i] = None
            for i, g in enumerate(guess_letters):
                if g is None:
                    continue
                if g in secret_letters:
                    pattern[i] = "yellow"
                    secret_letters[secret_letters.index(g)] = None
                else:
                    pattern[i] = "gray"
            feedback_pattern[secret] = tuple(pattern)
        return feedback_pattern

    def calculate_probabilities(self, feedback_pattern: dict) -> dict[tuple, float]:
        """Probability of each distinct feedback pattern across the candidates."""
        counts = Counter(feedback_pattern.values())
        total = len(self.words)
        return {pattern: count / total for pattern, count in counts.items()}

    @staticmethod
    def compute_entropy(probabilities: dict) -> float:
        """Shannon entropy, in bits, of a probability distribution."""
        # `or 0.0` turns the -0.0 of a single certain outcome into a plain 0.0.
        return -sum(p * math.log2(p) for p in probabilities.values()) or 0.0

    def compute_entropy_words(
        self,
        word_threshold: int = 10,
        top_k_words: int = 10,
    ) -> dict[str, float]:
        """Rank potential guesses by the entropy of their feedback.

        Every allowed guess is considered until the candidate list shrinks to
        ``word_threshold`` words or fewer, after which only the remaining
        candidates are considered so the suggestion can also be the answer.

        Returns:
            The ``top_k_words`` guesses with the highest entropy, best first.
            Also stored on :attr:`top_entropy_words`.
        """
        if not self.words:
            raise ValueError("no candidate words; call find_words() first")
        potential_words = (
            self.words if len(self.words) <= word_threshold else self.possible_words
        )
        words_entropy = {}
        for guess in potential_words:
            pattern = self.simulate_feedback_pattern(guess)
            probabilities = self.calculate_probabilities(pattern)
            words_entropy[guess] = self.compute_entropy(probabilities)
        ranked = sorted(words_entropy.items(), key=lambda item: item[1], reverse=True)
        self.top_entropy_words = dict(ranked[:top_k_words])
        return self.top_entropy_words

    def compute_letter_frequencies(self) -> Counter:
        """Number of remaining candidates containing each letter."""
        letter_counts: Counter = Counter()
        for word in self.words:
            letter_counts.update(set(word))
        return letter_counts

    def choose_word_to_play(
        self,
        word_threshold: int = 10,
        top_k_words: int = 10,
    ) -> pd.DataFrame:
        """Rank the best next guesses.

        Combines each guess's entropy with how many candidates share its letters,
        so among equally informative guesses the one made of common letters wins.

        Args:
            word_threshold: Candidate count at or below which only remaining
                candidates are considered as guesses.
            top_k_words: How many guesses to rank.

        Returns:
            DataFrame with ``Word``, ``Entropy`` and ``Score`` columns, best first.
        """
        top_entropy_words = self.compute_entropy_words(word_threshold, top_k_words)
        letter_frequencies = self.compute_letter_frequencies()
        rows = []
        for word, entropy in top_entropy_words.items():
            frequency_score = sum(letter_frequencies[char] for char in set(word))
            rows.append(
                {
                    "Word": word.upper(),
                    "Entropy": round(entropy, 4),
                    "Score": round(entropy * frequency_score, 2),
                }
            )
        df = pd.DataFrame(rows, columns=["Word", "Entropy", "Score"])
        return df.sort_values("Score", ascending=False, ignore_index=True)

    def repetitive_letters(self) -> pd.DataFrame:
        """Count of each letter across the remaining candidates, most common first."""
        counts = Counter(letter for word in self.words for letter in word)
        data = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        return pd.DataFrame(
            [(letter.upper(), count) for letter, count in data],
            columns=["Letters", "Count"],
        )
