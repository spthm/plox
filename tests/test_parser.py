import pytest

from plox.ast.expressions import Assign, Binary, Grouping, Literal, Unary, Variable
from plox.ast.statements import Block, Expression, Var
from plox.errors import ParserError
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
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
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
        semicolon,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
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
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Binary(Literal(2.0), plus, Binary(Literal(3.0), star, Literal(4.0)))
    )


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
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Binary(Literal(2.0), minus, Binary(Literal(3.0), star, Literal(4.0)))
    )


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
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Binary(Literal(2.0), plus, Binary(Literal(3.0), slash, Literal(4.0)))
    )


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
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Binary(Literal(2.0), minus, Binary(Literal(3.0), slash, Literal(4.0)))
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
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Binary(Literal(False), equal, Binary(Literal(2.0), lt, Literal(1.0)))
    )


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
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Binary(Literal(False), equal, Binary(Literal(2.0), lte, Literal(1.0)))
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
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Binary(Literal(False), equal, Binary(Literal(2.0), gt, Literal(1.0)))
    )


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
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Binary(Literal(False), equal, Binary(Literal(2.0), gte, Literal(1.0)))
    )


def test_number_leading_dot(capsys):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/number/leading_dot.lox
    dot = Token(TokenType.DOT, ".", None, 1)
    number = Token(TokenType.NUMBER, "123", 123.0, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # .123;
    tokens = [dot, number, semicolon, end]

    with pytest.raises(ParserError, match="Expect expression"):
        Parser(tokens).parse()

    _, err = capsys.readouterr()
    assert "Error at '.': Expect expression." in err


def test_associativity():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/assignment/associativity.lox
    equals = Token(TokenType.EQUAL, "=", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    b = Token(TokenType.IDENTIFIER, "b", None, 1)
    c = Token(TokenType.IDENTIFIER, "c", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # a = b = c;
    tokens = [
        a,
        equals,
        b,
        equals,
        c,
        semicolon,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(Assign(a, Assign(b, Variable(c))))


def test_assign_to_group_fails(capsys):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/assignment/grouping.lox
    equals = Token(TokenType.EQUAL, "=", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    string_a = Token(TokenType.STRING, '"a"', "a", 1)
    lbracket = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rbracket = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # (a) = "a";
    tokens = [
        lbracket,
        a,
        rbracket,
        equals,
        string_a,
        semicolon,
        end,
    ]

    with pytest.raises(ParserError, match="Invalid assignment target"):
        Parser(tokens).parse()

    _, err = capsys.readouterr()
    assert "Error at '=': Invalid assignment target." in err


def test_block():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/block/scope.lox
    equals = Token(TokenType.EQUAL, "=", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    inner = Token(TokenType.STRING, '"inner"', "inner", 1)
    outer = Token(TokenType.STRING, '"outer"', "outer", 1)
    lbrace = Token(TokenType.LEFT_BRACE, "{", None, 1)
    rbrace = Token(TokenType.RIGHT_BRACE, "}", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    var = Token(TokenType.VAR, "var", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # a = "inner";
    # { var a = "outer"; }
    tokens = [
        a,
        equals,
        outer,
        semicolon,
        lbrace,
        var,
        a,
        equals,
        inner,
        semicolon,
        rbrace,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 2
    assert statements[0] == Expression(Assign(a, Literal("outer")))
    assert statements[1] == Block([Var(a, Literal("inner"))])


def test_print_no_expression(capsys):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/print/missing_argument.lox
    print_ = Token(TokenType.PRINT, "print", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # print;
    tokens = [
        print_,
        semicolon,
        end,
    ]

    with pytest.raises(ParserError, match="Expect expression"):
        Parser(tokens).parse()

    _, err = capsys.readouterr()
    assert "Error at ';': Expect expression." in err
