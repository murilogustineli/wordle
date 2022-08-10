"""
Wordle Functions
"""

# Import libraries
import numpy as np
import pandas as pd


# Function to load words text file and return a list of words
def load_words(file_path) -> list:
    my_file = open(file_path, "r")
    content = my_file.read()
    words = content.split('\n')
    return words


# Function to find words in list of possible words in Wordle
def find_words(words: list,
               green_letters: str,
               green_letter_positions: list,
               yellow_letters: str,
               yellow_letter_positions: list,
               bad_letters: str) -> list:
    # List of possible words
    possible_words = []
    final_words = []

    # Subtract 1 from every value in green and yellow letter positions
    green_letter_positions = np.array(green_letter_positions) - 1
    yellow_letter_positions = np.array(yellow_letter_positions) - 1

    # Iterate over each word in Wordle list
    for w in range(len(words)):
        # Check words that do not have bad_letters and have yellow_letters
        if not any(let in words[w] for let in bad_letters) and all(let in words[w] for let in yellow_letters):
            # Check position of yellow letters in word
            if len(yellow_letters) > 0 and len(yellow_letter_positions) == 0:
                possible_words.append(words[w])

            elif len(yellow_letter_positions) > 0:
                counter = 0
                for i in range(len(yellow_letter_positions)):
                    if str(words[w][yellow_letter_positions[i]]) != str(yellow_letters[i]):
                        counter += 1
                        if counter == len(yellow_letter_positions):
                            possible_words.append(words[w])
            else:
                possible_words.append(words[w])

    # Check position of letters in word if it has green letters
    if (len(green_letters) and len(green_letter_positions)) > 0:
        for i in range(len(possible_words)):
            # Go through each letter and check if they're in the right place
            for n in range(len(green_letter_positions)):
                if str(possible_words[i][green_letter_positions[n]]) == str(green_letters[n]):
                    # final_words.append(possible_words[i])
                    if n == len(green_letter_positions) - 1:
                        final_words.append(possible_words[i])
                else:
                    break
    else:
        final_words = possible_words

    # Return list of possible words
    return final_words


# Main function that returns a list of possible words
def main(green_letters: str,
         green_letter_positions: list,
         yellow_letters: str,
         yellow_letter_positions: list,
         bad_letters: str) -> print():
    """
    Function takes  5 arguments:
    1. green_letters --> string that represents green letters in wordle guess
    2. green_letter_positions --> list of the positions of the green_letters ranging from 1 to 5
    3. yellow_letters --> string that represents yellow letters in wordle guess
    4. yellow_letter_positions --> list of the positions of the yellow_letters ranging from 1 to 5
    5. bad_letters --> string that represents gray letters in wordle guess
    """
    # Load words list
    words = load_words(file_path="wordle-answers-alphabetical.txt")

    # Variables
    green_letters = green_letters.lower()
    green_letter_positions = green_letter_positions
    yellow_letters = yellow_letters.lower()
    yellow_letter_positions = yellow_letter_positions
    bad_letters = bad_letters.lower()

    # Print list of possible words
    return print(find_words(words,
                            green_letters=green_letters,
                            yellow_letters=yellow_letters,
                            bad_letters=bad_letters,
                            green_letter_positions=green_letter_positions,
                            yellow_letter_positions=yellow_letter_positions))


# Function to load the ranking data
def load_data(file_name='wordle_ranking.csv') -> pd.DataFrame:
    """
    Function that loads the CSV file storing the score for each person
    """
    df = pd.read_csv(file_name, index_col=False)
    return df


# Function to compute the score
def score() -> pd.DataFrame:
    """
    Function that tracks the score for wordle. There are 3 possibilities:
    1. Murilo wins --> 'M'
    2. Barbara wins --> 'B'
    3. Draw; no winners --> 'D'
    """
    # Load data
    data = load_data(file_name='wordle_ranking.csv')

    # Filter for Murilo and Barbara rows
    m_df = data[data['Names'] == 'Murilo'].copy()
    b_df = data[data['Names'] == 'Barbara'].copy()

    # Select winner
    winner = input("Who won the game? Murilo, Barbara, or Draw? \
    \nEnter 'M' if Murilo won. \
    \nEnter 'B' if Barbara won. \
    \nEnter 'D' if it was a Draw. \
    \nPlease enter [M/B/D]:").lower()

    # Add points to winner
    if winner == 'M'.lower():
        m_df['Games_Won'] = m_df['Games_Won'] + 1
    elif winner == 'B'.lower():
        b_df['Games_Won'] = b_df['Games_Won'] + 1
    elif winner == 'D'.lower():
        b_df['Draw'] = b_df['Draw'] + 1
        m_df['Draw'] = m_df['Draw'] + 1

    # Convert into DataFrame
    frames = [m_df, b_df]
    df = pd.concat(frames)

    # Write DF to CSV
    df.to_csv('wordle_ranking.csv', index=False)

    return df


# Function that resets the score
def reset_score() -> (str, pd.DataFrame):
    """
    Function that resets the score.
    Enter 'y' to reset the score
    Enter 'n' to not reset the score
    """
    reset = input('Would you like to reset the ranking? [y/n]')
    if reset == 'y':
        data = [['Murilo', 0, 0], ['Barbara', 0, 0]]
        df = pd.DataFrame(data, columns=['Names', 'Games_Won', 'Draw'])
        df.to_csv('wordle_ranking.csv', index=False)
    else:
        return 'Ranking is not reset'

    return df


# Function that sets a custom score
def set_score(m_score, b_score, draw) -> pd.DataFrame:
    """
    Function that sets a custom score for both people.
    m_score --> Murilo's score
    b_score --> Barbara's score
    draw --> Draw
    """
    # Load DataFrame
    data = load_data(file_name='wordle_ranking.csv')

    # Set draw score
    data['Draw'] = draw

    # Filter for Murilo and Barbara rows
    m_df = data[data['Names'] == 'Murilo'].copy()
    b_df = data[data['Names'] == 'Barbara'].copy()

    # Set new score
    m_df['Games_Won'] = m_score
    b_df['Games_Won'] = b_score

    # Convert into DataFrame
    frames = [m_df, b_df]
    df = pd.concat(frames)

    # Write DF to CSV
    df.to_csv('wordle_ranking.csv', index=False)

    return df


# # Call main function
# if __name__ == '__main__':
#     # Main function that returns a list of possible words
#     green_letter = 'CRA'
#     green_positions = [1, 2, 3]
#     yellow_letter = ''
#     yellow_positions = []
#     bad_letter = 'NESTIK'

#     # Main function that returns a list of possible words
#     main(green_letter, green_positions, yellow_letter, yellow_positions, bad_letter)
