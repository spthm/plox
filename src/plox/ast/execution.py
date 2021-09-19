from functools import singledispatch
from typing import Any, overload

from plox.environment import Environment

from .evaluation import _truthy, evaluate
from .statements import Block, Expression, If, Print, Stmt, Var, While


def _stringify(value: object) -> str:
    if value is None:
        return "nil"
    if value is True:
        return "true"
    if value is False:
        return "false"

    text = str(value)

    if isinstance(value, float) and text.endswith(".0"):
        text = text[:-2]

    return text


# mypy's @overload is buggy for @singledispatch. Use of the separate _execute here
# is a workaround https://github.com/python/mypy/issues/8356.


@singledispatch
def _execute(stmt: Any, _: Environment) -> None:
    raise TypeError(f"execute does not support {type(stmt)}")


@overload
@_execute.register(Block)
def execute(stmt: Block, env: Environment) -> None:
    env = Environment(enclosing=env)
    for s in stmt.statements:
        execute(s, env)


@overload
@_execute.register(Expression)
def execute(stmt: Expression, env: Environment) -> None:
    evaluate(stmt.expression, env)


@overload
@_execute.register(If)
def execute(stmt: If, env: Environment) -> None:
    if _truthy(evaluate(stmt.condition, env)):
        execute(stmt.then_branch, env)
    elif stmt.else_branch is not None:
        execute(stmt.else_branch, env)


@overload
@_execute.register(Print)
def execute(stmt: Print, env: Environment) -> None:
    value = evaluate(stmt.expression, env)
    print(_stringify(value))


@overload
@_execute.register(Var)
def execute(stmt: Var, env: Environment) -> None:
    value = evaluate(stmt.initializer, env)
    env.define(stmt.name, value)


@overload
@_execute.register(While)
def execute(stmt: While, env: Environment) -> None:
    while _truthy(evaluate(stmt.condition, env)):
        execute(stmt.body, env)


def execute(stmt: Stmt, env: Environment) -> None:
    return _execute(stmt, env)
