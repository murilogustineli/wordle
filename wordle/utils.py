import math
import os
from collections import Counter

import numpy as np
import pandas as pd


class Wordle:
    def __init__(self):
        self.words = None
        self.top_entropy_words = None
        self.LEN_WORDS = None
        self.RANKING_PATH = None
        self.PROJECT_ROOT = self.get_project_root()
        self.ANSWERS_PATH = os.path.join(
            self.PROJECT_ROOT, "wordle", "wordle-answers.txt"
        )
        self.POSSIBLE_WORDS_PATH = os.path.join(
            self.PROJECT_ROOT, "wordle", "wordle-possible-words.txt"
        )
        self.RAKING_PATH = os.path.join(
            self.PROJECT_ROOT, "wordle", "wordle_ranking.csv"
        )

    # get the directory of the current file
    @staticmethod
    def get_project_root():
        curr_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(curr_file_dir, os.pardir))
        return project_root

    # Function to load words text file and return a list of words
    @staticmethod
    def load_words(file_path: str) -> list:
        with open(file_path, "r") as file:
            content = file.read()
            words = content.split("\n")
        if len(words[-1]) == 0:  # remove empty word after last word from the list
            words.pop()
        return words

    # Function to find words in list of possible words in Wordle
    def find_words(
        self,
        green_letters: str,
        green_letter_positions: list,
        yellow_letters: str,
        yellow_letter_positions: list,
        gray_letters: str,
        answer_word_list: bool = True,
    ) -> list:
        """
        Function that takes the green, yellow, ang gray letters and their positions and returns a list of possible words.
        Args:
            :param green_letters: string of green letters
            :param green_letter_positions: list of positions of green letters
            :param yellow_letters: string of yellow letters
            :param yellow_letter_positions: list of positions of yellow letters
            :param gray_letters: string of bad letters
            :param answer_word_list: boolean to check if the possible words are the answer words
        Returns:
            :return final_words: list of possible words
        """
        # Subtract 1 from every value in green and yellow letter positions
        green_letter_positions = np.array(green_letter_positions) - 1
        yellow_letter_positions = np.array(yellow_letter_positions) - 1

        # Make all letters lower case
        green_letters = green_letters.lower()
        yellow_letters = yellow_letters.lower()
        gray_letters = gray_letters.lower()

        # Get list of words
        if answer_word_list:
            words = self.load_words(file_path=self.ANSWERS_PATH)
        else:
            words = self.load_words(file_path=self.POSSIBLE_WORDS_PATH)

        # Convert letters to sets for efficient checking
        set_yellow_letters = set(yellow_letters)
        set_bad_letters = set(gray_letters)

        possible_words = []
        # Iterate over each word
        for word in words:
            # Exclude words with bad letters
            if set_bad_letters & set(word):
                continue

            # Include words with yellow letters, but not at the specified positions
            if set_yellow_letters <= set(word) and all(
                word[pos] != yellow_letters[i]
                for i, pos in enumerate(yellow_letter_positions)
            ):
                possible_words.append(word)

        final_words = []
        # Filter words based on green letter positions
        if green_letters:
            for word in possible_words:
                if all(
                    word[pos] == green_letter
                    for green_letter, pos in zip(green_letters, green_letter_positions)
                ):
                    final_words.append(word)
        else:
            final_words = possible_words
        self.words = final_words
        self.LEN_WORDS = len(self.words)
        print(f"Number of possible words: {self.LEN_WORDS}")
        return final_words

    # function to simulate feedback pattern
    def simulate_feedback_pattern(self, word_played: str) -> dict:
        """
        Method to simulate the feedback pattern for a given word played.
        Handles the cases if a letter appears multiple times in the guess word.
        Args:
            :param word_played: word played by the user
        Returns:
            :return: dictionary with the feedback pattern for each word
        """
        feedback_pattern = {}
        for word in self.words:
            pattern = []
            secret_word_letters = list(word)
            guess_letters = list(word_played)
            # First pass for greens
            for i in range(len(guess_letters)):
                if guess_letters[i] == secret_word_letters[i]:
                    pattern.append("green")
                    secret_word_letters[i] = None  # Mark as used
                    guess_letters[i] = None
                else:
                    pattern.append(None)
            # Second pass for yellows and grays
            for i in range(len(guess_letters)):
                if guess_letters[i] is not None:
                    if guess_letters[i] in secret_word_letters:
                        pattern[i] = "yellow"
                        secret_word_letters[
                            secret_word_letters.index(guess_letters[i])
                        ] = None
                    else:
                        pattern[i] = "gray"
            feedback_pattern[word] = pattern
        return feedback_pattern

    # calculate probabilities of feedback pattern
    def calculate_probabilities(self, feedback_pattern: dict) -> dict:
        """
        Method to calculate the probabilities of each feedback pattern.
        Args:
            :param feedback_pattern: dictionary with the feedback pattern for each word
        Returns:
            :return: dictionary with the probabilities of each feedback pattern
        """
        # count the number of each feedback pattern
        list_counts = Counter(tuple(lst) for lst in feedback_pattern.values())
        # calculate the probabilities of each feedback pattern
        probabilities = {}
        for word, pattern_value in list_counts.items():
            probabilities[word] = pattern_value / self.LEN_WORDS
        return probabilities

    # calculate the entropy of the probabilities
    @staticmethod
    def compute_entropy(probabilities: dict) -> float:
        """
        Method to compute the entropy of the probabilities.
        Args:
            :param probabilities: dictionary with the probabilities of each feedback pattern
        Returns:
            :return: entropy of the probabilities
        """
        entropy = 0
        for prob in probabilities.values():
            entropy += -prob * math.log2(prob)
        return entropy

    # compute entropy for all words
    def compute_entropy_words(
        self,
        word_threshold: int = 10,
        top_k_words: int = 10,
    ) -> None:
        """
        Method to compute the entropy of all possible words.
        Args:
            :param word_threshold: threshold to consider the number of possible words
            :param top_k_words: number of top words to consider
        """
        words_entropy = {}
        potential_words = self.load_words(self.POSSIBLE_WORDS_PATH)
        if self.LEN_WORDS <= word_threshold:  # adjust the threshold as needed
            # Use remaining possible words as potential guesses
            potential_words = self.words
        # compute the entropy for each word
        for guess_word in potential_words:
            feedback_pattern = self.simulate_feedback_pattern(guess_word)
            probabilities = self.calculate_probabilities(feedback_pattern)
            entropy = self.compute_entropy(probabilities)
            words_entropy[guess_word] = entropy
        # Order the words by entropy in descending order
        words_entropy = dict(
            sorted(words_entropy.items(), key=lambda item: item[1], reverse=True)
        )
        # Get top 10 words with the highest entropy
        top_entropy_words = dict(list(words_entropy.items())[:top_k_words])
        self.top_entropy_words = top_entropy_words

    # compute the frequency of each letter in the words
    def compute_letter_frequencies(self) -> Counter:
        """
        Method to compute the frequency of each letter in the words.
        Returns:
            :return: Counter object with the frequency of each letter
        """
        letter_counts = Counter()
        for word in self.words:
            letter_counts.update(
                set(word)
            )  # Use set to avoid counting duplicate letters
        return letter_counts

    # choose the word to play
    def choose_word_to_play(
        self,
        word_threshold: int = 10,
        top_k_words: int = 10,
    ) -> None:
        """
        Method to choose the word to play based on the entropy and frequency of the letters.
        Args:
            :param word_threshold: threshold to consider the number of possible words
            :param top_k_words: number of top words to consider
        """
        # compute the entropy of the words
        self.compute_entropy_words(word_threshold, top_k_words)
        # compute the frequency of each letter in the words
        letter_frequencies = self.compute_letter_frequencies()
        # compute the score of each word
        words_scores = {}
        for word, entropy in self.top_entropy_words.items():
            # calculate the frequency score for the word
            frequency_score = sum(letter_frequencies[char] for char in set(word))
            # combine entropy and frequency score
            combined_score = entropy * frequency_score
            words_scores[word] = combined_score
        # sort words based on the combined score in descending order
        sorted_words = dict(
            sorted(words_scores.items(), key=lambda item: item[1], reverse=True)
        )
        for key, val in sorted_words.items():
            print(key.upper(), round(val, 3))

    # Function that returns most repetitive letters
    def repetitive_letters(self) -> pd.DataFrame:
        """
        Takes the possible word list from find_words() method and returns a DataFrame of the most repetitive letters
        :return df: DataFrame of the most repetitive letters
        """
        letter_dic = {}
        for word in self.words:
            for i in word:
                if i in letter_dic:
                    letter_dic[i] += 1
                else:
                    letter_dic[i] = 1

        # Convert to upper case
        letter_dic = {k.upper(): v for k, v in letter_dic.items()}
        sorted_dic = dict(sorted(letter_dic.items(), key=lambda x: x[1], reverse=True))

        # Convert to Pandas DataFrame
        data = {"Letters": sorted_dic.keys(), "Count": sorted_dic.values()}
        df = pd.DataFrame(data)
        return df

    # Function to load the ranking data
    def load_data(self) -> pd.DataFrame:
        """
        Function that loads the CSV file storing the score for each person
        :return df: DataFrame with the ranking data
        """
        df = pd.read_csv(self.RAKING_PATH, index_col=False)
        df["Games_Won"] = df["Games_Won"].astype(int)
        return df

    # Function to compute the score
    def update_score(self) -> pd.DataFrame:
        """
        Function that tracks the score for wordle. There are 3 possibilities:
        1. Murilo wins --> 'M'
        2. Barbara wins --> 'B'
        3. Draw; no winners --> 'D'
        """
        # Load data
        data = self.load_data()

        # Filter for Murilo, Barbara, and Draw rows
        m_df = data[data["Names"] == "Murilo"].copy()
        b_df = data[data["Names"] == "Barbara"].copy()
        d_df = data[data["Names"] == "Draw"].copy()

        # Select winner
        winner = input(
            "Who won the game? Murilo, Barbara, or Draw? \
            \nEnter 'M' if Murilo won. \
            \nEnter 'B' if Barbara won. \
            \nEnter 'D' if it was a Draw. \
            \nPlease enter [M/B/D]:"
        ).lower()

        # Add points to winner
        if winner == "M".lower():
            m_df["Games_Won"] = m_df["Games_Won"] + 1
        elif winner == "B".lower():
            b_df["Games_Won"] = b_df["Games_Won"] + 1
        elif winner == "D".lower():
            d_df["Games_Won"] = d_df["Games_Won"] + 1

        # Convert into DataFrame
        frames = [m_df, b_df, d_df]
        df = pd.concat(frames)

        # Write DF to CSV
        df.to_csv(self.RAKING_PATH, index=False)
        return df

    # Function that resets the score
    def reset_score(self):
        """
        Function that resets the score.
        Enter 'y' to reset the score
        Enter 'n' to NOT reset the score
        """
        reset = input("Would you like to reset the ranking? [y/n]")
        if reset == "y":
            data = [["Murilo", 0], ["Barbara", 0], ["Draw", 0]]
            df = pd.DataFrame(data, columns=["Names", "Games_Won"])
            df.to_csv(self.RANKING_PATH, index=False)
        else:
            return "Ranking is not reset"
        return df

    # Function that sets a custom score
    def set_score(self, m_score, b_score, draw_score) -> pd.DataFrame:
        """
        Function that sets a custom score for both people.
        m_score --> Murilo's score
        b_score --> Barbara's score
        draw_score --> Draw score
        """
        # Load DataFrame
        data = self.load_data()

        # Filter for Murilo and Barbara rows
        m_df = data[data["Names"] == "Murilo"].copy()
        b_df = data[data["Names"] == "Barbara"].copy()
        d_df = data[data["Names"] == "Draw"].copy()

        # Set new score
        m_df["Games_Won"] = m_score
        b_df["Games_Won"] = b_score
        d_df["Games_Won"] = draw_score

        # Convert into DataFrame
        frames = [m_df, b_df, d_df]
        df = pd.concat(frames)

        # Write DF to CSV
        df.to_csv(self.RANKING_PATH, index=False)
        return df

    # Function that returns a commit message with updated scores
    def get_commit_message(self):
        score_df = self.load_data()
        score = score_df["Games_Won"].tolist()
        score_formatted = f"{score[0]}-{score[1]}-{score[2]}"
        commit_msg = f'git commit -m "updated wordle {score_formatted}"'
        return commit_msg
