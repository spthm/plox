import pytest

from plox.ast import Assign, Binary, Bindings, Grouping, Literal, Unary, evaluate
from plox.environment import Environment
from plox.errors import ExecutionError
from plox.tokens import Token, TokenType


# fmt: off
def test_evaluate():
    # Test case from
    #  https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/expressions/evaluate.lox
    minus = Token(TokenType.MINUS, "-", None, 1, 1)
    plus = Token(TokenType.PLUS, "+", None, 1, 1)

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
    id_a = Token(TokenType.IDENTIFIER, "a", None, 1, 1)
    literal_a = Literal("a")

    # a = "a";
    expr = Assign(id_a, literal_a)
    env = Environment()
    env.resolve(Bindings.from_dict({expr: 0}))

    # var a;
    env.define(id_a, None)
    assert evaluate(expr, env) == literal_a.value


@pytest.mark.parametrize("value", [False, None])
def test_unary_bang_falsey_literals(value):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/operator/not.lox
    bang = Token(TokenType.BANG, "1", None, 1, 1)
    literal = Literal(value)

    env = Environment()
    expr = Unary(bang, literal)

    assert evaluate(expr, env) is True


@pytest.mark.parametrize("value", [True, 0, 123, ""])
def test_unary_bang_truthy_literals(value):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/operator/not.lox
    bang = Token(TokenType.BANG, "1", None, 1, 1)
    literal = Literal(value)

    env = Environment()
    expr = Unary(bang, literal)

    assert evaluate(expr, env) is False


def test_unary_double_bang():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/operator/not.lox
    bang = Token(TokenType.BANG, "1", None, 1, 1)
    true = Literal(True)

    # !!true;
    env = Environment()
    expr = Unary(bang, Unary(bang, true))

    assert evaluate(expr, env) is True


def test_unary_neg_string_error():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/operator/negate_nonnum.lox
    neg = Token(TokenType.MINUS, "-", None, 1, 1)
    literal_a = Literal("a")

    # -"a";
    env = Environment()
    expr = Unary(neg, literal_a)

    with pytest.raises(
        ExecutionError, match="Unsupported operand for '-', must be 'number'"
    ):
        evaluate(expr, env)
