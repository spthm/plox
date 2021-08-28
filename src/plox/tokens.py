from __future__ import annotations

from enum import Enum, auto, unique


@unique
class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One- or two-character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


class Token:
    def __init__(self, kind: TokenType, lexeme: str, literal: object, lno: int):
        self._kind = kind
        self._lexeme = lexeme
        self._literal = literal
        self._lno = lno

    def __eq__(self, other: Token):
        return (
            self._kind == other._kind
            and self._lexeme == other._lexeme
            and self._literal == other._literal
            and self._lno == other._lno
        )

    def __repr__(self):
        # We use repr() for lexeme and literal so that, respectively, the empty string
        # and None are printed.
        return (
            "Token("
            f"kind={self._kind}"
            f", lexeme={repr(self._lexeme)}"
            f", literal={repr(self._literal)}"
            f", lno={self._lno}"
            ")"
        )

    def __str__(self):
        return f"{self._kind} {self._lexeme} {self._literal}"
