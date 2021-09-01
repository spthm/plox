import argparse

from plox.lox import Lox


def main() -> None:
    parser = argparse.ArgumentParser(
        "plox", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("script", metavar="FILE", nargs="?", help="Lox script to run")

    args = parser.parse_args()

    lox = Lox()
    if args.script is None:
        lox.run_prompt()
        return
