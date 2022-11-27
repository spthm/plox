from __future__ import annotations

from typing import Optional

# avoid circular dependencies by specifying the specific modules of ast.
from plox.ast.expressions import Assign, Variable
from plox.ast.resolve import Bindable, Bindings, Scope
from plox.errors import ExecutionError
from plox.tokens import Token


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None) -> None:
        self._enclosing: Optional[Environment] = enclosing
        self._bindings: Bindings = (
            enclosing._bindings if enclosing is not None else Bindings()
        )
        self._locals: dict[str, object] = {}

    def resolve(self, bindings: Bindings) -> None:
        self._bindings |= bindings

    @classmethod
    def as_root(cls, builtins: dict[str, object]) -> Environment:
        self = cls()
        self._locals = dict(builtins.items())
        return self

    def local_scope(self) -> Scope:
        return {k: True for k in self._locals}

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
        try:
            distance = self._bindings[expr]
        except KeyError:
            raise ExecutionError(
                f"Undefined variable '{expr.name.lexeme}'.", expr.name
            ) from None

        return self._ascend(distance)._locals  # pylint: disable=protected-access

    def __getitem__(self, expr: Variable) -> object:
        return self._get_values(expr)[expr.name.lexeme]

    def __setitem__(self, expr: Assign, value: object) -> None:
        values = self._get_values(expr)
        values[expr.name.lexeme] = value

    def __str__(self) -> str:
        return f"{self._locals}"
