from plox.evaluate import evaluate
from plox.expressions import Binary, Grouping, Literal, Unary
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

    assert evaluate(expr) == 2
# fmt: on
