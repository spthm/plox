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


class Scanner:
    def __init__(self, source: str):
        self._source = source
        self._tokens: list[Token] = list()

        self._start = 0
        self._current = 0
        self._lno = 1

    def scan_tokens(self):
        while not self._at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._lno))

    def _add_token(self, kind: TokenType, literal: object = None):
        text = self._source[self._start : self._current]
        self._tokens.append(Token(kind, text, literal, self._lno))

    def _advance(self) -> str:
        char = self._source[self._current]
        self._current += 1
        return char

    def _identifier(self):
        while self._is_alphanum(self._peek()):
            self._advance()

        text = self._source[self._start : self._current]
        kind = _KEYWORDS.get(text, TokenType.IDENTIFIER)
        self._add_token(kind)

    def _is_alpha(self, char: str) -> bool:
        return "a" <= char <= "z" or "A" <= char <= "Z" or char == "_"

    def _is_alphanum(self, char: str) -> bool:
        return self._is_alpha(char) or self._is_digit(char)

    def _is_digit(self, char: str) -> bool:
        assert len(char) == 1
        # char.isdigit() allows other characters, that are not valid for float()
        # conversions, e.g. Kharosthi Numerals
        return "0" <= char <= "9"

    def _at_end(self) -> bool:
        return self._current >= len(self._source)

    def _match(self, char: str) -> bool:
        if self._peek() != char:
            return False

        self._current += 1
        return True

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == "." and self._is_digit(self._peek_next()):
            # Consume the "."
            self._advance()

            while self._is_digit(self._peek()):
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

    def _scan_token(self):
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

        elif char == '"':
            self._string()

        elif self._is_digit(char):
            self._number()
        elif self._is_alpha(char):
            self._identifier()

        else:
            raise SyntaxError(f"Unexpected character: {char}")

    def _string(self):
        while (peek := self._peek()) != '"' and not self._at_end():
            # Allow for multi-line strings.
            if peek == "\n":
                self._lno += 1
            self._advance()

        if self._at_end():
            raise SyntaxError("Unterminated string")

        # The closing '"'
        self._advance()

        # Trim the quotes.
        value = self._source[self._start + 1 : self._current - 1]
        self._add_token(TokenType.STRING, value)
