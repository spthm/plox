from functools import singledispatch
from math import copysign
from operator import add, eq, ge, gt, le, lt, mul, ne, neg, sub, truediv
from typing import Any, Protocol, overload

from plox.environment import Environment
from plox.errors import ExecutionError
from plox.protocols import SupportsCall
from plox.tokens import Token, TokenType

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


def _binary_op_error(op: Token) -> str:
    if op.kind == TokenType.PLUS:
        fix = "must both be 'string' or 'number'"
    else:
        fix = "must both be 'number'"
    return f"Unsupported operands for '{op.lexeme}', {fix}."


def _unary_op_error(op: Token) -> str:
    return f"Unsupported operand for '{op.lexeme}', must be 'number'."


def _neg(x: object) -> object:
    if isinstance(x, float):
        return neg(x)
    raise TypeError


def _truthy(x: object) -> bool:
    if x is None or x is False:
        return False
    return True


def _is_numeric(*args: object) -> bool:
    return all(isinstance(x, float) for x in args)


def _is_string(*args: object) -> bool:
    return all(isinstance(x, str) for x in args)


def _is_numeric_or_string(*args: object) -> bool:
    return _is_numeric(*args) or _is_string(*args)


class OpCheck(Protocol):
    def __call__(self, *args: object) -> bool: ...


_binary_op_fn = {
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

_binary_op_check: dict[TokenType, OpCheck] = {
    TokenType.GREATER: _is_numeric,
    TokenType.GREATER_EQUAL: _is_numeric,
    TokenType.LESS: _is_numeric,
    TokenType.LESS_EQUAL: _is_numeric,
    TokenType.MINUS: _is_numeric,
    TokenType.PLUS: _is_numeric_or_string,
    TokenType.SLASH: _is_numeric,
    TokenType.STAR: _is_numeric,
}

_unary_op_fn = {
    TokenType.BANG: lambda x: not _truthy(x),
    TokenType.MINUS: _neg,
}


# mypy's @overload is buggy for @singledispatch. Use of the separate _evaluate here
# is a workaround https://github.com/python/mypy/issues/8356.


@singledispatch
def _evaluate(expr: Any, _: Environment) -> object:
    raise TypeError(f"evaluate does not support {type(expr)}")


@overload
@_evaluate.register(Assign)
def evaluate(expr: Assign, env: Environment) -> object:
    value = evaluate(expr.value, env)
    env[expr.name] = value
    return value


@overload
@_evaluate.register(Binary)
def evaluate(expr: Binary, env: Environment) -> object:
    # We evaluate operands in left-to-right order, and evaluate both before type
    # checking either.
    left = evaluate(expr.left, env)
    right = evaluate(expr.right, env)

    check = _binary_op_check.get(expr.operator.kind, None)
    if check is not None and not check(left, right):
        msg = _binary_op_error(expr.operator)
        raise ExecutionError(msg, expr.operator)

    try:
        op = _binary_op_fn[expr.operator.kind]
    except KeyError as e:
        # This is an internal error.
        raise RuntimeError(f"unexpected Binary operator: {expr.operator.kind}") from e

    try:
        return op(left, right)
    except ZeroDivisionError:
        if not (isinstance(left, float) and isinstance(right, float)):
            raise

        if left == 0:
            return float("nan")

        # Account for right being signed zero.
        return copysign(float("inf"), left * right)


@overload
@_evaluate.register(Call)
def evaluate(expr: Call, env: Environment) -> object:
    callee = evaluate(expr.callee, env)
    if not isinstance(callee, SupportsCall):
        raise ExecutionError("Can only call functions and classes.", expr.paren)

    arguments = [evaluate(arg, env) for arg in expr.arguments]
    if len(arguments) != callee.arity():
        raise ExecutionError(
            f"Expected {callee.arity()} arguments but got {len(arguments)}.", expr.paren
        )

    return callee.call(arguments)


@overload
@_evaluate.register(Grouping)
def evaluate(expr: Grouping, env: Environment) -> object:
    return evaluate(expr.expression, env)


@overload
@_evaluate.register(Literal)
def evaluate(expr: Literal, env: Environment) -> object:
    return expr.value


@overload
@_evaluate.register(Logical)
def evaluate(expr: Logical, env: Environment) -> object:
    left = evaluate(expr.left, env)

    if expr.operator.kind == TokenType.OR:
        if _truthy(left):
            return left
    else:
        if not _truthy(left):
            return left

    return evaluate(expr.right, env)


@overload
@_evaluate.register(Unary)
def evaluate(expr: Unary, env: Environment) -> object:
    right = evaluate(expr.right, env)

    try:
        op = _unary_op_fn[expr.operator.kind]
    except KeyError as e:
        # This is an internal error.
        raise RuntimeError(f"unexpected Unary operator: {expr.operator.kind}") from e

    try:
        return op(right)
    except TypeError:
        msg = _unary_op_error(expr.operator)
        raise ExecutionError(msg, expr.operator) from None


@overload
@_evaluate.register(Variable)
def evaluate(expr: Variable, env: Environment) -> object:
    return env[expr.name]


def evaluate(expr: Expr, env: Environment) -> object:
    return _evaluate(expr, env)
