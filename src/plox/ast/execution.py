from functools import singledispatch
from typing import overload

from .evaluation import evaluate
from .statements import Expression, Print, Stmt


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
def _execute(stmt: Stmt) -> None:
    raise TypeError(f"execute does not support {type(stmt)}")


@overload
@_execute.register(Expression)
def execute(stmt: Expression) -> None:
    evaluate(stmt.expression)
    return None


@overload
@_execute.register(Print)
def execute(stmt: Print) -> None:
    value = evaluate(stmt.expression)
    print(_stringify(value))
    return None


def execute(stmt: Stmt) -> None:
    return _execute(stmt)
