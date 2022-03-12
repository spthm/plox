import pytest

from plox.ast.expressions import (
    Assign,
    Binary,
    Call,
    Grouping,
    Literal,
    Unary,
    Variable,
)
from plox.ast.statements import Block, Expression, If, Print, Var, While
from plox.errors import ParserError
from plox.parser import Parser
from plox.tokens import Token, TokenType

# pylint: disable=too-many-lines
# pylint: disable=too-many-locals


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


def test_if_expression_else_expression():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/if/else.lox
    if_ = Token(TokenType.IF, "if", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    true = Token(TokenType.TRUE, "true", None, 1)
    print_ = Token(TokenType.PRINT, "print", None, 1)
    good = Token(TokenType.STRING, '"good"', "good", 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    else_ = Token(TokenType.ELSE, "else", None, 1)
    bad = Token(TokenType.STRING, '"bad"', "bad", 1)
    end = Token(TokenType.EOF, "", None, 1)

    # if (true) print "good"; else print "bad";
    tokens = [
        if_,
        lparen,
        true,
        rparen,
        print_,
        good,
        semicolon,
        else_,
        print_,
        bad,
        semicolon,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == If(
        Literal(True), Print(Literal("good")), Print(Literal("bad"))
    )


def test_if_expression_else_block():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/if/else.lox
    if_ = Token(TokenType.IF, "if", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    false = Token(TokenType.FALSE, "false", None, 1)
    nil = Token(TokenType.NIL, "nil", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    else_ = Token(TokenType.ELSE, "else", None, 1)
    lbrace = Token(TokenType.LEFT_BRACE, "{", None, 1)
    rbrace = Token(TokenType.RIGHT_BRACE, "}", None, 1)
    print_ = Token(TokenType.PRINT, "print", None, 1)
    block = Token(TokenType.STRING, '"block"', "block", 1)
    end = Token(TokenType.EOF, "", None, 1)

    # if (false) nil; else { print "block"; }
    tokens = [
        if_,
        lparen,
        false,
        rparen,
        nil,
        semicolon,
        else_,
        lbrace,
        print_,
        block,
        semicolon,
        rbrace,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == If(
        Literal(False), Expression(Literal(None)), Block([Print(Literal("block"))])
    )


def test_if_expression_no_else():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/if/if.lox
    if_ = Token(TokenType.IF, "if", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    true = Token(TokenType.TRUE, "true", None, 1)
    print_ = Token(TokenType.PRINT, "print", None, 1)
    good = Token(TokenType.STRING, '"good"', "good", 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # if (true) print "good";
    tokens = [if_, lparen, true, rparen, print_, good, semicolon, end]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == If(Literal(True), Print(Literal("good")), None)


def test_if_block_no_else():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/if/if.lox
    if_ = Token(TokenType.IF, "if", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    true = Token(TokenType.TRUE, "true", None, 1)
    lbrace = Token(TokenType.LEFT_BRACE, "{", None, 1)
    rbrace = Token(TokenType.RIGHT_BRACE, "}", None, 1)
    print_ = Token(TokenType.PRINT, "print", None, 1)
    block = Token(TokenType.STRING, '"block"', "block", 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # if (true) { print "block"; }
    tokens = [if_, lparen, true, rparen, lbrace, print_, block, semicolon, rbrace, end]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == If(Literal(True), Block([Print(Literal("block"))]), None)


def test_dangling_else_binds_rightmost():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/if/dangling_else.lox
    if_ = Token(TokenType.IF, "if", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    true = Token(TokenType.TRUE, "true", None, 1)
    false = Token(TokenType.FALSE, "false", None, 1)
    print_ = Token(TokenType.PRINT, "print", None, 1)
    bad = Token(TokenType.STRING, '"bad"', "bad", 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    else_ = Token(TokenType.ELSE, "else", None, 1)
    bad = Token(TokenType.STRING, '"bad"', "bad", 1)
    good = Token(TokenType.STRING, '"good"', "good", 1)
    end = Token(TokenType.EOF, "", None, 1)

    # if (true) if (false) print "bad"; else print "good";
    tokens = [
        if_,
        lparen,
        true,
        rparen,
        if_,
        lparen,
        false,
        rparen,
        print_,
        bad,
        semicolon,
        else_,
        print_,
        good,
        semicolon,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == If(
        Literal(True),
        If(Literal(False), Print(Literal("bad")), Print(Literal("good"))),
        None,
    )


def test_for_statement_condition(capsys):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/for/statement_condition.lox
    for_ = Token(TokenType.FOR, "for", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    var = Token(TokenType.VAR, "var", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    equals = Token(TokenType.EQUAL, "=", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    lbrace = Token(TokenType.LEFT_BRACE, "{", None, 1)
    rbrace = Token(TokenType.RIGHT_BRACE, "}", None, 1)
    plus = Token(TokenType.PLUS, "+", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # for (var a = 1; {}; a = a + 1) {}
    tokens = [
        for_,
        lparen,
        var,
        a,
        equals,
        one,
        semicolon,
        lbrace,
        rbrace,
        semicolon,
        a,
        equals,
        a,
        plus,
        one,
        rparen,
        lbrace,
        rbrace,
        end,
    ]

    with pytest.raises(ParserError, match="Expect expression"):
        Parser(tokens).parse()

    _, err = capsys.readouterr()
    assert "Error at '{': Expect expression." in err
    assert "Error at ')': Expect ';' after expression." in err


def test_for_statement_increment(capsys):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/for/statement_increment.lox
    for_ = Token(TokenType.FOR, "for", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    var = Token(TokenType.VAR, "var", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    equals = Token(TokenType.EQUAL, "=", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    lt = Token(TokenType.LESS, "<", None, 1)
    two = Token(TokenType.NUMBER, "2", 2, 1)
    lbrace = Token(TokenType.LEFT_BRACE, "{", None, 1)
    rbrace = Token(TokenType.RIGHT_BRACE, "}", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # for (var a = 1; a < 2; {}) {}
    tokens = [
        for_,
        lparen,
        var,
        a,
        equals,
        one,
        semicolon,
        a,
        lt,
        two,
        semicolon,
        lbrace,
        rbrace,
        semicolon,
        rparen,
        lbrace,
        rbrace,
        end,
    ]

    with pytest.raises(ParserError, match="Expect expression"):
        Parser(tokens).parse()

    _, err = capsys.readouterr()
    assert "Error at '{': Expect expression." in err


def test_for_statement_initializer(capsys):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/for/statement_initializer.lox
    for_ = Token(TokenType.FOR, "for", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    lbrace = Token(TokenType.LEFT_BRACE, "{", None, 1)
    rbrace = Token(TokenType.RIGHT_BRACE, "}", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    lt = Token(TokenType.LESS, "<", None, 1)
    two = Token(TokenType.NUMBER, "2", 2, 1)
    equals = Token(TokenType.EQUAL, "=", None, 1)
    plus = Token(TokenType.PLUS, "+", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # for ({}; a < 2; a = a + 1) {}
    tokens = [
        for_,
        lparen,
        lbrace,
        rbrace,
        semicolon,
        a,
        lt,
        two,
        semicolon,
        a,
        equals,
        a,
        plus,
        one,
        rparen,
        lbrace,
        rbrace,
        end,
    ]

    with pytest.raises(ParserError, match="Expect expression"):
        Parser(tokens).parse()

    _, err = capsys.readouterr()
    assert "Error at '{': Expect expression." in err
    assert "Error at ')': Expect ';' after expression." in err


def test_for_single_expression_body():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/for/syntax.lox
    for_ = Token(TokenType.FOR, "for", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    var = Token(TokenType.VAR, "var", None, 1)
    c = Token(TokenType.IDENTIFIER, "c", None, 1)
    equals = Token(TokenType.EQUAL, "=", None, 1)
    zero = Token(TokenType.NUMBER, "0", 0, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    lt = Token(TokenType.LESS, "<", None, 1)
    three = Token(TokenType.NUMBER, "3", 3, 1)
    plus = Token(TokenType.PLUS, "+", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # for (var c = 0; c < 3;) c = c + 1;
    tokens = [
        for_,
        lparen,
        var,
        c,
        equals,
        zero,
        semicolon,
        c,
        lt,
        three,
        semicolon,
        rparen,
        c,
        equals,
        c,
        plus,
        one,
        semicolon,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Block(
        [
            Var(c, Literal(0.0)),
            While(
                Binary(Variable(c), lt, Literal(3.0)),
                Expression(Assign(c, Binary(Variable(c), plus, Literal(1.0)))),
            ),
        ]
    )


def test_for_block_body():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/for/syntax.lox
    for_ = Token(TokenType.FOR, "for", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    var = Token(TokenType.VAR, "var", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    equals = Token(TokenType.EQUAL, "=", None, 1)
    zero = Token(TokenType.NUMBER, "0", 0, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    lt = Token(TokenType.LESS, "<", None, 1)
    three = Token(TokenType.NUMBER, "3", 3, 1)
    equals = Token(TokenType.EQUAL, "=", None, 1)
    plus = Token(TokenType.PLUS, "+", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    lbrace = Token(TokenType.LEFT_BRACE, "{", None, 1)
    rbrace = Token(TokenType.RIGHT_BRACE, "{", None, 1)
    print_ = Token(TokenType.PRINT, "print", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # for (var a = 0; a < 3; a = a + 1) {
    #   print a;
    # }
    tokens = [
        for_,
        lparen,
        var,
        a,
        equals,
        zero,
        semicolon,
        a,
        lt,
        three,
        semicolon,
        a,
        equals,
        a,
        plus,
        one,
        rparen,
        lbrace,
        print_,
        a,
        semicolon,
        rbrace,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Block(
        [
            Var(a, Literal(0.0)),
            While(
                Binary(Variable(a), lt, Literal(3.0)),
                Block(
                    [
                        Block(
                            [
                                Print(Variable(a)),
                            ]
                        ),
                        Expression(Assign(a, Binary(Variable(a), plus, Literal(1.0)))),
                    ]
                ),
            ),
        ]
    )


def test_for_statement_body():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/for/syntax.lox
    for_ = Token(TokenType.FOR, "for", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    false = Token(TokenType.FALSE, "false", False, 1)
    true = Token(TokenType.TRUE, "true", True, 1)
    if_ = Token(TokenType.IF, "if", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    two = Token(TokenType.NUMBER, "2", 2, 1)
    else_ = Token(TokenType.ELSE, "else", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # for (; false;) if (true) 1; else 2;
    tokens = [
        for_,
        lparen,
        semicolon,
        false,
        semicolon,
        rparen,
        if_,
        lparen,
        true,
        rparen,
        one,
        semicolon,
        else_,
        two,
        semicolon,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == While(
        Literal(False),
        If(Literal(True), Expression(Literal(1)), Expression(Literal(2))),
    )


def test_while_single_expression_body():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/while/syntax.lox
    while_ = Token(TokenType.WHILE, "while", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    c = Token(TokenType.IDENTIFIER, "c", None, 1)
    lt = Token(TokenType.LESS, "<", None, 1)
    three = Token(TokenType.NUMBER, "3", 3, 1)
    print_ = Token(TokenType.PRINT, "print", None, 1)
    equals = Token(TokenType.EQUAL, "=", None, 1)
    plus = Token(TokenType.PLUS, "+", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # while (c < 3) print c = c + 1;
    tokens = [
        while_,
        lparen,
        c,
        lt,
        three,
        rparen,
        print_,
        c,
        equals,
        c,
        plus,
        one,
        semicolon,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == While(
        Binary(Variable(c), lt, Literal(3.0)),
        Print(Assign(c, Binary(Variable(c), plus, Literal(1.0)))),
    )


def test_while_block_body():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/while/syntax.lox
    while_ = Token(TokenType.WHILE, "while", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    lt = Token(TokenType.LESS, "<", None, 1)
    three = Token(TokenType.NUMBER, "3", 3, 1)
    lbrace = Token(TokenType.LEFT_BRACE, "{", None, 1)
    rbrace = Token(TokenType.RIGHT_BRACE, "{", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    equals = Token(TokenType.EQUAL, "=", None, 1)
    plus = Token(TokenType.PLUS, "+", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # while (a < 3) {
    #   a = a + 1;
    # }
    tokens = [
        while_,
        lparen,
        a,
        lt,
        three,
        rparen,
        lbrace,
        a,
        equals,
        a,
        plus,
        one,
        semicolon,
        rbrace,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == While(
        Binary(Variable(a), lt, Literal(3.0)),
        Block([Expression(Assign(a, Binary(Variable(a), plus, Literal(1.0))))]),
    )


def test_while_statement_body():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/while/syntax.lox
    while_ = Token(TokenType.WHILE, "while", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    false = Token(TokenType.FALSE, "false", False, 1)
    true = Token(TokenType.TRUE, "true", True, 1)
    if_ = Token(TokenType.IF, "if", None, 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    two = Token(TokenType.NUMBER, "2", 2, 1)
    else_ = Token(TokenType.ELSE, "else", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # while (false) if (true) 1; else 2;
    tokens = [
        while_,
        lparen,
        false,
        rparen,
        if_,
        lparen,
        true,
        rparen,
        one,
        semicolon,
        else_,
        two,
        semicolon,
        end,
    ]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == While(
        Literal(False),
        If(Literal(True), Expression(Literal(1)), Expression(Literal(2))),
    )


def test_call_no_arguments():
    foo = Token(TokenType.IDENTIFIER, "foo", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # foo();
    tokens = [foo, lparen, rparen, semicolon, end]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(Call(Variable(foo), rparen, []))


def test_call_with_arguments():
    foo = Token(TokenType.IDENTIFIER, "foo", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    string_a = Token(TokenType.STRING, '"a"', "a", 1)
    one = Token(TokenType.NUMBER, "1", 1, 1)
    comma = Token(TokenType.COMMA, ",", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # foo(a, "a", 1);
    tokens = [foo, lparen, a, comma, string_a, comma, one, rparen, semicolon, end]
    statements = Parser(tokens).parse()

    assert len(statements) == 1
    assert statements[0] == Expression(
        Call(Variable(foo), rparen, [Variable(a), Literal("a"), Literal(1)])
    )


def test_call_too_many_arguments(capsys):
    # https://github.com/munificent/craftinginterpreters/blob/01e6f5b8f3e5dfa65674c2f9cf4700d73ab41cf8/test/function/too_many_arguments.lox
    foo = Token(TokenType.IDENTIFIER, "foo", None, 1)
    lparen = Token(TokenType.LEFT_PAREN, "(", None, 1)
    rparen = Token(TokenType.RIGHT_PAREN, ")", None, 1)
    a = Token(TokenType.IDENTIFIER, "a", None, 1)
    b = Token(TokenType.IDENTIFIER, "b", None, 1)
    comma = Token(TokenType.COMMA, ",", None, 1)
    semicolon = Token(TokenType.SEMICOLON, ";", None, 1)
    end = Token(TokenType.EOF, "", None, 1)

    # foo(a, a, ..., a, b);
    tokens = [foo, lparen] + [a, comma] * 255 + [b] + [rparen, semicolon, end]
    with pytest.raises(ParserError, match="more than 255 arguments"):
        Parser(tokens).parse()

    _, err = capsys.readouterr()
    assert "Error at ')': Can't have more than 255 arguments." in err
