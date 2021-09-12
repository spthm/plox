from functools import singledispatch
from typing import overload

from plox.environment import Environment

from .evaluation import evaluate
from .statements import Block, Expression, Print, Stmt, Var


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


@singledispatch
def _execute(stmt: Stmt, _: Environment) -> None:
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
    return None


@overload
@_execute.register(Print)
def execute(stmt: Print, env: Environment) -> None:
    value = evaluate(stmt.expression, env)
    print(_stringify(value))
    return None


@overload
@_execute.register(Var)
def execute(stmt: Var, env: Environment) -> None:
    value = evaluate(stmt.initializer, env)
    env.define(stmt.name, value)
    return None


def execute(stmt: Stmt, env: Environment) -> None:
    return _execute(stmt, env)
