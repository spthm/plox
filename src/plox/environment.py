from plox.errors import ExecutionError
from plox.tokens import Token


class Environment:
    def __init__(self) -> None:
        self._values: dict[str, object] = {}

    def __getitem__(self, name: Token) -> object:
        try:
            return self._values[name.lexeme]
        except KeyError:
            raise ExecutionError(f"Undefined variable '{name.lexeme}'.", name) from None

    def __setitem__(self, name: Token, value: object) -> None:
        self._values[name.lexeme] = value
