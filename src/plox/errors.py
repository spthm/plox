import sys

from plox.tokens import Token


class ParserError(Exception):
    def __init__(self, message: str, token: Token) -> None:
        super().__init__(message, token)
        self.message = message
        self.token = token


def _report(lno: int, where: str, message: str) -> None:
    if where:
        where = f" {where.lstrip()}"
    print(f"[line {lno}] Error{where}: {message}", file=sys.stderr)
