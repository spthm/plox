from functools import singledispatch
from operator import add, eq, ge, gt, le, lt, mul, ne, neg, not_, sub, truediv
from typing import overload

from plox.expressions import Binary, Expr, Grouping, Literal, Unary
from plox.tokens import TokenType

_binary_op_lookup = {
    TokenType.BANG_EQUAL: ne,
    TokenType.EQUAL_EQUAL: eq,
    TokenType.GREATER: gt,
    TokenType.GREATER_EQUAL: ge,
    TokenType.LESS: lt,
    TokenType.LESS_EQUAL: le,
    TokenType.MINUS: sub,
    TokenType.PLUS: add,  # This works for strings and numbers
    TokenType.SLASH: truediv,
    TokenType.STAR: mul,
}

_unary_op_lookup = {
    TokenType.BANG: not_,
    TokenType.MINUS: neg,
}


def _truthy(x: object) -> bool:
    if x is None or x is False:
        return False
    return True


# mypy's @overload is buggy for @singledispatch. Use of the separate _evaluate here
# is a workaround https://github.com/python/mypy/issues/8356.


@singledispatch
def _evaluate(expr: Expr) -> object:
    raise TypeError(f"evaluate does not support {type(expr)}")


@overload
@_evaluate.register(Binary)
def evaluate(expr: Binary) -> object:
    # We evaluate operands in left-to-right order.
    left = evaluate(expr.left)
    right = evaluate(expr.right)

    try:
        op = _binary_op_lookup[expr.operator.kind]
        return op(left, right)
    except KeyError:
        raise RuntimeError(
            f"unexpected Binary operator: {expr.operator.kind}"
        ) from None


@overload
@_evaluate.register(Grouping)
def evaluate(expr: Grouping) -> object:
    return evaluate(expr.expression)


@overload
@_evaluate.register(Literal)
def evaluate(expr: Literal) -> object:
    return expr.value


@overload
@_evaluate.register(Unary)
def evaluate(expr: Unary) -> object:
    right = evaluate(expr.right)

    try:
        op = _unary_op_lookup[expr.operator.kind]
        return op(right)
    except KeyError:
        raise RuntimeError(f"unexpected Unary operator: {expr.operator.kind}") from None


def evaluate(expr: Expr) -> object:
    return _evaluate(expr)
