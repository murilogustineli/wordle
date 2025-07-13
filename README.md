# Wordle

Python program to play wordle

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
