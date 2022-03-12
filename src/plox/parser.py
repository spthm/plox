from typing import Optional, Union

from plox.ast import (
    Assign,
    Binary,
    Block,
    Call,
    Expr,
    Expression,
    Function,
    Grouping,
    If,
    Literal,
    Logical,
    Print,
    Stmt,
    Unary,
    Var,
    Variable,
    While,
)
from plox.errors import ParserError, report
from plox.tokens import Token, TokenType


def _report(e: ParserError) -> None:
    t = e.token
    where = "at end" if t.kind == TokenType.EOF else f"at '{t.lexeme}'"
    report(t.lno, where, e.message)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._exc: Optional[ParserError] = None
        self._tokens = tokens
        self._current = 0

    def parse(self) -> list[Stmt]:
        statements = []
        while not self._at_end():
            try:
                statements.append(self._declaration())
            except ParserError:
                # Continue parsing so we can report other errors to the user.
                self._synchronize()

        if self._exc is not None:
            raise self._exc

        return statements

    def _declaration(self) -> Stmt:
        if self._match(TokenType.FUN):
            return self._function_declaration("function")
        if self._match(TokenType.VAR):
            return self._variable_declaration()
        return self._statement()

    def _function_declaration(self, kind: str):
        name = self._consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        parameters: list[Token] = []

        self._consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")

        # Account for zero-argument case.
        if not self._check(TokenType.RIGHT_PAREN):
            parameters.append(
                self._consume(TokenType.IDENTIFIER, "Expect parameter name.")
            )

            while self._match(TokenType.COMMA):
                parameters.append(
                    self._consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )

        # The parser isn't confused, so we don't need to raise.
        # The reference jlox does this in-loop above, which seems to be
        # overkill since all the arguments still need to be parsed. On the
        # other hand, this will point to the end of the function call, not
        # the 256th argument.
        if len(parameters) > 255:
            self._error("Can't have more than 255 parameters.", self._peek())

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self._consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self._block_statement()

        return Function(name, parameters, body)

    def _variable_declaration(self) -> Var:
        name = self._consume(TokenType.IDENTIFIER, "Expect a variable name.")
        initializer = (
            self._expression() if self._match(TokenType.EQUAL) else Literal(None)
        )

        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")

        return Var(name, initializer)

    def _statement(self) -> Stmt:
        if self._match(TokenType.FOR):
            return self._for_statement()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.WHILE):
            return self._while_statement()
        if self._match(TokenType.LEFT_BRACE):
            return self._block_statement()
        return self._expression_statement()

    def _for_statement(self) -> Union[Block, While]:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer: Union[None, Expression, Var]
        if self._match(TokenType.SEMICOLON):
            initializer = None
        elif self._match(TokenType.VAR):
            initializer = self._variable_declaration()
        else:
            initializer = self._expression_statement()

        condition = (
            Literal(True) if self._check(TokenType.SEMICOLON) else self._expression()
        )
        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = (
            None
            if self._check(TokenType.RIGHT_PAREN)
            else Expression(self._expression())
        )
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self._statement()
        if increment is not None:
            body = Block([body, increment])
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def _if_statement(self) -> If:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self._statement()
        else_branch = self._statement() if self._match(TokenType.ELSE) else None

        return If(condition, then_branch, else_branch)

    def _print_statement(self) -> Print:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def _while_statement(self) -> While:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")

        body = self._statement()

        return While(condition, body)

    def _block_statement(self) -> Block:
        statements = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._at_end():
            statements.append(self._declaration())

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return Block(statements)

    def _expression_statement(self) -> Expression:
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)

    def _expression(self) -> Expr:
        return self._assignment()

    def _assignment(self) -> Expr:
        expr = self._or()

        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self._assignment()

            if isinstance(expr, Variable):
                return Assign(expr.name, value)

            # The parser is not in a confused state, so we do not need to raise and
            # trigger a _synchronize().
            self._error("Invalid assignment target.", equals)

        return expr

    def _or(self) -> Expr:
        expr = self._and()

        while self._match(TokenType.OR):
            op = self._previous()
            rhs = self._and()
            expr = Logical(expr, op, rhs)

        return expr

    def _and(self) -> Expr:
        expr = self._equality()

        while self._match(TokenType.AND):
            op = self._previous()
            rhs = self._equality()
            expr = Logical(expr, op, rhs)

        return expr

    def _equality(self) -> Expr:
        expr = self._comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self._previous()
            rhs = self._comparison()
            expr = Binary(expr, op, rhs)

        return expr

    def _comparison(self) -> Expr:
        expr = self._term()

        while self._match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            op = self._previous()
            rhs = self._term()
            expr = Binary(expr, op, rhs)

        return expr

    def _term(self) -> Expr:
        expr = self._factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            op = self._previous()
            rhs = self._factor()
            expr = Binary(expr, op, rhs)

        return expr

    def _factor(self) -> Expr:
        expr = self._unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            op = self._previous()
            rhs = self._unary()
            expr = Binary(expr, op, rhs)

        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            op = self._previous()
            rhs = self._unary()
            return Unary(op, rhs)

        return self._call()

    def _call(self) -> Expr:
        expr = self._primary()

        while self._match(TokenType.LEFT_PAREN):
            expr = self._finish_call(expr)

        return expr

    def _primary(self) -> Expr:
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self._error("Expect expression.", self._peek())

    def _advance(self) -> Token:
        if not self._at_end():
            self._current += 1
        return self._previous()

    def _at_end(self) -> bool:
        return self._peek().kind == TokenType.EOF

    def _check(self, kind: TokenType) -> bool:
        if self._at_end():
            return False
        return self._peek().kind == kind

    def _consume(self, kind: TokenType, message: str) -> Token:
        if self._check(kind):
            return self._advance()

        raise self._error(message, self._peek())

    def _error(self, message: str, token: Token) -> ParserError:
        e = ParserError(message, token)
        _report(e)
        # The first parser error encountered is a sensible error to later raise.
        if self._exc is None:
            self._exc = e
        return e

    def _finish_call(self, callee: Expr):
        arguments: list[Expr] = []

        # Account for the zero-argument case.
        if not self._check(TokenType.RIGHT_PAREN):
            arguments.append(self._expression())

            while self._match(TokenType.COMMA):
                arguments.append(self._expression())

        if len(arguments) > 255:
            # The parser isn't confused, so we don't need to raise.
            # The reference jlox does this in-loop above, which seems to be
            # overkill since all the arguments still need to be parsed. On the
            # other hand, this will point to the end of the function call, not
            # the 256th argument.
            self._error("Can't have more than 255 arguments.", self._peek())

        paren = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

        return Call(callee, paren, arguments)

    def _match(self, *args: TokenType) -> bool:
        if any(self._check(kind) for kind in args):
            self._advance()
            return True
        return False

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        assert self._current > 0
        return self._tokens[self._current - 1]

    def _synchronize(self) -> None:
        self._advance()

        while not self._at_end():
            if self._previous().kind == TokenType.SEMICOLON:
                return

            if self._peek().kind in {
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            }:
                return

            self._advance()
