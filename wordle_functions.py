"""
Wordle Functions
"""


# Import libraries
import numpy as np
import pandas as pd


# Function to load words text file and return a list of words
def load_words(file_path):
	my_file = open(file_path, "r")
	content = my_file.read()
	words = content.split('\n')
	return words


# Function to find words in list of possible words in Wordle
def find_words(words, good_letters, yellow_letters, bad_letters, letter_positions):
	# List of possible words
	possible_words = []
	# Subtract 1 from every value in letter_positions 
	letter_positions = np.array(letter_positions)-1
	
	# Iterate over each word in Wordle
	for w in range(len(words)):
		# Check words that dont' have bad_letters and have yellow_letters
		if not any((l in words[w]) for l in bad_letters) and all((l in words[w]) for l in yellow_letters):
			# Check position of letters in word if it has green letters
			if (len(good_letters) and len(letter_positions)) > 0:
				# Go through each letter and check if they're in the right place
				for n in range(len(letter_positions)):
					if str(words[w][letter_positions[n]]) == str(good_letters[n]):
						if n == len(letter_positions)-1:
							possible_words.append(words[w])
					else:
						break
			else:
				possible_words.append(words[w])
						
	# Return list of possible words
	return possible_words


# Main function that returns a list of possible words
def main(good_letters, letter_positions, yellow_letters, bad_letters):
	"""
	Function takes  4 arguments:
	1. good_letters --> string that represents green letters in wordle guess
	2. letter_positions --> list of the positions of the good_letters ranging from 1 to 5
	3. yellow_letters --> string that represents yellow letters in wordle guess
	4. bad_letters --> string that represents gray letters in wordle guess
	"""
	# Load words list
	words = load_words(file_path="wordle-answers-alphabetical.txt")
	
	# Variables
	good_letters = good_letters.lower()
	letter_positions = letter_positions
	yellow_letters = yellow_letters.lower()
	bad_letters = bad_letters.lower()
	
	# Return list of possible words
	print(find_words(words,
					 good_letters=good_letters,
					 yellow_letters=yellow_letters,
					 bad_letters=bad_letters,
					 letter_positions=letter_positions))
	

# Function to load the ranking data
def load_data(file_name='wordle_ranking.csv'):
	"""
	Function that loads the CSV file storing the score for each person
	"""
	df = pd.read_csv(file_name, index_col=False)
	return df


# Function to compute the score
def score():
	"""
	Function that tracks the score for wordle. There are 3 possibilities:
	1. Murilo wins --> 'M'
	2. Barbara wins --> 'B'
	3. Draw; no winners --> 'D'
	"""
	# Load data
	data = load_data(file_name = 'wordle_ranking.csv')
	
	# Filter for Murilo and Barbara rows
	m_df = data[data['Names'] == 'Murilo'].copy()
	b_df = data[data['Names'] == 'Barbara'].copy()
	
	# Select winner
	winner = input("Who won the game? Murilo, Barbara, or Draw? \
		\nEnter 'M' if Murilo won. \
		\nEnter 'B' if Barbara won. \
		\nEnter 'D' if it was a Draw. \
		\nPlease enter [M/B/D]").lower()
	
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
def reset_score():
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
def set_score(m_score, b_score, draw):
	"""
	Function that sets a custom score for both people.
	m_score --> Murilo's score
	b_score --> Barbara's score
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


# Call main function
# if __name__ == '__main__':
#     main()
