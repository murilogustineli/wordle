import os

import numpy as np
import pandas as pd


class Wordle:
    def __init__(
        self,
    ):
        self.words = None
        self.project_root = self.get_project_root()
        self.wordle_ranking = os.path.join(
            self.project_root, "wordle", "wordle_ranking.csv"
        )
        self.wordle_answers_path = os.path.join(
            self.project_root, "wordle", "wordle-answers.txt"
        )
        self.wordle_possible_path = os.path.join(
            self.project_root, "wordle", "wordle-possible-words.txt"
        )

    # get the directory of the current file
    def get_project_root(self):
        curr_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(curr_file_dir, os.pardir))
        return project_root

    # Function to load words text file and return a list of words
    @staticmethod
    def load_words(file_path: str) -> list:
        with open(file_path, "r") as file:
            content = file.read()
            words = content.split("\n")
        if len(words[-1]) == 0:  # remove empty word after last word from
            words.pop()
        return words

    # Function to find words in list of possible words in Wordle
    def find_words(
        self,
        green_letters: str,
        green_letter_positions: list,
        yellow_letters: str,
        yellow_letter_positions: list,
        bad_letters: str,
        answer_word_list: bool = True,
    ) -> list:
        """
        Function that takes the green and yellow letters and their positions and returns a list of possible words
        Args:
            :param green_letters: string of green letters
            :param green_letter_positions: list of green letter positions
            :param yellow_letters: string of yellow letters
            :param yellow_letter_positions: list of yellow letter positions
            :param bad_letters: string of bad letters
            :param answer_word_list: boolean to check if the possible words are the answer words
        Returns:
            :return: list of possible words
        """
        # List of possible words
        possible_words = []
        final_words = []

        # Subtract 1 from every value in green and yellow letter positions
        green_letter_positions = np.array(green_letter_positions) - 1
        yellow_letter_positions = np.array(yellow_letter_positions) - 1

        # Make all letters lower case
        green_letters = green_letters.lower()
        yellow_letters = yellow_letters.lower()
        bad_letters = bad_letters.lower()

        # Get list of words
        if answer_word_list:
            words = self.load_words(file_path=self.wordle_answers_path)
        else:
            words = self.load_words(file_path=self.wordle_possible_path)

        # Convert letters to sets for efficient checking
        set_yellow_letters = set(yellow_letters)
        set_bad_letters = set(bad_letters)

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
                    word[pos] == green_letters[i]
                    for i, pos in enumerate(green_letter_positions)
                ):
                    final_words.append(word)
        else:
            final_words = possible_words
        self.words = final_words
        return final_words

    # Function that returns most repetitive letters
    def repetitive_letters(self, wordle_list) -> pd.DataFrame:
        """
        Takes the possible word list from find_words() function and returns a DataFrame of the most repetitive letters
        :param wordle_list: list of possible words from find_words() function
        :return: dictionary of letters in word_list and their count
        """
        letter_dic = {}
        for word in wordle_list:
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
        """

        df = pd.read_csv(self.wordle_ranking, index_col=False)
        df["Games_Won"] = df["Games_Won"].astype(int)
        return df

    # Function to compute the score
    def score(
        self,
    ) -> pd.DataFrame:
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
        df.to_csv(self.wordle_ranking, index=False)
        return df

    # Function that resets the score
    def reset_score(self) -> pd.DataFrame:
        """
        Function that resets the score.
        Enter 'y' to reset the score
        Enter 'n' to NOT reset the score
        """
        reset = input("Would you like to reset the ranking? [y/n]")
        if reset == "y":
            data = [["Murilo", 0], ["Barbara", 0], ["Draw", 0]]
            df = pd.DataFrame(data, columns=["Names", "Games_Won"])
            df.to_csv(self.wordle_ranking, index=False)
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
        df.to_csv(self.wordle_ranking, index=False)
        return df

    # Function that returns a commit message with updated scores
    def get_commit_message(self):
        score_df = self.load_data()
        score = score_df["Games_Won"].tolist()
        score_formatted = f"{score[0]}-{score[1]}-{score[2]}"
        commit_msg = f'git commit -m "updated wordle {score_formatted}"'
        return commit_msg
