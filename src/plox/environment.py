from __future__ import annotations

from typing import Optional

# avoid circular dependencies by specifying the specific modules of ast.
from plox.ast.expressions import Assign, Variable
from plox.ast.resolve import Bindable, Bindings
from plox.errors import ExecutionError
from plox.tokens import Token


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None) -> None:
        self._enclosing: Optional[Environment] = enclosing
        self._bindings: Bindings = (
            enclosing._bindings if enclosing is not None else Bindings()
        )
        self._globals: dict[str, object] = (
            enclosing._globals if enclosing is not None else {}
        )
        self._locals: dict[str, object] = {}

    def resolve(self, bindings: Bindings) -> None:
        self._bindings |= bindings

    @classmethod
    def from_globals(cls, dct: dict[str, object]) -> Environment:
        self = cls()
        self._globals = dict(dct.items())
        return self

    def define(self, name: Token, value: object) -> None:
        self._locals[name.lexeme] = value

    def _ascend(self, distance: int) -> Environment:
        env = self
        for _ in range(distance):
            enclosing = env._enclosing  # pylint: disable=protected-access
            assert enclosing is not None
            env = enclosing
        return env

    def _get_values(self, expr: Bindable) -> dict[str, object]:
        if expr in self._bindings:
            distance = self._bindings[expr]
            return self._ascend(distance)._locals  # pylint: disable=protected-access
        return self._globals

    def __getitem__(self, expr: Variable) -> object:
        values = self._get_values(expr)

        try:
            return values[expr.name.lexeme]
        except KeyError:
            raise ExecutionError(
                f"Undefined variable '{expr.name.lexeme}'.", expr.name
            ) from None

    def __setitem__(self, expr: Assign, value: object) -> None:
        values = self._get_values(expr)

        if expr.name.lexeme in values:
            values[expr.name.lexeme] = value
            return

        raise ExecutionError(f"Undefined variable '{expr.name.lexeme}'.", expr.name)
