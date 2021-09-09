from plox.ast import Stmt, execute
from plox.environment import Environment
from plox.errors import ExecutionError, report


class Interpreter:
    def __init__(self) -> None:
        self._env = Environment()

    def interpret(self, statements: list[Stmt]) -> None:
        for statement in statements:
            try:
                execute(statement, self._env)
            except ExecutionError as e:
                report(e.token.lno, "", e.message)
                raise
