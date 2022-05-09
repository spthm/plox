from plox.ast import Binary, Grouping, Literal, Unary, ast_str
from plox.tokens import Token, TokenType


def test_literal_int():
    assert ast_str(Literal(123)) == "123"


def test_literal_float():
    assert ast_str(Literal(45.67)) == "45.67"


def test_binry_unary_grouping_literal():
    minus = Token(TokenType.MINUS, "-", None, 1, 1)
    lhs = Unary(minus, Literal(123))
    op = Token(TokenType.STAR, "*", None, 1, 1)
    rhs = Grouping(Literal(45.67))

    expr = Binary(lhs, op, rhs)
    assert ast_str(expr) == "(* (- 123) (group 45.67))"
