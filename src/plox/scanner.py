from plox.tokens import Token, TokenType


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

    def _at_end(self) -> bool:
        return self._current >= len(self._source)

    def _match(self, char: str) -> bool:
        if self._peek() != char:
            return False

        self._current += 1
        return True

    def _peek(self) -> str:
        if self._at_end():
            return "\0"
        return self._source[self._current]

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

        else:
            # TODO: we want to keep scanning. We need to call an error function (free
            # or one that is provided to __init__) or accumlate errors and return those
            # at the end of the scan. Maybe add a TokenType.ERROR?
            raise SyntaxError(f"Unexpected character: {char}")

    def _string(self):
        # just while self._peek() I think; if at_end, peek() -> "\0"
        # also, walrus operator :)
        while self._peek() != '"' and not self._at_end():
            # Allow for multi-line strings.
            if self._peek() == "\n":
                self._lno += 1
            self._advance()

        if self._at_end():
            # TODO: we want to return and then keep scanning.
            raise SyntaxError("Unterminated string")

        # The closing '"'
        self._advance()

        # Trim the quotes.
        value = self._source[self._start + 1 : self._current - 1]
        self._add_token(TokenType.STRING, value)
