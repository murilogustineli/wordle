# Wordle

A Wordle solver based on information theory (entropy) with score tracking between players.

![wordle-banner](/images/wordle.jpg)

## Quickstart

### 1. Install `uv`

Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) as the package manager for the project.

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install the project

`uv sync` creates `.venv`, installs the `wordle` package in editable mode, and installs the development tools (Jupyter, matplotlib, pytest, ruff, pre-commit) from the `dev` dependency group. It pins everything to `uv.lock`.

```bash
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install pre-commit hooks

```bash
pre-commit install
```

## Usage

The recommended way to use the solver is through the Jupyter notebook:

```bash
jupyter lab
```

Open [`notebooks/wordle_solver.ipynb`](notebooks/wordle_solver.ipynb) and fill in the variables under the `### Play Wordle` heading with the feedback from your guesses:

- **green_letters** / **green_positions**: correct letters in the correct position (1-indexed)
- **yellow_letters** / **yellow_positions**: correct letters in the wrong position (1-indexed)
- **gray_letters**: letters marked absent

Run the cells to get word suggestions ranked by entropy and letter frequency. Start with `answer_word_list=True` to search the smaller list of possible answers, and switch to `False` to search every allowed guess if the answer is not in it.

### Python API

```python
from wordle import Solver

solver = Solver()
words = solver.find_words(
    green_letters="lien",
    green_letter_positions=[1, 2, 4, 5],
    yellow_letters="en",
    yellow_letter_positions=[5, 3],
    gray_letters="tarykm",
    answer_word_list=False,
)
solver.choose_word_to_play()  # DataFrame of guesses, best first
solver.answer  # "liven" once exactly one candidate remains
```

### Score tracking

Scores live in [`data/scores.csv`](data/scores.csv). The players are the rows of that file, so adding or renaming a player is a data change only.

```python
from wordle import ScoreBoard

board = ScoreBoard()
board.load()  # current scores as a DataFrame
board.update()  # prompts for the winner (M/B/D) and adds a game
board.set_scores(Murilo=477, Barbara=215, Draw=473)
board.commit_message(word=solver.answer)  # git commit -m "updated wordle 543-250-541, word=LIVEN"
```

The same is available from the command line:

```bash
wordle --score   # print the table
wordle --update  # record today's result
wordle --plot    # save images/wordle_scores.png
```

## Project layout

```
wordle/                    the installable package
  solver.py                Solver: word filtering and entropy ranking
  scores.py                ScoreBoard: score sheet and plotting
  cli.py                   `wordle` console script
  data/answers.txt         words that can be the daily answer
  data/possible_words.txt  every word Wordle accepts as a guess (the bigger list)
data/scores.csv            score sheet, committed after every game
notebooks/                 wordle_solver.ipynb and an entropy walkthrough
tests/                     pytest suite
```

## Development

```bash
pytest                        # run the tests
ruff check . && ruff format . # lint and format
```

`ruff` handles Python (including notebooks) and `prettier` handles everything else. The pre-commit hooks run both automatically.
