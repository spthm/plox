from __future__ import annotations

from functools import singledispatch
from typing import Any, Optional, Sequence, Union, overload

from plox.errors import ExecutionError

from .expressions import (
    Assign,
    Binary,
    Call,
    Expr,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from .statements import Block, Expression, Function, If, Print, Return, Stmt, Var, While

Bindable = Union[Assign, Variable]
Scope = dict[str, Optional[bool]]


class Bindings:
    def __init__(self) -> None:
        self._distances: dict[Bindable, int] = {}

    @classmethod
    def from_dict(cls, dct: dict[Bindable, int]) -> Bindings:
        self = cls()
        self._distances = dict(dct.items())
        return self

    def __contains__(self, expr: Bindable) -> bool:
        return expr in self._distances

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Bindings):
            return NotImplemented
        return self._distances == rhs._distances

    def __getitem__(self, expr: Bindable) -> int:
        return self._distances[expr]

    def __ior__(self, rhs: Bindings) -> Bindings:
        self._check_merge(rhs)

        self._distances |= rhs._distances
        return self

    def __or__(self, rhs: Bindings) -> Bindings:
        self._check_merge(rhs)

        merged = self.__class__()
        merged._distances = self._distances | rhs._distances
        return merged

    def __str__(self) -> str:
        return str(self._distances)

    def _check_merge(self, rhs: Bindings) -> None:
        # pylint: disable=protected-access
        assert not set(self._distances.keys()) & set(rhs._distances.keys())


def _resolve_local(expr: Bindable, scopes: list[Scope]) -> Bindings:
    for distance, scope in enumerate(scopes):
        if expr.name.lexeme in scope:
            return Bindings.from_dict({expr: distance})

    raise ExecutionError(f"Undefined variable '{expr.name.lexeme}'.", expr.name)


def _resolve_list(lst: Sequence[Union[Expr, Stmt]], scopes: list[Scope]) -> Bindings:
    bindings = Bindings()
    for s in lst:
        resolved = resolve(s, scopes)
        bindings |= resolved
    return bindings


# mypy's @overload is buggy for @singledispatch. Use of the separate _resolve here
# is a workaround https://github.com/python/mypy/issues/8356.


@singledispatch
def _resolve(x: Any, _: list[Scope]) -> Bindings:
    raise TypeError(f"resolve does not support {type(x)}")


@overload
@_resolve.register(Assign)
def resolve(x: Assign, scopes: list[Scope]) -> Bindings:
    target_binding = _resolve_local(x, scopes)
    value_bindings = resolve(x.value, scopes)
    return target_binding | value_bindings


@overload
@_resolve.register(Binary)
def resolve(x: Binary, scopes: list[Scope]) -> Bindings:
    return _resolve_list([x.left, x.right], scopes)


@overload
@_resolve.register(Call)
def resolve(x: Call, scopes: list[Scope]) -> Bindings:
    return _resolve_list([x.callee] + x.arguments, scopes)


@overload
@_resolve.register(Grouping)
def resolve(x: Grouping, scopes: list[Scope]) -> Bindings:
    return resolve(x.expression, scopes)


@overload
@_resolve.register(Literal)
def resolve(x: Literal, scopes: list[Scope]) -> Bindings:
    return Bindings()


@overload
@_resolve.register(Logical)
def resolve(x: Logical, scopes: list[Scope]) -> Bindings:
    return _resolve_list([x.left, x.right], scopes)


@overload
@_resolve.register(Unary)
def resolve(x: Unary, scopes: list[Scope]) -> Bindings:
    return resolve(x.right, scopes)


@overload
@_resolve.register(Variable)
def resolve(x: Variable, scopes: list[Scope]) -> Bindings:
    scope = scopes[0]
    if scope.get(x.name.lexeme, False) is None:
        raise ExecutionError(
            "Can't read local variable in its own initializer.", x.name
        )
    return _resolve_local(x, scopes)


@overload
@_resolve.register(Block)
def resolve(x: Block, scopes: list[Scope]) -> Bindings:
    block_scope: Scope = Scope()
    block_scopes = [block_scope] + scopes
    return _resolve_list(x.statements, block_scopes)


@overload
@_resolve.register(Expression)
def resolve(x: Expression, scopes: list[Scope]) -> Bindings:
    return resolve(x.expression, scopes)


@overload
@_resolve.register(Function)
def resolve(x: Function, scopes: list[Scope]) -> Bindings:
    scopes[0][x.name.lexeme] = True

    fn_scope: Scope = Scope()
    for param in x.parameters:
        fn_scope[param.lexeme] = True

    resolved = resolve(x.body, [fn_scope] + scopes)
    return resolved


@overload
@_resolve.register(If)
def resolve(x: If, scopes: list[Scope]) -> Bindings:
    statements = [x.condition, x.then_branch]
    if x.else_branch is not None:
        statements.append(x.else_branch)
    return _resolve_list(statements, scopes)


@overload
@_resolve.register(Print)
def resolve(x: Print, scopes: list[Scope]) -> Bindings:
    return resolve(x.expression, scopes)


@overload
@_resolve.register(Return)
def resolve(x: Return, scopes: list[Scope]) -> Bindings:
    if x.expression is not None:
        return resolve(x.expression, scopes)
    return Bindings()


@overload
@_resolve.register(Var)
def resolve(x: Var, scopes: list[Scope]) -> Bindings:
    bindings = Bindings()
    init_scope = scopes[0]

    if x.name.lexeme in init_scope:
        raise ExecutionError("Already a variable with this name in this scope.", x.name)

    # Add the declared variable to the scope so that it shadows any
    # outer variable with this name, but explicitly set it to None
    # so that we can detect if it is referenced from the initializer;
    # in Lox, doing so is a 'compile'-time error.
    init_scope[x.name.lexeme] = None
    if x.initializer is not None:
        bindings = resolve(x.initializer, scopes)
    init_scope[x.name.lexeme] = True
    return bindings


@overload
@_resolve.register(While)
def resolve(x: While, scopes: list[Scope]) -> Bindings:
    return resolve(x.condition, scopes) | resolve(x.body, scopes)


def resolve(x: Union[Expr, Stmt], scopes: list[Scope]) -> Bindings:
    return _resolve(x, scopes)


def resolve_statements(
    statements: list[Stmt], root_scope: Optional[Scope] = None
) -> Bindings:
    if root_scope is None:
        root_scope = Scope()
    return _resolve_list(statements, [root_scope])
