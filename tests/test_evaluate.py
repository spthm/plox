import pytest

from plox.ast import Assign, Binary, Grouping, Literal, Unary, evaluate
from plox.environment import Environment
from plox.errors import ExecutionError
from plox.tokens import Token, TokenType


# fmt: off
def test_evaluate():
    # Test case from
    #  https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/expressions/evaluate.lox
    minus = Token(TokenType.MINUS, "-", None, 1)
    plus = Token(TokenType.PLUS, "+", None, 1)

    # (5 - (3 - 1)) + -1
    expr = \
        Binary(
            Grouping(
                Binary(
                    Literal(5.0),
                    minus,
                    Grouping(Binary(Literal(3.0), minus, Literal(1.0)))
                )
            ),
            plus,
            Unary(minus, Literal(1.0)),
        )

    assert evaluate(expr, Environment()) == 2
# fmt: on


def test_assignment():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/assignment/grouping.lox
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    literal_a = Literal("a")

    # var a;
    # a = "a"
    env = Environment()
    env.define(a, None)
    expr = Assign(a, literal_a)

    assert evaluate(expr, env) == literal_a.value


def test_assignment_undefined_variable():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/assignment/undefined.lox
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    literal_a = Literal("a")

    # a = "a";
    env = Environment()
    expr = Assign(a, literal_a)

    with pytest.raises(ExecutionError, match="Undefined variable 'a'"):
        assert evaluate(expr, env) == literal_a.value
