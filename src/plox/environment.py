from __future__ import annotations

from typing import Optional, Union

# avoid circular dependencies by specifying the specific modules of ast.
from plox.ast.expressions import Assign, Variable
from plox.ast.resolve import Bindable, Bindings, Scope
from plox.ast.statements import Function, Var


class Environment:
    def __init__(self, enclosing: Optional[Environment] = None) -> None:
        self._enclosing: Optional[Environment] = enclosing
        # It is safe for all environments to share the same bindings because,
        #   1. We only ever call .resolve() on the root Environment; the bindings are
        #      never updated through a different Environment.
        #   2. We OR update bindings in .resolve(), so previously-resolved bindings
        #      (e.g., in a function closure) will not be erased by later resolves.
        #   3. Binding keys are tokens, which are unique across their name and position
        #      in the source code, so we cannot overwrite a binding.
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

    def define(self, stmt: Union[Function, Var], value: object) -> None:
        self._locals[stmt.name.lexeme] = value

    def _ascend(self, distance: int) -> Environment:
        env = self
        for _ in range(distance):
            enclosing = env._enclosing  # pylint: disable=protected-access
            assert enclosing is not None
            env = enclosing
        return env

    def _get_values(self, expr: Bindable) -> dict[str, object]:
        assert expr in self._bindings, f"_get_values() on unresolved expr {expr}"
        distance = self._bindings[expr]
        return self._ascend(distance)._locals  # pylint: disable=protected-access

    # TODO: rename (or also add) 'get'?
    def __getitem__(self, expr: Variable) -> object:
        values = self._get_values(expr)
        assert expr.name.lexeme in values, f"__getitem__() on expr not in locals {expr}"
        return values[expr.name.lexeme]

    # TODO: rename 'assign'?
    def __setitem__(self, expr: Assign, value: object) -> None:
        values = self._get_values(expr)
        values[expr.name.lexeme] = value

    def __str__(self) -> str:
        return f"{self._locals}"
