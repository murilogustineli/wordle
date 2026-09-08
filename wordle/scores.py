"""Score tracking between players.

Scores live in a CSV with ``Names`` and ``Games_Won`` columns. The players are
whatever rows the file contains, so adding or renaming a player is a data
change, not a code change. A row named ``Draw`` records games nobody won.
"""

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCORES_PATH = REPO_ROOT / "data" / "scores.csv"
DEFAULT_PLOT_PATH = REPO_ROOT / "images" / "wordle_scores.png"
DRAW = "draw"


class ScoreBoard:
    """Read and update the shared score sheet.

    Args:
        path: CSV file holding the scores. Defaults to ``data/scores.csv`` at
            the repository root.
    """

    def __init__(self, path: str | Path = DEFAULT_SCORES_PATH) -> None:
        self.path = Path(path)

    def load(self) -> pd.DataFrame:
        """Current scores as a DataFrame with ``Names`` and ``Games_Won``."""
        df = pd.read_csv(self.path, index_col=False)
        df["Games_Won"] = df["Games_Won"].astype(int)
        return df

    def save(self, df: pd.DataFrame) -> pd.DataFrame:
        """Write ``df`` back to the score sheet and return it."""
        df.to_csv(self.path, index=False)
        return df

    @property
    def names(self) -> list[str]:
        """Player names in file order, including ``Draw`` if present."""
        return self.load()["Names"].tolist()

    @staticmethod
    def _letters(names: list[str]) -> dict[str, str]:
        """Map each name's first letter to the name; letters must be unique."""
        letters = {name[0].upper(): name for name in names}
        if len(letters) != len(names):
            raise ValueError(f"player names must start with distinct letters: {names}")
        return letters

    def _prompt(self, letters: dict[str, str]) -> str:
        names = list(letters.values())
        lines = [f"Who won the game? {', '.join(names[:-1])}, or {names[-1]}?"]
        for letter, name in letters.items():
            outcome = "it was a Draw" if name.lower() == DRAW else f"{name} won"
            lines.append(f"Enter '{letter}' if {outcome}.")
        lines.append(f"Please enter [{'/'.join(letters)}]:")
        return "\n".join(lines)

    def update(self) -> pd.DataFrame:
        """Ask who won and add one game to that row.

        Each player is chosen by the first letter of their name, so with the
        default sheet the prompt accepts ``M``, ``B`` or ``D``. An unrecognised
        answer leaves the scores unchanged.
        """
        df = self.load()
        letters = self._letters(df["Names"].tolist())
        choice = input(self._prompt(letters)).strip().upper()
        if choice in letters:
            df.loc[df["Names"] == letters[choice], "Games_Won"] += 1
        else:
            print(f"'{choice}' is not one of {'/'.join(letters)}; scores unchanged.")
        return self.save(df)

    def set_scores(self, **scores: int) -> pd.DataFrame:
        """Overwrite scores by name, e.g. ``set_scores(Murilo=477, Barbara=215)``.

        Names not mentioned keep their current score.
        """
        df = self.load()
        unknown = set(scores) - set(df["Names"])
        if unknown:
            raise KeyError(f"unknown players {sorted(unknown)}; have {self.names}")
        for name, score in scores.items():
            df.loc[df["Names"] == name, "Games_Won"] = int(score)
        return self.save(df)

    def reset(self, confirm: bool | None = None) -> pd.DataFrame:
        """Set every score to zero.

        Args:
            confirm: Skip the interactive ``[y/n]`` prompt when given.
        """
        if confirm is None:
            confirm = (
                input("Would you like to reset the ranking? [y/n] ").lower() == "y"
            )
        df = self.load()
        if not confirm:
            print("Ranking is not reset")
            return df
        df["Games_Won"] = 0
        return self.save(df)

    def commit_message(self, word: str | None = None) -> str:
        """Git command recording the current scores, e.g. ``543-250-541``.

        Args:
            word: Today's answer, appended as ``word=LIVEN`` when given.
        """
        score = "-".join(str(n) for n in self.load()["Games_Won"])
        suffix = f", word={word.upper()}" if word else ""
        return f'git commit -m "updated wordle {score}{suffix}"'

    def plot(self, output_path: str | Path = DEFAULT_PLOT_PATH) -> Path:
        """Save a bar chart of the scores and return the image path.

        Requires ``matplotlib``, which is a development dependency.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "plotting requires matplotlib: uv sync --group dev"
            ) from exc

        df = self.load()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(8, 6))
        colors = ["skyblue", "lightcoral", "lightgray"][: len(df)]
        bars = plt.bar(df["Names"], df["Games_Won"], color=colors or None)
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height}",
                ha="center",
                va="bottom",
            )
        plt.title("Wordle Scores")
        plt.xlabel("Player")
        plt.ylabel("Games Won")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.savefig(output_path)
        plt.close()
        return output_path
