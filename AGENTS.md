# AGENTS.md

Guidance for AI coding agents working in this repository. `CLAUDE.md` and
`GEMINI.md` are symlinks to this file.

## Project Overview

A Python Wordle solver that uses information theory (entropy) to suggest optimal
word guesses, plus score tracking between two players who play every day.

## Commands

```bash
# Setup (creates .venv, installs the package editable plus the dev group)
uv sync
source .venv/bin/activate
pre-commit install

# Run Jupyter (primary interface)
jupyter lab

# Tests and lint
pytest
ruff check . && ruff format .

# CLI
wordle --score    # show scores
wordle --update   # record today's result
wordle --plot     # save images/wordle_scores.png
```

## Layout

```
wordle/                    the installable package
  solver.py                Solver: word filtering + entropy ranking
  scores.py                ScoreBoard: read/update data/scores.csv, plot
  cli.py                   `wordle` console script
  data/answers.txt         words that can be the daily answer (smaller list)
  data/possible_words.txt  every word Wordle accepts as a guess (the bigger list)
data/scores.csv            mutable score sheet, committed after every game
images/                    banner and generated score chart
notebooks/                 wordle_solver.ipynb is how the game is actually played
tests/                     pytest suite
```

Word lists are package data, loaded with `importlib.resources`, so they work
from an installed wheel. The score sheet is user state and deliberately lives
outside the package; its git history doubles as the score history.

## Architecture

- `Solver.find_words()` filters words by green/yellow/gray feedback. Gray
  letters that also appear as green or yellow are ignored, because Wordle marks
  surplus copies of a repeated letter gray.
- `Solver.simulate_feedback_pattern()` -> `calculate_probabilities()` ->
  `compute_entropy()` rank guesses by information gain.
- `Solver.choose_word_to_play()` combines entropy with letter frequency and
  returns a DataFrame, best guess first. Below `word_threshold` remaining
  candidates it only considers those candidates so the guess can be the answer.
- `ScoreBoard` derives the players from the rows of the CSV. The `update()`
  prompt accepts the first letter of each name (`M`, `B`, `D` today).

## Conventions

- Library code returns values; printing and `input()` belong in the notebook
  and `cli.py`. The only exceptions are the interactive `ScoreBoard.update()`
  and `reset()` prompts.
- Runtime dependencies are numpy, pandas and tabulate only. Everything else
  (Jupyter, matplotlib, pytest, ruff, pre-commit) is in the `dev` dependency
  group in `pyproject.toml`. There is no `requirements.txt`.
- `ruff` formats and lints Python (including notebooks); `prettier` formats
  everything else. Pre-commit hooks enforce both.
- Daily commits follow `updated wordle <M>-<B>-<D>, word=<ANSWER>`, produced by
  `ScoreBoard.commit_message()`.
