from plox.ast import Binary, Grouping, Literal, Unary
from plox.parser import Parser
from plox.tokens import Token, TokenType


# fmt: off
def test_parse_grouping():
    # Test case from
    #  https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/expressions/parse.lox
    minus = Token(TokenType.MINUS, "-", None, 1)
    plus = Token(TokenType.PLUS, "+", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    three = Token(TokenType.NUMBER, "3", 3, 1)
    five = Token(TokenType.NUMBER, "5", 5, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # (5 - (3 - 1)) + -1
    tokens = [
        lparen,
        five,
        minus,
        lparen,
        three,
        minus,
        one,
        rparen,
        rparen,
        plus,
        minus,
        one,
        end,
    ]
    expr = Parser(tokens).parse()

    assert expr == \
        Binary(
            Grouping(
                Binary(
                    Literal(5.0),
                    minus,
                    Grouping(Binary(Literal(3.0), minus, Literal(1.0)))
                )
            ),
            plus,
            Unary(minus, Literal(1.0))
        )
# fmt: on


# Precedence test cases adapted from
#  https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/precedence.lox


def test_parse_precedence_plus_star():
    plus = Token(TokenType.PLUS, "+", None, 1)
    star = Token(TokenType.STAR, "*", None, 1)

    # 2 + 3 * 4
    tokens = [
        Token(TokenType.NUMBER, "2", 2, 1),
        plus,
        Token(TokenType.NUMBER, "3", 3, 1),
        star,
        Token(TokenType.NUMBER, "4", 4, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    expr = Parser(tokens).parse()

    assert expr == Binary(Literal(2.0), plus, Binary(Literal(3.0), star, Literal(4.0)))


def test_parse_precedence_minus_star():
    minus = Token(TokenType.MINUS, "-", None, 1)
    star = Token(TokenType.STAR, "*", None, 1)

    # 2 - 3 * 4
    tokens = [
        Token(TokenType.NUMBER, "2", 2, 1),
        minus,
        Token(TokenType.NUMBER, "3", 3, 1),
        star,
        Token(TokenType.NUMBER, "4", 4, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    expr = Parser(tokens).parse()

    assert expr == Binary(Literal(2.0), minus, Binary(Literal(3.0), star, Literal(4.0)))


def test_parse_precedence_plus_slash():
    plus = Token(TokenType.PLUS, "+", None, 1)
    slash = Token(TokenType.STAR, "/", None, 1)

    # 2 + 3 / 4
    tokens = [
        Token(TokenType.NUMBER, "2", 2, 1),
        plus,
        Token(TokenType.NUMBER, "3", 3, 1),
        slash,
        Token(TokenType.NUMBER, "4", 4, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    expr = Parser(tokens).parse()

    assert expr == Binary(Literal(2.0), plus, Binary(Literal(3.0), slash, Literal(4.0)))


def test_parse_precedence_minus_slash():
    minus = Token(TokenType.MINUS, "+", None, 1)
    slash = Token(TokenType.STAR, "/", None, 1)

    # 2 - 3 / 4
    tokens = [
        Token(TokenType.NUMBER, "2", 2, 1),
        minus,
        Token(TokenType.NUMBER, "3", 3, 1),
        slash,
        Token(TokenType.NUMBER, "4", 4, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    expr = Parser(tokens).parse()

    assert expr == Binary(
        Literal(2.0), minus, Binary(Literal(3.0), slash, Literal(4.0))
    )


def test_parse_precedence_equalequal_lt():
    equal = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
    lt = Token(TokenType.LESS, "<", None, 1)

    # false == 2 < 1
    tokens = [
        Token(TokenType.FALSE, "false", False, 1),
        equal,
        Token(TokenType.NUMBER, "2", 2, 1),
        lt,
        Token(TokenType.NUMBER, "1", 1, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    expr = Parser(tokens).parse()

    assert expr == Binary(Literal(False), equal, Binary(Literal(2.0), lt, Literal(1.0)))


def test_parse_precedence_equalequal_lte():
    equal = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
    lte = Token(TokenType.LESS_EQUAL, "<=", None, 1)

    # false == 2 < 1
    tokens = [
        Token(TokenType.FALSE, "false", False, 1),
        equal,
        Token(TokenType.NUMBER, "2", 2, 1),
        lte,
        Token(TokenType.NUMBER, "1", 1, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    expr = Parser(tokens).parse()

    assert expr == Binary(
        Literal(False), equal, Binary(Literal(2.0), lte, Literal(1.0))
    )


def test_parse_precedence_equalequal_gt():
    equal = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
    gt = Token(TokenType.GREATER, ">", None, 1)

    # false == 2 > 1
    tokens = [
        Token(TokenType.FALSE, "false", False, 1),
        equal,
        Token(TokenType.NUMBER, "2", 2, 1),
        gt,
        Token(TokenType.NUMBER, "1", 1, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    expr = Parser(tokens).parse()

    assert expr == Binary(Literal(False), equal, Binary(Literal(2.0), gt, Literal(1.0)))


def test_parse_precedence_equalequal_gte():
    equal = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
    gte = Token(TokenType.GREATER_EQUAL, ">=", None, 1)

    # false == 2 > 1
    tokens = [
        Token(TokenType.FALSE, "false", False, 1),
        equal,
        Token(TokenType.NUMBER, "2", 2, 1),
        gte,
        Token(TokenType.NUMBER, "1", 1, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    expr = Parser(tokens).parse()

    assert expr == Binary(
        Literal(False), equal, Binary(Literal(2.0), gte, Literal(1.0))
    )
