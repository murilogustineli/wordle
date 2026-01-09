import os
import matplotlib.pyplot as plt
from wordle.utils import Wordle


def plot_scores():
    """
    Plots the scores from wordle_ranking.csv using matplotlib and saves it to wordle_scores.png.
    """
    game = Wordle()
    try:
        df = game.load_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Create the plot
    plt.figure(figsize=(8, 6))

    # Create bars with specific colors if desired, otherwise default
    bars = plt.bar(
        df["Names"], df["Games_Won"], color=["skyblue", "lightcoral", "lightgray"]
    )

    # Add values on top of bars
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

    # Save the plot
    output_path = os.path.join(game.PROJECT_ROOT, "images/wordle_scores.png")
    plt.savefig(output_path)
    print(f"Score plot saved to {output_path}")


if __name__ == "__main__":
    plot_scores()
