"""
Wordle Functions
"""

# Import libraries
import numpy as np
import pandas as pd


class Wordle:
    def __init__(
        self,
    ):
        self.words = None
        self.wordle_ranking = "/Users/mgustine/github/wordle/wordle/wordle_ranking.csv"
        self.wordle_answers_path = (
            "/Users/mgustine/github/wordle/wordle/wordle-answers.txt"
        )
        self.wordle_possible_path = (
            "/Users/mgustine/github/wordle/wordle/wordle-possible-words.txt"
        )

    # Function to load words text file and return a list of words
    @staticmethod
    def load_words(file_path: str) -> list:
        my_file = open(file_path, "r")
        content = my_file.read()
        words = content.split("\n")
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
        df.to_csv(self.wordle_rankingk, index=False)
        return df
