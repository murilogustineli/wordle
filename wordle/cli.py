import argparse

from tabulate import tabulate

from wordle.scores import ScoreBoard


def _show(df) -> None:
    print(tabulate(df, headers="keys", tablefmt="rounded_grid", showindex=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Wordle solver and score tracker")
    parser.add_argument("--score", action="store_true", help="Display current scores")
    parser.add_argument(
        "--update", action="store_true", help="Update score after a game"
    )
    parser.add_argument(
        "--plot", action="store_true", help="Save a bar chart of scores"
    )
    args = parser.parse_args()

    board = ScoreBoard()
    if args.score:
        _show(board.load())
    elif args.update:
        df = board.update()
        print("\nUpdated scores:")
        _show(df)
    elif args.plot:
        print(f"Score plot saved to {board.plot()}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
