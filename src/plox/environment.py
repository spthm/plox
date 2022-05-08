from __future__ import annotations

from typing import Optional

# avoid circular dependencies by specifying the specific modules of ast.
from plox.ast.expressions import Assign, Variable
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

    def __getitem__(self, expr: Variable) -> object:
        try:
            return self._values[expr.name.lexeme]
        except KeyError:
            pass

        if self._enclosing is not None:
            return self._enclosing[expr]

        raise ExecutionError(f"Undefined variable '{expr.name.lexeme}'.", expr.name)

    def __setitem__(self, expr: Assign, value: object) -> None:
        if expr.name.lexeme in self._values:
            self._values[expr.name.lexeme] = value
            return

        if self._enclosing is not None:
            self._enclosing[expr] = value
            return

        raise ExecutionError(f"Undefined variable '{expr.name.lexeme}'.", expr.name)
