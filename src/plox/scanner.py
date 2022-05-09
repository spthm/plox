from plox.errors import ScannerError, report
from plox.tokens import Token, TokenType

_KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "fun": TokenType.FUN,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


def _is_alpha(char: str) -> bool:
    return "a" <= char <= "z" or "A" <= char <= "Z" or char == "_"


def _is_alphanum(char: str) -> bool:
    return _is_alpha(char) or _is_digit(char)


def _is_digit(char: str) -> bool:
    assert len(char) == 1
    # char.isdigit() allows characters that are not valid
    # for float conversions, e.g. Kharosthi Numerals
    return "0" <= char <= "9"


class Scanner:
    def __init__(self, source: str) -> None:
        self._source = source
        self._tokens: list[Token] = []

        self._start = 0
        self._lstart = 0
        self._current = 0
        self._lno = 1

    def scan_tokens(self) -> list[Token]:
        while not self._at_end():
            self._start = self._current
            try:
                self._scan_token()
            except ScannerError as e:
                report(e.lno, "", e.message)
                raise

        self._tokens.append(
            Token(TokenType.EOF, "", None, self._lno, self._col(eof=True))
        )

        return list(self._tokens)

    def _add_token(self, kind: TokenType, literal: object = None) -> None:
        text = self._source[self._start : self._current]
        self._tokens.append(Token(kind, text, literal, self._lno, self._col()))

    def _advance(self) -> str:
        char = self._source[self._current]
        self._current += 1
        return char

    def _identifier(self) -> None:
        while _is_alphanum(self._peek()):
            self._advance()

        text = self._source[self._start : self._current]
        kind = _KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add_token(kind)

    def _at_end(self) -> bool:
        return self._current >= len(self._source)

    def _col(self, eof: bool = False) -> int:
        # Column index is 1-based, like line number.
        if eof:
            # At EOF, we introduce a phantom \0 character, but this
            # is not actually scanned, and self._start will still point
            # to the start of the last real token.
            return self._current - self._lstart + 1
        return self._start - self._lstart + 1

    def _match(self, char: str) -> bool:
        if self._peek() != char:
            return False

        self._current += 1
        return True

    def _number(self) -> None:
        while _is_digit(self._peek()):
            self._advance()

        if self._peek() == "." and _is_digit(self._peek_next()):
            # Consume the "."
            self._advance()

            while _is_digit(self._peek()):
                self._advance()

        self._add_token(
            TokenType.NUMBER, float(self._source[self._start : self._current])
        )

    def _peek(self) -> str:
        if self._at_end():
            return "\0"
        return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return "\0"
        return self._source[self._current + 1]

    def _scan_token(self) -> None:
        # pylint: disable=too-many-branches
        char = self._advance()

        if char == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif char == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif char == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self._add_token(TokenType.COMMA)
        elif char == ".":
            self._add_token(TokenType.DOT)
        elif char == "-":
            self._add_token(TokenType.MINUS)
        elif char == "+":
            self._add_token(TokenType.PLUS)
        elif char == ";":
            self._add_token(TokenType.SEMICOLON)
        elif char == "*":
            self._add_token(TokenType.STAR)

        elif char == "!":
            self._add_token(
                TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
            )
        elif char == "=":
            self._add_token(
                TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
            )
        elif char == "<":
            self._add_token(
                TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
            )
        elif char == ">":
            self._add_token(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            )

        elif char == "/":
            if self._match("/"):
                # A comment. It goes until the end of the line.
                # Be robust to files that end without a newline.
                while self._peek() != "\n" and not self._at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)

        elif char in {" ", "\r", "\t"}:
            # Ignore whitespace
            pass
        elif char == "\n":
            self._lno += 1
            self._lstart = self._current

        elif char == '"':
            self._string()

        elif _is_digit(char):
            self._number()
        elif _is_alpha(char):
            self._identifier()

        else:
            raise ScannerError(f"Unexpected character: {char}.", self._lno)

    def _string(self) -> None:
        while (peek := self._peek()) != '"' and not self._at_end():
            # Allow for multi-line strings.
            if peek == "\n":
                self._lno += 1
            self._advance()

        if self._at_end():
            raise ScannerError("Unterminated string.", self._lno)

        # The closing '"'
        self._advance()

        # Trim the quotes.
        value = self._source[self._start + 1 : self._current - 1]
        self._add_token(TokenType.STRING, value)
