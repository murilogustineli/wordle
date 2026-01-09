# GEMINI.md

This file provides a comprehensive overview of the `wordle` project, to be used as instructional context for future interactions.

## Project Overview

This is a Python project designed to help play and solve the popular game Wordle. The project includes a command-line interface (CLI) to play the game, a solver based on information theory (entropy), and tools to track scores and analyze word patterns.

**Main technologies:**

*   **Programming Language:** Python
*   **Package Manager:** `uv`
*   **Main Libraries:** `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `torch`
*   **Code Style:** `ruff` for formatting and linting, and `prettier` for other file types.

**Project Structure:**

*   `wordle/`: The main Python package.
    *   `utils.py`: Contains the core logic for the Wordle game, including the `Wordle` class which manages game state, word filtering, and entropy calculations.
    *   `plot_scores.py`: A script to generate a plot of the Wordle scores.
    *   `wordle-answers.txt`: A list of possible Wordle answers.
    *   `wordle-possible-words.txt`: A list of all possible words that can be guessed.
*   `notebooks/`: Jupyter notebooks for data analysis and experimentation.
    *   `wordle_solver.ipynb`: A notebook that likely contains the implementation and exploration of the Wordle solver.
*   `pyproject.toml`: Defines project metadata and dependencies.
*   `README.md`: Provides setup and installation instructions.

## Building and Running

### 1. Install `uv`:

Install `uv` as the package manager for the project. Follow the [`uv` installation](https://docs.astral.sh/uv/getting-started/installation/) instructions for macOS, Linux, and Windows.

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create a virtual environment and install the package:

```bash
# Create and activate a virtual environment
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the wordle package
uv pip install -e .
```

### 3. Running the solver:

The primary entry point for the solver is the `Wordle` class in `wordle/utils.py`. You can use it in a Python script or a Jupyter notebook to get word suggestions.

Example usage:

```python
from wordle.utils import Wordle

# Initialize the Wordle helper
wordle_helper = Wordle()

# Find possible words based on your guesses
wordle_helper.find_words(
    green_letters="a",
    green_letter_positions=[1],
    yellow_letters="e",
    yellow_letter_positions=[3],
    gray_letters="s"
)

# Get the best words to play next
wordle_helper.choose_word_to_play()
```

## Development Conventions

*   **Linting and Formatting:** The project uses `ruff` and `prettier` to enforce a consistent code style. Before committing any changes, please run the pre-commit hooks.
*   **Pre-commit Hooks:** Install the pre-commit hooks to automatically format and lint your code before committing.

    ```bash
    pre-commit install
    ```
*   **Dependencies:** All dependencies are managed in `pyproject.toml`.
