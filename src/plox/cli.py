import argparse


def main():
    parser = argparse.ArgumentParser(
        "plox", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("script", metavar="FILE", nargs="?", help="Lox script to run")

    _ = parser.parse_args()
