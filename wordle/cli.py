import argparse

from tabulate import tabulate

from wordle.utils import Wordle


def main():
    parser = argparse.ArgumentParser(description="Wordle solver and score tracker")
    parser.add_argument("--score", action="store_true", help="Display current scores")
    parser.add_argument("--update", action="store_true", help="Update score after a game")
    args = parser.parse_args()

    if args.score:
        wordle = Wordle()
        df = wordle.load_data()
        print(tabulate(df, headers="keys", tablefmt="rounded_grid", showindex=False))
    elif args.update:
        wordle = Wordle()
        df = wordle.update_score()
        print("\nUpdated scores:")
        print(tabulate(df, headers="keys", tablefmt="rounded_grid", showindex=False))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
