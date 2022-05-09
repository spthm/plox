from textwrap import dedent

import pytest

from plox.errors import ScannerError
from plox.scanner import Scanner
from plox.tokens import Token, TokenType


def test_identifiers():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/scanning/identifiers.lox
    src = """
    andy formless fo _ _123 _abc ab123
    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_
    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.IDENTIFIER, "andy", None, 2, 1),
        Token(TokenType.IDENTIFIER, "formless", None, 2, 6),
        Token(TokenType.IDENTIFIER, "fo", None, 2, 15),
        Token(TokenType.IDENTIFIER, "_", None, 2, 18),
        Token(TokenType.IDENTIFIER, "_123", None, 2, 20),
        Token(TokenType.IDENTIFIER, "_abc", None, 2, 25),
        Token(TokenType.IDENTIFIER, "ab123", None, 2, 30),
        Token(
            TokenType.IDENTIFIER,
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_",
            None,
            3,
            1,
        ),
        Token(TokenType.EOF, "", None, 4, 1),
    ]


def test_keywords():
    # https://github.com/munificent/craftinginterpreters/tree/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/scanning/keywords.lox
    src = "and class else false for fun if nil or return super this true var while"
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.AND, "and", None, 1, 1),
        Token(TokenType.CLASS, "class", None, 1, 5),
        Token(TokenType.ELSE, "else", None, 1, 11),
        Token(TokenType.FALSE, "false", None, 1, 16),
        Token(TokenType.FOR, "for", None, 1, 22),
        Token(TokenType.FUN, "fun", None, 1, 26),
        Token(TokenType.IF, "if", None, 1, 30),
        Token(TokenType.NIL, "nil", None, 1, 33),
        Token(TokenType.OR, "or", None, 1, 37),
        Token(TokenType.RETURN, "return", None, 1, 40),
        Token(TokenType.SUPER, "super", None, 1, 47),
        Token(TokenType.THIS, "this", None, 1, 53),
        Token(TokenType.TRUE, "true", None, 1, 58),
        Token(TokenType.VAR, "var", None, 1, 63),
        Token(TokenType.WHILE, "while", None, 1, 67),
        Token(TokenType.EOF, "", None, 1, 72),
    ]


def test_numbers():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/scanning/numbers.lox
    src = """
    123
    123.456
    .456
    123.
    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.NUMBER, "123", 123.0, 2, 1),
        Token(TokenType.NUMBER, "123.456", 123.456, 3, 1),
        Token(TokenType.DOT, ".", None, 4, 1),
        Token(TokenType.NUMBER, "456", 456.0, 4, 2),
        Token(TokenType.NUMBER, "123", 123.0, 5, 1),
        Token(TokenType.DOT, ".", None, 5, 4),
        Token(TokenType.EOF, "", None, 6, 1),
    ]


def test_punctuators():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/scanning/punctuators.lox
    src = "(){};,+-*!===<=>=!=<>/."
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.LEFT_PAREN, "(", None, 1, 1),
        Token(TokenType.RIGHT_PAREN, ")", None, 1, 2),
        Token(TokenType.LEFT_BRACE, "{", None, 1, 3),
        Token(TokenType.RIGHT_BRACE, "}", None, 1, 4),
        Token(TokenType.SEMICOLON, ";", None, 1, 5),
        Token(TokenType.COMMA, ",", None, 1, 6),
        Token(TokenType.PLUS, "+", None, 1, 7),
        Token(TokenType.MINUS, "-", None, 1, 8),
        Token(TokenType.STAR, "*", None, 1, 9),
        Token(TokenType.BANG_EQUAL, "!=", None, 1, 10),
        Token(TokenType.EQUAL_EQUAL, "==", None, 1, 12),
        Token(TokenType.LESS_EQUAL, "<=", None, 1, 14),
        Token(TokenType.GREATER_EQUAL, ">=", None, 1, 16),
        Token(TokenType.BANG_EQUAL, "!=", None, 1, 18),
        Token(TokenType.LESS, "<", None, 1, 20),
        Token(TokenType.GREATER, ">", None, 1, 21),
        Token(TokenType.SLASH, "/", None, 1, 22),
        Token(TokenType.DOT, ".", None, 1, 23),
        Token(TokenType.EOF, "", None, 1, 24),
    ]


def test_strings():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/scanning/strings.lox
    src = """
    ""
    "string"

    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.STRING, '""', "", 2, 1),
        Token(TokenType.STRING, '"string"', "string", 3, 1),
        Token(TokenType.EOF, "", None, 5, 1),
    ]


def test_unterminated_string(capsys):
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/string/unterminated.lox
    src = """"this string has no close quote"""

    with pytest.raises(ScannerError, match="Unterminated string"):
        Scanner(dedent(src)).scan_tokens()

    _, err = capsys.readouterr()
    assert "[line 1] Error: Unterminated string." in err


def test_whitespace():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/scanning/whitespace.lox
    src = """
    space    tabs				newlines




    end
    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.IDENTIFIER, "space", None, 2, 1),
        Token(TokenType.IDENTIFIER, "tabs", None, 2, 10),
        Token(TokenType.IDENTIFIER, "newlines", None, 2, 18),
        Token(TokenType.IDENTIFIER, "end", None, 7, 1),
        Token(TokenType.EOF, "", None, 8, 1),
    ]


def test_comments_ignored():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/comments/line_at_eof.lox
    src = """
    print "ok";
    // comment
    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [
        Token(TokenType.PRINT, "print", None, 2, 1),
        Token(TokenType.STRING, '"ok"', "ok", 2, 7),
        Token(TokenType.SEMICOLON, ";", None, 2, 11),
        Token(TokenType.EOF, "", None, 4, 1),
    ]


def test_only_comment():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/comments/only_line_comment.lox
    src = "// comment"
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [Token(TokenType.EOF, "", None, 1, 11)]


def test_only_comment_and_newline():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/comments/only_line_comment_and_line.lox
    src = "// comment\n"
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [Token(TokenType.EOF, "", None, 2, 1)]


def test_unicode_in_comments():
    # https://github.com/munificent/craftinginterpreters/blob/6c2ea6f7192910053a78832f0cc34ad56b17ce7c/test/comments/unicode.lox
    src = """
    // Unicode characters are allowed in comments.
    //
    // Latin 1 Supplement: £§¶ÜÞ
    // Latin Extended-A: ĐĦŋœ
    // Latin Extended-B: ƂƢƩǁ
    // Other stuff: ឃᢆ᯽₪ℜ↩⊗┺░
    // Emoji: ☃☺♣
    """
    t = Scanner(dedent(src)).scan_tokens()

    assert t == [Token(TokenType.EOF, "", None, 9, 1)]
