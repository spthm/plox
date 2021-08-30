from functools import singledispatch
from typing import overload

from plox.expressions import Binary, Expr, Grouping, Literal, Unary


def _parenthesize(name: str, *args: Expr) -> str:
    content = " ".join(ast_str(e) for e in args)
    return f"({name} {content})"


# mypy's @overload is buggy for @singledispatch. Use of the separate _ast_str here
# is a workaround https://github.com/python/mypy/issues/8356.


@singledispatch
def _ast_str(expr: Expr) -> str:
    raise TypeError(f"ast_str does not support {type(expr)}")


@overload
@_ast_str.register(Binary)
def ast_str(expr: Binary) -> str:
    return _parenthesize(expr.operator.lexeme, expr.left, expr.right)


@overload
@_ast_str.register(Grouping)
def ast_str(expr: Grouping) -> str:
    return _parenthesize("group", expr.expression)


@overload
@_ast_str.register(Literal)
def ast_str(expr: Literal) -> str:
    if expr.value is None:
        return "nil"
    return str(expr.value)


@overload
@_ast_str.register(Unary)
def ast_str(expr: Unary) -> str:
    return _parenthesize(expr.operator.lexeme, expr.right)


def ast_str(expr: Expr) -> str:
    return _ast_str(expr)
