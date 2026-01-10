# Wordle

A Wordle solver based on information theory (entropy) with score tracking between players.

![wordle-banner](/images/wordle.jpg)

## Quickstart

Install the `wordle` package in _"editable"_ mode, which means changes to the Python files will be immediately available without needing to reinstall the package.

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

### 3. Install pre-commit hooks for formatting code

```bash
pre-commit install
```

## Usage

The recommended way to use the solver is through the Jupyter notebook:

```bash
jupyter lab
```

Open [`notebooks/wordle_solver.ipynb`](notebooks/wordle_solver.ipynb) and modify the variables under the `### Play Wordle` heading with your game results:

- **green_letters** / **green_letter_positions**: correct letters in correct positions (1-indexed)
- **yellow_letters** / **yellow_letter_positions**: correct letters in wrong positions (1-indexed)
- **gray_letters**: letters not in the word

Run the cells to get word suggestions ranked by entropy and letter frequency.

### Python API

```python
from wordle.utils import Wordle

wordle = Wordle()
wordle.find_words(
    green_letters="",
    green_letter_positions=[],
    yellow_letters="",
    yellow_letter_positions=[],
    gray_letters="",
)
wordle.choose_word_to_play()
```

### Score Tracking

```python
wordle.load_data()           # View current scores
wordle.update_score()        # Record a win (M=Murilo, B=Barbara, D=Draw)
wordle.get_commit_message()  # Get formatted commit message
```

## Development

Uses `ruff` for Python formatting/linting and `prettier` for other file types. Pre-commit hooks enforce this automatically.
