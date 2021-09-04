import sys

from plox.tokens import Token


class ScannerError(Exception):
    # pylint: disable=super-init-not-called
    def __init__(self, message: str) -> None:
        self.message = message


class ParserError(Exception):
    # pylint: disable=super-init-not-called
    def __init__(self, message: str, token: Token) -> None:
        self.message = message
        self.token = token


class ExecutionError(Exception):
    # pylint: disable=super-init-not-called
    def __init__(self, message: str, token: Token) -> None:
        self.message = message
        self.token = token


def _report(lno: int, where: str, message: str) -> None:
    if where:
        where = f" {where.lstrip()}"
    print(f"[line {lno}] Error{where}: {message}", file=sys.stderr)
