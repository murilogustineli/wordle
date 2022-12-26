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
         bad_letters: str) -> list:
    """
    Function takes  5 arguments:
    1. green_letters --> string that represents green letters in wordle guess
    2. green_letter_positions --> list of the positions of the green_letters ranging from 1 to 5
    3. yellow_letters --> string that represents yellow letters in wordle guess
    4. yellow_letter_positions --> list of the positions of the yellow_letters ranging from 1 to 5
    5. bad_letters --> string that represents gray letters in wordle guess
    """
    # Load words list
    words_list = load_words(file_path="wordle-answers-alphabetical.txt")

    # Variables
    green_letters = green_letters.lower()
    green_letter_positions = green_letter_positions
    yellow_letters = yellow_letters.lower()
    yellow_letter_positions = yellow_letter_positions
    bad_letters = bad_letters.lower()

    # Print list of possible words
    return find_words(words_list,
                      green_letters=green_letters,
                      yellow_letters=yellow_letters,
                      bad_letters=bad_letters,
                      green_letter_positions=green_letter_positions,
                      yellow_letter_positions=yellow_letter_positions)


# Function that returns most repetitive letters
def repetitive_letters(wordle_list) -> pd.DataFrame:
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
    data = {'Letters': sorted_dic.keys(), 'Count': sorted_dic.values()}
    df = pd.DataFrame(data)

    return df


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

    # Filter for Murilo, Barbara, and Draw rows
    m_df = data[data['Names'] == 'Murilo'].copy()
    b_df = data[data['Names'] == 'Barbara'].copy()
    d_df = data[data['Names'] == 'Draw'].copy()

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
        d_df['Games_Won'] = d_df['Games_Won'] + 1

    # Convert into DataFrame
    frames = [m_df, b_df, d_df]
    df = pd.concat(frames)

    # Write DF to CSV
    df.to_csv('wordle_ranking.csv', index=False)

    return df


# Function that resets the score
def reset_score() -> (str, pd.DataFrame):
    """
    Function that resets the score.
    Enter 'y' to reset the score
    Enter 'n' to NOT reset the score
    """
    reset = input('Would you like to reset the ranking? [y/n]')
    if reset == 'y':
        data = [['Murilo', 0], ['Barbara', 0], ['Draw', 0]]
        df = pd.DataFrame(data, columns=['Names', 'Games_Won'])
        df.to_csv('wordle_ranking.csv', index=False)
    else:
        return 'Ranking is not reset'

    return df


# Function that sets a custom score
def set_score(m_score, b_score, draw_score) -> pd.DataFrame:
    """
    Function that sets a custom score for both people.
    m_score --> Murilo's score
    b_score --> Barbara's score
    draw_score --> Draw score
    """
    # Load DataFrame
    data = load_data(file_name='wordle_ranking.csv')

    # Filter for Murilo and Barbara rows
    m_df = data[data['Names'] == 'Murilo'].copy()
    b_df = data[data['Names'] == 'Barbara'].copy()
    d_df = data[data['Names'] == 'Draw'].copy()

    # Set new score
    m_df['Games_Won'] = m_score
    b_df['Games_Won'] = b_score
    d_df['Games_Won'] = draw_score

    # Convert into DataFrame
    frames = [m_df, b_df, d_df]
    df = pd.concat(frames)

    # Write DF to CSV
    df.to_csv('wordle_ranking.csv', index=False)

    return df


# # Call main function
# if __name__ == '__main__':
#     # Main function that returns a list of possible words
#     green_letter = ''
#     green_positions = []
#     yellow_letter = 'ANEL'
#     yellow_positions = [3, 4, 5, 4]
#     bad_letter = 'CRK'

#     # Main function that returns a list of possible words
#     word_list = main(green_letter, green_positions, yellow_letter, yellow_positions, bad_letter)
#     letters_df = repetitive_letters(wordle_list=word_list)
#     print(f"Word list: {word_list}")
#     print(letters_df.to_string(index=False))


# Convert JSON to CSV
import json
import csv

def open_json(file_name: str) -> list:
    # Opening JSON file and loading the data into the variable data
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data

def convert_json_csv(data: list, download=False) -> pd.DataFrame:
    dic = {}
    
    # Loop through list and convert to dictionary
    for row in data:  # iterate every row
        for key in row:
            if type(row[key]) != dict:  # if key is not a dictionary type object
                if key not in dic.keys():  # if key not in dictionary
                    dic[key] = [row[key]]
                else:
                    dic[key].append(row[key])  # add element to dictionary key
            else:
                for ele in row[key]:  # iterate nested dictionary
                    sub_dic = row[key]
                    if ele not in dic.keys():  # if key is not in dictionary
                        dic[ele] = [sub_dic[ele]]
                    else:
                        dic[ele].append(sub_dic[ele])  # add element to dictionary key
    
    # Convert dictionary to pandas DF
    df = pd.DataFrame(dic)
    
    # Download CSV
    if download:
        df.to_csv("output.csv")
    
    return df

# Call functions
data = open_json(file_name="data.json")
df = convert_json_csv(data=data, download=False)
display(df)
