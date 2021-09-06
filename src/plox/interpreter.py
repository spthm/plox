from plox.ast import Stmt, execute
from plox.errors import ExecutionError, report


class Interpreter:
    def interpret(self, statements: list[Stmt]) -> None:
        for statement in statements:
            try:
                execute(statement)
            except ExecutionError as e:
                report(e.token.lno, "", e.message)
                raise
