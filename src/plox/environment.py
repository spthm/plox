from __future__ import annotations

from typing import Optional

from plox.errors import ExecutionError
from plox.tokens import Token


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None) -> None:
        self._enclosing: Optional[Environment] = enclosing
        self._values: dict[str, object] = {}

    @classmethod
    def from_globals(cls, dct: dict[str, object]) -> Environment:
        self = cls()
        self._values = dict(dct.items())
        return self

    def define(self, name: Token, value: object) -> None:
        self._values[name.lexeme] = value

    def __getitem__(self, name: Token) -> object:
        try:
            return self._values[name.lexeme]
        except KeyError:
            pass

        if self._enclosing is not None:
            return self._enclosing[name]

        raise ExecutionError(f"Undefined variable '{name.lexeme}'.", name)

    def __setitem__(self, name: Token, value: object) -> None:
        if name.lexeme in self._values:
            self._values[name.lexeme] = value
            return

        if self._enclosing is not None:
            self._enclosing[name] = value
            return

        raise ExecutionError(f"Undefined variable '{name.lexeme}'.", name)
