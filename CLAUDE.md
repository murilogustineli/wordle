# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python Wordle solver that uses information theory (entropy) to suggest optimal word guesses. Includes score tracking between players.

## Commands

```bash
# Setup
uv venv .venv && source .venv/bin/activate
uv pip install -e .
pre-commit install

# Run Jupyter (primary interface)
jupyter lab

# Plot scores
python wordle/plot_scores.py
```

## Architecture

The core logic is in the `Wordle` class (`wordle/utils.py`):

1. **Word filtering**: `find_words()` filters words based on green/yellow/gray letter constraints
2. **Entropy calculation**: `simulate_feedback_pattern()` → `calculate_probabilities()` → `compute_entropy()` ranks words by information gain
3. **Word recommendation**: `choose_word_to_play()` combines entropy with letter frequency to suggest optimal guesses
4. **Score tracking**: `load_data()`, `update_score()`, `set_score()` manage player scores in `wordle/wordle_ranking.csv`

Word lists:

- `wordle/wordle-answers.txt` - possible answer words
- `wordle/wordle-possible-words.txt` - all valid guess words

Primary usage is through `notebooks/wordle_solver.ipynb`.

## Code Style

Uses `ruff` for formatting/linting and `prettier` for non-Python files. Pre-commit hooks enforce this automatically.
