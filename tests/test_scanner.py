from textwrap import dedent

from plox.scanner import Scanner
from plox.tokens import Token, TokenType

# Test cases from
#  https://github.com/munificent/craftinginterpreters/tree/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/scanning


def test_identifiers():
    src = """
    andy formless fo _ _123 _abc ab123
    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_
    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.IDENTIFIER, "andy", None, 2),
        Token(TokenType.IDENTIFIER, "formless", None, 2),
        Token(TokenType.IDENTIFIER, "fo", None, 2),
        Token(TokenType.IDENTIFIER, "_", None, 2),
        Token(TokenType.IDENTIFIER, "_123", None, 2),
        Token(TokenType.IDENTIFIER, "_abc", None, 2),
        Token(TokenType.IDENTIFIER, "ab123", None, 2),
        Token(
            TokenType.IDENTIFIER,
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_",
            None,
            3,
        ),
        Token(TokenType.EOF, "", None, 4),
    ]


def test_keywords():
    src = "and class else false for fun if nil or return super this true var while"
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.AND, "and", None, 1),
        Token(TokenType.CLASS, "class", None, 1),
        Token(TokenType.ELSE, "else", None, 1),
        Token(TokenType.FALSE, "false", None, 1),
        Token(TokenType.FOR, "for", None, 1),
        Token(TokenType.FUN, "fun", None, 1),
        Token(TokenType.IF, "if", None, 1),
        Token(TokenType.NIL, "nil", None, 1),
        Token(TokenType.OR, "or", None, 1),
        Token(TokenType.RETURN, "return", None, 1),
        Token(TokenType.SUPER, "super", None, 1),
        Token(TokenType.THIS, "this", None, 1),
        Token(TokenType.TRUE, "true", None, 1),
        Token(TokenType.VAR, "var", None, 1),
        Token(TokenType.WHILE, "while", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]


def test_numbers():
    src = """
    123
    123.456
    .456
    123.
    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.NUMBER, "123", 123.0, 2),
        Token(TokenType.NUMBER, "123.456", 123.456, 3),
        Token(TokenType.DOT, ".", None, 4),
        Token(TokenType.NUMBER, "456", 456.0, 4),
        Token(TokenType.NUMBER, "123", 123.0, 5),
        Token(TokenType.DOT, ".", None, 5),
        Token(TokenType.EOF, "", None, 6),
    ]


def test_punctuators():
    src = "(){};,+-*!===<=>=!=<>/."
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.LEFT_PAREN, "(", None, 1),
        Token(TokenType.RIGHT_PAREN, ")", None, 1),
        Token(TokenType.LEFT_BRACE, "{", None, 1),
        Token(TokenType.RIGHT_BRACE, "}", None, 1),
        Token(TokenType.SEMICOLON, ";", None, 1),
        Token(TokenType.COMMA, ",", None, 1),
        Token(TokenType.PLUS, "+", None, 1),
        Token(TokenType.MINUS, "-", None, 1),
        Token(TokenType.STAR, "*", None, 1),
        Token(TokenType.BANG_EQUAL, "!=", None, 1),
        Token(TokenType.EQUAL_EQUAL, "==", None, 1),
        Token(TokenType.LESS_EQUAL, "<=", None, 1),
        Token(TokenType.GREATER_EQUAL, ">=", None, 1),
        Token(TokenType.BANG_EQUAL, "!=", None, 1),
        Token(TokenType.LESS, "<", None, 1),
        Token(TokenType.GREATER, ">", None, 1),
        Token(TokenType.SLASH, "/", None, 1),
        Token(TokenType.DOT, ".", None, 1),
        Token(TokenType.EOF, "", None, 1),
    ]


def test_strings():
    src = """
    ""
    "string"

    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.STRING, '""', "", 2),
        Token(TokenType.STRING, '"string"', "string", 3),
        Token(TokenType.EOF, "", None, 5),
    ]


def test_whitespace():
    src = """
    space    tabs				newlines




    end
    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.IDENTIFIER, "space", None, 2),
        Token(TokenType.IDENTIFIER, "tabs", None, 2),
        Token(TokenType.IDENTIFIER, "newlines", None, 2),
        Token(TokenType.IDENTIFIER, "end", None, 7),
        Token(TokenType.EOF, "", None, 8),
    ]
