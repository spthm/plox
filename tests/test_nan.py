from math import isnan

from plox.ast import Binary, Literal, evaluate
from plox.environment import Environment
from plox.tokens import Token, TokenType

# https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/number/nan_equality.lox


def test_zero_div_zero_is_nan():
    slash = Token(TokenType.SLASH, "/", None, 1)
    expr = Binary(Literal(0.0), slash, Literal(0.0))

    v = evaluate(expr, Environment())

    assert isnan(v)  # type: ignore


def test_nan_eq_nan_false():
    equal = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
    expr = Binary(Literal(float("nan")), equal, Literal(float("nan")))

    assert evaluate(expr, Environment()) is False


def test_nan_eq_zero_false():
    equal = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
    expr = Binary(Literal(float("nan")), equal, Literal(0.0))

    assert evaluate(expr, Environment()) is False


def test_nan_neq_nan_true():
    n_equal = Token(TokenType.BANG_EQUAL, "!=", None, 1)
    expr = Binary(Literal(float("nan")), n_equal, Literal(float("nan")))

    assert evaluate(expr, Environment()) is True


def test_nan_neq_zero_true():
    n_equal = Token(TokenType.BANG_EQUAL, "!=", None, 1)
    expr = Binary(Literal(float("nan")), n_equal, Literal(0.0))

    assert evaluate(expr, Environment()) is True
